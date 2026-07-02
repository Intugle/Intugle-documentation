---
title: A2A API Reference
sidebar_position: 3
---

# A2A API Reference

This document provides a complete reference for Intugle's Agent-to-Agent (A2A) protocol implementation.

## Base URL

```
https://your-instance.intugle.ai/a2a/
```

## Authentication

All endpoints (except Agent Card discovery) require JWT Bearer authentication:

```
Authorization: Bearer <your-jwt-token>
```

### Token Structure

The JWT token contains:

```json
{
  "sub": "user-id",
  "workspace_id": "workspace-id",
  "chatapp_id": "chatapp-id",
  "exp": 1735689600,
  "iat": 1704153600
}
```

### Token Expiration

Tokens have a configurable expiration. Check the `exp` claim to determine validity. Regenerate tokens through the Intugle UI when needed.

## Endpoints

### Agent Card Discovery

Retrieve the agent's capabilities and metadata.

```
GET /.well-known/agent-card.json
```

**Authentication**: Not required

**Response**:

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
    },
    {
      "id": "metadata-exploration",
      "name": "Metadata Exploration", 
      "description": "Explore data models and semantic layer definitions"
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

### Send Message

Send a message to the agent and receive a streaming response.

```
POST /
```

**Authentication**: Required

**Headers**:

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | Yes |
| `Content-Type` | `application/json` | Yes |
| `Accept` | `text/event-stream` | Recommended |

**Request Body**:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "context_id": "optional-session-id",
    "task_id": "optional-existing-task-id",
    "message": {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "Your query or message"
        }
      ]
    }
  },
  "id": "request-id"
}
```

**Response**: Server-Sent Events stream

## JSON-RPC Methods

### `message/send`

Send a new message to the agent.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | Message | Yes | The message to send |
| `context_id` | string | No | Session ID for context continuity |
| `task_id` | string | No | Existing task ID (for input responses) |

### `task/cancel`

Cancel a running task.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | string | Yes | The task ID to cancel |

**Example**:

```json
{
  "jsonrpc": "2.0",
  "method": "task/cancel",
  "params": {
    "task_id": "task-abc-123"
  },
  "id": "2"
}
```

## Data Types

### Message

```typescript
interface Message {
  role: "user" | "assistant";
  parts: MessagePart[];
  message_id?: string;
  timestamp?: string;
}
```

### MessagePart

```typescript
type MessagePart = TextPart | FilePart;

interface TextPart {
  type: "text";
  text: string;
}

interface FilePart {
  type: "file";
  file: {
    name: string;
    mimeType: string;
    data: string; // base64 encoded
  };
}
```

### Task

```typescript
interface Task {
  id: string;
  state: TaskState;
  created_at: string;
  updated_at: string;
  error?: TaskError;
  input_request?: InputRequest;
}

type TaskState = 
  | "submitted"
  | "working" 
  | "input_required"
  | "completed"
  | "failed"
  | "canceled";
```

### TaskError

```typescript
interface TaskError {
  code: string;
  message: string;
  details?: Record<string, any>;
}
```

### InputRequest

```typescript
interface InputRequest {
  type: "text" | "selection" | "confirmation";
  message: string;
  options?: string[];  // For selection type
}
```

### Artifact

```typescript
type Artifact = 
  | MarkdownArtifact
  | ChartArtifact
  | TableArtifact
  | CardArtifact;

interface MarkdownArtifact {
  type: "markdown";
  content: string;
}

interface ChartArtifact {
  type: "chart";
  chartType: "bar" | "line" | "pie" | "scatter" | "area";
  data: ChartData;
  config: ChartConfig;
}

interface TableArtifact {
  type: "table";
  columns: string[];
  rows: any[][];
  metadata?: {
    totalRows?: number;
    truncated?: boolean;
  };
}

interface CardArtifact {
  type: "card";
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    direction: "up" | "down" | "neutral";
    value: string;
  };
}
```

## Streaming Events

The server sends events using Server-Sent Events (SSE) format:

```
event: <event-type>
data: <json-payload>

```

### Event Types

#### `task.created`

Fired when a new task is created.

```json
{
  "type": "task.created",
  "task": {
    "id": "task-abc-123",
    "state": "submitted",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### `task.updated`

Fired when task state or properties change.

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-abc-123",
    "state": "working",
    "updated_at": "2024-01-15T10:30:01Z"
  }
}
```

#### `message.created`

Fired when a new message is added to the conversation.

```json
{
  "type": "message.created",
  "message": {
    "role": "assistant",
    "message_id": "msg-xyz-789",
    "parts": [
      {
        "type": "text",
        "text": "I'm analyzing your sales data..."
      }
    ]
  }
}
```

#### `message.updated`

Fired when message content is updated (streaming text).

```json
{
  "type": "message.updated",
  "message": {
    "message_id": "msg-xyz-789",
    "parts": [
      {
        "type": "text",
        "text": "I'm analyzing your sales data. Here are the top customers..."
      }
    ]
  }
}
```

#### `artifact.created`

Fired when a new artifact is created.

```json
{
  "type": "artifact.created",
  "artifact": {
    "id": "artifact-001",
    "type": "table",
    "columns": ["Customer", "Revenue"],
    "rows": []
  }
}
```

#### `artifact.updated`

Fired when artifact content is updated.

```json
{
  "type": "artifact.updated",
  "artifact": {
    "id": "artifact-001",
    "type": "table",
    "columns": ["Customer", "Revenue", "Region"],
    "rows": [
      ["Acme Corp", 150000, "North"],
      ["Globex Inc", 120000, "South"]
    ]
  }
}
```

#### `progress.updated`

Fired to report execution progress.

```json
{
  "type": "progress.updated",
  "progress": {
    "message": "Executing query...",
    "percentage": 45
  }
}
```

## Error Codes

### JSON-RPC Errors

| Code | Message | Description |
|------|---------|-------------|
| `-32700` | Parse error | Invalid JSON |
| `-32600` | Invalid request | JSON-RPC structure invalid |
| `-32601` | Method not found | Unknown method |
| `-32602` | Invalid params | Invalid method parameters |
| `-32603` | Internal error | Server-side error |

### Application Errors

| Code | Message | Description |
|------|---------|-------------|
| `-32001` | Unauthorized | Invalid or expired token |
| `-32002` | Rate limited | Too many requests |
| `-32003` | Task not found | Invalid task ID |
| `-32004` | Task timeout | Execution exceeded time limit |
| `-32005` | Workspace unavailable | Workspace not accessible |

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Unauthorized: Token expired",
    "data": {
      "expired_at": "2024-01-14T00:00:00Z"
    }
  },
  "id": "1"
}
```

## Task State Transitions

```
                     ┌───────────────────┐
                     │                   │
                     ▼                   │
┌──────────┐    ┌─────────┐    ┌────────┴────────┐
│submitted │───►│ working │───►│ input_required  │
└──────────┘    └────┬────┘    └─────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐  ┌──────────┐  ┌─────────┐
│ completed │  │  failed  │  │canceled │
└───────────┘  └──────────┘  └─────────┘
```

### State Descriptions

| State | Description | Terminal |
|-------|-------------|----------|
| `submitted` | Task received, queued | No |
| `working` | Agent processing request | No |
| `input_required` | Waiting for user input | No |
| `completed` | Success, results available | Yes |
| `failed` | Error occurred | Yes |
| `canceled` | User canceled | Yes |

## Input Elicitation

When the agent needs additional input, it transitions to `input_required`:

### Text Input

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-123",
    "state": "input_required",
    "input_request": {
      "type": "text",
      "message": "Please provide the date range for the report"
    }
  }
}
```

### Selection Input

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-123",
    "state": "input_required",
    "input_request": {
      "type": "selection",
      "message": "Which metric would you like to analyze?",
      "options": ["Revenue", "Units Sold", "Profit Margin"]
    }
  }
}
```

### Confirmation Input

```json
{
  "type": "task.updated",
  "task": {
    "id": "task-123",
    "state": "input_required",
    "input_request": {
      "type": "confirmation",
      "message": "This query will process 1M+ rows. Continue?"
    }
  }
}
```

### Responding to Input Requests

Send a message with the `task_id`:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "task_id": "task-123",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "Revenue"}]
    }
  },
  "id": "2"
}
```

## Rate Limits

| Limit | Value |
|-------|-------|
| Requests per minute | 60 |
| Concurrent tasks | 5 |
| Max message size | 100KB |
| Max response time | 300 seconds |

## Configuration Reference

### Server Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `A2A_HOST` | Server bind address | `0.0.0.0` |
| `A2A_PORT` | Server port | `8001` |
| `A2A_AGENT_NAME` | Agent name in card | `Intugle Agent` |
| `A2A_AGENT_VERSION` | Agent version | `0.1.0` |
| `A2A_CLIENT_DISCONNECT_TIMEOUT_MS` | Client disconnect timeout | `15000` |
| `A2A_DISABLE_GENUI_STREAMING` | Disable rich UI streaming | `false` |

### Authentication Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `MCP_AUTHENTICATION_JWT_SECRET` | JWT signing secret | Required |
| `MCP_AUTHENTICATION_JWT_ALGORITHM` | JWT algorithm | `HS256` |

## Protocol Versions

### Version 1.0

Current version with full feature support:
- Streaming responses
- All artifact types
- Input elicitation
- Task cancellation

### Version 0.3 (Legacy)

Backward compatibility mode:
- Basic message/response
- Limited artifact support
- No input elicitation

Specify version in the `Accept` header if needed:

```
Accept: application/json; version=1.0
```

## Example: Complete Request/Response Cycle

### Request

```bash
curl -X POST "https://your-instance.intugle.ai/a2a/" \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "Show top 5 products by revenue"}]
      }
    },
    "id": "1"
  }'
```

### Response Stream

```
data: {"type":"task.created","task":{"id":"task-f7a8b9c0","state":"submitted","created_at":"2024-01-15T10:30:00Z"}}

data: {"type":"task.updated","task":{"id":"task-f7a8b9c0","state":"working"}}

data: {"type":"progress.updated","progress":{"message":"Analyzing product data...","percentage":25}}

data: {"type":"message.created","message":{"role":"assistant","message_id":"msg-123","parts":[{"type":"text","text":"I'll query the sales data to find the top products."}]}}

data: {"type":"progress.updated","progress":{"message":"Executing query...","percentage":50}}

data: {"type":"artifact.created","artifact":{"id":"art-456","type":"table","columns":["Product","Revenue"],"rows":[]}}

data: {"type":"progress.updated","progress":{"message":"Processing results...","percentage":75}}

data: {"type":"artifact.updated","artifact":{"id":"art-456","type":"table","columns":["Product","Revenue","Units"],"rows":[["Widget Pro",150000,3200],["Gadget Plus",120000,2800],["Tool Max",95000,1900],["Device X",82000,1650],["Item Prime",75000,1500]]}}

data: {"type":"message.updated","message":{"message_id":"msg-123","parts":[{"type":"text","text":"Here are the top 5 products by revenue:\n\n1. **Widget Pro** - $150,000 (3,200 units)\n2. **Gadget Plus** - $120,000 (2,800 units)\n3. **Tool Max** - $95,000 (1,900 units)\n4. **Device X** - $82,000 (1,650 units)\n5. **Item Prime** - $75,000 (1,500 units)"}]}}

data: {"type":"task.updated","task":{"id":"task-f7a8b9c0","state":"completed","updated_at":"2024-01-15T10:30:05Z"}}
```

## Next Steps

- [Getting Started](./getting-started.md) - Quick start guide
- [A2A Overview](./overview.md) - Conceptual overview
- [MCP Server](../mcp/mcp-server.md) - Alternative MCP integration
