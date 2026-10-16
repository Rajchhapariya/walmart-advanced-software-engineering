-- ============================================================================
-- Walmart Global Tech - Enterprise Relational Database Schema
-- Task: Normalized Relational Database Design for Pet Products & Logistics
-- Standard: ANSI SQL / PostgreSQL / MySQL Compatible (3NF / BCNF Compliant)
-- ============================================================================

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS shipment_item CASCADE;
DROP TABLE IF EXISTS shipment CASCADE;
DROP TABLE IF EXISTS walmart_location CASCADE;
DROP TABLE IF EXISTS transaction_item CASCADE;
DROP TABLE IF EXISTS customer_transaction CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS product_animal CASCADE;
DROP TABLE IF EXISTS animal CASCADE;
DROP TABLE IF EXISTS pet_apparel CASCADE;
DROP TABLE IF EXISTS pet_toy CASCADE;
DROP TABLE IF EXISTS pet_food CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS manufacturer CASCADE;

-- ----------------------------------------------------------------------------
-- 1. MANUFACTURERS
-- ----------------------------------------------------------------------------
CREATE TABLE manufacturer (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 2. PRODUCTS (Base / Supertype Entity)
-- Implements Class Table Inheritance for Pet Food, Toys, and Apparel
-- ----------------------------------------------------------------------------
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    product_type VARCHAR(20) NOT NULL CHECK (product_type IN ('FOOD', 'TOY', 'APPAREL')),
    manufacturer_id INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_manufacturer 
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(manufacturer_id) 
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 3. PET FOOD (Subtype Extension)
-- ----------------------------------------------------------------------------
CREATE TABLE pet_food (
    product_id INT PRIMARY KEY,
    weight_lbs DECIMAL(6, 2) NOT NULL CHECK (weight_lbs > 0.0),
    flavor VARCHAR(100) NOT NULL,
    target_health_condition VARCHAR(255) NOT NULL,
    CONSTRAINT fk_food_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 4. PET TOYS (Subtype Extension)
-- ----------------------------------------------------------------------------
CREATE TABLE pet_toy (
    product_id INT PRIMARY KEY,
    material VARCHAR(100) NOT NULL,
    durability VARCHAR(50) NOT NULL,
    CONSTRAINT fk_toy_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 5. PET APPAREL (Subtype Extension)
-- ----------------------------------------------------------------------------
CREATE TABLE pet_apparel (
    product_id INT PRIMARY KEY,
    color VARCHAR(50) NOT NULL,
    size VARCHAR(20) NOT NULL,
    care_instructions TEXT NOT NULL,
    CONSTRAINT fk_apparel_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 6. ANIMALS (Target Species Catalog)
-- ----------------------------------------------------------------------------
CREATE TABLE animal (
    animal_id SERIAL PRIMARY KEY,
    species_name VARCHAR(100) NOT NULL UNIQUE
);

-- ----------------------------------------------------------------------------
-- 7. PRODUCT_ANIMAL (M:N Junction Table)
-- Associates each product with one or more animals
-- ----------------------------------------------------------------------------
CREATE TABLE product_animal (
    product_id INT NOT NULL,
    animal_id INT NOT NULL,
    PRIMARY KEY (product_id, animal_id),
    CONSTRAINT fk_pa_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_pa_animal 
        FOREIGN KEY (animal_id) REFERENCES animal(animal_id) 
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 8. CUSTOMERS
-- ----------------------------------------------------------------------------
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 9. CUSTOMER TRANSACTIONS (Order Header)
-- ----------------------------------------------------------------------------
CREATE TABLE customer_transaction (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.0 CHECK (total_amount >= 0.0),
    CONSTRAINT fk_tx_customer 
        FOREIGN KEY (customer_id) REFERENCES customer(customer_id) 
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 10. TRANSACTION ITEMS (Line Items: M:N Junction Table)
-- Connects transactions to one or more products with historical price lock
-- ----------------------------------------------------------------------------
CREATE TABLE transaction_item (
    transaction_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0.0),
    PRIMARY KEY (transaction_id, product_id),
    CONSTRAINT fk_ti_transaction 
        FOREIGN KEY (transaction_id) REFERENCES customer_transaction(transaction_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_ti_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 11. WALMART LOCATIONS (Stores & Distribution Centers)
-- ----------------------------------------------------------------------------
CREATE TABLE walmart_location (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 12. SHIPMENTS (Logistics Multi-Leg Movement)
-- ----------------------------------------------------------------------------
CREATE TABLE shipment (
    shipment_id SERIAL PRIMARY KEY,
    origin_location_id INT NOT NULL,
    destination_location_id INT NOT NULL,
    shipment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' 
        CHECK (status IN ('PENDING', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED')),
    CONSTRAINT fk_shipment_origin 
        FOREIGN KEY (origin_location_id) REFERENCES walmart_location(location_id) 
        ON DELETE RESTRICT,
    CONSTRAINT fk_shipment_destination 
        FOREIGN KEY (destination_location_id) REFERENCES walmart_location(location_id) 
        ON DELETE RESTRICT,
    CONSTRAINT chk_different_locations 
        CHECK (origin_location_id <> destination_location_id)
);

-- ----------------------------------------------------------------------------
-- 13. SHIPMENT ITEMS (Shipment Manifest: M:N Junction Table)
-- Represents collection of products and assigned quantities
-- ----------------------------------------------------------------------------
CREATE TABLE shipment_item (
    shipment_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (shipment_id, product_id),
    CONSTRAINT fk_si_shipment 
        FOREIGN KEY (shipment_id) REFERENCES shipment(shipment_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_si_product 
        FOREIGN KEY (product_id) REFERENCES product(product_id) 
        ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- Performance Indexes for Operational Queries
-- ----------------------------------------------------------------------------
CREATE INDEX idx_product_manufacturer ON product(manufacturer_id);
CREATE INDEX idx_product_animal_animal ON product_animal(animal_id);
CREATE INDEX idx_tx_customer ON customer_transaction(customer_id);
CREATE INDEX idx_tx_date ON customer_transaction(transaction_date);
CREATE INDEX idx_shipment_origin ON shipment(origin_location_id);
CREATE INDEX idx_shipment_dest ON shipment(destination_location_id);
CREATE INDEX idx_location_zip ON walmart_location(zip_code);
