import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 将 util.py 所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 计算 Bollinger Bands
def calculate_bollinger_bands(df, window=20):
    df['SMA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * 2)
    df['Lower Band'] = df['SMA'] - (df['STD'] * 2)
    return df

# 找出连续超过 Bollinger 上轨线的周
def find_bollinger_breakouts(df):
    df['Above Upper'] = df['Close'] > df['Upper Band']
    breakout_dates = df[df['Above Upper']].index
    return breakout_dates

# 统计下一周的表现
def analyze_post_breakout_performance(df, breakout_dates):
    results = []
    for date in breakout_dates:
        start_index = df.index.get_loc(date)
        if start_index + 1 < len(df):
            start_price = df.iloc[start_index]['Close']
            end_price = df.iloc[start_index + 1]['Close']
            performance = (end_price - start_price) / start_price * 100
            results.append(performance)
    return pd.Series(results)

# 主程序
def main(symbol, days):
    filename = f"{symbol}.csv"
    data = _util.load_csv_as_dataframe_v2(filename)
    data = data[data.index >= '1950-01-01']

    # 将数据重新采样为周数据
    data = data.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Adj Close': 'last'
    })

    data = calculate_bollinger_bands(data)
    breakout_dates = find_bollinger_breakouts(data)
    performances = analyze_post_breakout_performance(data, breakout_dates)

    # 打印结果
    breakout_dates_str = "\n".join([str(i) for i in breakout_dates])
    print(f"Breakout Dates:\n{breakout_dates_str}")
    print(f"Performances after {days} trading days:\n{performances.describe()}")

    # 可视化结果
    plt.figure(figsize=(14, 7))
    sns.histplot(performances, bins=20, kde=True, edgecolor='k', alpha=0.7)
    plt.title(f'Distribution of {symbol} Performance the Week After Bollinger Breakouts')
    plt.xlabel('Performance (%)')
    plt.ylabel('Frequency')
    plt.show(block=True)


if __name__ == "__main__":
    # 参数化的符号和天数
    symbol = '^SPX'  # 你可以在这里更改符号
    days = 1  # 设置为1以表示下一周的表现
    # 改成周级别，统计超出upper那周之后。下一周的表现
    main(symbol, days)
