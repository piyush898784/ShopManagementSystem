-- Shop Management System - MySQL Database Schema
-- Optimized for high performance, indexing, and transactional data integrity

CREATE DATABASE IF NOT EXISTS `shop_management_db`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `shop_management_db`;

-- 1. Categories Table
CREATE TABLE IF NOT EXISTS `categories` (
    `category_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `description` VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Products Table (Inventory)
CREATE TABLE IF NOT EXISTS `products` (
    `product_id` INT AUTO_INCREMENT PRIMARY KEY,
    `category_id` INT NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `barcode` VARCHAR(50) UNIQUE DEFAULT NULL,
    `price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `cost_price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `quantity` INT NOT NULL DEFAULT 0,
    `min_stock_alert` INT NOT NULL DEFAULT 10,
    `status` ENUM('In Stock', 'Low Stock', 'Out of Stock') GENERATED ALWAYS AS (
        CASE 
            WHEN `quantity` <= 0 THEN 'Out of Stock'
            WHEN `quantity` <= `min_stock_alert` THEN 'Low Stock'
            ELSE 'In Stock'
        END
    ) STORED,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) 
        REFERENCES `categories` (`category_id`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `idx_product_name` (`name`),
    INDEX `idx_product_barcode` (`barcode`),
    INDEX `idx_product_category` (`category_id`)
) ENGINE=InnoDB;

-- 3. Customers Table
CREATE TABLE IF NOT EXISTS `customers` (
    `customer_id` INT AUTO_INCREMENT PRIMARY KEY,
    `phone` VARCHAR(20) NOT NULL UNIQUE,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) DEFAULT NULL,
    `address` TEXT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_customer_phone` (`phone`)
) ENGINE=InnoDB;

-- 4. Invoices Table (Billing Sales Header)
CREATE TABLE IF NOT EXISTS `invoices` (
    `invoice_no` VARCHAR(30) PRIMARY KEY,
    `customer_id` INT DEFAULT NULL,
    `customer_name` VARCHAR(100) DEFAULT 'Walk-in Customer',
    `customer_phone` VARCHAR(20) DEFAULT NULL,
    `subtotal` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `tax_percent` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    `tax_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `discount_percent` DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    `discount_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `grand_total` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `payment_mode` VARCHAR(50) NOT NULL DEFAULT 'Cash',
    `invoice_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_invoice_customer` FOREIGN KEY (`customer_id`) 
        REFERENCES `customers` (`customer_id`) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `idx_invoice_date` (`invoice_date`)
) ENGINE=InnoDB;

-- 5. Invoice Line Items Table
CREATE TABLE IF NOT EXISTS `invoice_items` (
    `item_id` INT AUTO_INCREMENT PRIMARY KEY,
    `invoice_no` VARCHAR(30) NOT NULL,
    `product_id` INT NOT NULL,
    `product_name` VARCHAR(150) NOT NULL,
    `unit_price` DECIMAL(10, 2) NOT NULL,
    `quantity` INT NOT NULL,
    `line_total` DECIMAL(10, 2) NOT NULL,
    CONSTRAINT `fk_item_invoice` FOREIGN KEY (`invoice_no`) 
        REFERENCES `invoices` (`invoice_no`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_item_product` FOREIGN KEY (`product_id`) 
        REFERENCES `products` (`product_id`) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `idx_item_invoice` (`invoice_no`),
    INDEX `idx_item_product` (`product_id`)
) ENGINE=InnoDB;
