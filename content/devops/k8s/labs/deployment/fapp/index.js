const http = require('http');
const express = require('express');
const app = express();
const port = 4000;

app.get('/', (req, res) => {
  http.get('http://backend:3000/helloworld', (apiRes) => {
    let data = '';

    // A chunk of data has been received.
    apiRes.on('data', (chunk) => {
      data += chunk;
    });

    // The whole response has been received. Send it to the frontend.
    apiRes.on('end', () => {
      const parsedData = JSON.parse(data);
      res.send(`Frontend V2 received: ${parsedData.message}`);
    });

  }).on("error", (err) => {
    console.log("Error: " + err.message);
    res.status(500).send(err.message);
  });
});

app.listen(port, () => {
  console.log(`Frontend listening at http://localhost:${port}`);
});
