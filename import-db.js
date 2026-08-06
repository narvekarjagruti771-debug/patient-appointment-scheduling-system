const fs = require('fs');
const path = require('path');
const mysql = require('mysql2');

console.log('🔄 Starting Database Import Utility...');

// Connection options (without specifying database, since we will create it)
const connectionOptions = {
  host: 'localhost',
  port: 3307,
  user: 'root',
  password: '', // Default XAMPP password is empty
  multipleStatements: true // Essential to execute multiple queries in schema.sql
};

const connection = mysql.createConnection(connectionOptions);

connection.connect((err) => {
  if (err) {
    console.error('\n==================================================================');
    console.error('❌ DATABASE CONNECTION ERROR!');
    console.error('==================================================================');
    console.error('Failed to connect to MySQL database engine.');
    console.error('Please make sure that the "MySQL" service is running in XAMPP.');
    console.error('Error Code:', err.code);
    console.error('Error Message:', err.sqlMessage || err.message);
    console.error('==================================================================\n');
    process.exit(1);
  }

  console.log('✅ Connected to MySQL Server successfully.');

  // Read the schema.sql file
  const schemaPath = path.join(__dirname, 'database', 'schema.sql');
  let sqlScript;

  try {
    sqlScript = fs.readFileSync(schemaPath, 'utf8');
    console.log('📖 Successfully read "database/schema.sql".');
  } catch (readErr) {
    console.error('❌ Error reading schema.sql file:', readErr.message);
    connection.end();
    process.exit(1);
  }

  // MySQL2 handles multiple statements, but delimiters (like DELIMITER //) are 
  // command-line client features. The Node.js mysql2 driver doesn't support 
  // DELIMITER statements directly and expects statements separated by semicolons.
  // We need to strip DELIMITER lines and replace custom delimiters in stored procedures.
  
  let formattedSql = sqlScript
    // Remove "DELIMITER //" and "DELIMITER ;" commands
    .replace(/DELIMITER\s+\/\/|DELIMITER\s+;/gi, '')
    // Replace stored procedure/trigger ending // with ;
    .replace(/\/\//g, ';');

  console.log('⏳ Creating database and importing tables, view, triggers, and stored procedures...');

  connection.query(formattedSql, (queryErr, results) => {
    if (queryErr) {
      console.error('\n==================================================================');
      console.error('❌ IMPORT DATABASE ERROR!');
      console.error('==================================================================');
      console.error('An error occurred during database importing:');
      console.error('SQL State:', queryErr.sqlState);
      console.error('Error Message:', queryErr.message);
      console.error('==================================================================\n');
      connection.end();
      process.exit(1);
    }

    console.log('\n==================================================================');
    console.log('🎉 DATABASE SETUP COMPLETED SUCCESSFULLY!');
    console.log('==================================================================');
    console.log('Database "appointment_db" is ready.');
    console.log('All tables, triggers, views, and procedures are created.');
    console.log('Sample Patient and Doctor data has been loaded.');
    console.log('==================================================================\n');
    
    connection.end();
  });
});
