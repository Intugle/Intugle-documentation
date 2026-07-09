#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bulk Run and Cache - CHATAI Questions

Bulk runs questions through CHATAI and caches results for faster lookups.
Supports both full caching and partial caching (up to SQL generation step).

Usage:
    python bulk_run_and_cache.py \
        --csv-file questions.csv \
        --api-url https://your-api-url.com \
        --token "your-jwt-token" \
        --subscription-id 123

See doc.txt for detailed instructions.
"""

import argparse
import asyncio
import csv
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Literal

import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# Tool name constants
GENERATE_SQL_QUERY_TOOL = "generate_sql_query"
CLARIFICATION_TOOL = "clarification"


@dataclass
class QuestionTask:
    """Represents a single question to be warmed."""

    question: str
    index: int
    total: int
    cache_type: Literal["full", "partial"] = "full"  # Cache type from CSV
    session_id: Optional[int] = None
    query_id: Optional[int] = None
    status: str = "pending"
    output: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: Optional[float] = None
    breakpoint_step_id: Optional[str] = None  # Step ID for partial caching
    not_cached_reason: Optional[str] = None  # Reason when caching is skipped
    start_time: Optional[float] = field(default=None, repr=False)


class ResultsWriter:
    """Handles incremental writing of results to CSV."""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.lock = asyncio.Lock()
        self._initialized = False

    async def _ensure_header(self) -> None:
        """Write CSV header if file doesn't exist or is empty."""
        if self._initialized:
            return

        path = Path(self.output_path)
        write_header = not path.exists() or path.stat().st_size == 0

        if write_header:
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["question", "cache_type", "session_id", "query_id", "status", "duration_seconds", "breakpoint_step_id", "not_cached_reason", "output", "error"]
                )
        self._initialized = True

    async def write_result(self, task: QuestionTask) -> None:
        """Append a single result to the CSV file."""
        async with self.lock:
            await self._ensure_header()

            with open(self.output_path, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        task.question,
                        task.cache_type,
                        task.session_id or "",
                        task.query_id or "",
                        task.status,
                        task.duration_seconds or "",
                        task.breakpoint_step_id or "",
                        task.not_cached_reason or "",
                        task.output or "",
                        task.error or "",
                    ]
                )


class CacheWarmer:
    """
    Handles the cache warming process for CHATAI questions.

    Uses a sliding window approach to maintain N concurrent question processes.
    """

    TERMINAL_STATUSES = {"completed", "failed"}  # "partial" means still processing

    def __init__(
        self,
        api_url: str,
        token: str,
        subscription_id: int,
        results_writer: ResultsWriter,
        concurrency: int = 5,
        timeout: int = 1200,
        poll_interval: float = 5.0,
    ):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.subscription_id = subscription_id
        self.results_writer = results_writer
        self.concurrency = concurrency
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def create_session(self, name: str) -> int:
        """Create a new conversation session."""
        url = f"{self.api_url}/api/v2/conversation_ai/sessions"
        params = {"subscription_id": self.subscription_id}
        body = {"name": name}

        response = await self.client.post(url, params=params, json=body)
        response.raise_for_status()
        data = response.json()
        return data["id"]

    async def ask_question(self, session_id: int, question: str) -> int:
        """Submit a question to CHATAI, returns query_id."""
        url = f"{self.api_url}/api/v3/conversation_ai/sessions/{session_id}/queries/ask_question"
        params = {
            "subscription_id": self.subscription_id,
            "namespace": "/chatai",
        }
        body = {"question": question}

        response = await self.client.post(url, params=params, json=body)
        response.raise_for_status()
        query_id = response.json()
        return query_id

    async def get_query(self, session_id: int) -> list[dict]:
        """Get all queries for a session."""
        url = f"{self.api_url}/api/v2/conversation_ai/sessions/{session_id}/queries"
        params = {"subscription_id": self.subscription_id}

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _extract_rendered_output(self, output: Any) -> str:
        """
        Extract and render the output into a human-readable format.
        
        Handles various output formats from CHATAI:
        - Dict with 'answer' key
        - List of output items with tables, charts, text
        - Nested structures
        """
        if output is None:
            return ""

        if isinstance(output, str):
            return output

        rendered_parts = []

        if isinstance(output, dict):
            # Check for direct answer
            if "answer" in output:
                rendered_parts.append(output["answer"])
            
            # Check for text content
            if "text" in output:
                rendered_parts.append(output["text"])
            
            # Check for message
            if "message" in output:
                rendered_parts.append(output["message"])
            
            # If nothing found, try to extract meaningful content
            if not rendered_parts:
                # Look for common keys
                for key in ["result", "response", "content", "data", "summary"]:
                    if key in output:
                        val = output[key]
                        if isinstance(val, str):
                            rendered_parts.append(val)
                        elif isinstance(val, (dict, list)):
                            rendered_parts.append(self._extract_rendered_output(val))

        elif isinstance(output, list):
            for item in output:
                if isinstance(item, dict):
                    # Handle output items (tables, charts, text, etc.)
                    item_type = item.get("type", "")
                    
                    if item_type == "text" or "answer" in item:
                        text = item.get("answer") or item.get("text") or item.get("content", "")
                        if text:
                            rendered_parts.append(str(text))
                    
                    elif item_type == "table":
                        # Render table summary
                        table_name = item.get("name", "Table")
                        rows = item.get("rows", [])
                        columns = item.get("columns", [])
                        if rows:
                            rendered_parts.append(f"[{table_name}: {len(rows)} rows, {len(columns)} columns]")
                    
                    elif item_type == "chart":
                        chart_type = item.get("chartType", "chart")
                        title = item.get("title", "")
                        rendered_parts.append(f"[Chart: {chart_type}" + (f" - {title}]" if title else "]"))
                    
                    elif item_type == "sql":
                        sql = item.get("sql", "")
                        if sql:
                            rendered_parts.append(f"[SQL: {sql[:100]}...]" if len(sql) > 100 else f"[SQL: {sql}]")
                    
                    else:
                        # Try to extract any text content
                        for key in ["answer", "text", "content", "message", "result"]:
                            if key in item and item[key]:
                                rendered_parts.append(str(item[key]))
                                break
                
                elif isinstance(item, str):
                    rendered_parts.append(item)

        # Join all parts with newlines
        result = "\n".join(filter(None, rendered_parts))
        
        # If still empty, return a JSON summary
        if not result and output:
            try:
                # Return a compact JSON representation
                return json.dumps(output, ensure_ascii=False, separators=(',', ':'))[:500]
            except (TypeError, ValueError):
                return str(output)[:500]

        return result

    def _find_first_sql_generation_step_id(self, stages: list[dict]) -> Optional[str]:
        """
        Find the first SQL generation step ID in stages.
        
        Uses the tool_name field for reliable identification.
        Searches both root stages and sub-agent stages.
        
        Args:
            stages: List of stage dictionaries from query response
            
        Returns:
            The step ID to use as breakpoint_step_id, or None if not found
        """
        if not stages:
            return None
            
        for stage in stages:
            tool_name = stage.get("tool_name")
            if tool_name == GENERATE_SQL_QUERY_TOOL:
                step_id = stage.get("id")
                if step_id:
                    log.debug(f"Found SQL generation step: id={step_id}, name={stage.get('name', '')[:50]}")
                    return step_id
        
        log.debug(f"No SQL generation step found in {len(stages)} stages")
        return None

    def _has_clarification_stage(self, stages: list[dict]) -> bool:
        """
        Check if any stage has a clarification tool.
        
        Questions that resulted in clarification should not be cached
        as they represent incomplete/ambiguous queries.
        
        Args:
            stages: List of stage dictionaries from query response
            
        Returns:
            True if any stage has tool_name == "clarification"
        """
        if not stages:
            return False
            
        for stage in stages:
            tool_name = stage.get("tool_name")
            if tool_name == CLARIFICATION_TOOL:
                log.debug(f"Found clarification stage: id={stage.get('id')}, name={stage.get('name', '')[:50]}")
                return True
        
        return False

    async def poll_until_complete(
        self, session_id: int, query_id: int, timeout: float
    ) -> tuple[str, Optional[str], Optional[list[dict]]]:
        """
        Poll query status until completed or failed.

        Returns:
            tuple of (status, output_text, stages)
        """
        start_time = time.time()
        last_log_time = 0

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                return "timeout", None, None

            queries = await self.get_query(session_id)
            query = next((q for q in queries if q["id"] == query_id), None)

            if query is None:
                await asyncio.sleep(self.poll_interval)
                continue

            status = query.get("status", "")
            if status in self.TERMINAL_STATUSES:
                # Extract and render output
                output = query.get("output")
                output_text = self._extract_rendered_output(output)
                stages = query.get("stages") or []
                return status, output_text, stages

            # Log progress every 30 seconds
            if elapsed - last_log_time >= 30:
                log.debug(f"Query {query_id} still processing (status={status}, elapsed={int(elapsed)}s)")
                last_log_time = elapsed

            await asyncio.sleep(self.poll_interval)

    async def cache_question(
        self, 
        session_id: int, 
        query_id: int, 
        question: str,
        cache_type: str = "full",
        breakpoint_step_id: Optional[str] = None,
    ) -> bool:
        """Trigger caching of the completed question.
        
        Args:
            session_id: Session ID
            query_id: Query ID
            question: Question text
            cache_type: "full" or "partial"
            breakpoint_step_id: Step ID for partial caching (required if cache_type is "partial")
        """
        url = f"{self.api_url}/api/v2/conversation_ai/search-questions"
        params = {"subscription_id": self.subscription_id}
        body = {
            "query_id": query_id,
            "session_id": session_id,
            "question": question,
            "cache_type": cache_type,
        }
        
        # Add breakpoint_step_id for partial caching
        if cache_type == "partial" and breakpoint_step_id:
            body["breakpoint_step_id"] = breakpoint_step_id

        response = await self.client.post(url, params=params, json=body)
        return response.status_code == 200

    async def process_question(
        self, task: QuestionTask, semaphore: asyncio.Semaphore
    ) -> None:
        """Process a single question end-to-end."""
        async with semaphore:
            task.start_time = time.time()
            cache_type_label = f"[{task.cache_type}]" if task.cache_type == "partial" else ""
            prefix = f"[{task.index}/{task.total}]{cache_type_label}"

            try:
                # 1. Create session
                log.info(f"{prefix} Starting: {task.question[:60]}...")
                session_name = f"warm_cache_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{task.index}"
                task.session_id = await self.create_session(session_name)
                log.debug(f"{prefix} Created session {task.session_id}")

                # 2. Submit question
                task.query_id = await self.ask_question(task.session_id, task.question)
                task.status = "running"
                log.debug(f"{prefix} Submitted query {task.query_id}")

                # 3. Poll until complete
                status, output_text, stages = await self.poll_until_complete(
                    task.session_id, task.query_id, self.timeout
                )
                task.duration_seconds = round(time.time() - task.start_time, 2)

                if status == "timeout":
                    task.status = "timeout"
                    task.error = f"Query did not complete within {self.timeout} seconds"
                    task.not_cached_reason = "query_timeout"
                    log.warning(f"{prefix} Timeout after {task.duration_seconds}s")
                    await self.results_writer.write_result(task)
                    return

                if status != "completed":
                    task.status = f"failed:{status}"
                    task.error = f"Query ended with status: {status}"
                    task.not_cached_reason = f"query_failed_{status}"
                    log.warning(f"{prefix} Failed with status {status} after {task.duration_seconds}s")
                    await self.results_writer.write_result(task)
                    return

                # 4. Check for clarification - skip caching if question required clarification
                task.output = output_text
                if self._has_clarification_stage(stages or []):
                    task.status = "completed_not_cached"
                    task.not_cached_reason = "clarification_required"
                    log.info(f"{prefix} Completed but skipping cache (clarification required) in {task.duration_seconds}s")
                    await self.results_writer.write_result(task)
                    return

                # 5. Determine cache parameters
                cache_type = task.cache_type
                breakpoint_step_id = None
                
                if task.cache_type == "partial":
                    # Find the first SQL generation step for partial caching
                    breakpoint_step_id = self._find_first_sql_generation_step_id(stages or [])
                    
                    if breakpoint_step_id:
                        task.breakpoint_step_id = breakpoint_step_id
                        log.debug(f"{prefix} Using breakpoint_step_id={breakpoint_step_id} for partial cache")
                    else:
                        # Fallback to full cache if no SQL generation step found
                        cache_type = "full"
                        task.cache_type = "full"  # Update task to reflect actual cache type
                        log.warning(f"{prefix} No SQL generation step found, falling back to full cache")

                # 6. Cache the question
                cached = await self.cache_question(
                    task.session_id, 
                    task.query_id, 
                    task.question,
                    cache_type=cache_type,
                    breakpoint_step_id=breakpoint_step_id,
                )

                if cached:
                    task.status = f"cached:{cache_type}"
                    log.info(f"{prefix} Completed and cached ({cache_type}) in {task.duration_seconds}s")
                else:
                    task.status = "completed_not_cached"
                    task.not_cached_reason = "cache_api_failed"
                    task.error = "Question completed but caching failed"
                    log.warning(f"{prefix} Completed but caching failed after {task.duration_seconds}s")

            except httpx.HTTPStatusError as e:
                task.duration_seconds = round(time.time() - task.start_time, 2)
                task.status = "error"
                task.error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
                task.not_cached_reason = "http_error"
                log.error(f"{prefix} HTTP error: {task.error}")

            except Exception as e:
                task.duration_seconds = round(time.time() - task.start_time, 2)
                task.status = "error"
                task.error = str(e)
                task.not_cached_reason = "exception_error"
                log.error(f"{prefix} Error: {task.error}")

            # Write result immediately after completion
            await self.results_writer.write_result(task)

    async def run(self, tasks: list[QuestionTask]) -> None:
        """Run all tasks with sliding window concurrency."""
        semaphore = asyncio.Semaphore(self.concurrency)
        log.info(f"Starting cache warming for {len(tasks)} questions with concurrency={self.concurrency}, poll_interval={self.poll_interval}s")
        await asyncio.gather(*[self.process_question(t, semaphore) for t in tasks])


def load_csv(csv_path: str) -> list[QuestionTask]:
    """Load questions from CSV file.
    
    CSV format:
        question,cache_type
        What is the total revenue?,full
        Show me top 10 products,partial
        
    The cache_type column is optional. If not present, defaults to "full".
    Valid cache_type values: "full", "partial"
    """
    tasks = []
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "question" not in reader.fieldnames:
            raise ValueError("CSV must have a 'question' column")

        has_cache_type = "cache_type" in (reader.fieldnames or [])
        
        for i, row in enumerate(reader, start=1):
            question = row.get("question", "").strip()
            if question:
                # Get cache_type, default to "full" if not specified
                cache_type = row.get("cache_type", "").strip().lower() if has_cache_type else "full"
                if cache_type not in ("full", "partial"):
                    if cache_type == "":
                        cache_type = "full"
                    else:
                        log.warning(f"Row {i}: Invalid cache_type '{cache_type}', defaulting to 'full'")
                        cache_type = "full"
                
                tasks.append(QuestionTask(
                    question=question, 
                    index=i, 
                    total=0,
                    cache_type=cache_type,
                ))

    # Update total count
    for task in tasks:
        task.total = len(tasks)

    # Log cache type distribution
    full_count = sum(1 for t in tasks if t.cache_type == "full")
    partial_count = sum(1 for t in tasks if t.cache_type == "partial")
    log.info(f"Loaded {len(tasks)} questions: {full_count} full, {partial_count} partial")

    return tasks


def print_summary(tasks: list[QuestionTask]) -> None:
    """Print summary of results."""
    total = len(tasks)
    cached_full = sum(1 for t in tasks if t.status == "cached:full")
    cached_partial = sum(1 for t in tasks if t.status == "cached:partial")
    cached = cached_full + cached_partial
    completed = sum(1 for t in tasks if t.status == "completed_not_cached")
    failed = sum(1 for t in tasks if t.status.startswith("failed"))
    timeout = sum(1 for t in tasks if t.status == "timeout")
    errors = sum(1 for t in tasks if t.status == "error")
    other = total - cached - completed - failed - timeout - errors

    print("\n" + "=" * 60)
    print("CACHE WARMING SUMMARY")
    print("=" * 60)
    print(f"  Total questions:     {total}")
    print(f"  Successfully cached: {cached}")
    if cached_full > 0:
        print(f"    - Full cache:      {cached_full}")
    if cached_partial > 0:
        print(f"    - Partial cache:   {cached_partial}")
    if completed > 0:
        print(f"  Completed (not cached): {completed}")
    print(f"  Failed:              {failed}")
    print(f"  Timeout:             {timeout}")
    print(f"  Errors:              {errors}")
    if other > 0:
        print(f"  Other:               {other}")
    print("=" * 60)

    if cached == total:
        print("All questions cached successfully!")
    elif cached + completed > 0:
        print(f"Success rate: {(cached + completed)/total*100:.1f}%")
    else:
        print("No questions were completed successfully.")


async def main_async(args: argparse.Namespace) -> int:
    """Async main entry point."""
    # Load questions
    try:
        tasks = load_csv(args.csv_file)
    except (FileNotFoundError, ValueError) as e:
        log.error(str(e))
        return 1

    if not tasks:
        log.error("No questions found in CSV file")
        return 1

    log.info(f"Loaded {len(tasks)} questions from {args.csv_file}")

    if args.dry_run:
        log.info("Dry run mode - validating CSV only")
        for task in tasks:
            cache_label = f"[{task.cache_type}]" if task.cache_type == "partial" else "[full]"
            print(f"  [{task.index}] {cache_label} {task.question[:70]}")
        return 0

    # Remove existing output file to start fresh
    output_path = Path(args.output)
    if output_path.exists():
        output_path.unlink()
        log.debug(f"Removed existing output file: {args.output}")

    # Create results writer
    results_writer = ResultsWriter(args.output)

    # Run cache warming
    async with CacheWarmer(
        api_url=args.api_url,
        token=args.token,
        subscription_id=args.subscription_id,
        results_writer=results_writer,
        concurrency=args.concurrency,
        timeout=args.timeout,
        poll_interval=args.poll_interval,
    ) as warmer:
        await warmer.run(tasks)

    log.info(f"Results written to {args.output}")
    print_summary(tasks)

    # Return non-zero if any failures
    failures = sum(1 for t in tasks if t.status not in ("cached", "completed_not_cached"))
    return 1 if failures > 0 else 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bulk run and cache CHATAI questions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--csv-file",
        required=True,
        help="Path to CSV file with questions (must have 'question' column)",
    )
    parser.add_argument(
        "--api-url",
        required=True,
        help="Base API URL (e.g., http://localhost:8000)",
    )
    parser.add_argument(
        "--token",
        required=True,
        help="JWT Bearer token for authentication",
    )
    parser.add_argument(
        "--subscription-id",
        required=True,
        type=int,
        help="Subscription ID to use for all questions",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Number of parallel questions (default: 5)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1200,
        help="Timeout per question in seconds (default: 1200 = 20 minutes)",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=5.0,
        help="Polling interval in seconds (default: 5.0)",
    )
    parser.add_argument(
        "--output",
        default="warm_cache_results.csv",
        help="Output file path for results (default: warm_cache_results.csv)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate CSV without executing",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose/debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
