const http = require('http');
const express = require('express');
const app = express();
const port = 4000;

app.get('/', (req, res) => {
  fetchDataFromAPI('http://backend:3000/helloworld', res, 'Frontend V2 received:');
});

app.get('/db', (req, res) => {
  fetchDataFromAPI('http://backend:3000/db', res, 'Data from table:');
});

const fetchDataFromAPI = (url, res, messagePrefix) => {
  http.get(url, (apiRes) => {
    let data = '';

    // A chunk of data has been received.
    apiRes.on('data', (chunk) => {
      data += chunk;
    });

    // The whole response has been received. Send it to the frontend.
    apiRes.on('end', () => {
      res.send(`${messagePrefix} ${data}`);
    });

  }).on("error", (err) => {
    console.log("Error: " + err.message);
    res.status(500).send(err.message);
  });
};

app.listen(port, () => {
  console.log(`Frontend listening at http://localhost:${port}`);
});
