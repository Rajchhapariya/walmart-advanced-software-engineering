# 03. Relational Database Design: 3NF Retail Logistics Schema

Normalized relational database schema (Third Normal Form) designed to manage Walmart's pet merchandise catalog, multi-species animal compatibility, customer orders, and multi-facility logistics manifests.

## Normalization & Modeling Decisions
- **Class Table Inheritance (Table-Per-Type):** Shared attributes (`name`, `price`, `manufacturer_id`) reside in the root `product` table. Category-specific columns are isolated in 1:1 subtype tables (`pet_food`, `pet_toy`, `pet_apparel`) linked by primary key / foreign key `product_id`. This eliminates NULL sprawl across unshared columns.
- **Many-to-Many Mappings:**
  - `product_animal`: Maps multi-species compatibility (e.g. products suited for both cats and dogs) via composite PK `(product_id, animal_id)`.
  - `transaction_item`: Records customer purchase line items with historical price snapshots (`unit_price`) and quantities.
  - `shipment_item`: Tracks individual SKU quantities packed into freight shipments.
- **Logistics Route Tracking:** `shipment` maintains dual foreign keys referencing `walmart_location` (`origin_location_id` and `destination_location_id`) with check constraints preventing identical origin and destination points.

## DDL Schema Execution
Execute against PostgreSQL:
```bash
psql -U postgres -d walmart_logistics -f schema.sql
```
