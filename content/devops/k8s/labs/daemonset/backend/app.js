const express = require('express');
const cors = require('cors');
const mysql = require('mysql');

const app = express();
const port = 3000;

// MySQL connection
const db = mysql.createConnection({
  host: process.env.MYSQL_HOST || 'localhost',
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || 'defaultpassword',
  database: process.env.MYSQL_DATABASE || 'testDB'
});

db.connect((err) => {
  if (err) throw err;
  console.log('Connected to the database');
});

app.use(cors());

app.get('/hello', (req, res) => {
  res.json({ message: 'I am Backend App' });
});

app.get('/click', (req, res) => {
  // Get the value from query parameter
  const value = req.query.value;

  // Validate the value, very important
  if (!Number.isInteger(parseInt(value))) {
    res.status(400).json({ error: 'Invalid value provided' });
    return;
  }

  // Use parameterized query for inserting the value
  const sql = 'INSERT INTO clicks (clicked) VALUES (?)';

  db.query(sql, [value], (err, results) => {
    if (err) {
      res.status(500).json({ error: 'An error occurred' });
      return;
    }
    res.json({ message: 'Successfully incremented clicked', results });
  });
});

app.get('/report', (req, res) => {
  const sql = 'SELECT COUNT(*) FROM clicks';

  db.query(sql, (err, results) => {
    if (err) {
      res.status(500).json({ error: 'An error occurred' });
      return;
    }

    // Extract the count from the results
    const count = results[0]['COUNT(*)'];

    // Include the count in the JSON response
    res.json({ message: 'Successfully retrieved count', count });
  });
});

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});
