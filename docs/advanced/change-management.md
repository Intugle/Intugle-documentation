---
title: Change Management of Workspaces
sidebar_position: 4
---

# Change Management of Workspaces


What gets promoted when app is promoted (deployed) within the workspace — A full workspace. When you deploy an agent, the platform creates a separate copy of your context and semantic graph for that deployed app, and that copy is what travels with the workspace. Each time a workspace is imported into the NetApp production environment, a brand-new workspace is created on the prod side.

The promotion is driven from the Intugle platform.

## Promotion Steps

1. Create a workspace in **Staging** by connecting your StageDB data to the Intugle platform (stage).
2. Configure the agent context in the developer instance, then deploy the agent within the same workspace. Deployment is what creates the separate copy of context and semantic graph.
3. Test against the deployed app in staging.
4. Once you are satisfied with the deployed agent's results, export the staging workspace. See the [Workspace Import/Export](./import-export.md) guide for instructions.
5. On import into the production environment, a new workspace is created.
6. The import automatically triggers vector DB creation for Row Shortlisting, Auto Correction, few-shots, concepts, and cached questions.
7. Deploy the agent inside the new production workspace.
8. Update any compute connection details to point to the correct production data source. See [Edit Workspace Compute Connection Details](./edit-workspace-compute.md) for instructions.

## MCP Keys

- Redeploying an agent **within the same workspace** does **not** change its MCP key.
- MCP keys are unique per workspace, so a newly imported production workspace will have a different MCP key.
- The new key must be shared with your MCP client so it can communicate with the new deployment.

## Downtime

The only downtime window is the duration of the import plus the Row Shortlisting and Auto Correction jobs (which depend on collection size). In practice this is effectively **zero downtime**, because the old workspace and its deployed agent continue serving traffic throughout the entire process.

## Rollback

Because each promotion creates a new workspace and your previous production workspace (with its deployed agent) keeps running, reverting is fast and low-risk:

- To roll back, point your MCP client back to the old workspace token.
- The previous deployment is untouched and continues serving — no rebuild or restore step is required.

## When Import/Export Can Be Avoided

If you only need to update **few-shots**, **concepts**, or **cached questions**, you can add or remove them directly in the developer instance inside the production namespace and then redeploy the app. A full import/export cycle is not necessary in this case.

## When Import/Export is Recommended

A full export and import is recommended when:

- A **new table** has been added to the semantic layer.
- The **schema has been updated** for an existing set of tables.
