---
id: context-history
title: Activity (Beta)
sidebar_position: 8
---

# Activity (Beta)

**Activity (Beta)** is a read-only, workspace-wide record of meaningful changes to AI context, workspace configuration, data setup, and deployments.

<!-- Screenshot: Activity page with the toolbar, filter sidebar, and timeline. -->

---

## 1. Overview

Activity gives workspace users and administrators a chronological audit trail of configuration and context updates across a workspace.

With Activity, you can:

- **Understand what changed and who changed it** across prompts, metadata, business concepts, data sources, and deployments.
- **Troubleshoot unexpected AI behavior** by tracing recent edits to instructions, few-shots, concepts, or data scope.
- **Review deployment and data-scope changes** before or after publishing or updating a ChatApp.
- **Support governance and change-management processes** with filterable history and CSV exports.

:::note Beta feature
Activity is currently labeled **Beta** and may not be enabled in every deployment.
:::

:::info Activity vs. Observability
- **Activity** records **configuration and context changes** (what was edited, added, removed, enabled, or deployed).
- **Observability** records **AI queries, responses, feedback, errors, and performance** (how the AI answered user questions).
:::

---

## 2. Accessing Activity

You can open Activity in two ways:

1. **From Prompt Flow:** Open **Prompt Flow** in the left navigation and select **Activity (Beta)**.
2. **From contextual Activity shortcuts:** Supported areas include an **Activity** shortcut that opens Activity pre-filtered to that area or item.

<!-- Screenshot: Prompt Flow navigation showing Activity (Beta) and a contextual Activity shortcut. -->

Contextual shortcuts are available from supported areas, including:

- **Agent Configurator / Prompts**
- **Few-Shots**
- **Concepts**
- **Use-Case Summary / Instructions**
- **Memory**
- **Metadata / Semantic Layer**
- **Cache**
- **Data Assets and Data Products**
- **Document Connections and Processing**

---

## 3. What Activity Tracks

Activity focuses on meaningful changes to workspace configuration, AI context, data setup, and deployments:

| Category | Examples of changes tracked |
|---|---|
| **Prompts** | Prompt edits and restores, test cases, custom model settings, agent preferences and configuration |
| **Skills** | Workspace version saves, skill restores, enablement changes |
| **Few-shots** | Create, edit, delete, bulk deletion, restore, agent-submitted examples |
| **Concepts** | Create, edit, delete, restore, agent-submitted concepts |
| **Instructions** | Use-case summary updates and restores |
| **Semantic metadata** | Table and column metadata, chat enablement, calculated fields, relationships, semantic-layer restores, completion summaries |
| **Data products** | Product creation and updates, SQL edits, names and formats, refresh modes, schedules |
| **Documents** | Upload and delete, metadata and rename, processing/OCR settings, generated summaries, resets |
| **Memory** | Workspace, ChatApp, and user memory configuration; universal instructions; schedules; import confirmation |
| **Cached questions** | Create and delete, status updates, bulk changes |
| **Integrations** | MCP connector changes, MCP tool permissions, credential-rotation metadata |
| **Deployments** | ChatApp context, content, agent, tool, integration, data, and memory scopes; create, redeploy, revert, disable, enable, and import baseline |
| **Data sources** | Source-table selection, creation, and deletion; connection changes; Fivetran setup and table selection |
| **Workspace settings** | Data and agent scope, response structure, glossary, document instructions, retrieval, database summary, web/chat domains |

### Additional Coverage Notes

- **Jobs** may show schedule changes for autocorrection and row shortlisting.
- **Evaluations** has partial coverage for evaluation schedule changes and feedback annotations.
- **Application presentation settings**—including ChatApp display/branding, App Designer configurations, dashboard/widget configurations, and embed configuration—are not currently tracked.
- **Operational output is intentionally excluded:** job runs, progress updates, logs, retries, generated results, query outputs, and vector or cache internals are not recorded in Activity.
- **No-op saves do not create events:** saving without a meaningful change (for example, redeploying without context-scope changes) does not create a context event.

---

## 4. Understanding Coverage

Click the **Activity coverage** help icon (`?`) in the toolbar to view what is tracked in your current deployment.

<!-- Screenshot: Activity coverage dialog showing Tracked, Partial, Untracked, and Remaining areas. -->

The coverage dialog uses the following statuses:

| Status | Meaning |
|---|---|
| **Tracked** | The listed areas are recorded in the current deployment. |
| **Partial** | Some, but not all, related areas are recorded. |
| **Untracked** | The category is not recorded in the current deployment. |
| **Remaining areas** | Related behavior not yet represented in Activity. |

Coverage reflects what is enabled in your current environment, so available categories may differ between deployments.

---

## 5. Using the Activity Page

<!-- Screenshot: Complete Activity page showing toolbar, filters, timeline rows, and pagination controls. -->

### Toolbar

| Control | What It Does |
|---|---|
| **Show / Hide filters** | Toggles the filter sidebar and displays the active-filter count. |
| **Search** | Searches event names and summaries. A short delay applies before results update as you type. |
| **Refresh** | Reloads the timeline with the latest events. |
| **Export CSV** | Downloads matching events as `activity.csv`. |
| **Time range** | Filters events by time. Defaults to **Past 1 day**, with presets from **30 minutes** through **90 days**, plus a **Custom** date/time range. |
| **Coverage (`?`)** | Opens the Activity coverage dialog for your current deployment. |

### Filters

Use the filter sidebar to narrow the timeline:

- **Category** — Filter by functional area (for example, Prompts, Few-shots, Deployments).
- **Entity type** — Filter by the specific type of item changed.
- **Action** — Filter by **Create**, **Update**, **Delete**, **Restore**, **Enabled**, **Disabled**, or **Baseline**.
- **Changed by** — Filter by the user, agent, or service associated with the change.
- **Actor type** — Filter by **User**, **Agent**, **Service**, or **System**.

:::note System events
System-generated events are hidden by default to keep the feed focused on user, agent, and service changes. Select **System** under **Actor type** when you want to include them.
:::

Available filter values and counts update dynamically to reflect the current filtered result set. Select **Clear all** to reset all active filters.

### Timeline and Pagination

- Events are listed in **reverse-chronological order** (newest first).
- Each row displays the **changed item**, **action**, **category**, **summary**, **changed-field preview**, **actor**, and **relative timestamp**.
- Bulk updates saved in a single operation are grouped together (for example, **“N changes saved together.”**).
- Use the page size selector to display **10**, **15**, **25**, **50**, or **100** rows per page, and use **Previous** and **Next** to page through results.

---

## 6. Reviewing an Event

Click any row in the timeline to open the **Change details** side panel.

<!-- Screenshot: Change details drawer showing a field diff and complete JSON comparison. -->

The side panel displays:

- **Changed item**
- **Category and entity type**
- **Changed by**
- **Date and time**
- **Summary**
- **Fields changed**

### How Changes Are Displayed

Depending on what changed, the panel adapts how before-and-after values are presented:

- **Simple values** are shown as `before → after`.
- **Lists** highlight additions and removals.
- **Long text, prompts, and SQL** are shown as a text diff.
- **Purpose-built views** format structured changes for deployment scopes, data scope, agent scope/configuration/preferences, MCP permissions, domain configuration, memory records, table lifecycle, and pipeline-completion events.

Select **View complete JSON comparison** when you need to inspect the full recorded before-and-after structure.

:::note Activity is read-only
You cannot revert or edit configurations directly from Activity. To undo a change, restore or update it in the original feature. When a restore or revert succeeds in the source feature, it appears as a **Restore** event in Activity.
:::

---

## 7. Exporting Activity

To export Activity events to CSV:

1. Apply any **filters** and select the desired **time range**.
2. Click **Export CSV** in the toolbar.
3. Download **`activity.csv`**.

### Export Behavior and Columns

- Exports respect your **active filters**, **selected time range**, and **user visibility permissions**.
- Each export is limited to **10,000 events**. Narrow your filters or time range if your selection exceeds this limit.
- **Full before-and-after snapshots are omitted** from CSV exports to keep downloads lightweight and reduce exposure of unnecessary configuration detail.

`activity.csv` includes the following columns:

| Column | Description |
|---|---|
| **Occurred at** | Timestamp when the change completed |
| **Category** | High-level area of the change |
| **Entity type** | Specific type of item changed |
| **Entity name** | Name or identifier of the changed item |
| **Action** | Action performed (Create, Update, Delete, Restore, Enabled, Disabled, Baseline) |
| **Actor type** | User, Agent, Service, or System |
| **Changed by** | User, agent, or service that made the change |
| **Source** | Feature or workflow where the change originated |
| **Summary** | Human-readable description of the change |
| **Changed fields** | List of fields modified in the event |

---

## 8. Privacy, Visibility, and Security

- **Workspace isolation:** Users can view Activity only for workspaces they have access to.
- **Personal vs. workspace visibility:** Workspace and shared configuration changes are visible within the workspace. Personal records and preferences are visible only to the affected user and workspace administrators.
- **Automatic redaction:** Sensitive values are automatically redacted and are not exposed in Activity details or CSV exports, including:
  - Credentials and API keys
  - Passwords and tokens
  - OAuth payloads
  - Connection strings
  - Headers and private keys
  - Raw file content and binaries
- **Completed changes only:** Only completed changes appear in the Activity feed. Failed or in-progress save attempts do not appear as completed events.

---

## 9. Common Use Cases

- **Investigate a sudden change in AI answer quality** by reviewing recent prompt, instruction, concept, metadata, or scope changes.
- **Review data access and metadata modifications** across tables, columns, relationships, and data products.
- **Audit MCP connector or tool permission updates** to verify integration changes.
- **Review deployment scope** before or after a ChatApp redeploy.
- **Establish an audit trail after workspace import**, including deployment baselines (see [Change Management of Workspaces](./change-management) and [Workspace Import/Export](./import-export)).
- **Export filtered activity** for compliance, peer reviews, or change-management records.

---

## 10. FAQ

### Why is Activity missing from Prompt Flow?
Activity is a **Beta** feature and may not be enabled in your current deployment. If you expect it to be available, contact your workspace administrator or Intugle support.

### Why does Activity say "Context History Unavailable"?
The Activity service may be unavailable or disabled in your current environment. Try refreshing the page; if the message persists, contact your workspace administrator or Intugle support.

### Why does a change not appear in Activity?
Check the following:
- **Time range:** Expand the time range (the default is **Past 1 day**).
- **Filters:** Clear active filters or search terms.
- **Refresh:** Click **Refresh** in the toolbar.
- **Meaningful change:** Confirm the save actually modified something—no-op saves do not create events, and failed or in-progress saves are not recorded.
- **Coverage:** Check the **Coverage (`?`)** dialog to see whether the area is currently tracked or excluded (such as operational runs or presentation/branding settings).
- **System events:** If the update was system-initiated, select **System** under **Actor type**.

### Why can't I see another user's personal memory or preferences?
Personal memory records and user preferences are restricted to the affected user and workspace administrators.

### Can I restore a change directly in Activity?
No. Activity is read-only. To revert a change, open the original feature and restore or update it there. Successful restores appear in Activity as **Restore** events.

### Are credentials or secrets shown in Activity or CSV?
No. Credentials, API keys, passwords, tokens, OAuth payloads, connection strings, headers, private keys, and raw file binaries are automatically redacted.

### Why does the CSV not include full before-and-after values?
Full before-and-after snapshots are omitted from `activity.csv` to keep exports lightweight and avoid exposing unnecessary configuration detail. Open an event's **Change details** panel in the UI to inspect field-level diffs or the complete JSON comparison.

### Is there an export limit?
Yes. CSV exports are limited to **10,000 events** per download. Narrow your time range or filters if you need to export a larger set in batches.

### What happens to Activity after workspace export/import?
Importing a workspace establishes **Baseline** events in the new workspace so you have a clear starting audit trail for imported configurations and deployments.

### What is the difference between Activity and Observability?
**Activity** tracks configuration and context changes (prompts, metadata, concepts, scopes, deployments), while **Observability** tracks runtime AI interactions (questions asked, responses, user feedback, execution time, and query errors).
