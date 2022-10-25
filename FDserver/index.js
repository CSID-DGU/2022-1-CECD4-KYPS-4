const express = require('express');
var fs = require('fs')
const path = require('path');
const converter = require('json-2-csv');
var stringify = require('csv-stringify');
const app = express();

app.use(express.json())

app.get('/', (req, res) => {
  res.send('Hello World!')
});

app.post('/sensor', (req, res) => {

  let now = new Date();
  
  sensorData = req.body;
  sensorData.servertime = now.toLocaleString();
  
  FILE_NAME = "test.csv";
  csvPath = path.join(__dirname, '/csvs', FILE_NAME);
  
  converter.json2csv(sensorData, {header:false}, (err, csvData) => {
    if (err){
      throw err
    }
    console.log(csvData)
    fs.appendFileSync(csvPath, csvData + '\r\n')
  })

  console.log(sensorData);
  res.send(sensorData);
});

app.listen(5000)