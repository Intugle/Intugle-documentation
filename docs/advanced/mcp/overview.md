---
title: MCP Overview
sidebar_position: 1
---

# MCP (Model Context Protocol) Overview

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect with external data sources, tools, and services. Intugle implements MCP as a **server provider**, allowing external AI tools to leverage Intugle's powerful data analytics capabilities.

## Intugle as MCP Server

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     INTUGLE MCP SERVER ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   EXTERNAL AI TOOLS                                                     │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │
│   │Claude Desktop│  │   Cursor    │  │  OpenCode   │                    │
│   │             │  │     IDE     │  │             │                    │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                    │
│          │                │                │                            │
│          └────────────────┼────────────────┘                            │
│                           │                                             │
│                    MCP Protocol (Streamable HTTP)                       │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                    INTUGLE MCP SERVER                        │      │
│   │                                                              │      │
│   │  ┌──────────────────────────────────────────────────────┐   │      │
│   │  │                  IntugleAgent Tool                    │   │      │
│   │  │                                                       │   │      │
│   │  │  INPUT:                    OUTPUT:                    │   │      │
│   │  │  • Natural language query  • Text responses           │   │      │
│   │  │  • Context/follow-ups      • Data tables              │   │      │
│   │  │                            • Charts/visualizations    │   │      │
│   │  │                            • Markdown reports         │   │      │
│   │  │                            • Elicitation requests     │   │      │
│   │  └──────────────────────────────────────────────────────┘   │      │
│   │                                                              │      │
│   │  Features:                                                   │      │
│   │  • JWT Authentication    • Session Management               │      │
│   │  • Progress Reporting    • Human-in-the-Loop               │      │
│   └─────────────────────────────────────────────────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

When operating as an **MCP Server**, Intugle exposes its AI agent capabilities to external MCP clients. This allows tools like Claude Desktop, Cursor, or any MCP-compatible client to leverage Intugle's data analytics and exploration features.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **IntugleAgent Tool** | A powerful tool providing data analytics, metadata exploration, and semantic layer operations |
| **JWT Authentication** | Secure token-based authentication for all MCP connections |
| **Session Management** | Persistent sessions maintaining conversation context |
| **Progress Reporting** | Real-time progress updates during long-running operations |
| **Human-in-the-Loop** | Elicitation support for calculated fields, metadata edits, and attribute selection |

## Input & Output Formats

### Input Options

The IntugleAgent tool accepts natural language queries:

| Input Type | Description | Example |
|------------|-------------|---------|
| **Data Query** | Questions about your data | "What were total sales last quarter?" |
| **Aggregation** | Requests for grouped/summarized data | "Show revenue by region and product category" |
| **Trend Analysis** | Time-based analysis requests | "Compare this month's performance to last year" |
| **Metadata Exploration** | Questions about data structure | "What tables are available?" |
| **Follow-up Query** | Contextual refinements | "Now filter that to only include North America" |

**Input Schema:**
```json
{
  "query": {
    "type": "string",
    "description": "Natural language query or instruction for the data agent"
  }
}
```

### Output Options

The IntugleAgent returns rich, structured responses:

| Output Type | Description | When Used |
|-------------|-------------|-----------|
| **Text** | Plain text explanations and summaries | All responses include explanatory text |
| **Markdown** | Formatted text with headers, lists, emphasis | Reports and detailed explanations |
| **Table** | Structured tabular data | Query results with multiple rows/columns |
| **Chart** | Data visualizations | Trend analysis, comparisons, distributions |
| **Card** | Summary metrics with KPIs | Executive summaries, key metrics |
| **Elicitation** | Requests for user input | When clarification or choices are needed |

**Output Examples:**

```json
// Text/Markdown Response
{
  "type": "text",
  "content": "## Sales Summary\n\nTotal revenue for Q4 was **$1.2M**, representing a 15% increase..."
}

// Table Response
{
  "type": "table",
  "columns": ["Region", "Revenue", "Growth"],
  "rows": [
    ["North America", "$500K", "+12%"],
    ["Europe", "$400K", "+18%"],
    ["Asia Pacific", "$300K", "+22%"]
  ]
}

// Chart Response
{
  "type": "chart",
  "chartType": "bar",
  "title": "Revenue by Region",
  "data": {...}
}

// Elicitation Request
{
  "type": "elicitation",
  "elicitationType": "selection",
  "message": "Which time period would you like to analyze?",
  "options": ["Last 7 days", "Last 30 days", "Last quarter", "Year to date"]
}
```

## Key Concepts

### Tools

MCP Tools are callable functions that perform specific actions. Intugle exposes the **IntugleAgent** tool to external clients, providing a unified interface for all data operations.

### Resources

Resources are data sources that can be read by MCP clients. Intugle's MCP server provides access to:
- Workspace metadata
- Semantic layer definitions
- Query results and data products

### Elicitation (Human-in-the-Loop)

Elicitation allows the MCP server to request additional input from the user during execution:

| Elicitation Type | Description |
|------------------|-------------|
| **Calculated Field** | Request user input for defining computed columns |
| **Metadata Editor** | Allow users to modify metadata definitions |
| **Attribute Selection** | Let users choose specific attributes or dimensions |
| **Confirmation** | Request confirmation before proceeding with an action |

### Sessions

MCP sessions maintain state across multiple interactions:
- Context preservation for multi-turn conversations
- Persistent workspace and connection settings
- Session tracking for analytics and debugging

## Use Cases

### IDE Integration
Connect Cursor IDE to your Intugle workspace to ask data questions while coding, without switching contexts.

### AI Assistant Enhancement
Add Intugle as a tool in Claude Desktop to give your AI assistant the ability to query and analyze your business data.

### Automated Workflows
Build automation scripts that leverage Intugle's MCP server to fetch data and generate reports programmatically.

## Next Steps

- [Configure Intugle as MCP Server](./mcp-server.md) - Get credentials and connect external AI tools
