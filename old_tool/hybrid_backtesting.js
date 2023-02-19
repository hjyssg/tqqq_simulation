// 下载的csv date source: https://www.nasdaq.com/market-activity/funds-and-etfs/voo/historical
// 回测混合qqq和tqqq策略

const assert = require('assert');
const path = require('path');
const util = require("./util");

function doSimulation(data_qqq, data_tqqq, doBalancing, tqqq_ratio, begin, balancing_interval,init_total, month_dca){
    const qqq_ratio = 1 - tqqq_ratio;

    // let monthly_added = 1; // the income added monthly
    let qqq_value = init_total * qqq_ratio;
    let tqqq_value = init_total * tqqq_ratio;

    let qqq_last_price = data_qqq[begin].Open;
    let tqqq_last_price = data_tqqq[begin].Open;
    
    // console.log(`total:${(qqq_value+tqqq_value).toFixed(3)} qqq:${qqq_value.toFixed(3)}  tqqq:${tqqq_value.toFixed(3)}`)
    let max_increase = 0;
    

    for(let ii = (begin + balancing_interval); ii < data_qqq.length; ii=balancing_interval+ii){
    // for(let ii = 5; ii < 200; ii=10+ii){
        let qqq_price = data_qqq[ii].Open;
        let tqqq_price = data_tqqq[ii].Open;

        let qqq_change = qqq_price/qqq_last_price;
        let tqqq_change = tqqq_price/tqqq_last_price;

        qqq_last_price = qqq_price;
        tqqq_last_price = tqqq_price;

        qqq_value *= qqq_change;
        tqqq_value *= tqqq_change;

        let total = (qqq_value+tqqq_value);
        const percent = ((total-init_total)/init_total*100);

        // if(percent > 0){
        //     max_increase = Math.max(max_increase, percent);
        // }else{
        //     max_drop = Math.min(max_drop, max_increase);
        // }

        max_increase = Math.max(max_increase, percent);
       

        // console.log(`${data_qqq[ii].Date.toDateString()} total:${(total).toFixed(3)} ${((total-init_total)/init_total*100).toFixed(2)}%  qqq:${qqq_value.toFixed(3)}  tqqq:${tqqq_value.toFixed(3)}`)
        // console.log(`${data_qqq[ii].Date.toDateString()} ${((total-init_total)/init_total*100).toFixed(2)}%  qqq:${qqq_value.toFixed(3)}  tqqq:${tqqq_value.toFixed(3)}`)
        // console.log(" ");
        // console.log(`${data_qqq[ii].Date.toDateString()} total:${((total-init_total)/init_total*100).toFixed(2)}%`)
        // console.log(`qqq:${qqq_value.toFixed(3)}  tqqq:${tqqq_value.toFixed(3)}`)
        
        let new_added = (balancing_interval/30) * month_dca;
        qqq_value += qqq_ratio * new_added;
        tqqq_value += tqqq_ratio * new_added;


        if(doBalancing){
            const rebalancing = tqqq_value - total * tqqq_ratio;
            tqqq_value -= rebalancing;
            qqq_value += rebalancing;
        }
        // console.log(`relanced  qqq:${qqq_value.toFixed(3)}  tqqq:${tqqq_value.toFixed(3)}`)
    }

    let total = (qqq_value+tqqq_value);
    const percent = ((total-init_total)/init_total*100);

    // console.log(`final:${percent.toFixed(3)}% max_drop:${max_drop.toFixed(3)}% max_increase:${max_increase.toFixed(3)}%`);
    console.log(`tqqq_ratio:${tqqq_ratio.toFixed(3)} balancing_interval:${balancing_interval}  final:${percent.toFixed(3)}%  max_increase:${max_increase.toFixed(3)}%`);
}

async function main(){
    let data_qqq = await util.getFileContents(path.resolve(".", "data", "voo.csv"));
    let data_tqqq = await util.getFileContents(path.resolve(".", "data","tqqq.csv"));

    const range = util.findSuitableRange(data_qqq, data_tqqq);
    data_qqq = util.filterByRange(data_qqq, range.max, range.min);
    data_tqqq = util.filterByRange(data_tqqq, range.max, range.min);

    //测试现金平衡策略
    const MAKE_QQQ_AS_CASH = false;
    if (MAKE_QQQ_AS_CASH){
        data_qqq.forEach(e => {
            e["Close/Last"] = 1;
            e["High"] = 1;
            e["Low"] = 1;
            e["Open"] = 1;
            e["percent"] = 0;
            e["Volume"] = 1;
        })
    }

    const month_dca = 1; //每月定投金额
    // const trial_intervals = [5, 10, 30];
    const trial_intervals = [10];
    const begin = 1500;  // begin arr index

    const last = data_qqq[data_qqq.length-1];
    console.log(`${data_qqq[begin].Date.toDateString()} - ${last.Date.toDateString()} `);

    doSimulation(data_qqq, data_tqqq, doBalancing=false, tqqq_ratio=0, begin, balancing_interval=10, init_total=50, month_dca)
    console.log("");

    trial_intervals.forEach(balancing_interval => {
        for(let ii = 3; ii < 8; ii++){
            const tqqq_ratio = ii * 0.1;
            doSimulation(data_qqq, data_tqqq, doBalancing=true, tqqq_ratio, begin, balancing_interval, init_total=50, month_dca)

        }
        console.log("");
    })

    //结论1： balancing频率 30天以内都差不多，60天太慢了

    doSimulation(data_qqq, data_tqqq, doBalancing=false, tqqq_ratio=1, begin, balancing_interval=10, init_total=50, month_dca)
    console.log("");

    console.log("-------------------------------");
    console.log("         done");
}


main();