# Patient Appointment Scheduling System - DBMS Project

Welcome! This is a complete, beginner-friendly Patient Appointment Scheduling System. It connects a modern web user interface (HTML/CSS/JS) to a Node.js backend and a MySQL database (run via XAMPP).

This project mandatorily includes and demonstrates three core DBMS features:
1. **SQL View (`upcoming_appointments_view`)**: Simulates a consolidated, readable appointment schedule.
2. **SQL Trigger (`after_appointment_insert` & `after_appointment_update`)**: Automatically records system audits in log tables whenever appointments are made or modified.
3. **Cursor Stored Procedure (`generate_daily_report`)**: Uses a database cursor to loop through scheduled appointments for any selected date and builds a formatted text schedule summary.

---

## 🛠️ Step-by-Step Setup Guide

Follow these simple steps to run the application on your computer:

### Step 1: Start MySQL in XAMPP
1. Open the **XAMPP Control Panel** on your computer.
2. Click **Start** next to **MySQL** (Apache is **not** required for this project, so you can leave it stopped!).
3. Make sure **MySQL** turns green and is running.

### Step 2: Open project in VS Code
1. Open **VS Code**.
2. Click **File > Open Folder...** and select this directory:
   `C:\Users\HP\.gemini\antigravity\scratch\patient_appointment_system`
3. If VS Code asks if you trust the authors, click **Yes**.

### Step 3: Initialize the Database (Two Options)

#### Option A: Automatic Setup via Terminal (Recommended & Doesn't require Apache!)
1. Open the integrated terminal in VS Code (**Terminal > New Terminal**).
2. Run this command to automatically create and import the database:
   ```bash
   node import-db.js
   ```
3. You should see a success message: `🎉 DATABASE SETUP COMPLETED SUCCESSFULLY!`

#### Option B: Manual Setup via phpMyAdmin (Requires Apache to be working)
1. In XAMPP, start **Apache** and go to: [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
2. Click on **New** in the left sidebar to create a database.
3. Enter **`patient_appointment_db`** as the database name and click **Create**.
4. Select the database, click the **Import** tab at the top.
5. Click **Choose File** and select `database/schema.sql`.
6. Scroll to the bottom and click **Import** (or **Go**).

### Step 4: Run the Node.js Backend Server
1. In your VS Code terminal, run:
   ```bash
   npm start
   ```
2. You should see:
   `✅ Connected to MySQL database successfully!`
   `🌐 Server is running on: http://localhost:3008`

### Step 5: Access the Frontend
1. Open your web browser and navigate to: [http://localhost:3008](http://localhost:3008)
2. You're ready to use the app!

---

## 🔍 How to Test the DBMS Features in the App

1. **Test the SQL View**:
   - Go to the **Appointments** tab in the sidebar. This list queries the `upcoming_appointments_view` which joins tables inside MySQL to display Patient names, Doctor names, and specializations without repeating data.

2. **Test the SQL Triggers**:
   - Go to the **Book & Stats** tab and book a new appointment.
   - Now click on the **DB Trigger Logs** tab. You will see a newly generated row. That log entry was written by a database **Trigger** (`after_appointment_insert`) automatically, not by Node.js!
   - Go back to the **Appointments** list, find a "Scheduled" appointment, and click **Done** or **Cancel**.
   - Review the **DB Trigger Logs** tab again. The trigger `after_appointment_update` caught the status change, kept a record of the old status vs new status, and logged it automatically.

3. **Test the Cursor Stored Procedure**:
   - Go to the **Cursor Reports** tab in the sidebar.
   - Choose a date (e.g. `2026-05-23` which has pre-loaded sample appointments) and click **Run SQL Cursor SP**.
   - The database executes the `generate_daily_report` stored procedure. It activates a **Cursor** inside MySQL, loops through all matching appointments one by one, formats them into a neat report block, saves it to `daily_reports`, and returns it to the screen.
