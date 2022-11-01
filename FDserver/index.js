const express = require('express');
var fs = require('fs')
const path = require('path');
const converter = require('json-2-csv');
const json2csv = require('json2csv');
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
  
  fields = ['sensor1', 'sensor2', 'date']
  var toCsv = {
    data : req.body,
    fields : fields,
    header: false,
  };
  
  converter.json2csv(sensorData, (err, csvData) => {
    if (err){
      throw err
    }
    console.log(csvData)
    fs.appendFileSync(csvPath, csvData + '\n')
  }, {prependHeader:false})  

  console.log(sensorData);
  res.send(sensorData);
});

app.listen(5000)