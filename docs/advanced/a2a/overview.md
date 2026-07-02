---
title: A2A Overview
sidebar_position: 1
---

# A2A (Agent-to-Agent) Protocol Overview

Agent-to-Agent (A2A) is an open protocol that enables AI agents to communicate directly with each other. Intugle implements A2A as a **server provider**, allowing external AI agents and applications to interact with the Intugle Data Agent programmatically.

## What is A2A?

A2A is a JSON-RPC based protocol designed for agent interoperability. It provides:

- **Standardized Communication**: A common language for agents to exchange messages
- **Task Management**: Track the state of requests through defined lifecycle states
- **Streaming Support**: Real-time response streaming for long-running operations
- **Discovery**: Agent Card mechanism for capability advertisement

## Intugle as A2A Server

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     INTUGLE A2A SERVER ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   EXTERNAL AGENTS / APPLICATIONS                                        │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │
│   │  Custom AI  │  │  Slack Bot  │  │  Automated  │                    │
│   │ Application │  │             │  │  Pipeline   │                    │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                    │
│          │                │                │                            │
│          └────────────────┼────────────────┘                            │
│                           │                                             │
│                    A2A Protocol (JSON-RPC + SSE)                        │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                    INTUGLE A2A SERVER                        │      │
│   │                                                              │      │
│   │  ┌──────────────────────────────────────────────────────┐   │      │
│   │  │                   Intugle Agent                       │   │      │
│   │  │                                                       │   │      │
│   │  │  INPUT:                    OUTPUT:                    │   │      │
│   │  │  • Text messages           • Text/Markdown responses  │   │      │
│   │  │  • Follow-up queries       • Table artifacts          │   │      │
│   │  │  • Elicitation responses   • Chart artifacts          │   │      │
│   │  │                            • Card artifacts (KPIs)    │   │      │
│   │  │                            • Input requests           │   │      │
│   │  │                            • Progress updates         │   │      │
│   │  └──────────────────────────────────────────────────────┘   │      │
│   │                                                              │      │
│   │  Features:                                                   │      │
│   │  • JWT Authentication    • Task Lifecycle Management        │      │
│   │  • Streaming Responses   • Session Continuity               │      │
│   └─────────────────────────────────────────────────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Natural Language Queries** | Send data questions in plain English |
| **Streaming Responses** | Receive real-time updates as the agent works |
| **Rich Artifacts** | Get structured outputs: charts, tables, markdown, cards |
| **Session Continuity** | Maintain context across multiple interactions |
| **Input Elicitation** | Handle requests for additional user input |

## Input & Output Formats

### Input Options

A2A accepts messages with one or more parts:

| Input Type | Description | Example |
|------------|-------------|---------|
| **Text Message** | Natural language query | "What were total sales last quarter?" |
| **Follow-up** | Contextual continuation | "Now break that down by region" |
| **Elicitation Response** | Answer to agent's question | "Use the last 30 days" |
| **File Attachment** | Supporting documents | CSV data, images |

**Input Message Structure:**
```json
{
  "role": "user",
  "parts": [
    {
      "type": "text",
      "text": "Show me the top 10 customers by revenue"
    }
  ]
}
```

### Output Options

A2A returns streaming events containing various artifact types:

| Output Type | Description | When Used |
|-------------|-------------|-----------|
| **Text/Markdown** | Formatted text responses | Explanations, summaries, reports |
| **Table** | Structured tabular data | Query results with rows/columns |
| **Chart** | Data visualizations | Trends, comparisons, distributions |
| **Card** | Summary metrics/KPIs | Key performance indicators |
| **Input Request** | Elicitation for user input | When clarification is needed |
| **Progress** | Status updates | During long-running operations |

**Output Examples:**

```json
// Markdown Response
{
  "type": "artifact.updated",
  "artifact": {
    "type": "markdown",
    "content": "## Sales Summary\n\nTotal revenue: **$1.2M** (+15% vs last quarter)"
  }
}

// Table Artifact
{
  "type": "artifact.updated",
  "artifact": {
    "type": "table",
    "columns": ["Customer", "Revenue", "Growth"],
    "rows": [
      ["Acme Corp", "$150,000", "+12%"],
      ["Globex Inc", "$120,000", "+8%"]
    ]
  }
}

// Chart Artifact
{
  "type": "artifact.updated",
  "artifact": {
    "type": "chart",
    "chartType": "bar",
    "title": "Revenue by Region",
    "data": { ... }
  }
}

// Card Artifact (KPIs)
{
  "type": "artifact.updated",
  "artifact": {
    "type": "card",
    "title": "Total Revenue",
    "value": "$1.2M",
    "trend": { "direction": "up", "value": "+15%" }
  }
}
```

## A2A vs MCP

Both A2A and MCP enable agent communication, but they serve different purposes:

| Aspect | A2A | MCP |
|--------|-----|-----|
| **Purpose** | Agent-to-agent messaging | Tool and resource sharing |
| **Protocol** | JSON-RPC over HTTP | JSON-RPC over Streamable HTTP |
| **Communication** | Message-based conversations | Tool invocations |
| **State** | Task lifecycle management | Session-based context |
| **Best For** | Custom applications, automation | IDE/AI assistant integration |

### When to Use A2A

- Building custom AI applications that need Intugle's data capabilities
- Creating automated pipelines that query data programmatically
- Integrating Intugle into existing agent orchestration systems
- Developing chatbots or assistants that leverage Intugle for data tasks

### When to Use MCP

- Connecting existing MCP clients (Claude Desktop, Cursor) to Intugle
- Using Intugle as a tool within another AI assistant
- Quick integration without custom development

## Protocol Versions

Intugle supports the following A2A protocol versions:

| Version | Status | Notes |
|---------|--------|-------|
| **1.0** | Current | Full feature support |
| **0.3** | Legacy | Backward compatibility |

## Core Concepts

### Agent Card

The Agent Card is a JSON document that describes Intugle's A2A capabilities:

```json
{
  "name": "Intugle Agent",
  "description": "Intelligent data analytics agent for exploring and analyzing your data",
  "version": "0.1.0",
  "url": "https://your-instance.intugle.ai/a2a/",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
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
  }
}
```

### Tasks

Every A2A interaction creates a **Task** that progresses through defined states:

```
                    ┌───────────┐
                    │ submitted │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
              ┌────►│  working  │◄────┐
              │     └─────┬─────┘     │
              │           │           │
              │     ┌─────┴─────┐     │
              │     ▼           ▼     │
        ┌─────┴─────┐    ┌──────┴────┐
        │input_     │    │           │
        │required   │    │           │
        └───────────┘    │           │
                         ▼           ▼
                   ┌──────────┐ ┌────────┐
                   │completed │ │ failed │
                   └──────────┘ └────────┘
                         │
                         ▼
                   ┌──────────┐
                   │ canceled │ (user-initiated)
                   └──────────┘
```

| State | Description |
|-------|-------------|
| `submitted` | Task received, queued for processing |
| `working` | Agent is actively processing the request |
| `input_required` | Agent needs additional input from user |
| `completed` | Task finished successfully |
| `failed` | Task encountered an error |
| `canceled` | Task was canceled by user |

### Messages

Messages are the primary communication unit:

```json
{
  "role": "user",
  "parts": [
    {
      "type": "text",
      "text": "Show me sales trends for the last quarter"
    }
  ]
}
```

### Artifacts

Artifacts are structured outputs produced by the agent:

| Type | Description |
|------|-------------|
| **Markdown** | Formatted text responses |
| **Chart** | Data visualizations (bar, line, pie, scatter, area) |
| **Table** | Tabular data with columns and rows |
| **Card** | Summary cards with key metrics and trends |

## Authentication

A2A uses JWT Bearer token authentication:

```
Authorization: Bearer <your-jwt-token>
```

Tokens are obtained through the Intugle UI (see [Getting Started](./getting-started.md)).

## Use Cases

### 1. Custom Data Assistant

Build a Slack bot that answers data questions:

```python
# User asks in Slack: "What were our top products last month?"
# Your bot sends to Intugle A2A
response = await a2a_client.send_message(
    "What were our top products last month?"
)
# Bot posts the response back to Slack
```

### 2. Automated Reporting

Create scheduled reports that query Intugle:

```python
# Daily report generation
async def generate_daily_report():
    tasks = await a2a_client.send_message(
        "Generate executive summary of yesterday's metrics"
    )
    # Save artifacts to report storage
```

### 3. Multi-Agent Orchestration

Integrate Intugle into a larger agent system:

```python
# Orchestrator delegates data tasks to Intugle
if task.requires_data_analysis:
    result = await intugle_a2a.send_message(task.query)
    return process_intugle_response(result)
```

## Next Steps

- [Getting Started](./getting-started.md) - Obtain credentials and send your first message
- [API Reference](./api-reference.md) - Complete protocol documentation
- [MCP Overview](../mcp/overview.md) - Compare with MCP integration
