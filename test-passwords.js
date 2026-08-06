const mysql = require('mysql2');
const fs = require('fs');
const path = require('path');

// Common passwords to test
const commonPasswords = ['', 'root', 'admin', '123456', '1234', 'mysql', 'password'];

console.log('🔍 Scanning for your MySQL database password...');

async function testPassword(password) {
  return new Promise((resolve) => {
    const conn = mysql.createConnection({
      host: 'localhost',
      port: 3307,
      user: 'root',
      password: password
    });

    conn.connect((err) => {
      conn.end();
      if (err) {
        resolve({ success: false, code: err.code });
      } else {
        resolve({ success: true });
      }
    });
  });
}

function updateFiles(correctPassword) {
  const serverPath = path.join(__dirname, 'server.js');
  const importPath = path.join(__dirname, 'import-db.js');

  // Helper to replace password in a file
  function replacePasswordInFile(filePath, newPassword) {
    let content = fs.readFileSync(filePath, 'utf8');
    // Regex matches: password: 'any_value' or password: "any_value" or password: ''
    content = content.replace(/(password:\s*['"])[^'"]*(['"])/g, `$1${newPassword}$2`);
    fs.writeFileSync(filePath, content, 'utf8');
  }

  replacePasswordInFile(serverPath, correctPassword);
  replacePasswordInFile(importPath, correctPassword);
}

async function run() {
  let found = false;
  let correctPass = '';

  for (const pass of commonPasswords) {
    const displayPass = pass === '' ? '(empty password)' : `"${pass}"`;
    console.log(`Checking password: ${displayPass}...`);
    
    const result = await testPassword(pass);
    if (result.success) {
      correctPass = pass;
      found = true;
      break;
    }
  }

  if (found) {
    const displaySuccess = correctPass === '' ? 'empty (no password)' : `"${correctPass}"`;
    console.log('\n==================================================================');
    console.log(`✅ FOUND CORRECT PASSWORD: ${displaySuccess}`);
    console.log('==================================================================');
    console.log('🔧 Automatically updating your configuration files...');
    
    try {
      updateFiles(correctPass);
      console.log('✅ Updated "server.js" with the correct password.');
      console.log('✅ Updated "import-db.js" with the correct password.');
      console.log('\n👉 NOW RUN THIS COMMAND in your terminal to set up the database:');
      console.log('   node import-db.js');
      console.log('==================================================================\n');
    } catch (e) {
      console.error('❌ Failed to update files:', e.message);
    }
  } else {
    console.log('\n==================================================================');
    console.log('❌ PASSWORD NOT FOUND IN COMMON LIST');
    console.log('==================================================================');
    console.log('None of the default passwords worked.');
    console.log('Please reply with your custom MySQL password, and I will set it up for you.');
    console.log('==================================================================\n');
  }
}

run();
