-- ====================================================================
-- DBMS Project: Patient Appointment Scheduling System
-- Database Schema, View, Triggers, Cursor Stored Procedure, and Seed Data
-- ====================================================================

-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS `appointment_db`;
USE `appointment_db`;

-- ====================================================================
-- 1. DROP EXISTING OBJECTS (for clean re-runs)
-- ====================================================================
DROP PROCEDURE IF EXISTS generate_daily_report;
DROP TRIGGER IF EXISTS after_appointment_insert;
DROP TRIGGER IF EXISTS after_appointment_update;
DROP VIEW IF EXISTS upcoming_appointments_view;
DROP TABLE IF EXISTS appointment_logs;
DROP TABLE IF EXISTS daily_reports;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;

-- ====================================================================
-- 2. TABLE CREATION
-- ====================================================================

-- Table: patients
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Table: doctors
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Table: appointments
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Table: appointment_logs (Used by Trigger to record insert/update events)
CREATE TABLE appointment_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    action_type ENUM('CREATE', 'UPDATE', 'DELETE') NOT NULL,
    old_status VARCHAR(20) DEFAULT NULL,
    new_status VARCHAR(20) NOT NULL,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
) ENGINE=InnoDB;

-- Table: daily_reports (Used by Stored Procedure with Cursor to store summaries)
CREATE TABLE daily_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_date DATE UNIQUE NOT NULL,
    report_summary TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ====================================================================
-- 3. SQL VIEW CREATION (Mandatory Element #1)
-- ====================================================================
-- The view consolidates data from patients, doctors, and appointments to
-- provide a comprehensive, read-only summary of upcoming schedules.
CREATE VIEW upcoming_appointments_view AS
SELECT 
    a.appointment_id,
    a.patient_id,
    p.name AS patient_name,
    p.phone AS patient_phone,
    a.doctor_id,
    d.name AS doctor_name,
    d.specialization AS doctor_specialization,
    a.appointment_date,
    a.appointment_time,
    a.status,
    a.reason
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
ORDER BY a.appointment_date ASC, a.appointment_time ASC;

-- ====================================================================
-- 4. SQL TRIGGERS CREATION (Mandatory Element #2)
-- ====================================================================

-- Trigger for NEW appointments
DELIMITER //
CREATE TRIGGER after_appointment_insert
AFTER INSERT ON appointments
FOR EACH ROW
BEGIN
    INSERT INTO appointment_logs (
        appointment_id, 
        action_type, 
        old_status, 
        new_status, 
        description
    ) VALUES (
        NEW.appointment_id, 
        'CREATE', 
        NULL, 
        NEW.status, 
        CONCAT('New appointment booked for patient ID ', NEW.patient_id, ' with doctor ID ', NEW.doctor_id, ' for ', NEW.appointment_date, ' at ', NEW.appointment_time)
    );
END//
DELIMITER ;

-- Trigger for UPDATING appointments (e.g. status changes)
DELIMITER //
CREATE TRIGGER after_appointment_update
AFTER UPDATE ON appointments
FOR EACH ROW
BEGIN
    -- Log the change if the status or date/time was modified
    IF OLD.status <> NEW.status OR OLD.appointment_date <> NEW.appointment_date OR OLD.appointment_time <> NEW.appointment_time THEN
        INSERT INTO appointment_logs (
            appointment_id, 
            action_type, 
            old_status, 
            new_status, 
            description
        ) VALUES (
            NEW.appointment_id, 
            'UPDATE', 
            OLD.status, 
            NEW.status, 
            CONCAT('Appointment (ID: ', NEW.appointment_id, ') details updated. Status changed from ', OLD.status, ' to ', NEW.status, '.')
        );
    END IF;
END//
DELIMITER ;

-- ====================================================================
-- 5. STORED PROCEDURE WITH CURSOR CREATION (Mandatory Element #3)
-- ====================================================================
-- This stored procedure uses a SQL cursor to loop through all appointments
-- scheduled for a specific date, aggregates them into a detailed summary,
-- and saves it to the `daily_reports` table.
DELIMITER //
CREATE PROCEDURE generate_daily_report(IN target_date DATE)
BEGIN
    -- Declare variables for cursor fetch
    DECLARE done INT DEFAULT FALSE;
    DECLARE appt_id INT;
    DECLARE p_name VARCHAR(100);
    DECLARE d_name VARCHAR(100);
    DECLARE d_spec VARCHAR(100);
    DECLARE appt_time TIME;
    DECLARE appt_reason VARCHAR(255);
    DECLARE appt_status VARCHAR(20);
    
    -- Variables to construct the final report summary
    DECLARE report_text TEXT DEFAULT '';
    DECLARE appt_count INT DEFAULT 0;
    
    -- Declare Cursor to fetch appointments for the target date
    DECLARE appt_cursor CURSOR FOR
        SELECT 
            a.appointment_id,
            p.name AS patient_name,
            d.name AS doctor_name,
            d.specialization AS doctor_specialization,
            a.appointment_time,
            a.reason,
            a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date = target_date
        ORDER BY a.appointment_time ASC;
        
    -- Declare Not Found handler to close the cursor loop
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Open Cursor
    OPEN appt_cursor;
    
    -- Loop through appointments
    read_loop: LOOP
        FETCH appt_cursor INTO appt_id, p_name, d_name, d_spec, appt_time, appt_reason, appt_status;
        
        -- Check if loop is completed
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Append current appointment info to report_text
        SET appt_count = appt_count + 1;
        SET report_text = CONCAT(
            report_text, 
            appt_count, '. [', appt_time, '] Patient: ', p_name, 
            ' | Doctor: Dr. ', d_name, ' (', d_spec, ')',
            ' | Reason: ', appt_reason, 
            ' | Status: ', appt_status, '\n'
        );
    END LOOP;
    
    -- Close Cursor
    CLOSE appt_cursor;
    
    -- If no appointments were found, create a placeholder summary
    IF appt_count = 0 THEN
        SET report_text = CONCAT('No appointments scheduled for ', DATE_FORMAT(target_date, '%W, %M %d, %Y'), '.');
    ELSE
        SET report_text = CONCAT(
            'Daily Schedule Summary for ', DATE_FORMAT(target_date, '%W, %M %d, %Y'), '\n',
            'Total Appointments: ', appt_count, '\n',
            '-----------------------------------------\n',
            report_text
        );
    END IF;
    
    -- Insert or Update report in the database
    INSERT INTO daily_reports (report_date, report_summary)
    VALUES (target_date, report_text)
    ON DUPLICATE KEY UPDATE 
        report_summary = VALUES(report_summary),
        generated_at = CURRENT_TIMESTAMP;
        
    -- Select the report to return it to the caller
    SELECT report_date, report_summary, generated_at 
    FROM daily_reports 
    WHERE report_date = target_date;
    
END//
DELIMITER ;

-- ====================================================================
-- 6. INSERT SEED DATA
-- ====================================================================

-- Insert Sample Patients
INSERT INTO patients (name, email, phone, dob, gender) VALUES
('Annapoorna Hasabi', 'annapoorna@email.com', '555-0199', '1998-05-15', 'Female'),
('Kavana Araladinni', 'kavana@email.com', '555-0144', '1999-08-22', 'Female'),
('Amruta M', 'amruta@email.com', '555-0177', '1997-12-05', 'Female'),
('Deepti Patil', 'deepti@email.com', '555-0188', '1998-03-10', 'Female'),
('Ramya D', 'ramya@email.com', '555-0122', '1996-10-31', 'Female');

-- Insert Sample Doctors
INSERT INTO doctors (name, specialization, email, phone) VALUES
('Jagruti Narvekar', 'Cardiology', 'dr.jagruti@clinic.com', '555-0211'),
('David Miller', 'Pediatrics', 'dr.miller@clinic.com', '555-0222'),
('Lisa Anderson', 'Dermatology', 'dr.anderson@clinic.com', '555-0233'),
('Thomas Taylor', 'General Medicine', 'dr.taylor@clinic.com', '555-0244');

-- Insert Sample Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason) VALUES
(1, 1, '2026-05-23', '09:00:00', 'Scheduled', 'Annual Health Checkup with Dr. Jagruti Narvekar'),
(2, 2, '2026-05-23', '10:30:00', 'Scheduled', 'Child Vaccination and Growth Review'),
(3, 1, '2026-05-23', '14:00:00', 'Scheduled', 'Cardiovascular Checkup with Dr. Jagruti Narvekar'),
(4, 3, '2026-05-24', '11:00:00', 'Scheduled', 'Skin rash consultation'),
(5, 4, '2026-05-24', '15:30:00', 'Scheduled', 'Follow-up on Lab Test Results'),
(1, 3, '2026-05-20', '10:00:00', 'Completed', 'Acne treatment followup');
