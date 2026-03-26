-- Fix missing Payment columns for legacy databases
USE tabora_agridairy;

ALTER TABLE payments
    ADD COLUMN IF NOT EXISTS payment_method VARCHAR(20) NOT NULL DEFAULT 'Cash',
    ADD COLUMN IF NOT EXISTS reference VARCHAR(120) NULL,
    ADD COLUMN IF NOT EXISTS description TEXT NULL;

