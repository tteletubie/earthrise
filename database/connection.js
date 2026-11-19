const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, '..', 'db.db');
const db = new Database(dbPath);

// Enable foreign keys and Write-Ahead Logging
db.pragma('foreign_keys = ON');
db.pragma('journal_mode = WAL');

const schemaPath = path.join(__dirname, 'database.sql');

if (!fs.existsSync(schemaPath)) {
  console.warn(`[Database] Schema file not found: ${schemaPath}`);
} else {
  try {
    const schemaSql = fs.readFileSync(schemaPath, 'utf8');
    db.exec(schemaSql);
    console.warn(`[Database] Schema loaded successfully: ${schemaPath}`);
  } catch (error) {
    console.error(`[Database] Failed to execute schema: ${schemaPath}`, error);
  }
}

module.exports = db;
