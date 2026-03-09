# Google BigQuery Connection Requirements

This document outlines the information required to connect to Google BigQuery using a Service Account.

---

## Authentication Method

Service Account JSON Key

---

## Information Required

### 1. Project ID

Example:
intugle-saas

How to find:
Google Cloud Console → IAM & Admin → Settings

---

### 2. Service Account JSON Key

Required fields include:

- project_id
- private_key
- client_email
- client_id
- token_uri

How to create:

1. Google Cloud Console → IAM & Admin → Service Accounts
2. Create Service Account
3. Assign roles:
   - BigQuery Admin (or minimum required)
4. Keys → Add Key → JSON
5. Download JSON file

---

## Required Permissions

Service Account must have:

- BigQuery Data Viewer
- BigQuery Data Editor (if writing)
- BigQuery Job User

If accessing GCS:
- Storage Object Viewer

---

## Security Best Practices

- Store JSON securely
- Do not commit keys to source control
- Rotate keys periodically
- Use workload identity where possible