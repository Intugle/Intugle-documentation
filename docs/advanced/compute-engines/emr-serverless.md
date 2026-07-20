---
sidebar_position: 2
---
# EMR Serverless Connection Requirements

This document outlines the information and access required to connect your AWS EMR Serverless environment with Glue Data Catalog to our application.

> **Recommendation:**
> For best performance, your EMR Serverless application should be deployed in the **same AWS region as the application** to minimize latency and network costs.

---

## Prerequisites

Before connecting, ensure you have:

* An AWS account with EMR Serverless enabled
* An S3 bucket for data storage
* AWS Glue Data Catalog configured

---

## AWS Setup Required

### 1. Create EMR Serverless Application

Create a Spark-type application in the EMR Serverless console.

---

### 2. Create IAM Execution Role (EMRServerlessTrustPolicy)

Create an IAM role with trust policy for EMR Serverless service.

Required permissions:

* S3 access to data that needs to be consumed
* Glue access to the catalog that needs to be consumed


---

### 3. Create IAM User (emr-serverless-user)

Create an IAM user for API access.

Required permissions:

* S3 access to data that needs to be consumed
* Glue access to the catalog that needs to be consumed
* EMR Serverless actions (CreateApplication, StartJobRun, etc.)
* iam:PassRole for the execution role

---

## Information Required

Please provide the following details:

### 1. Application ID

The EMR Serverless application ID.

---

### 2. Execution Role ARN

The IAM execution role ARN (EMRServerlessTrustPolicy).

Example:

```text
arn:aws:iam::123456789012:role/EMRServerlessTrustPolicy
```

---

### 3. AWS Region

The AWS region where your EMR Serverless application is deployed.

Example:

```text
us-east-1
```

---

### 4. Access Key ID

AWS access key ID from the emr-serverless-user.

---

### 5. Secret Access Key

AWS secret access key from the emr-serverless-user.

---

### 6. Glue Catalog ID

The AWS Glue Data Catalog ID (typically your AWS account ID).

---

### 7. Session Idle Timeout

Session idle timeout in minutes.

Default: 20 minutes

---

### 8. Sink Database

The Glue catalog database path where the application will create or write tables.

Format:

```text
database.
```

---

### 9. Sink Path

The S3 path for data product output.

Format:

```text
s3://bucket/path/
```

---

## Security Best Practices

* Store credentials securely (e.g., in AWS Secrets Manager)
* Grant only the minimum required permissions
* Rotate access keys periodically
* Use VPC endpoints for enhanced security

---

## References

* [EMR Serverless User Access Policies](http://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/security-iam-user-access-policies.html)
* [Spark Connect with EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/spark-connect.html)
