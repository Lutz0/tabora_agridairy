-- Tabora AgriDairy schema updates
-- Run after initial create_tables.sql

USE tabora_agridairy;

-- 1) Cows table: keep existing structure and ensure status-like field support.
-- Existing app uses health_status column as status value.
ALTER TABLE cows
    MODIFY health_status VARCHAR(50) NOT NULL DEFAULT 'Healthy';

-- 2) Health tracking module
CREATE TABLE IF NOT EXISTS health_records (
    id INT NOT NULL AUTO_INCREMENT,
    cow_id INT NOT NULL,
    disease VARCHAR(150) NOT NULL,
    treatment TEXT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id),
    KEY ix_health_records_cow_id (cow_id),
    CONSTRAINT fk_health_records_cow FOREIGN KEY (cow_id)
        REFERENCES cows (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3) Payment system enhancements
ALTER TABLE payments
    ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20) NOT NULL DEFAULT 'Cash',
    ADD COLUMN IF NOT EXISTS reference VARCHAR(120) NULL;

-- Optional: allow payments without farmer link for sales receipts
ALTER TABLE payments
    MODIFY farmer_id INT NULL;

-- 4) Settings table
CREATE TABLE IF NOT EXISTS settings (
    id INT NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(80) NOT NULL,
    `value` TEXT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_settings_key (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

