---
id: prompt-flow
title: Page 5 — Prompt Flow & Agents
sidebar_position: 6
---

# Page 5 — Prompt Flow & Agents

The **Prompt Flow** page is the control center for customizing how Intugle's AI agents think, reason, and respond to your questions. This is where you fine-tune the AI to understand your specific business context, terminology, and data.

:::warning Admin access required
To edit prompts, concepts, few-shots, and metadata, you must enable the **Admin** toggle (top-right corner). Without it, you can view but not modify configurations.
:::

---

## Understanding the Prompt Flow System

When you ask Intugle a question, here's what happens behind the scenes:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR QUESTION                                 │
│              "What were our top products last quarter?"              │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION AGENT                               │
│  • Reads your question                                               │
│  • Checks Universal Instructions (global rules)                      │
│  • Decides which specialist agent(s) to call                         │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
           ┌───────────┐  ┌───────────┐  ┌───────────┐
           │ MetaData  │  │   Data    │  │ Semantic  │
           │ Analysis  │  │ Analysis  │  │   Graph   │
           └───────────┘  └───────────┘  └───────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AI REFERENCES:                                    │
│  • Analytics Catalog → Business concept definitions                  │
│  • Few-Shots → Example Q&A pairs for similar questions               │
│  • Metadata → Table/column descriptions and relationships            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR ANSWER                                   │
│  "Based on your sales data, the top 5 products by revenue were..."   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Page Layout

The page has **four tabs** across the top:

| Tab | Purpose |
|---|---|
| **Agent Configurator** | Edit the prompts that control how each AI agent behaves |
| **Few-Shots** | Create example Q&A pairs to train the AI |
| **Analytics Catalog** | Define business concepts and metric formulas |
| **Metadata** | View and edit table/column descriptions |

### Global Controls (Top-Right)

| Control | What It Does |
|---|---|
| **Subscription** toggle | Switch between subscription views |
| **Admin** toggle | Enable edit mode for all configurations |
| **+ Add LLM Model** | Connect additional AI models (GPT-4, Claude, Gemini, etc.) |

---

## Tab 1 — Agent Configurator

The Agent Configurator lets you customize the **system prompts** that control how each AI agent processes your questions.

![Agent Configurator tab](/img/manual/pf-agent-configurator.png)

### Three-Panel Layout

| Panel | What It Shows |
|---|---|
| **Left: Categories** | List of all AI agent types |
| **Center: Subcategories & Tasks** | The specific tasks within each agent |
| **Right: Prompt Editor** | View/edit the actual prompt text |

### Agent Categories Explained

Each agent is a specialist that handles a specific type of task:

| Agent | Role | When It's Called |
|---|---|---|
| **Orchestration Agent** | The "manager" — decides which specialist to call | Every question goes through this first |
| **Semantic Graph Agent** | Navigates table relationships | When questions involve multiple related tables |
| **MetaData Analysis** | Understands table structure | When the AI needs to know what columns exist |
| **Data Analysis** | Writes and runs SQL queries | When you ask for specific data or metrics |
| **Data Transformation** | Cleans and reshapes data | When data needs formatting or aggregation |
| **Link Discovery** | Finds hidden relationships | When discovering new table connections |
| **Document Search** | Searches uploaded documents | When questions relate to PDFs, Word docs, etc. |
| **Web Search** | Searches the internet | When contextual web information is needed |

### How to Edit an Agent Prompt

1. Click an **agent category** (left panel)
2. Select a **subcategory** (center panel)
3. Choose a **task** (center panel)
4. Edit the prompt in the **Prompt Editor** (right panel)
5. Click **Save** — changes take effect immediately

---

## Tab 2 — Few-Shots

Few-Shots are **example question-and-answer pairs** that teach the AI how to handle specific types of queries for your business.

![Few-Shots tab](/img/manual/05_pf_fewshots.png)

### Why Few-Shots Matter

Without few-shots, the AI might:
- Use the wrong table for a query
- Misunderstand business terminology
- Calculate metrics incorrectly

With few-shots, you show the AI: *"When someone asks THIS, here's exactly how to answer."*

### Few-Shot Card Details

Each card shows:

| Field | Description |
|---|---|
| **Name** | Descriptive title (e.g., "Customer 360 Query") |
| **Status** | 🟢 Active (AI uses it) or 🔴 Inactive (disabled) |
| **Table Tags** | Which data tables this example references |
| **Created By** | Who authored this few-shot |

### Top-Right Actions

| Button | What It Does |
|---|---|
| **Find Similar** | Identifies duplicate or overlapping few-shots |
| **Import/Export** | Bulk import/export few-shots as JSON or CSV |
| **Run All** | Tests all active few-shots to verify they still work |
| **+ New Few-Shot** | Create a new example Q&A pair |

### Creating a New Few-Shot

1. Click **+ New Few-Shot**
2. Enter a **question** — the type of query users might ask
3. Enter the **ideal answer** or SQL query the AI should generate
4. Select which **tables** are involved
5. Set status to **Active**
6. Click **Save**

---

## Tab 3 — Analytics Catalog

The Analytics Catalog is a library of **business concepts and metric definitions** that the AI references when answering questions.

![Analytics Catalog tab](/img/manual/pf-analytics-catalog.png)

### What is a Concept?

A **concept** is a business term with a defined meaning. For example:

| Concept Name | Definition |
|---|---|
| **Customer Churn** | "Customers who cancelled their subscription in the last 30 days, calculated as cancelled / total active" |
| **Net Revenue Retention** | "Revenue from existing customers this period / revenue from same customers last period × 100" |
| **Top Products** | "Products ranked by total order value, excluding returns and refunds" |

### Why the Catalog Matters

Without catalog entries, asking "What's our churn rate?" might give inconsistent results because the AI doesn't know YOUR specific definition. With a catalog entry, it always uses your formula.

### Top-Right Actions

| Button | What It Does |
|---|---|
| **Universal Instructions** | Set global rules that apply to ALL concepts and AI responses |
| **Find Similar** | Find duplicate or overlapping concepts |
| **Import/Export** | Bulk import/export concepts |
| **+ New Concept** | Create a new business concept definition |

### Universal Instructions

Click **Universal Instructions** to open a dialog where you can set global rules that apply to ALL AI interactions:

![Universal Instructions dialog](/img/manual/pf-universal-instructions.png)

| Field | Description |
|---|---|
| **Instruction Content** | Global rules the AI follows for every query (e.g., "Always report currency in USD", "Use fiscal year starting April 1") |
| **Change Note** | Optional description of what you changed (for version history) |
| **Version History** tab | View previous versions of the instructions |

### Creating a New Concept

1. Click **+ New Concept**
2. Enter a **concept name** (e.g., "Monthly Active Users")
3. Write a **description** explaining what this metric means and how to calculate it
4. Set status to **Active**
5. Click **Save**

---

## Tab 4 — Metadata

The Metadata tab provides a **spreadsheet-like view** of all your data tables, columns, relationships, and descriptions.

![Metadata tab](/img/manual/05_pf_metadata.png)

### Page Header Summary

```
Metadata Management
Excel-like view for all column metadata and table relationships
19 tables · 192 columns · 35 links
```

This tells you exactly how much data the AI has access to.

### Three Sub-Tabs

| Sub-Tab | What It Shows |
|---|---|
| **Table Metadata** | All tables with domain, name, description, row/column counts |
| **Column Metadata** | Every column across all tables with types and descriptions |
| **Table Relationships** | Foreign-key links between tables |

### Table Metadata Columns

| Column | Description |
|---|---|
| **Domain** | Business domain (Marketing, Sales, Products, Support) |
| **Table Name** | The actual table name in your database |
| **Glossary** | AI-generated description of what the table contains |
| **Table Type** | Source = raw data table |
| **Row Count** | Number of rows |
| **Column Count** | Number of columns |

### Top-Right Actions

| Button | What It Does |
|---|---|
| **Usecase Summary** | View a summary of use cases across your data |
| **History** | See change history of metadata edits |
| **Commit Changes** | Save and apply any edits you've made |
| **Profile** dropdown | Switch between metadata profile views |
| **Columns** dropdown | Show/hide columns in the grid |

### Editing Metadata

Click any cell to edit it directly:
- Edit **Glossary** descriptions to help the AI understand table contents
- Change **Domain** assignments to re-classify tables

:::warning
Click **Commit Changes** (red button) after editing — changes are NOT saved automatically.
:::

---

## How It All Works Together

Here's a complete example of how Prompt Flow components work together:

### Scenario: User asks "What's our customer churn this quarter?"

1. **Orchestration Agent** receives the question
2. It checks **Universal Instructions** for global rules
3. It routes to **MetaData Analysis** to find relevant tables
4. **MetaData Analysis** checks the **Metadata** tab and finds `customers`, `subscriptions` tables
5. The system checks the **Analytics Catalog** and finds a "Customer Churn" concept definition
6. It checks **Few-Shots** for similar questions that have been answered before
7. **Data Analysis** agent writes a SQL query using:
   - The concept definition (how to calculate churn)
   - The metadata (which tables/columns to use)
   - Any matching few-shot examples
8. The query runs and returns results
9. The answer is formatted and returned to the user

---

## Best Practices

### For Agent Prompts
- Keep prompts concise and specific
- Include examples of expected behavior
- Test changes with real questions before deploying

### For Few-Shots
- Create few-shots for your most common questions
- Include variations of how users might ask the same thing
- Run "Run All" periodically to catch broken examples

### For Analytics Catalog
- Define ALL your key business metrics
- Be specific about calculation methods
- Include edge cases (e.g., "exclude returns from revenue calculations")

### For Metadata
- Write clear, business-friendly descriptions for every table
- Keep descriptions up-to-date when schemas change
- Use consistent domain classifications
