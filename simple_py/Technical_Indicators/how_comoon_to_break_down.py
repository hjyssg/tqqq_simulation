import pandas as pd
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

# 统计突破 Bollinger 下轨的频率
def count_below_lower_band(df):
    df['Below Lower'] = df['Close'] < df['Lower Band']
    count = df['Below Lower'].sum()
    total = len(df)
    frequency = count / total
    return count, frequency

# 重新采样并计算频率
def resample_and_calculate(df, freq, window=20):
    resampled_df = df.resample(freq).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Adj Close': 'last'
    })
    resampled_df = calculate_bollinger_bands(resampled_df, window)
    count, frequency = count_below_lower_band(resampled_df)
    return count, frequency, resampled_df

# 主程序
def main(filepath, window=20):
    data = _util.load_csv_as_dataframe_v2(filepath)
    
    # 过滤数据，只保留1950年之后的
    data = data[data.index >= '1950-01-01']

    # 计算并统计日线突破下轨频率
    daily_data = calculate_bollinger_bands(data, window)
    daily_count, daily_frequency = count_below_lower_band(daily_data)
    print(f"日线突破Bollinger下轨次数: {daily_count}, 频率: {daily_frequency:.2%}")

    # 计算并统计周线突破下轨频率
    weekly_count, weekly_frequency, weekly_data = resample_and_calculate(data, 'W', window)
    print(f"周线突破Bollinger下轨次数: {weekly_count}, 频率: {weekly_frequency:.2%}")

    # 计算并统计月线突破下轨频率
    monthly_count, monthly_frequency, monthly_data = resample_and_calculate(data, 'M', window)
    print(f"月线突破Bollinger下轨次数: {monthly_count}, 频率: {monthly_frequency:.2%}")


if __name__ == "__main__":
    # filepath = "^SPX.csv"  # 替换为你的CSV文件路径
    filepath = "^NDX.csv"  # 替换为你的CSV文件路径
    main(filepath)


# "^SPX.csv"
# 日线突破Bollinger下轨次数: 908, 频率: 4.85%
# 周线突破Bollinger下轨次数: 141, 频率: 3.63%
# 月线突破Bollinger下轨次数: 30, 频率: 3.36%

# "^NDX.csv"
# 日线突破Bollinger下轨次数: 422, 频率: 4.33%
# 周线突破Bollinger下轨次数: 49, 频率: 2.43%
# 月线突破Bollinger下轨次数: 5, 频率: 1.08%