# verify_boll_day_level.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 计算Bollinger Bands
def calculate_bollinger_bands(df, window=20):
    df['SMA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower Band'] = df['SMA'] - (df['STD'] * 2)
    return df

# 找出连续超过Bollinger上轨线3天的日期
def find_bollinger_breakouts(df):
    df['Above Upper'] = df['Close'] > df['Upper Band']
    breakout_dates = df[df['Above Upper']].index
    consecutive_breakouts = []

    for i in range(len(breakout_dates) - 2):
        if (breakout_dates[i+1] - breakout_dates[i] == pd.Timedelta(days=1)) and \
           (breakout_dates[i+2] - breakout_dates[i+1] == pd.Timedelta(days=1)):
            consecutive_breakouts.append(breakout_dates[i+2])
    
    return consecutive_breakouts

# 统计之后指定天数的结果
def analyze_post_breakout_performance(df, breakout_dates, days):
    results = []
    for date in breakout_dates:
        start_index = df.index.get_loc(date)
        end_index = start_index + days
        if end_index < len(df):
            start_price = df.iloc[start_index]['Close']
            end_price = df.iloc[end_index]['Close']
            performance = (end_price - start_price) / start_price * 100
            results.append(performance)
    return pd.Series(results)

# 主程序
def main(symbol, days):
    filename = f"{symbol}.csv"
    data =  _util.load_csv_as_dataframe_v2(filename)  # get_data(symbol, filename)
    data = data[data.index >= '1950-01-01']
    data = calculate_bollinger_bands(data)
    breakout_dates = find_bollinger_breakouts(data)
    performances = analyze_post_breakout_performance(data, breakout_dates, days)

    # 打印结果
    breakout_dates_str = "\n".join([str(i) for i in breakout_dates])
    print(f"Breakout Dates:\n{breakout_dates_str}")
    print(f"Performances after {days} trading days:\n{performances.describe()}")

    # 可视化结果
    plt.figure(figsize=(14, 7))
    sns.histplot(performances, bins=20, kde=True, edgecolor='k', alpha=0.7)
    plt.title(f'Distribution of {symbol} Performance {days} Days After Bollinger Breakouts')
    plt.xlabel('Performance (%)')
    plt.ylabel('Frequency')
    plt.show(block=True)



if __name__ == "__main__":
    # 参数化的符号和天数
    symbol = '^SPX'  # 你可以在这里更改符号
    days = 10  # 你可以在这里更改天数
    main(symbol, days)


