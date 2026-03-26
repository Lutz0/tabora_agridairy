# Tabora AgriDairy — Database ERD

Entity-Relationship Diagram for the Tabora AgriDairy Management System (MySQL / SQLAlchemy).

---

## Mermaid ER Diagram

View this file in GitHub, VS Code (with Mermaid extension), or any Mermaid-compatible viewer.

```mermaid
erDiagram
    users ||--o{ cows : "owns"
    cows ||--o{ milk_production : "produces"
    users ||--o{ payments : "receives"

    users {
        int id PK "Primary Key"
        varchar username UK "Unique, indexed"
        varchar email UK "Unique, indexed"
        varchar password_hash "Not null"
        varchar role "admin or farmer"
    }

    cows {
        int id PK "Primary Key"
        varchar tag_number UK "Unique, indexed"
        varchar breed "Not null"
        int age "Years, not null"
        varchar health_status "Default Healthy"
        int owner_id FK "References users.id"
    }

    milk_production {
        int id PK "Primary Key"
        int cow_id FK "References cows.id"
        date date "Not null"
        float quantity_liters "Not null"
        text notes "Nullable"
    }

    inventory {
        int id PK "Primary Key"
        varchar item_name "Not null"
        varchar category "Feed, Medicine, Equipment"
        int quantity "Default 0"
        varchar unit "kg, liters, pieces"
        datetime date_added "Default current"
    }

    payments {
        int id PK "Primary Key"
        int farmer_id FK "References users.id"
        float amount "Not null"
        date payment_date "Not null"
        text description "Nullable"
    }
```

---

## Relationship Summary

| From (Parent) | Relationship | To (Child)   | Cardinality | Description |
|---------------|-------------|--------------|-------------|-------------|
| **users**     | owns        | **cows**     | 1 : N       | One user (farmer/admin) can own many cows. |
| **cows**      | produces    | **milk_production** | 1 : N | One cow has many milk production records. |
| **users**     | receives    | **payments** | 1 : N       | One user (farmer) can have many payments. |
| **inventory** | —           | —            | —           | Standalone table; no FK to other entities. |

---

## Table Overview

| Table            | Purpose |
|------------------|--------|
| **users**        | User accounts (admin/farmer), authentication. |
| **cows**         | Livestock; each cow belongs to one user. |
| **milk_production** | Daily milk quantity per cow. |
| **inventory**    | Farm supplies (feed, medicine, equipment). |
| **payments**     | Payments to farmers (recorded by admin). |

---

## Indexes (from models)

- **users:** `username`, `email` (unique + index).
- **cows:** `tag_number` (unique + index), `owner_id` (FK).
- **milk_production:** composite index on `(cow_id, date)`.
- **inventory:** (no extra indexes).
- **payments:** `farmer_id` (FK).
