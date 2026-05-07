---
id: adls
title: Azure Data Lake Storage
hide_table_of_contents: true
---

# Azure Data Lake Storage Gen2 Connection Requirements

This document outlines the information required to connect to Azure Data Lake Storage Gen2 using Managed Identity authentication.

---

## Authentication Method

Managed Identity (Recommended)

---

## Information Required

### 1. Access Connector ID (Resource ID)

Full Azure Resource ID of the User Assigned Managed Identity.

Example:

```text
/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>
```

How to find:
Azure Portal → Managed Identity → Overview → JSON View → copy `id`

---

### 2. User Assigned Managed Identity ID (Client ID)

Client ID of the Managed Identity.

How to find:
Azure Portal → Managed Identity → Overview → Client ID

IMPORTANT: Use Client ID, not Object ID.

---

### 3. ADLS URL

Format:

```text
abfss://<container>@<storage-account>.dfs.core.windows.net/
```

Example:
abfss://testing@userupload.dfs.core.windows.net/

---

## Required Permissions

### 1. IAM Role Assignment

Assign to Managed Identity:

Role:
Storage Blob Data Contributor

How:
Storage Account → Access Control (IAM) → Add Role Assignment

---

### 2. Container ACL Permissions

Navigate to:

```text
Storage Account → Containers → <container> → Manage ACL
```

Grant:

- Read
- Write
- Execute

Also configure same permissions under:
Default Permissions

---

## Security Best Practices

- Prefer Managed Identity over Access Keys
- Avoid hardcoding credentials
- Restrict IAM scope to required storage account only