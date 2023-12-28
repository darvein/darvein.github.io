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

app.get('/helloworld', (req, res) => {
  res.json({ message: 'I am Backend V2 now!!' });
});

app.get('/db', (req, res) => {
  //const sql = 'SELECT * FROM testTable';
  const sql = 'select name from testTable limit 1,1;';
  
  db.query(sql, (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});
