# Data Models & Relational Schema Specification

**Database Engine:** PostgreSQL 16+  
**Normalization Level:** Third Normal Form (3NF)

---

## 1. Schema Entity Relationship Summary

| Entity        | Primary Key | Foreign Keys             | Responsibility                                                 |
| :------------ | :---------- | :----------------------- | :------------------------------------------------------------- |
| `users`       | `id (UUID)` | None                     | Stores user credentials, email, and authentication profile     |
| `products`    | `id (UUID)` | `manufacturer_id`        | Core catalog items with pricing, category, and metadata        |
| `orders`      | `id (UUID)` | `customer_id`            | Transaction records, status, total amount, and timestamp       |
| `order_items` | `id (UUID)` | `order_id`, `product_id` | Junction table tracking items, quantities, and price snapshots |

---

## 2. SQL DDL Baseline

```sql
-- Core Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Core Products Table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    inventory_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_sku ON products(sku);
```
