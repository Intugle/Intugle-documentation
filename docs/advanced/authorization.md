---
title: Authorization & Policy Evaluation
sidebar_position: 6
---

# Authorization & Policy Evaluation

Intugle's authorization system controls data access at two levels:

- **Object-Level Security (OLS)** — which tables and columns a user can access
- **Row-Level Security (RLS)** — which rows within an accessible table a user can see

Access is managed through **policies** assigned to users and groups. This document explains how policies work and how Intugle resolves conflicts when multiple policies apply.

---

## 1. Understanding Policies

A policy is a JSON document containing one or more access rules (called **statements**). Each statement specifies:

- **What resource** it applies to (tables, columns, or rows)
- **Whether to allow or deny** access
- **Optional conditions** (for row-level filtering)

### Policy Structure

Every policy follows this JSON structure:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.*"],
      "kind": "object"
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `version` | Policy schema version |
| `statements` | Array of access rules |
| `category` | Policy category (`"dac"` = discretionary access control) |
| `effect` | `"allow"` or `"deny"` |
| `resource` | Array of resource patterns |
| `kind` | `"object"` for OLS, `"row"` for RLS |
| `condition` | Filter predicates (RLS only) |

### Policy Placement

Policies can be attached to:

- **Users directly** — personal access rules for an individual
- **Groups** — shared rules inherited by all members

A user can belong to multiple groups, and each group can have multiple policies. Intugle combines all applicable policies to determine final access.

```
User
 ├── Direct Policies
 ├── Group A
 │    ├── Policy 1
 │    └── Policy 2
 └── Group B
      ├── Policy 3
      └── Policy 4
```

---

## 2. Object-Level Security (OLS)

OLS controls access to tables and columns using **resource patterns**.

### Resource Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*` | All tables and columns | Grant or restrict everything |
| `table.*` | All columns of a specific table | `phones.*` = entire phones table |
| `table.column` | Specific column only | `phones.price` = only the price column |

### Allow and Deny

OLS supports both `allow` and `deny` effects:

- **Allow** — grants access to the specified resource
- **Deny** — blocks access to the specified resource

When multiple statements apply to the same resource, Intugle uses **specificity** to resolve conflicts:

> **Rule**: A more specific pattern always wins, regardless of whether it's an allow or deny.

| Pattern | Specificity Level |
|---------|-------------------|
| `*` | Level 1 (broadest) |
| `table.*` | Level 2 |
| `table.column` | Level 3 (most specific) |

### OLS Examples

#### Example 1: Grant Access to All Tables

Allow access to every table and column in the database:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["*"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can access all tables and columns.

---

#### Example 2: Grant Access to Specific Table

Allow access to all columns in the `phones` table:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.*"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can access only the `phones` table (all columns). Other tables are denied.

---

#### Example 3: Grant Access to Specific Column

Allow access to only the `name` column in the `phones` table:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.name"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can see only `phones.name`. Other columns in `phones` and all other tables are denied.

---

#### Example 4: Multiple Statements in One Policy

Allow access to multiple tables and columns in a single policy:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands.*"],
      "kind": "object"
    },
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.name", "phones.price"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can access:
- All columns of the `brands` table
- Only `name` and `price` columns of the `phones` table

---

#### Example 5: Allow All + Deny Specific Table

Allow access to everything, then block the `phones` table:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["*"],
      "kind": "object"
    },
    {
      "category": "dac",
      "effect": "deny",
      "resource": ["phones.*"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can access all tables **except** `phones`.  
**Why**: `DENY phones.*` (specificity 2) is more specific than `ALLOW *` (specificity 1).

---

#### Example 6: Deny Table + Allow Specific Column

Block the `phones` table:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "deny",
      "resource": ["phones.*"],
      "kind": "object"
    },
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.name"],
      "kind": "object"
    }
  ]
}
```

**Result**: All `phones` columns are denied.  
**Why**: Within a group, `DENY` policies take precedence over `ALLOW` policies.

---

#### Example 7: Multiple Policies from Different Groups

**Group A Policy** (`policy-a.json`):

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["phones.*"],
      "kind": "object"
    }
  ]
}
```

**Group B Policy** (`policy-b.json`):

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "deny",
      "resource": ["phones.*"],
      "kind": "object"
    }
  ]
}
```

**Result**: User can access the `phones` table.  
**Why**: Both statements have the same specificity. Intugle uses union semantics — an allow at the same level as a deny means the user gets access.

### Default Behavior

- **No OLS policies configured**: User has unrestricted access to all tables and columns
- **OLS policies exist**: User must have an explicit `allow` statement to access each resource

---

## 3. Row-Level Security (RLS)

RLS filters rows within tables the user can already access (via OLS). It answers: "Which rows can this user see?"

### RLS Examples

#### Example 1: Single Condition Filter

Allow access to rows where `brand_name = 'Samsung'`:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "brand_name",
          "value": "Samsung",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Result**: User can only see rows where `brand_name = 'Samsung'`.

---

#### Example 2: Multiple Conditions (AND)

Allow access to rows where `brand_name = 'Samsung'` AND `country = 'US'`:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "brand_name",
          "value": "Samsung",
          "option": "equals"
        },
        {
          "id": "country",
          "value": "US",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Result**: User can see rows matching **both** conditions:
```sql
WHERE brand_name = 'Samsung' AND country = 'US'
```

---

#### Example 3: Multiple Statements (OR)

Allow access to multiple sets of rows by using multiple statements:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "brand_name",
          "value": "Samsung",
          "option": "equals"
        },
        {
          "id": "country",
          "value": "US",
          "option": "equals"
        }
      ]
    },
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "brand_name",
          "value": "Verizon",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Result**: User can see rows matching **either** statement:
```sql
WHERE (brand_name = 'Samsung' AND country = 'US')
   OR (brand_name = 'Verizon')
```

This allows access to:
- Samsung brands in the US
- Verizon brands (any country)

---

#### Example 4: RLS on Multiple Tables

Apply row filters to multiple tables in a single policy:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "country",
          "value": "US",
          "option": "equals"
        }
      ]
    },
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["products"],
      "kind": "row",
      "condition": [
        {
          "id": "category",
          "value": "Electronics",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Result**: 
- On `brands` table: see rows where `country = 'US'`
- On `products` table: see rows where `category = 'Electronics'`

---

#### Example 5: RLS from Multiple Groups

**Group A Policy**:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "brand_name",
          "value": "Samsung",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Group B Policy**:

```json
{
  "version": "0.1.0",
  "statements": [
    {
      "category": "dac",
      "effect": "allow",
      "resource": ["brands"],
      "kind": "row",
      "condition": [
        {
          "id": "country",
          "value": "US",
          "option": "equals"
        }
      ]
    }
  ]
}
```

**Result**: User can see rows matching **either** policy:
```sql
WHERE brand_name = 'Samsung' OR country = 'US'
```

### How Conditions Combine

| Scope | Logic |
|-------|-------|
| **Within one statement** | All conditions combine with **AND** |
| **Across multiple statements** | Statements combine with **OR** |
| **Across multiple groups** | All statements combine with **OR** |

### Default Behavior

- **No RLS policy for a table**: User can see all rows
- **RLS policy exists**: User can only see rows matching the policy conditions

---

## 4. How Policies Combine

### Direct vs. Group Policies

- Direct policies: Assigned specifically to the user
- Group policies: Inherited from all groups the user belongs to

Intugle treats both sources equally. Neither has automatic precedence over the other.

### Aggregation Rules

1. **Collect all statements** from direct policies + all group policies
2. **Apply OLS rules** for table/column access
3. **Apply RLS rules** for row filtering

### Group Membership = Union Access

When a user belongs to multiple groups, access is **additive**:

- Group A grants access to Table A
- Group B grants access to Table B
- User gets access to Table A **and** Table B

This is called **union semantics** — joining a group should only add access, never remove it.

### Conflict Resolution

| Situation | Resolution |
|-----------|-------------|
| Different specificity levels | More specific wins |
| Same specificity, both from groups | Allow wins (union semantics) |
| Same specificity, direct vs. group | Allow wins (no implicit precedence) |
| Multiple RLS statements | Combined with OR |
| Multiple conditions in one RLS statement | Combined with AND |

---

## 5. Decision Table

This table shows the expected result for common policy combinations.

| # | Scenario | Result | Reason |
|---|----------|--------|--------|
| 1 | `ALLOW *` + `DENY phones.*` | All tables except phones | `DENY phones.*` more specific than `ALLOW *` |
| 2 | `ALLOW phones.*` + `DENY phones.price` | All phones columns except price | `DENY phones.price` more specific than `ALLOW phones.*` |
| 3 | `DENY phones.*` + `ALLOW phones.name` | Only phones.name accessible | `ALLOW phones.name` more specific than `DENY phones.*` |
| 4 | Group A: `ALLOW phones.*` + Group B: `DENY phones.*` | Phones accessible | Same specificity → allow wins (union) |
| 5 | Group A RLS: `brand=Samsung` + Group B RLS: `country=US` | `brand='Samsung' OR country='US'` | RLS uses OR across statements |
| 6 | Direct: `ALLOW *` + Group: `DENY phones.*` | All tables except phones | Specificity wins (source doesn't matter) |
| 7 | Direct: `DENY phones.*` + Group: `ALLOW phones.*` | Phones accessible | Same specificity → allow wins |
| 8 | Direct: `ALLOW phones.*` + Group: `DENY phones.*` | Phones accessible | Same specificity → allow wins |
| 9 | No OLS policy defined | All tables accessible | No policy = unrestricted |
| 10 | OLS policy exists but table not granted | Table denied | Policy exists → explicit allow required |
| 11 | No RLS policy for a table | All rows visible | No RLS = no row filter |

---

## 6. Design Principles

### Why More Specific Always Wins

Specificity provides predictable behavior: administrators can carve out exceptions. A narrow `allow phones.name` inside a broad `deny phones.*` gives precise control.

### Why Allow Wins at Same Specificity

Group membership should be additive. If Group A grants and Group B denies at the same level, the user shouldn't lose access. Intugle treats multiple groups as a union of permissions.

### Why Direct and Group Policies Are Equal

If a user has both direct and group policies with the same specificity, Intugle doesn't prioritize one source over the other. Use specificity (not source) to create user-specific exceptions.

### Why OLS Excludes Unlisted Resources

When any OLS policy exists, unmentioned tables/columns are denied by default. This ensures administrators can't accidentally leave resources exposed when they intend to enforce access control.

---

## 7. Quick Reference

| Feature | Behavior |
|---------|----------|
| **OLS conflict** | More specific pattern wins |
| **OLS tiebreaker** | Allow wins at same specificity |
| **OLS default (no policy)** | Unrestricted access |
| **OLS default (policy exists)** | Explicit allow required for each resource |
| **RLS combination** | OR across statements, AND within conditions |
| **RLS default** | All rows visible if no policy |
| **Group aggregation** | Additive (union) |
| **Direct vs. group** | Treated equally |
