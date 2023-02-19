const csv = require('csv-parser');
const fs = require('fs');
var assert = require('assert');


// used to read data from csv file
const getFileContents = (filepath) => {
  //https://stackoverflow.com/questions/61088584/how-to-return-my-csv-data-from-my-service-async-await-issue
  const results = [];
  return new Promise(function(resolve, reject) {
    fs.createReadStream(filepath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => {
        // return data;
        resolve(processRaw(results));
      });
    });
}

// process the raw data
const processRaw = (rawData) => {
    rawData.forEach(row => {
        row['Close/Last'] = parseFloat(row['Close/Last']);
        row['Open'] = parseFloat(row['Open']);
        row["percent"] = (row['Close/Last'] - row['Open'])/row['Open'];
        row["percent"] = 100 * row["percent"];
        row["Date"] = new Date(row["Date"]);
    })
    // the data from nasdaq.com is reverse
    return rawData.reverse();
}


function findSuitableRange(data1, data2){
    return {
        max: new Date(Math.min(data1[data1.length-1].Date, data2[data2.length-1].Date)),
        min: new Date(Math.max(data1[0].Date, data2[0].Date))
    }
}

function filterByRange(data, max, min){
    return data.filter(e => {
        return e.Date >= min && e.Date <= max;
    })
}

module.exports = {
    getFileContents,
    processRaw,
    findSuitableRange,
    filterByRange
};