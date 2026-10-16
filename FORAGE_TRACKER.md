# Walmart Advanced Software Engineering Job Simulation (Forage)

Central workspace tracker for engineering tasks, architectural designs, algorithms, schemas, and pipeline implementations.


---

## Verified Completion Credential

- **Issued To:** Raj Chhapariya
- **Issuing Entity:** Walmart Global Tech & Forage
- **Issue Date:** October 16th, 2026
- **Signatories:** Suresh Kumar (Global CTO & CDO, Walmart), Tom Brunskill (Co-Founder, Forage)
- **Enrolment Verification Code:** 6abc21502beab4d7ee49fcb2
- **User Verification Code:** 6abc0c9cf140e02e14508f40
- **Official Credential File:** Walmart_Global_Tech_Advanced_Software_Engineering_Certificate_Raj_Chhapariya.pdf (285.5 KB)

---

## Program Progress Overview

- **Public GitHub Repository:** [github.com/Rajchhapariya/walmart-advanced-software-engineering](https://github.com/Rajchhapariya/walmart-advanced-software-engineering)


| Module | Engineering Domain | Primary Submission Deliverable | Status |
| :--- | :--- | :--- | :---: |
| **Task 1** | Advanced Data Structures | PowerOfTwoMaxHeap.java (Bitwise 2^x-ary Max Heap) | **COMPLETED** |
| **Task 2** | Software Architecture | Data_Processor_Pipeline_UML_Diagram.pdf (UML 2.5 Specification) | **COMPLETED** |
| **Task 3** | Relational Database Design | Walmart_Relational_Database_ERD.pdf (3NF Schema & ERD) | **COMPLETED** |
| **Task 4** | Data Munging | populate_database_submission.pdf (Automated ETL Script) | **COMPLETED** |

**Current Completion:** 100% (4 of 4 modules finalized & verified)

---

## Detailed Task Documentation

### Task 1: Advanced Data Structures [COMPLETED]

- **Problem Scope:** Design and implement a high-performance 2^x-ary max heap in Java where every parent node has 2^x children.
- **Architectural & Algorithmic Highlights:**
  - **Bitwise Node Arithmetic:** Replaced costly integer division and multiplication with arithmetic right shifts (>>> x) and left shifts (<< x).
  - **Half-Exchange Sift-Down (Hole Percolation):** Caches target element and moves strictly dominant child values up, reducing array writes by 50% compared to full swaps.
  - **Overflow Protection:** Robust index range validations preventing signed 32-bit integer overflow for large exponents (x >= 30).
  - **Dynamic Capacity Management:** Self-scaling backing array with amortized O(1) insertions.
- **Verification Suite:**
  - 102 automated unit test cases passed (PowerOfTwoMaxHeapTest.java).
  - Verified edge cases: single-element heaps, duplicate values, sorted/reverse-sorted inputs, and exponent boundary conditions (x=0 to x=5).
- **Source Artifacts:**
  - PowerOfTwoMaxHeap.java (Production Java implementation, 7.0 KB)
  - PowerOfTwoMaxHeap.js (Portal submission export, 3.0 KB)
  - PowerOfTwoMaxHeapTest.java (Comprehensive JUnit-style test harness, 10.4 KB)

---

### Task 2: Software Architecture [COMPLETED]

- **Problem Scope:** Draft an enterprise UML class diagram modeling a dynamic pipeline data processor supporting runtime operating modes (DUMP, PASSTHROUGH, VALIDATE) and polymorphic database connectors (POSTGRES, REDIS, ELASTIC).
- **Architectural & Design Pattern Highlights:**
  - **Strategy Pattern for Processing Modes:** Mode interface realized by DumpMode (discard), PassthroughMode (direct insert), and ValidateMode (validate then insert). Eliminates conditional branching (if-else / switch) inside the pipeline execution path.
  - **Bridge / Connector Pattern for Storage:** DatabaseConnector interface isolates vendor-specific client SDKs behind uniform insert(data) and validate(data) contracts.
  - **Factory Pattern for Configuration:** ModeFactory encapsulates runtime dependency assembly and connector injection during configure(modeId, dbId) calls.
  - **Domain Primitives Integration:** Cleanly integrates pre-existing Datapoint abstraction, ModeIdentifier enum, and DatabaseIdentifier enum.
  - **SOLID Verification:** Fully complies with Single Responsibility (SRP), Open/Closed (OCP), Liskov Substitution (LSP), Interface Segregation (ISP), and Dependency Inversion (DIP).
- **Standards Compliance:**
  - Adheres strictly to the University of Helsinki Java MOOC Part 11 specification and ISO/IEC 19505 UML 2.5 standards.
- **Source & Submission Artifacts:**
  - Data_Processor_Pipeline_UML_Diagram.pdf (Primary vector landscape PDF submission, 318 KB)
  - Data_Processor_Pipeline_UML_Diagram.png (High-resolution 300 PPI raster submission, 455 KB)
  - Data_Processor_Pipeline_Architecture_Report.pdf (3-page technical architecture specification, 307 KB)
  - Data_Processor_Pipeline_UML_Diagram.svg (Raw vector SVG source, 22.5 KB)
  - Data_Processor_Pipeline_UML_Diagram.typ & Data_Processor_Pipeline_Architecture_Report.typ (Typst source definitions)

---

### Task 3: Relational Database Design [COMPLETED]

- **Problem Scope:** Design an enterprise Third Normal Form (3NF) relational database schema for Walmart's Pet Department managing specialized product categories, multi-species animal compatibility, vendor manufacturing, customer transactions, and nationwide logistics fulfillment.
- **Architectural & Normalization Highlights:**
  - **Class Table Inheritance (Table-Per-Type):** Base Product entity stores shared attributes (Name, Price, ProductType, ManufacturerID), while specialized attributes are isolated in 1:1 subtype tables (PetFood, PetToy, PetApparel) linked via ProductID PK/FK. Completely eliminates NULL column sprawl while satisfying 3NF.
  - **Normalized Associative M:N Tables:**
    - Product_Animal: Models multi-species compatibility (e.g., shared dog/cat harnesses) with composite PK (ProductID, AnimalID).
    - Transaction_Product: Tracks customer purchase line items with historical snapshot pricing (UnitPrice) and purchase quantities.
    - Shipment_Product: Records multi-SKU freight cargo manifests with per-SKU quantity counts.
  - **Dual FK Logistics Tracking:** Shipment table features two distinct foreign keys pointing to WalmartLocation (OriginLocationID and DestinationLocationID) with validation preventing identical origin/destination routes.
  - **Visual Paradigm Standard Compliance:** Modeled with exact rounded peach containers (#fce4be), amber header bands (#f8c070), gold PK keys, green arrow FK keys, blue column icons, right-aligned nullable [N] badges, solid identifying lines, dashed non-identifying lines, and Crow's foot cardinalities.
- **Source & Submission Artifacts:**
  - Walmart_Relational_Database_ERD.pdf / walmart_relational_database_erd.pdf (Primary vector landscape PDF submission, 121 KB)
  - Walmart_Relational_Database_ERD.png / walmart_relational_database_erd.png (High-resolution raster submission, 89 KB)
  - Walmart_Relational_Database_Design_Report.pdf (Executive technical design report, 165 KB)
  - Walmart_Relational_Database_Schema.sql / schema.sql (Production PostgreSQL / ANSI SQL-92 migration script, 9.1 KB)
  - Walmart_Relational_Database_ERD.svg / erd_visual_paradigm.svg (Vector SVG diagram source, 25.7 KB)
  - erd_visual_paradigm.html (Interactive browser diagram viewer, 26.1 KB)

---

### Task 4: Data Munging [COMPLETED]

- **Problem Scope:** Ingest, clean, aggregate, and normalize disparate shipping spreadsheets into the target SQLite database (shipment_database.db).
- **ETL Architecture & Normalization Highlights:**
  - **Spreadsheet 0 Ingestion:** Reads 110 self-contained shipment rows (origin_warehouse, destination_store, product, product_quantity), dynamically registering unique product entities in the product table with (1)$ in-memory caching and generating 110 records in shipment.
  - **Spreadsheets 1 & 2 Relational Aggregation:**
    - Correlates route mapping (origin_warehouse, destination_store) from shipping_data_2.csv via shipment_identifier.
    - Aggregates single-unit product line items in shipping_data_1.csv by (shipment_identifier, product) across 110 raw rows into 44 grouped shipment items.
    - Inserts combined shipment records into shipment with resolved product IDs and multi-leg warehouse-to-store routes.
  - **Transaction Integrity & Idempotency:** Executes inside an atomic transaction with rollback safety, clean reset hooks, and zero data corruption.
- **Verification Audit Results:**
  - **Total Unique Products:** 45 records (product table)
  - **Total Shipment Records:** 154 rows (shipment table, 110 from S0 + 44 from S1/S2)
  - **Total Product Units Accounted:** 5,908 physical items
  - **Referential Integrity:** 100% foreign key compliance (shipment.product_id -> product.id)
- **Source & Submission Artifacts:**
  - populate_database_submission.pdf / Data_Munging_Script.pdf (Primary portal submission PDF, 148 KB)
  - populate_database.py (Production Python ETL pipeline script, 7.3 KB)
  - shipment_database.db (Fully populated and validated SQLite database, 98 KB)
  - populate_database_submission.typ (Typst source for formatted script report)

---

## Directory Manifest (C:\Users\Rajch\Desktop\forage)

`	ext
forage/
│── FORAGE_TRACKER.md                             # Central job simulation roadmap (100% completed)
│
├── [Task 1: Advanced Data Structures]
│   ├── PowerOfTwoMaxHeap.java                    # 2^x-ary Max Heap implementation
│   ├── PowerOfTwoMaxHeap.js                      # Portal format wrapper
│   └── PowerOfTwoMaxHeapTest.java                # 102 unit test cases
│
├── [Task 2: Software Architecture]
│   ├── Data_Processor_Pipeline_UML_Diagram.pdf   # Portal upload PDF (Vector landscape)
│   ├── Data_Processor_Pipeline_UML_Diagram.png   # 300 PPI diagram image
│   ├── Data_Processor_Pipeline_Architecture_Report.pdf # 3-page technical design report
│   ├── Data_Processor_Pipeline_UML_Diagram.svg   # Vector SVG diagram
│   ├── Data_Processor_Pipeline_UML_Diagram.typ   # Typst diagram definition
│   └── Data_Processor_Pipeline_Architecture_Report.typ # Typst report source
│
├── [Task 3: Relational Database Design]
│   ├── Walmart_Relational_Database_ERD.pdf       # Primary vector landscape ERD for portal upload (121 KB)
│   ├── Walmart_Relational_Database_ERD.png       # High-resolution ERD image (89 KB)
│   ├── Walmart_Relational_Database_Design_Report.pdf # Executive technical design report (165 KB)
│   ├── Walmart_Relational_Database_Design_Report.typ # Typst technical report source
│   ├── Walmart_Relational_Database_Schema.sql    # Production PostgreSQL / ANSI SQL DDL schema
│   ├── Walmart_Relational_Database_ERD.svg       # Visual Paradigm compliant vector SVG
│   └── erd_visual_paradigm.html                  # Interactive browser diagram viewer
│
└── [Task 4: Data Munging]
    ├── populate_database_submission.pdf          # Primary portal submission PDF of Python script (148 KB)
    ├── Data_Munging_Script.pdf                   # Mirror PDF copy for submission (148 KB)
    ├── populate_database.py                      # Production ETL script (7.3 KB)
    ├── populate_database_submission.typ          # Typst documentation source
    └── forage-walmart-task-4/                    # Cloned upstream repository
        ├── shipment_database.db                  # Fully populated SQLite database
        ├── populate_database.py                  # Local runner script
        ├── populate_database_submission.pdf      # Local submission PDF
        └── data/
            ├── shipping_data_0.csv               # 110 self-contained shipments
            ├── shipping_data_1.csv               # 110 raw item rows (aggregated to 44 items)
            └── shipping_data_2.csv               # 20 shipment route definitions
`
