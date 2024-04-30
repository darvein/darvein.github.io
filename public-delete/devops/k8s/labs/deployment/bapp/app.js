const express = require('express');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

app.get('/helloworld', (req, res) => {
  res.json({ message: 'I am Backend V2 now!!' });
});

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});
