---
title: MCP Server Configuration
sidebar_position: 2
---

# Using Intugle as an MCP Server

This guide explains how to connect external MCP clients (like Claude Desktop, Cursor, or other AI tools) to your Intugle ChatApp using the Model Context Protocol.

## Overview

When configured as an MCP server, Intugle exposes the **IntugleAgent** tool that allows external AI assistants to:
- Query and analyze your connected data sources
- Explore metadata and semantic layer definitions
- Generate visualizations and data products
- Access workspace-specific knowledge

## Prerequisites

Before connecting an MCP client to Intugle:

1. **Deployed ChatApp**: You must have a deployed ChatApp in your workspace
2. **MCP Credentials**: Obtain your MCP URL and API key from the Deploy Wizard
3. **MCP-Compatible Client**: An MCP client that supports Streamable HTTP transport

## Getting MCP Credentials

### Step 1: Access Deploy Wizard

Navigate to your deployed ChatApp and open the settings or deployment configuration panel.

:::info Screenshot Needed
**mcp-config-panel.png** - Deploy Wizard → MCP Config Panel showing the MCP URL field and masked API key field with copy buttons visible.
:::

### Step 2: Copy Connection Details

The MCP Config Panel displays:
- **MCP URL**: The endpoint for MCP connections (e.g., `https://your-instance.intugle.ai/mcp/`)
- **API Key**: Your JWT authentication token (click the eye icon to reveal)
- **Expiration**: When the current API key expires

Click the copy icon next to each field to copy the values to your clipboard.

:::info Screenshot Needed
**mcp-copy-credentials.png** - After clicking the copy button, showing the success toast/notification confirming the value was copied.
:::

### Step 3: Regenerate API Key (Optional)

If your API key is compromised or expired, you can regenerate it:

1. Click the **Regenerate** button
2. Confirm the action in the dialog

:::info Screenshot Needed
**mcp-regenerate-confirm.png** - The confirmation dialog that appears when clicking Regenerate, warning that existing connections will be invalidated.
:::

:::warning
Regenerating the API key will invalidate all existing MCP connections. You will need to update the API key in all connected clients.
:::

## Client Configuration

### Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "intugle": {
      "url": "https://your-instance.intugle.ai/mcp/",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Replace:
- `https://your-instance.intugle.ai/mcp/` with your MCP URL
- `YOUR_API_KEY` with your actual API key

### Cursor IDE

In Cursor, add an MCP server through the settings:

1. Open **Settings** → **MCP Servers**
2. Click **Add Server**
3. Enter the configuration:
   - **Name**: `Intugle`
   - **URL**: Your MCP URL
   - **Transport**: `streamable-http`
   - **Headers**: `Authorization: Bearer YOUR_API_KEY`

### Generic MCP Clients

For other MCP clients, use these connection parameters:

| Parameter | Value |
|-----------|-------|
| **URL** | Your MCP URL from the config panel |
| **Transport** | `streamable-http` |
| **Authentication** | Bearer token in `Authorization` header |

## IntugleAgent Tool

Once connected, your MCP client will have access to the **IntugleAgent** tool.

### Tool Schema

```json
{
  "name": "IntugleAgent",
  "description": "Intelligent data analytics agent for exploring, querying, and analyzing your connected data sources. Supports natural language queries, metadata exploration, and data visualization.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language query or instruction for the data agent"
      }
    },
    "required": ["query"]
  }
}
```

## Input Options

The IntugleAgent accepts various types of natural language inputs:

### Query Types

| Input Type | Description | Example |
|------------|-------------|---------|
| **Data Query** | Questions about your data | "What were total sales last quarter?" |
| **Aggregation** | Grouped/summarized data requests | "Show revenue by region and product category" |
| **Trend Analysis** | Time-based analysis | "Compare this month's performance to last year" |
| **Filtering** | Subset data requests | "Show only customers from North America with orders > $1000" |
| **Metadata Exploration** | Data structure questions | "What tables and columns are available?" |
| **Follow-up Query** | Contextual refinements | "Now break that down by month" |
| **Visualization Request** | Chart/graph generation | "Create a bar chart showing top 10 products" |

### Input Format

```json
{
  "query": "Your natural language question or instruction"
}
```

### Example Inputs

```json
// Simple data query
{ "query": "What were our total sales last month?" }

// Aggregation with grouping
{ "query": "Show revenue broken down by region and product category" }

// Time-based comparison
{ "query": "Compare Q4 2024 sales to Q4 2023" }

// Filtering with conditions
{ "query": "List all customers who purchased more than $10,000 this year" }

// Metadata exploration
{ "query": "What data sources are connected and what tables do they have?" }

// Visualization request
{ "query": "Create a line chart showing monthly revenue trends for the past 12 months" }

// Follow-up (uses session context)
{ "query": "Now filter that to only show the top 5" }
```

## Output Options

The IntugleAgent returns rich, structured responses in multiple formats:

### Output Types

| Output Type | Description | When Used |
|-------------|-------------|-----------|
| **Text** | Plain text explanations | Always included with responses |
| **Markdown** | Formatted text with headers, lists, tables | Reports, summaries, explanations |
| **Table** | Structured tabular data | Query results with rows and columns |
| **Chart** | Data visualizations | Trends, comparisons, distributions |
| **Card** | Summary metrics/KPIs | Executive summaries, key metrics |
| **Elicitation** | Request for user input | When clarification is needed |
| **Progress** | Status updates | During long-running operations |

### Output Format Examples

#### Text/Markdown Response

```json
{
  "type": "text",
  "content": "## Sales Summary\n\nTotal revenue for Q4 2024 was **$1.2M**, representing a **15% increase** compared to Q4 2023.\n\n### Key Highlights\n- North America: $500K (+12%)\n- Europe: $400K (+18%)\n- Asia Pacific: $300K (+22%)"
}
```

#### Table Response

```json
{
  "type": "table",
  "title": "Top 10 Customers by Revenue",
  "columns": [
    { "name": "Customer", "type": "string" },
    { "name": "Revenue", "type": "currency" },
    { "name": "Orders", "type": "number" },
    { "name": "Growth", "type": "percentage" }
  ],
  "rows": [
    ["Acme Corporation", "$150,000", 45, "+12%"],
    ["Globex Industries", "$120,000", 38, "+8%"],
    ["Initech LLC", "$95,000", 29, "+15%"]
  ],
  "metadata": {
    "totalRows": 10,
    "queryTime": "1.2s"
  }
}
```

#### Chart Response

```json
{
  "type": "chart",
  "chartType": "bar",
  "title": "Revenue by Region",
  "data": {
    "labels": ["North America", "Europe", "Asia Pacific", "Latin America"],
    "datasets": [{
      "label": "Revenue ($K)",
      "values": [500, 400, 300, 150]
    }]
  },
  "config": {
    "showLegend": true,
    "showValues": true
  }
}
```

#### Card Response (KPI Summary)

```json
{
  "type": "card",
  "cards": [
    {
      "title": "Total Revenue",
      "value": "$1.2M",
      "trend": { "direction": "up", "value": "+15%" },
      "subtitle": "vs. last quarter"
    },
    {
      "title": "Active Customers",
      "value": "1,247",
      "trend": { "direction": "up", "value": "+8%" },
      "subtitle": "vs. last quarter"
    },
    {
      "title": "Average Order Value",
      "value": "$342",
      "trend": { "direction": "down", "value": "-3%" },
      "subtitle": "vs. last quarter"
    }
  ]
}
```

#### Elicitation Response (Human-in-the-Loop)

```json
{
  "type": "elicitation",
  "elicitationType": "selection",
  "message": "Which time period would you like to analyze?",
  "options": [
    { "value": "7d", "label": "Last 7 days" },
    { "value": "30d", "label": "Last 30 days" },
    { "value": "quarter", "label": "Last quarter" },
    { "value": "ytd", "label": "Year to date" }
  ]
}
```

#### Progress Update

```json
{
  "type": "progress",
  "message": "Executing query against sales database...",
  "percentage": 45,
  "stage": "query_execution"
}
```

### Combined Response Example

A typical response may include multiple output types:

```json
{
  "outputs": [
    {
      "type": "text",
      "content": "Here's your sales analysis for Q4 2024:"
    },
    {
      "type": "card",
      "cards": [
        { "title": "Total Revenue", "value": "$1.2M", "trend": { "direction": "up", "value": "+15%" } }
      ]
    },
    {
      "type": "chart",
      "chartType": "line",
      "title": "Monthly Revenue Trend",
      "data": { ... }
    },
    {
      "type": "table",
      "title": "Revenue by Region",
      "columns": ["Region", "Revenue", "Growth"],
      "rows": [...]
    }
  ]
}
```

## Session Management

Intugle's MCP server maintains sessions to preserve context across interactions:

- **Session Persistence**: Conversation context is maintained within a session
- **Workspace Context**: Each session is bound to a specific workspace and its data connections
- **Timeout Handling**: Sessions automatically clean up after periods of inactivity

### Session Behavior

| Scenario | Behavior |
|----------|----------|
| New connection | Creates a new session with fresh context |
| Continued conversation | Maintains context from previous messages |
| Client disconnect | Session preserved for reconnection (configurable timeout) |
| Token expiration | Requires re-authentication with new token |

## Human-in-the-Loop (Elicitation)

Intugle's MCP server supports elicitation, allowing the agent to request additional input during execution:

### Elicitation Types

| Type | Description | Example |
|------|-------------|---------|
| **Selection** | Choose from predefined options | "Which metric: Revenue, Units, or Profit?" |
| **Text** | Free-form text input | "Enter the custom date range" |
| **Confirmation** | Yes/No decision | "This will process 1M rows. Continue?" |
| **Calculated Field** | Define a computation | "How should we calculate 'profit margin'?" |
| **Attribute Selection** | Choose dimensions/measures | "Which columns to include in the report?" |

:::info
Elicitation support depends on your MCP client's capabilities. Claude Desktop and other modern clients support this feature.
:::

## Progress Reporting

For long-running operations, Intugle reports progress to connected clients:

| Stage | Description |
|-------|-------------|
| `query_planning` | Analyzing the request and planning execution |
| `query_execution` | Running queries against data sources |
| `data_processing` | Processing and transforming results |
| `visualization` | Generating charts and visualizations |
| `response_generation` | Formatting the final response |

Progress updates appear in your MCP client's interface, allowing you to monitor operation status.

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid or expired API key | Regenerate API key and update client config |
| `403 Forbidden` | Insufficient permissions | Check workspace access permissions |
| `408 Request Timeout` | Query took too long | Simplify query or check data source connectivity |
| `503 Service Unavailable` | Server temporarily unavailable | Retry after a few moments |

### Troubleshooting

1. **Connection Refused**
   - Verify the MCP URL is correct
   - Check that the ChatApp is deployed and running
   - Ensure your network allows connections to the Intugle server

2. **Authentication Failed**
   - Confirm the API key is correct and not expired
   - Check that the Authorization header format is `Bearer <token>`
   - Regenerate the API key if issues persist

3. **Tool Not Found**
   - Restart your MCP client to refresh the tool list
   - Verify the MCP server is properly configured

## Security Considerations

### API Key Security

- **Never share** your API key publicly
- **Rotate keys** periodically or when team members change
- **Use environment variables** instead of hardcoding keys in config files

### Network Security

- All MCP connections use HTTPS encryption
- JWT tokens have configurable expiration
- Sessions are isolated per user and workspace

### Audit Logging

All MCP interactions are logged for security and debugging:
- Connection attempts (successful and failed)
- Tool invocations and parameters
- Session lifecycle events

## Configuration Reference

### Server Settings

These settings are configured on the Intugle server side:

| Setting | Description | Default |
|---------|-------------|---------|
| `MCP_TOOL_NAME` | Name of the exposed tool | `IntugleAgent` |
| `MCP_TOOL_DESCRIPTION` | Tool description for clients | See above |
| `MCP_CLIENT_DISCONNECT_TIMEOUT_MS` | Time to wait before cleaning up disconnected sessions | `15000` (15 seconds) |
| `MCP_AUTHENTICATION_JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
