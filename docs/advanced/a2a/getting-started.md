---
title: Getting Started with A2A
sidebar_position: 2
---

# Getting Started with A2A

This guide walks you through obtaining A2A credentials, discovering the agent, and sending your first message to Intugle's A2A endpoint.

## Prerequisites

Before you begin:

1. **Deployed ChatApp**: You need a deployed ChatApp in your Intugle workspace
2. **API Access**: Your account must have API access permissions
3. **Development Environment**: Python 3.8+ or Node.js 16+ (for the examples)

## Obtaining A2A Credentials

### Step 1: Access ChatApp Settings

Navigate to your deployed ChatApp and open the settings panel.

:::info Screenshot Needed
**a2a-connection-info.png** - The A2A Connection Info component showing the A2A URL and authentication details. Should display the endpoint URL prominently.
:::

### Step 2: Copy Credentials

The A2A Connection Info displays:
- **A2A URL**: The endpoint for A2A connections (e.g., `https://your-instance.intugle.ai/a2a/`)
- **API Key**: Your JWT authentication token

:::info Screenshot Needed
**a2a-credentials.png** - Close-up of the credentials section showing the copy buttons for URL and API key, and the regenerate button.
:::

Click the copy icons to copy each value.

### Step 3: Store Credentials Securely

Store your credentials as environment variables:

```bash
export INTUGLE_A2A_URL="https://your-instance.intugle.ai/a2a/"
export INTUGLE_A2A_API_KEY="your-jwt-token"
```

:::warning Security
Never commit API keys to version control. Use environment variables or a secrets manager.
:::

## Discovering the Agent

Before sending messages, you can discover the agent's capabilities via its Agent Card.

### Agent Card Endpoint

```
GET {A2A_URL}/.well-known/agent-card.json
```

This endpoint does **not** require authentication.

### Example Request

```bash
curl https://your-instance.intugle.ai/a2a/.well-known/agent-card.json
```

### Example Response

```json
{
  "name": "Intugle Agent",
  "description": "Intelligent data analytics agent for exploring, querying, and analyzing your connected data sources.",
  "version": "0.1.0",
  "url": "https://your-instance.intugle.ai/a2a/",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [
    {
      "id": "data-analytics",
      "name": "Data Analytics",
      "description": "Query and analyze data using natural language"
    }
  ],
  "securitySchemes": {
    "bearer": {
      "type": "http",
      "scheme": "bearer"
    }
  },
  "security": ["bearer"]
}
```

## Sending Your First Message

### Basic Request Structure

A2A uses JSON-RPC over HTTP. Here's the basic structure:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "Your question here"
        }
      ]
    }
  },
  "id": "unique-request-id"
}
```

### Python Example

```python
import os
import httpx
import json

A2A_URL = os.environ["INTUGLE_A2A_URL"]
API_KEY = os.environ["INTUGLE_A2A_API_KEY"]

async def send_message(query: str):
    """Send a message to Intugle A2A and stream the response."""
    
    request = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": query}]
            }
        },
        "id": "1"
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            A2A_URL,
            json=request,
            headers=headers,
            timeout=300
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    yield data

# Usage
import asyncio

async def main():
    async for event in send_message("What are our top 10 customers?"):
        print(f"Event: {event}")

asyncio.run(main())
```

### JavaScript/TypeScript Example

```typescript
const A2A_URL = process.env.INTUGLE_A2A_URL;
const API_KEY = process.env.INTUGLE_A2A_API_KEY;

async function* sendMessage(query: string) {
  const request = {
    jsonrpc: "2.0",
    method: "message/send",
    params: {
      message: {
        role: "user",
        parts: [{ type: "text", text: query }]
      }
    },
    id: "1"
  };

  const response = await fetch(A2A_URL, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      "Accept": "text/event-stream"
    },
    body: JSON.stringify(request)
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const lines = decoder.decode(value).split("\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        yield JSON.parse(line.slice(6));
      }
    }
  }
}

// Usage
async function main() {
  for await (const event of sendMessage("Show me sales by region")) {
    console.log("Event:", event);
  }
}

main();
```

### cURL Example

```bash
curl -X POST "${INTUGLE_A2A_URL}" \
  -H "Authorization: Bearer ${INTUGLE_A2A_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "What are our total sales?"}]
      }
    },
    "id": "1"
  }'
```

## Understanding Responses

### Streaming Events

The A2A server streams events as Server-Sent Events (SSE):

```
data: {"type": "task.created", "task": {"id": "task-123", "state": "submitted"}}

data: {"type": "task.updated", "task": {"id": "task-123", "state": "working"}}

data: {"type": "artifact.updated", "artifact": {"type": "markdown", "content": "..."}}

data: {"type": "task.updated", "task": {"id": "task-123", "state": "completed"}}
```

### Event Types

| Event Type | Description |
|------------|-------------|
| `task.created` | New task has been created |
| `task.updated` | Task state or properties changed |
| `message.updated` | New message content available |
| `artifact.updated` | New artifact (chart, table, etc.) available |

### Task States

Monitor the task state to track progress:

```python
async for event in send_message(query):
    if event.get("type") == "task.updated":
        state = event["task"]["state"]
        
        if state == "working":
            print("Agent is processing...")
        elif state == "completed":
            print("Task completed!")
            break
        elif state == "failed":
            print(f"Task failed: {event['task'].get('error')}")
            break
```

## Handling Artifacts

Artifacts contain the agent's structured outputs:

### Markdown Artifact

```json
{
  "type": "artifact.updated",
  "artifact": {
    "type": "markdown",
    "content": "## Sales Summary\n\nTotal revenue: **$1.2M**\n\n..."
  }
}
```

### Chart Artifact

```json
{
  "type": "artifact.updated",
  "artifact": {
    "type": "chart",
    "chartType": "bar",
    "data": {...},
    "config": {...}
  }
}
```

### Table Artifact

```json
{
  "type": "artifact.updated",
  "artifact": {
    "type": "table",
    "columns": ["Customer", "Revenue", "Region"],
    "rows": [
      ["Acme Corp", 150000, "North"],
      ["Globex", 120000, "South"]
    ]
  }
}
```

## Session Management

### Context IDs

To maintain conversation context across messages, use a `context_id`:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "context_id": "session-abc-123",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "Now break that down by month"}]
    }
  },
  "id": "2"
}
```

### Session Continuity

- **Same context_id**: Continues the conversation with previous context
- **New/no context_id**: Starts a fresh conversation

```python
# First message - establishes context
context_id = "my-session-123"
response1 = await send_with_context("Show me top customers", context_id)

# Follow-up message - uses previous context
response2 = await send_with_context("Filter to just Q4", context_id)
```

## Handling Input Requests

Sometimes the agent needs additional input:

### Input Required State

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-123",
    "state": "input_required",
    "input_request": {
      "type": "selection",
      "message": "Which time period would you like?",
      "options": ["Last 7 days", "Last 30 days", "Last quarter"]
    }
  }
}
```

### Responding to Input Requests

```python
# Detect input request
if task["state"] == "input_required":
    # Send response
    await send_message(
        query="Last 30 days",
        task_id=task["id"]
    )
```

## Error Handling

### Authentication Errors

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Unauthorized: Invalid or expired token"
  },
  "id": "1"
}
```

**Solution**: Regenerate your API key and update your credentials.

### Rate Limiting

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32002,
    "message": "Rate limit exceeded. Try again in 60 seconds."
  },
  "id": "1"
}
```

**Solution**: Implement exponential backoff and retry logic.

### Task Timeout

Tasks that run too long may be terminated:

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-123",
    "state": "failed",
    "error": {
      "code": "TIMEOUT",
      "message": "Task exceeded maximum execution time"
    }
  }
}
```

**Solution**: Break complex queries into smaller, focused questions.

## Complete Example

Here's a full example implementing a simple A2A client:

```python
import os
import httpx
import json
import asyncio
from typing import AsyncGenerator, Optional

class IntugleA2AClient:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self.request_id = 0
    
    async def send_message(
        self, 
        query: str, 
        context_id: Optional[str] = None
    ) -> AsyncGenerator[dict, None]:
        """Send a message and yield streaming events."""
        
        self.request_id += 1
        
        params = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": query}]
            }
        }
        
        if context_id:
            params["context_id"] = context_id
        
        request = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": params,
            "id": str(self.request_id)
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.url,
                json=request,
                headers=headers,
                timeout=300
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        yield json.loads(line[6:])
    
    async def query(self, question: str) -> dict:
        """Send a query and return the final result."""
        
        result = {"artifacts": [], "messages": []}
        
        async for event in self.send_message(question):
            event_type = event.get("type")
            
            if event_type == "artifact.updated":
                result["artifacts"].append(event["artifact"])
            
            elif event_type == "message.updated":
                result["messages"].append(event["message"])
            
            elif event_type == "task.updated":
                state = event["task"]["state"]
                if state == "completed":
                    break
                elif state == "failed":
                    raise Exception(f"Task failed: {event['task'].get('error')}")
        
        return result


# Usage
async def main():
    client = IntugleA2AClient(
        url=os.environ["INTUGLE_A2A_URL"],
        api_key=os.environ["INTUGLE_A2A_API_KEY"]
    )
    
    result = await client.query("What are our top 5 products by revenue?")
    
    for artifact in result["artifacts"]:
        if artifact["type"] == "markdown":
            print(artifact["content"])
        elif artifact["type"] == "table":
            print("Table:", artifact["columns"])
            for row in artifact["rows"]:
                print("  ", row)

if __name__ == "__main__":
    asyncio.run(main())
```

## Next Steps

- [API Reference](./api-reference.md) - Complete protocol documentation
- [A2A Overview](./overview.md) - Understand A2A concepts
- [MCP Server](../mcp/mcp-server.md) - Alternative integration via MCP
