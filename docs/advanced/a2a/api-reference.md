---
title: A2A API Reference
sidebar_position: 3
---

# A2A API Reference

Complete reference for Intugle's A2A protocol implementation.

## Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/.well-known/agent-card.json` | GET | No | Agent discovery |
| `/` | POST | Yes | Send messages (JSON-RPC) |

---

## Request Reference

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | **Yes** | `Bearer <JWT_TOKEN>` |
| `Content-Type` | **Yes** | `application/json` |
| `Accept` | Recommended | `text/event-stream` for streaming |
| `x-extra-params` | No | JSON object with extra parameters |
| `x-cache-payload` | No | Cache configuration |

#### x-extra-params Format

```json
{
  "custom_key": "custom_value"
}
```

#### x-cache-payload Format

```json
{
  "deterministic_cache": true,
  "cache_id": "optional-cache-key"
}
```

### JWT Token Claims

| Claim | Required | Description |
|-------|----------|-------------|
| `subscription_id` | **Yes** | Your subscription ID |
| `subscription_uuid` | **Yes** | Your subscription UUID |
| `user_id` | **Yes** | Your user ID |
| `chatapp_id` | No | ChatApp ID or `"latest"` |
| `exp` | **Yes** | Expiration timestamp |

**Example Token Payload:**
```json
{
  "subscription_id": 123,
  "subscription_uuid": "uuid-string",
  "user_id": 456,
  "chatapp_id": "latest",
  "exp": 1234567890
}
```

---

## Message Format

### Send Message Request

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "message_id": "unique-id",
      "context_id": "session-id",
      "task_id": "existing-task-id",
      "role": "user",
      "parts": [
        {
          "text": "Your question here",
          "media_type": "text/plain"
        }
      ]
    }
  },
  "id": "request-id"
}
```

### Message Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_id` | `string` | **Yes** | Unique message identifier |
| `context_id` | `string` | No | Session/conversation ID for context continuity |
| `task_id` | `string` | No | Existing task ID (for input responses) |
| `role` | `string` | **Yes** | Must be `"user"` |
| `parts` | `array` | **Yes** | Message content parts |

### Message Part Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | `string` | **Yes** | The message text |
| `media_type` | `string` | **Yes** | `"text/plain"` or `"application/json"` |

**Supported Media Types:** `text/plain`, `application/json`

---

## Response Reference

### Streaming Events

Responses are Server-Sent Events (SSE):

```
data: {"type": "event_type", ...}
```

### Event Types

| Event | Description |
|-------|-------------|
| `task.created` | Task created |
| `task.updated` | Task state changed |
| `message.updated` | Message content updated |
| `artifact.updated` | Artifact (output) updated |

### Task States

| State | Description |
|-------|-------------|
| `submitted` | Task received, queued |
| `working` | Processing in progress |
| `input_required` | Waiting for user input |
| `completed` | Finished successfully |
| `failed` | Error occurred |
| `canceled` | User canceled |

---

## Output Artifacts

### Artifact Structure

```json
{
  "type": "artifact.updated",
  "artifact": {
    "parts": [
      {
        "text": "Human-readable text",
        "media_type": "text/plain",
        "metadata": {
          "ui_components": [...],
          "execution_time": 2.5,
          "cache": "full",
          "cache_id": "abc123"
        }
      }
    ]
  }
}
```

### UI Component Structure

Each component in `ui_components`:

```json
{
  "index": 1,
  "type": "markdown",
  "content": "...",
  "status": "completed",
  "parentid": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `index` | `number` | Component order |
| `type` | `string` | `"markdown"`, `"table"`, `"chart"`, `"card"` |
| `content` | `string\|object` | Content (varies by type) |
| `status` | `string` | `"partial"`, `"completed"`, `"failed"` |
| `parentid` | `string\|null` | Parent component ID |

### Markdown Component

```json
{
  "type": "markdown",
  "content": "## Title\n\nFormatted **text**",
  "status": "completed"
}
```

### Table Component

```json
{
  "type": "table",
  "content": {
    "data": {
      "columns": ["Customer", "Revenue"],
      "rows": [["Acme", 150000]]
    },
    "title": "Top Customers",
    "column_mappings": {},
    "allow_publish": false
  },
  "status": "completed"
}
```

### Chart Component

```json
{
  "type": "chart",
  "content": {
    "chart_json": "{ vega-lite spec }",
    "title": "Revenue Trend",
    "chart_type": "line",
    "sample_data": {}
  },
  "status": "completed"
}
```

### Card Component

```json
{
  "type": "card",
  "content": {
    "title": "Total Revenue",
    "description": "$1.2M",
    "icon": "dollar",
    "right_content": "+15%",
    "right_icon": "arrow-up"
  },
  "status": "completed"
}
```

---

## Step/Action Events

Processing steps are sent as status updates:

```json
{
  "type": "task.updated",
  "task": {
    "state": "working"
  },
  "message": {
    "parts": [{
      "data": {
        "id": "step-1",
        "name": "Generating SQL",
        "tool_name": "generate_sql_query",
        "msg": "Building query...",
        "status": "completed",
        "type": "step",
        "ts": 1234567890.123
      },
      "media_type": "application/json"
    }]
  }
}
```

### Step Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Step identifier |
| `name` | `string` | Step name |
| `tool_name` | `string` | Tool being used (e.g., `generate_sql_query`, `execute_query`) |
| `msg` | `string` | Status message |
| `status` | `string` | `"partial"`, `"completed"`, `"failed"` |
| `type` | `string` | `"step"` or `"action"` |
| `ts` | `number` | Timestamp |
| `result` | `object` | Step result data |

---

## Input Required (Elicitation)

When the agent needs input, it sends:

```json
{
  "type": "task.updated",
  "task": {
    "state": "input_required"
  },
  "message": {
    "parts": [{
      "data": {
        "id": "CalculatedField",
        "name": "Define Calculation",
        "msg": "Please provide the formula for profit margin",
        "response_title": "Calculated Field",
        "response_description": "Enter the calculation logic",
        "default_response": "revenue - cost"
      },
      "media_type": "application/json"
    }]
  }
}
```

### Interrupt Types

| Type | Description |
|------|-------------|
| `CalculatedField` | Define a computed column |
| `MetadataEditor` | Edit metadata definitions |

### Responding to Input Requests

Send a follow-up message with the same `task_id`:

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "message": {
      "message_id": "response-001",
      "task_id": "task-123",
      "role": "user",
      "parts": [{
        "text": "revenue - cost",
        "media_type": "text/plain"
      }]
    }
  },
  "id": "2"
}
```

---

## Agent Card

Discover agent capabilities:

```
GET /.well-known/agent-card.json
```

**Response:**

```json
{
  "name": "Intugle Data Agent",
  "description": "Agent for building data apps...",
  "version": "0.1.0",
  "supported_interfaces": [
    {
      "protocol_binding": "JSONRPC",
      "protocol_version": "1.0",
      "url": "https://your-instance.intugle.ai/a2a/"
    }
  ],
  "capabilities": {
    "streaming": true,
    "push_notifications": false
  },
  "security_schemes": {
    "bearerAuth": {
      "http_auth_security_scheme": {
        "scheme": "bearer",
        "bearer_format": "JWT"
      }
    }
  },
  "default_input_modes": ["text/plain", "application/json"],
  "default_output_modes": ["text/plain", "application/json"],
  "skills": [{
    "id": "intugle_data_agent",
    "name": "Intugle Data Agent",
    "description": "...",
    "tags": ["data", "analytics", "metadata", "agent"],
    "examples": [
      "Show me customer growth over time",
      "Find tables related to revenue",
      "Build a chart for monthly sales"
    ]
  }]
}
```

---

## Cancel Task

```json
{
  "jsonrpc": "2.0",
  "method": "task/cancel",
  "params": {
    "task_id": "task-123"
  },
  "id": "3"
}
```

---

## Error Handling

### JSON-RPC Errors

| Code | Message |
|------|---------|
| `-32700` | Parse error |
| `-32600` | Invalid request |
| `-32601` | Method not found |
| `-32602` | Invalid params |

### Application Errors

| HTTP | Description |
|------|-------------|
| `401` | Invalid/expired token |
| `403` | No access to workspace |
| `408` | Request timeout |

---

## Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `A2A_AGENT_NAME` | `Intugle Agent` | Agent name in card |
| `A2A_AGENT_VERSION` | `0.1.0` | Agent version |
| `A2A_CLIENT_DISCONNECT_TIMEOUT_MS` | `15000` | Disconnect timeout |
