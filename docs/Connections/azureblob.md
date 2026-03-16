---
id: azureblob
title: Azure Blob Storage
hide_table_of_contents: true
---

# Azure Blob Storage Connection Requirements

This document outlines the information required to connect to Azure Blob Storage using Access Key authentication.

---

## Authentication Method

Storage Account Access Key

---

## Information Required

### 1. Storage Account Name

Example:
useruploadsstg

How to find:
Azure Portal → Storage Accounts → Select Account → Overview

---

### 2. Container Name

Example:
testing

How to find:
Storage Account → Containers

---

### 3. Path Prefix (Optional)

Folder path inside container.

Example:
data

Leave empty if accessing container root.

---

### 4. Access Key

Storage account key (Key1 or Key2).

How to find:
Storage Account → Security + networking → Access keys → Show → Copy Key1

IMPORTANT:
Copy the Key value only, not the connection string.

---

## Required Permissions

The Access Key grants full storage account access.

No additional IAM role assignment required.

---

## Security Best Practices

- Avoid using Access Keys in production if possible
- Prefer Managed Identity where supported
- Rotate keys periodically
- Store keys securely (e.g., Key Vault)