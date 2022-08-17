//计算混合qqq和tqqq下的收益矩阵

for(let ii = 1; ii < 10; ii++){

    for(let qqq = 2; qqq < 10; qqq++){
        const tqqq = 10 - qqq;
        const profit = (qqq * ii * 0.1) + (tqqq * ii * 0.3);
        console.log(`qqq:${qqq} tqqq:${tqqq} change:${(ii*0.1*100).toFixed(3)}% increase:${(profit*10).toFixed(3)}%`)
    }
    console.log();
}
