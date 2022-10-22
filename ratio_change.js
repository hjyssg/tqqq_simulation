// 下载的csv date source: https://www.nasdaq.com/market-activity/funds-and-etfs/voo/historical
// 本文件计算各类etf相对于qqq的杠杆率
// 一段时间内，qqq的前后差值百分比 除以 其他etf的前后差值百分比
// 来帮助预估一长段时间价格

const assert = require('assert');
const path = require('path');
const util = require("./util");


function toPercentStr(num){
    return  num.toFixed(3)+"%"
}

function dailyCompare(data1, data2){
    // assume both have the same amount of data. same start data
    let avg  = 0;
    for(let ii = 0; ii < data1.length; ii++){
        const row1 = data1[ii];
        const row2 = data2[ii];
        //https://www.w3schools.com/nodejs/met_assert.asp
        assert(row1.Date.getTime() == row2.Date.getTime(), "should have the same date");

        const mult = row2.percent/row1.percent;
        // when the percent is neat 0, the mult will be too big or too small
        console.log(toPercentStr(row1.percent) +"             " + toPercentStr(row2.percent) + "       " + (mult).toFixed(3));
        
        if(mult > 2 && mult < 4 && Math.abs(row1.percent) > 0.05 && Math.abs(row2.percent) > 0.05 ){
            avg += mult/data1.length;
        }else{
            avg += 3/data1.length;
        }

        // 确认涨跌是一样的
        // 结论：在波动极小的时候，不一定
        // if(!(row1.percent * row2.percent >= 0)){
            // debugger;
            // console.log(toPercentStr(row1.percent) +"             " + toPercentStr(row2.percent) + "       " + (mult).toFixed(3));
        // }
    }
    console.log("average leverage is ", avg)
}

function gapCompare(data1, data2, gap){
    let mult_sum = 0;
    let mult_count = 0;

    // assume both have the same amount of data. same start data
    for(let ii = 0; ii < data1.length - gap; ii++){
        const row1 = data1[ii];
        const row2 = data2[ii];
        //https://www.w3schools.com/nodejs/met_assert.asp
        assert(row1.Date.getTime() == row2.Date.getTime(), "should have the same date");
        assert(data2[ii+gap].Date.getTime() == data1[ii+gap].Date.getTime(), "should have the same date");


        const p1 = (data1[ii+gap]["Close/Last"] - data1[ii]['Open'])/data1[ii]['Open'] * 100;
        const p2 = (data2[ii+gap]["Close/Last"] - data2[ii]['Open'])/data2[ii]['Open'] * 100;

        const mult = p2/p1;
        // when the percent is neat 0, the mult will be too big or too small
        // console.log(`${row1.Date.toDateString()}-${data1[ii+gap].Date.toDateString()} ${toPercentStr(p1)}   ${toPercentStr(p2)}  ${(mult).toFixed(3)}`)

        if(mult != Infinity && mult != -Infinity  && !isNaN(mult)){
            mult_sum += mult;
            mult_count++;
        }

        // 确认涨跌是否一样的

        // TODO: 如何止盈最好
        // if((p1 * p2 < 0)){
        //     console.log(row1.Date+ "-" + data1[ii+gap].Date + "   " + toPercentStr(p1) + "             " + toPercentStr(p2) + "       " + (mult).toFixed(3));
        // }
    }
    console.log(gap + " days average leverage is ", (mult_sum/mult_count).toFixed(3))
}





async function main(){
    let data1 = await util.getFileContents(path.resolve(".", "data", "qqq.csv"));
    let data2 = await util.getFileContents(path.resolve(".", "data","tqqq.csv"));

    const range = util.findSuitableRange(data1, data2);
    data1 = util.filterByRange(data1, range.max, range.min);
    data2 = util.filterByRange(data2, range.max, range.min);

    //  gapCompare(data1, data2, 0);
    // gapCompare(data1, data2, 100);

    for(let ii = 0; ii < 360 * 3; ii=ii+5){
        gapCompare(data1, data2, ii);
    }

    console.log("-------------------------------");
    console.log("         done");
}


main();