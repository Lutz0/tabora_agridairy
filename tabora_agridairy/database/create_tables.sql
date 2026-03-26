-- ============================================================
-- Tabora AgriDairy Management System
-- MySQL Database Schema
-- Run this script to create all tables (matches SQLAlchemy models)
-- ============================================================

-- Create database (optional; skip if already created)
CREATE DATABASE IF NOT EXISTS tabora_agridairy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tabora_agridairy;

-- ============================================================
-- Table: users
-- User accounts for authentication (admin / farmer)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'farmer',
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email),
  KEY ix_users_username (username),
  KEY ix_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: cows
-- Livestock; each cow belongs to one user (owner)
-- ============================================================
CREATE TABLE IF NOT EXISTS cows (
  id INT NOT NULL AUTO_INCREMENT,
  tag_number VARCHAR(50) NOT NULL,
  breed VARCHAR(100) NOT NULL,
  age INT NOT NULL,
  health_status VARCHAR(50) NOT NULL DEFAULT 'Healthy',
  owner_id INT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_cows_tag_number (tag_number),
  KEY ix_cows_tag_number (tag_number),
  KEY ix_cows_owner_id (owner_id),
  CONSTRAINT fk_cows_owner FOREIGN KEY (owner_id)
    REFERENCES users (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: milk_production
-- Daily milk production per cow
-- ============================================================
CREATE TABLE IF NOT EXISTS milk_production (
  id INT NOT NULL AUTO_INCREMENT,
  cow_id INT NOT NULL,
  date DATE NOT NULL,
  quantity_liters DOUBLE NOT NULL,
  notes TEXT NULL,
  PRIMARY KEY (id),
  KEY idx_cow_date (cow_id, date),
  CONSTRAINT fk_milk_cow FOREIGN KEY (cow_id)
    REFERENCES cows (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: inventory
-- Farm supplies (feed, medicine, equipment)
-- ============================================================
CREATE TABLE IF NOT EXISTS inventory (
  id INT NOT NULL AUTO_INCREMENT,
  item_name VARCHAR(150) NOT NULL,
  category VARCHAR(50) NOT NULL,
  quantity INT NOT NULL DEFAULT 0,
  unit VARCHAR(30) NULL DEFAULT 'units',
  date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Table: payments
-- Payments to farmers (recorded by admin)
-- ============================================================
CREATE TABLE IF NOT EXISTS payments (
  id INT NOT NULL AUTO_INCREMENT,
  farmer_id INT NOT NULL,
  amount DOUBLE NOT NULL,
  payment_date DATE NOT NULL,
  description TEXT NULL,
  PRIMARY KEY (id),
  KEY ix_payments_farmer_id (farmer_id),
  CONSTRAINT fk_payments_farmer FOREIGN KEY (farmer_id)
    REFERENCES users (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- End of schema
-- ============================================================
