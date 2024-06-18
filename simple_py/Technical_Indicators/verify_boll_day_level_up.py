# verify_boll_day_level_up.py

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

# 找出连续超过Bollinger上轨线指定天数的日期
def find_bollinger_breakouts(df, consecutive_days=4):
    df['Above Upper'] = df['Close'] > df['Upper Band']
    breakout_dates = df[df['Above Upper']].index
    consecutive_breakouts = []

    for i in range(len(breakout_dates) - consecutive_days + 1):
        is_consecutive = True
        for j in range(consecutive_days - 1):
            if (breakout_dates[i + j + 1] - breakout_dates[i + j]) != pd.Timedelta(days=1):
                is_consecutive = False
                break
        if is_consecutive:
            consecutive_breakouts.append(breakout_dates[i + consecutive_days - 1])
    
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

# 保存每次情况前后30天的股票走势图片
def save_stock_trend_images(df, breakout_dates, days_before=30, days_after=30):
    for date in breakout_dates:
        start_index = df.index.get_loc(date) - days_before
        end_index = df.index.get_loc(date) + days_after

        if start_index >= 0 and end_index < len(df):
            subset = df.iloc[start_index:end_index]
            plt.figure(figsize=(14, 7))
            plt.plot(subset.index, subset['Close'], label='Close Price')
            plt.axvline(x=date, color='r', linestyle='--', label='Breakout Date')
            plt.title(f'Stock Trend {days_before} Days Before and {days_after} Days After Breakout on {date}')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.legend()
            date_str = date.strftime('%Y-%m-%d')
            plt.savefig(f'temp_output\stock_trend_{date_str}.png')
            plt.close()

# 主程序
def main(symbol, days, consecutive_days, save_images=False):
    filename = f"{symbol}.csv"
    data = _util.load_csv_as_dataframe_v2(filename)  # get_data(symbol, filename)
    data = data[data.index >= '1950-01-01']
    data = calculate_bollinger_bands(data)
    breakout_dates = find_bollinger_breakouts(data, consecutive_days)
    performances = analyze_post_breakout_performance(data, breakout_dates, days)

    if save_images:
        save_stock_trend_images(data, breakout_dates)

    # 打印结果
    breakout_dates_str = "\n".join([str(i) for i in breakout_dates])
    print(f"Breakout Dates:\n{breakout_dates_str}")
    print(f"Performances after {days} trading days:\n{performances.describe()}")

    # 可视化结果
    plt.figure(figsize=(14, 7))
    sns.histplot(performances, bins=20, kde=True, edgecolor='k', alpha=0.7)
    plt.title(f'Distribution of {symbol} Performance {days} Days After {consecutive_days}-Day Bollinger Breakouts')
    plt.xlabel('Performance (%)')
    plt.ylabel('Frequency')
    plt.show(block=True)

if __name__ == "__main__":
    # 参数化的符号、天数和连续天数
    symbol = '^SPX'  # 你可以在这里更改符号
    days = 10  # 你可以在这里更改天数
    consecutive_days = 3  # 你可以在这里更改连续天数
    save_images = True  # 设置是否保存图片
    main(symbol, days, consecutive_days, save_images)



