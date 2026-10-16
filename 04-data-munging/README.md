# 04. Data Munging: Automated SQLite ETL Pipeline

Production Python ETL script that ingests, aggregates, and normalizes disparate shipping spreadsheets into a clean SQLite relational database (`shipment_database.db`).

## Ingestion Pipeline
1. **Spreadsheet 0 (Self-Contained Shipments):**
   - 110 records containing origin warehouse, destination store, product name, and quantity.
   - Products are registered dynamically in `product` using an in-memory dictionary cache for O(1) lookups.
   - Inserts 110 rows into `shipment`.
2. **Spreadsheets 1 & 2 (Dependent Relational Spreadsheets):**
   - `shipping_data_2.csv`: Route directory mapping `shipment_identifier` to origin and destination facilities.
   - `shipping_data_1.csv`: 110 individual product units. The script aggregates rows by `(shipment_identifier, product)` into total SKU quantities (44 distinct line items).
   - Joins aggregated quantities with route information and writes 44 records into `shipment`.

## Verification Audit
```bash
python populate_database.py
```
Output statistics:
- Unique Products: 45
- Total Shipments: 154 (110 from Spreadsheet 0 + 44 from Spreadsheets 1 & 2)
- Total Product Units: 5,908
- Foreign Key Constraints: 100% verified
