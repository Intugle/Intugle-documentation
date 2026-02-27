---
sidebar_position: 1
---
# Databricks Connection Requirements

This document outlines the information and access required to connect your Databricks environment to our application.

> **Recommendation:**
> For best performance, your Databricks workspace should be deployed in the **same cloud region as the application** to minimize latency and network costs.

---

## Information Required

Please provide the following details:

### 1. Databricks Workspace URL (Host)

Your Databricks workspace URL.

Example:

```text
https://adb-xxxxxxxxxx.xx.azuredatabricks.net
```

---
### 2. SQL Warehouse ID

The ID of the SQL Warehouse that will be used for running queries.

The warehouse should:

* Be running or auto-start enabled
* Allow access to the Service Principal

---
### 3. Target Location (Sink Path)

The catalog and schema where the application will create or write tables.

Format:

```text
catalog.schema.
```

Example:

```text
main.analytics.
```

---
### 4. Workspace ID

The unique ID of your Databricks workspace.

---
### 5. Cluster ID (Used for sync)

If synchronization features are enabled, please provide:
* Cluster ID

The cluster must allow access to the Service Principal.

---
### 6. Service Principal (Service Account)

The application connects securely using a **Databricks Service Principal**.

Please provide:

* Client ID
* Client Secret

The Service Principal should be created in your Databricks workspace and granted the necessary access (see below).

---

## Required Access for the Service Principal

The Service Principal should have access to:
* The Databricks workspace
* The SQL Warehouse
* The specified catalog and schema
* The catalog that needs to be processed by application
* The cluster (Used for sync)

Minimum required permissions:
* Use catalog
* Use schema
* Create table
* Modify
* Select

---

## Security Best Practices

* Store credentials securely (e.g., in a secrets manager)
* Grant only the minimum required permissions
* Rotate secrets periodically (edited)