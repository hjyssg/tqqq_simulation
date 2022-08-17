// 下载的csv date source: https://www.nasdaq.com/market-activity/funds-and-etfs/voo/historical
// 回测混合qqq和tqqq策略

const assert = require('assert');
const path = require('path');
const util = require("./util");



async function main(){
    let data1 = await util.getFileContents(path.resolve(".", "data", "qqq.csv"));
    let data2 = await util.getFileContents(path.resolve(".", "data","tqqq.csv"));

    const range = util.findSuitableRange(data1, data2);
    data1 = util.filterByRange(data1, range.max, range.min);
    data2 = util.filterByRange(data2, range.max, range.min);


    const init_total = 50; 
    const tqqq_ratio = 0.7; // how much percent of tqqq in the profile
    const qqq_ratio = 1 - tqqq_ratio;

    let monthly_added = 1; // the income added monthly
    let total_value = init_total;
    let qqq_value = init_total * qqq_ratio;
    let tqqq_value = tqqq_ratio;

    //todo the simulation

    console.log("-------------------------------");
    console.log("         done");
}


main();