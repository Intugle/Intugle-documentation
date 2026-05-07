---
title: Architecture
sidebar_position: 1
---

<!-- ![Intugle Architecture](https://intugle.ai/intugle-logo.svg) -->
# 1. Architecture Diagram

![Alt text](/img/Intugle-v3-architecture-Databricks.png)


# 2. System Requirements

|   Category    | Service                           |   SKU                                 |   Purpose                                    |
|---------------|-----------------------------------|---------------------------------------|----------------------------------------------|
|   Compute     |   Kubernetes (AKS)                | 5 X Standard_D8lds_v5                 | Run application microservices                |
|   Compute     |   Databricks                      | 1 Small WH, 1 General Compute         | Compute Engine                               |
|   Compute     |   Virtual machine                 | Standard D4lds                        | Jump Host                                    |
|   Containers  |   Container registry              | 9 microservice images                 | Store container images                       |
|   LLM         |   Foundry/Foundry Project         | GPT 4X, GPT 5X, Text Embedding Ada    | Deploy LLM models                            |
|   Storage     |   Storage account                 | ADLS V2                               | Data Lake                                    |
|   Storage     |   Storage account                 | NFS - 1 TB                            | Persistance for microservices                |


# 3. Third party Tools

|   Category  | Service |   SKU      |   Purpose |
|-----------------|---------------------------------|----------|----------------------------------------------------|
| Authentication    | WorkOS    | WorkOS            | Authentication Identity Providor                              |
| Monitoring        | Datadog   | Datadog           | Log Analytics and Application Monitoring                               |
| Monitoring        | Langfuse  | Langfuse          | LLM Agents Analytics and monitoring                               |