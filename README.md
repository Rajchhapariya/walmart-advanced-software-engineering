# Walmart Global Tech: Advanced Software Engineering Case Study

Production-grade implementations for the Walmart Global Tech Advanced Software Engineering technical challenge. Covers custom data structures, object-oriented pipeline architecture, 3NF database normalization, and automated ETL ingestion.

---

## Technical Modules

| Directory | Domain | Core Technologies | Primary Deliverables |
| :--- | :--- | :--- | :--- |
| [`01-advanced-data-structures`](./01-advanced-data-structures/) | Data Structures & Algorithms | Java 17, Bitwise Shift Math, JUnit | `PowerOfTwoMaxHeap.java`, 102 test cases |
| [`02-software-architecture`](./02-software-architecture/) | System Architecture & Design | UML 2.5, GoF Patterns (Strategy, Bridge, Factory) | Architecture Report & UML Specification (PDF/SVG) |
| [`03-relational-database-design`](./03-relational-database-design/) | Relational Database Design | SQL, PostgreSQL, 3NF Normalization | Visual Paradigm ERD & ANSI DDL (`schema.sql`) |
| [`04-data-munging`](./04-data-munging/) | Data Engineering & ETL | Python 3, SQLite, CSV Normalization | Automated ETL pipeline (`populate_database.py`) |
| [`credentials`](./credentials/) | Verification | Forage Credential Registry | Verified Completion Certificate |

---

## Architecture Summary

### 1. Bitwise 2^x-ary Max Heap
- Replaced division and multiplication with arithmetic bitwise shifts (`>>> x`, `<< x`).
- Implemented half-exchange sift-down (hole percolation), reducing array writes by 50% compared to full swaps.
- Guarded against 32-bit signed integer overflow for large exponents (x >= 30).
- Validated with 102 automated unit test cases.

### 2. Pipeline Data Processor
- Decoupled runtime processing modes (`DUMP`, `PASSTHROUGH`, `VALIDATE`) via the Strategy pattern.
- Abstracted persistence backends (`PostgreSQL`, `Redis`, `Elasticsearch`) behind a uniform Bridge interface (`DatabaseConnector`).
- Integrated dynamic configuration assembly via `ModeFactory`.

### 3. Third Normal Form (3NF) Database Design
- Implemented Class Table Inheritance (Table-Per-Type) with base `product` and 1:1 subtype tables (`pet_food`, `pet_toy`, `pet_apparel`).
- Resolved M:N relationships for animal species compatibility (`product_animal`), order items (`transaction_item`), and freight manifests (`shipment_item`).
- Modeled multi-leg shipment logistics with origin and destination location constraints.

### 4. Automated ETL Ingestion Engine
- Ingested 110 self-contained shipments from Spreadsheet 0 with O(1) dynamic product caching.
- Correlated route lookups from Spreadsheet 2 with 110 raw unit items from Spreadsheet 1, aggregating them into 44 distinct shipment line items.
- Generated 154 total shipment rows and verified 5,908 physical inventory units with complete foreign key integrity.

---

## Verification & Build Instructions

### Run Java Unit Tests
```bash
cd 01-advanced-data-structures
javac PowerOfTwoMaxHeap.java PowerOfTwoMaxHeapTest.java
java PowerOfTwoMaxHeapTest
```

### Run Python ETL Pipeline
```bash
cd 04-data-munging
python populate_database.py
```

### Apply PostgreSQL Schema
```bash
cd 03-relational-database-design
psql -U postgres -d walmart_logistics -f schema.sql
```

---

## Verification Credential
- **Candidate:** Raj Chhapariya
- **Issuing Entity:** Walmart Global Tech & Forage
- **Verification ID:** `6abc0c9cf140e02e14508f40`
- **Official Credential Document:** [`credentials/Walmart_Global_Tech_Advanced_Software_Engineering_Certificate_Raj_Chhapariya.pdf`](./credentials/Walmart_Global_Tech_Advanced_Software_Engineering_Certificate_Raj_Chhapariya.pdf)
