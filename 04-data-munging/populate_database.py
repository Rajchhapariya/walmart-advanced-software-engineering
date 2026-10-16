"""
Walmart Advanced Software Engineering Job Simulation - Task 4: Data Munging
Automated ETL pipeline to clean, aggregate, and populate SQLite shipping database.

Authorship & Architecture:
- Reads spreadsheet 0 (self-contained shipments).
- Aggregates spreadsheet 1 (individual product rows) by shipment_identifier and product.
- Correlates routes (origin_warehouse, destination_store) from spreadsheet 2.
- Normalizes product entities into 'product' table and records into 'shipment' table.
"""

import csv
import sqlite3
import os
import sys
from collections import defaultdict
from typing import Dict, Tuple

# Base paths calibrated to repository structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "shipment_database.db")

CSV_0 = os.path.join(DATA_DIR, "shipping_data_0.csv")
CSV_1 = os.path.join(DATA_DIR, "shipping_data_1.csv")
CSV_2 = os.path.join(DATA_DIR, "shipping_data_2.csv")


def get_or_create_product(cursor: sqlite3.Cursor, product_name: str, cache: Dict[str, int]) -> int:
    """
    Retrieves the primary key ID for a product, inserting it into the
    'product' table if it does not already exist. Utilizes an in-memory
    dictionary cache for O(1) subsequent lookups.
    """
    product_name_clean = product_name.strip()
    if product_name_clean in cache:
        return cache[product_name_clean]

    # Check database in case it was inserted previously
    cursor.execute("SELECT id FROM product WHERE name = ?", (product_name_clean,))
    row = cursor.fetchone()
    if row:
        product_id = row[0]
    else:
        cursor.execute("INSERT INTO product (name) VALUES (?)", (product_name_clean,))
        product_id = cursor.lastrowid

    cache[product_name_clean] = product_id
    return product_id


def process_spreadsheet_0(cursor: sqlite3.Cursor, file_path: str, product_cache: Dict[str, int]) -> int:
    """
    Processes Spreadsheet 0:
    Each row contains a complete self-contained shipment record:
    [origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier]
    """
    print(f"[INFO] Ingesting self-contained shipments from '{os.path.basename(file_path)}'...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    rows_inserted = 0
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            origin = row["origin_warehouse"].strip()
            destination = row["destination_store"].strip()
            product_name = row["product"].strip()
            quantity = int(row["product_quantity"])

            product_id = get_or_create_product(cursor, product_name, product_cache)

            cursor.execute(
                """
                INSERT INTO shipment (product_id, quantity, origin, destination)
                VALUES (?, ?, ?, ?)
                """,
                (product_id, quantity, origin, destination)
            )
            rows_inserted += 1

    print(f"[SUCCESS] Spreadsheet 0 processed: {rows_inserted} shipment records inserted.")
    return rows_inserted


def process_spreadsheets_1_and_2(
    cursor: sqlite3.Cursor,
    file_path_1: str,
    file_path_2: str,
    product_cache: Dict[str, int]
) -> int:
    """
    Processes Spreadsheets 1 and 2:
    - Spreadsheet 2 provides route mapping: shipment_identifier -> (origin, destination).
    - Spreadsheet 1 contains single product units per row, which must be combined
      by (shipment_identifier, product) to determine aggregate quantity before insertion.
    """
    print(f"[INFO] Reading routing directory from '{os.path.basename(file_path_2)}'...")
    if not os.path.exists(file_path_2):
        raise FileNotFoundError(f"File not found: {file_path_2}")
    if not os.path.exists(file_path_1):
        raise FileNotFoundError(f"File not found: {file_path_1}")

    # Step 1: Ingest route lookup table from Spreadsheet 2
    routes: Dict[str, Tuple[str, str]] = {}
    with open(file_path_2, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["shipment_identifier"].strip()
            origin = row["origin_warehouse"].strip()
            destination = row["destination_store"].strip()
            routes[sid] = (origin, destination)

    print(f"[INFO] Loaded {len(routes)} distinct shipment routes.")

    # Step 2: Aggregate line items from Spreadsheet 1
    # Structure: shipment_items[shipment_identifier][product_name] = total_quantity
    print(f"[INFO] Aggregating product quantities from '{os.path.basename(file_path_1)}'...")
    shipment_items: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    total_raw_rows = 0

    with open(file_path_1, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["shipment_identifier"].strip()
            prod = row["product"].strip()
            shipment_items[sid][prod] += 1
            total_raw_rows += 1

    print(f"[INFO] Aggregated {total_raw_rows} raw unit rows across {len(shipment_items)} shipments.")

    # Step 3: Insert combined shipment product records into database
    rows_inserted = 0
    for sid, products in shipment_items.items():
        if sid not in routes:
            raise KeyError(f"Shipment identifier '{sid}' in spreadsheet 1 has no route in spreadsheet 2.")

        origin, destination = routes[sid]

        for product_name, quantity in products.items():
            product_id = get_or_create_product(cursor, product_name, product_cache)

            cursor.execute(
                """
                INSERT INTO shipment (product_id, quantity, origin, destination)
                VALUES (?, ?, ?, ?)
                """,
                (product_id, quantity, origin, destination)
            )
            rows_inserted += 1

    print(f"[SUCCESS] Spreadsheets 1 & 2 processed: {rows_inserted} grouped shipment records inserted.")
    return rows_inserted


def run_pipeline(db_file: str = DB_PATH) -> None:
    """
    Executes the complete ETL pipeline within an atomic database transaction.
    """
    print("=" * 70)
    print("WALMART ADVANCED SOFTWARE ENGINEERING: DATA MUNGING ETL PIPELINE")
    print("=" * 70)
    print(f"[TARGET DATABASE] {db_file}")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Clear existing data to maintain idempotency
        cursor.execute("DELETE FROM shipment;")
        cursor.execute("DELETE FROM product;")
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('product', 'shipment');")
        except sqlite3.OperationalError:
            pass
        conn.commit()
        print("[INFO] Cleared existing table records for fresh idempotent load.")
    except Exception as e:
        print(f"[WARN] Reset notification: {e}")
        conn.commit()

    product_cache: Dict[str, int] = {}

    try:
        # Execute Ingestion
        s0_count = process_spreadsheet_0(cursor, CSV_0, product_cache)
        s12_count = process_spreadsheets_1_and_2(cursor, CSV_1, CSV_2, product_cache)

        # Commit transaction atomically
        conn.commit()
        print("\n" + "-" * 70)
        print("[TRANSACTION COMMITTED] All spreadsheet datasets successfully ingested.")
        print("-" * 70)

        # Post-ingestion validation audit
        cursor.execute("SELECT COUNT(*) FROM product;")
        total_products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM shipment;")
        total_shipments = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity) FROM shipment;")
        total_units = cursor.fetchone()[0]

        print("\n=== DATABASE AUDIT & VERIFICATION REPORT ===")
        print(f"Total Unique Products Ingested : {total_products}")
        print(f"Total Shipment Records Created : {total_shipments} ({s0_count} from S0, {s12_count} from S1+S2)")
        print(f"Total Product Units Accounted  : {total_units}")

        print("\nSample Joined Shipment Records (First 5 Rows):")
        cursor.execute(
            """
            SELECT s.id, p.name, s.quantity, s.origin, s.destination
            FROM shipment s
            JOIN product p ON s.product_id = p.id
            ORDER BY s.id ASC
            LIMIT 5;
            """
        )
        sample_rows = cursor.fetchall()
        for r in sample_rows:
            print(f"  [Shipment #{r[0]:03d}] {r[1]:<15} | Qty: {r[2]:<4} | Origin: {r[3][:8]}... | Dest: {r[4][:8]}...")

        print("=" * 70)

    except Exception as exc:
        conn.rollback()
        print(f"\n[FATAL ERROR] Ingestion failed: {exc}. Transaction rolled back.", file=sys.stderr)
        raise exc
    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline()
