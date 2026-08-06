const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3008;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Database Connection Configuration (Default XAMPP settings)
const dbConfig = {
  host: 'localhost',
  port: 3307,
  user: 'root',
  password: '', // default XAMPP MySQL password is empty
  database: 'appointment_db',
  multipleStatements: true // Required to run stored procedures and multiple queries
};

// Create a database connection pool
const pool = mysql.createPool(dbConfig);

// Helper function to query the database using Promises
function query(sql, params) {
  return new Promise((resolve, reject) => {
    pool.query(sql, params, (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });
}

// Test database connection on startup
pool.getConnection((err, connection) => {
  if (err) {
    console.error('\n==================================================================');
    console.error('❌ DATABASE CONNECTION ERROR!');
    console.error('==================================================================');
    console.error('Could not connect to MySQL database "appointment_db".');
    console.error('Please verify the following:');
    console.error('1. XAMPP Control Panel is open and MySQL service is running.');
    console.error('2. You have imported the "database/schema.sql" file in phpMyAdmin.');
    console.error('3. Default XAMPP settings are used (localhost, user: root, no password).');
    console.error('Error Code:', err.code);
    console.error('Error Message:', err.sqlMessage || err.message);
    console.error('==================================================================\n');
  } else {
    console.log('\n==================================================================');
    console.log('✅ Connected to MySQL database successfully!');
    console.log('🌐 Server is running on: http://localhost:' + PORT);
    console.log('==================================================================\n');
    connection.release();
  }
});

// ====================================================================
// API ENDPOINTS
// ====================================================================

// 1. Get list of doctors (for dropdowns)
app.get('/api/doctors', async (req, res) => {
  try {
    const results = await query('SELECT doctor_id, name, specialization, email, phone FROM doctors ORDER BY name');
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve doctors.' });
  }
});

// 2. Get list of patients (for dropdowns)
app.get('/api/patients', async (req, res) => {
  try {
    const results = await query('SELECT patient_id, name, email, phone FROM patients ORDER BY name');
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve patients.' });
  }
});

// Register a new patient
app.post('/api/patients', async (req, res) => {
  const { name, email, phone, dob, gender } = req.body;
  if (!name || !email || !phone || !dob || !gender) {
    return res.status(400).json({ error: 'Missing required patient fields.' });
  }
  try {
    const sql = 'INSERT INTO patients (name, email, phone, dob, gender) VALUES (?, ?, ?, ?, ?)';
    const result = await query(sql, [name, email, phone, dob, gender]);
    res.status(201).json({ 
      message: 'Patient registered successfully!', 
      patient_id: result.insertId 
    });
  } catch (err) {
    console.error(err);
    if (err.code === 'ER_DUP_ENTRY') {
      res.status(400).json({ error: 'A patient with this email already exists.' });
    } else {
      res.status(500).json({ error: 'Failed to register patient.' });
    }
  }
});

// 3. Get all appointments (USING THE VIEW - Mandatory Requirement #1)
// We query the VIEW "upcoming_appointments_view" instead of doing raw joins here.
// This simplifies the server code and encapsulates query logic in the database!
app.get('/api/appointments', async (req, res) => {
  try {
    const results = await query('SELECT * FROM upcoming_appointments_view');
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve appointments using the SQL View.' });
  }
});

// Get appointments for a specific patient using the View
app.get('/api/patients/:id/appointments', async (req, res) => {
  const patientId = req.params.id;
  try {
    const results = await query('SELECT * FROM upcoming_appointments_view WHERE patient_id = ?', [patientId]);
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve patient appointments.' });
  }
});

// Get appointments for a specific doctor using the View
app.get('/api/doctors/:id/appointments', async (req, res) => {
  const doctorId = req.params.id;
  try {
    const results = await query('SELECT * FROM upcoming_appointments_view WHERE doctor_id = ?', [doctorId]);
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve doctor appointments.' });
  }
});

// 4. Book a new appointment
// When a row is inserted here, the database TRIGGER "after_appointment_insert" runs automatically!
app.post('/api/appointments', async (req, res) => {
  const { patient_id, doctor_id, appointment_date, appointment_time, reason } = req.body;
  
  if (!patient_id || !doctor_id || !appointment_date || !appointment_time || !reason) {
    return res.status(400).json({ error: 'Missing required appointment fields.' });
  }
  
  try {
    const sql = `INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status) 
                 VALUES (?, ?, ?, ?, ?, 'Scheduled')`;
    const result = await query(sql, [patient_id, doctor_id, appointment_date, appointment_time, reason]);
    res.status(201).json({ 
      message: 'Appointment booked successfully!', 
      appointment_id: result.insertId 
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create appointment.' });
  }
});

// 5. Update appointment status (e.g. Cancel or Complete)
// When status is updated, the database TRIGGER "after_appointment_update" runs automatically!
app.put('/api/appointments/:id/status', async (req, res) => {
  const appointmentId = req.params.id;
  const { status } = req.body;
  
  if (!status || !['Scheduled', 'Completed', 'Cancelled'].includes(status)) {
    return res.status(400).json({ error: 'Invalid or missing status.' });
  }
  
  try {
    const sql = 'UPDATE appointments SET status = ? WHERE appointment_id = ?';
    const result = await query(sql, [status, appointmentId]);
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Appointment not found.' });
    }
    res.json({ message: `Appointment status updated to ${status}!` });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update appointment status.' });
  }
});

// 6. Get database activity logs (Populated by TRIGGER - Mandatory Requirement #2)
// This lets the user see the trigger in action!
app.get('/api/logs', async (req, res) => {
  try {
    const results = await query('SELECT * FROM appointment_logs ORDER BY log_timestamp DESC');
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve database logs.' });
  }
});

// 7. Generate a daily schedule report (USING THE CURSOR STORED PROCEDURE - Mandatory Requirement #3)
// We call the stored procedure `generate_daily_report(?)` which handles fetching appointments 
// using a cursor, constructing a formatted summary, and saving it.
app.post('/api/reports/generate', async (req, res) => {
  const { date } = req.body;
  if (!date) {
    return res.status(400).json({ error: 'Date is required to generate report.' });
  }
  
  try {
    // MySQL returns procedure results inside an array of arrays
    const results = await query('CALL generate_daily_report(?)', [date]);
    
    // The procedure ends with a SELECT statement that returns the report row
    // results[0] will be the result of the SELECT statement in the procedure
    if (results && results[0] && results[0][0]) {
      res.json(results[0][0]);
    } else {
      res.status(500).json({ error: 'Stored procedure executed but returned no data.' });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to run stored procedure (Cursor-based Daily Report).' });
  }
});

// 8. Get all generated daily reports
app.get('/api/reports', async (req, res) => {
  try {
    const results = await query('SELECT * FROM daily_reports ORDER BY report_date DESC');
    res.json(results);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve reports.' });
  }
});

// Catch-all route to serve the frontend for other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start express server with port busy fallback
const server = app.listen(PORT, () => {
  console.log(`\n==================================================================`);
  console.log(`🌐 Application started successfully!`);
  console.log(`👉 Access URL: http://localhost:${PORT}`);
  console.log(`==================================================================\n`);
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    const ALT_PORT = Number(PORT) + 1;
    console.log(`⚠️ Port ${PORT} is occupied. Trying fallback port ${ALT_PORT}...`);
    app.listen(ALT_PORT, () => {
      console.log(`\n==================================================================`);
      console.log(`🌐 Application started on fallback port!`);
      console.log(`👉 Access URL: http://localhost:${ALT_PORT}`);
      console.log(`==================================================================\n`);
    });
  } else {
    console.error('Server error:', err);
  }
});

