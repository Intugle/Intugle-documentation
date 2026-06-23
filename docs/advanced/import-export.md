---
title: Workspace Import/Export
sidebar_position: 2
---

# Workspace Import/Export Guide

## Overview
This guide explains how to export and import workspaces, what data is included in the process, and how different settings affect your newly imported environment.

### Common Use Cases
A primary use case for the import/export functionality is promoting workspaces across environments. For example, you can fully configure and test your workspace in a staging or lower environment, and then export and import it to seamlessly move those configurations into your production environment.

## Exporting a Workspace

**⚠️ IMPORTANT: Commit Your Changes!**
Before exporting, you must ensure that all changes in your semantic layer have been committed. Any uncommitted changes will **NOT** be included in the final export bundle.

To export an existing workspace:
1. Navigate to the **Workspaces** list.
   ![List Workspaces](./export/1_list_workspaces.png)
2. Click the **Three-dots Menu** next to the workspace you want to export.
   ![Three-dots Menu](./export/2_three-dots-menu.png)
3. Select **Export** and wait for the workspace data to be packaged.
   ![Export Workspace](./export/3_click+export-.png)

## What is Included in the Export?
When you export a workspace, the system captures the following core components:

### Exported Artifacts and Core Configurations
- Workspace settings and subscription details
- Source connections (including credentials)
- Conversation bot configurations
- Execution engine configurations
- Unstructured file metadata
- `semantic_layer` (Contains your data assets, catalogue columns, links, and domains)
- `fewshots` (Your few-shot training examples)
- `prompts` (System and custom prompts)
- `analytics-catalogue` (Custom concepts)
- `universal-instruction`
- `use-case summary`

### Chat History (Filtered)
To keep the export lightweight and relevant, **general chat history is NOT exported**.
Only user query sessions that are functionally required are included:
- **Cached Questions:** Sessions linked to cached search questions.
- **Data Products:** Sessions linked to generated data products.

## What is NOT Included?
The following features are intentionally skipped during export and will not be available in the newly imported workspace:
- **Deployed Artifacts / Deployed ChatApps**
- **Dashboards and Dashboard Widgets**

## Importing a Workspace
To import a workspace:
1. Go to the workspaces screen and click on **Import Workspace**.
   ![Import Workspace](./import/1_import_workspace.png)
   ![Import Menu](./import/2_import_workspace_menu.png)
2. Upload the exported workspace ZIP file.
   ![Upload Menu](./import/3_after_upload_import_menu.png)
3. Vector Collection import options.
   ![Vector Collection Options](./import/3_after_upload_import_menu_vc_optoins.png)

   **Vector Collections: Recreate vs. Copy**
   - **Copy:** The system will perform a direct snapshot copy of vector collections from the source workspace to the new one. This is faster but only works if the source and destination are on the same environment.
   - **Recreate:** The system skips copying and will rebuild or re-embed the vector collections from scratch using your database rows and background processing jobs. Use this when importing across different environments.
   
   **ℹ️ Note:** The application will automatically select the appropriate option (Copy or Recreate) based on your source and destination environments. It is advised to keep the auto-selected option unless you are certain you need to override it.

4. Click **Import** and wait for the process to complete.
   ![Import Progress](./import/4_after_clicking_impprt.png)

## Post-Import Requirements
Because Deployed ChatApps are excluded from the export bundle, you must perform the following actions after importing your workspace:
1. **Deploy a New ChatApp:** You must trigger a new ChatApp deployment for the newly imported workspace.
2. **Update API Keys:** The new ChatApp deployment will require a fresh API key. You will need to update your integrations to use this newly generated key.
3. **Background Jobs:** After importing, background jobs for autocorrection and row-shortlisting will be automatically triggered. You will see these appear as active jobs in your workspace when deploying chatapp and prompt-flow jobs page.
   ![Active Jobs](./import/3_background_jobs.png)
4. **Update Compute Connection Details:** When promoting a workspace across environments (e.g., from staging to production) where the destination requires different source databases, you may need to manually edit the workspace's compute connection details to point to the correct production data source. See the [Edit Workspace Compute Connection Details](./edit-workspace-compute.md) guide for instructions.
