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

# 统计超出 Bollinger 上轨的频率
def count_above_upper_band(df):
    df['Above Upper'] = df['Close'] > df['Upper Band']
    count = df['Above Upper'].sum()
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
    count, frequency = count_above_upper_band(resampled_df)
    return count, frequency, resampled_df

# 主程序
def main(filepath, window=20):
    data = _util.load_csv_as_dataframe_v2(filepath)
    
    # 过滤数据，只保留1950年之后的
    data = data[data.index >= '1950-01-01']

    # 计算并统计日线超出上轨频率
    daily_data = calculate_bollinger_bands(data, window)
    daily_count, daily_frequency = count_above_upper_band(daily_data)
    print(f"日线超出Bollinger上轨次数: {daily_count}, 频率: {daily_frequency:.2%}")

    # 计算并统计周线超出上轨频率
    weekly_count, weekly_frequency, weekly_data = resample_and_calculate(data, 'W', window)
    print(f"周线超出Bollinger上轨次数: {weekly_count}, 频率: {weekly_frequency:.2%}")

    # 计算并统计月线超出上轨频率
    monthly_count, monthly_frequency, monthly_data = resample_and_calculate(data, 'M', window)
    print(f"月线超出Bollinger上轨次数: {monthly_count}, 频率: {monthly_frequency:.2%}")


if __name__ == "__main__":
    filepath = "^SPX.csv"  # 替换为你的CSV文件路径
    main(filepath)


# "^NDX.csv"
# 日线超出Bollinger上轨次数: 531, 频率: 5.44%
# 周线超出Bollinger上轨次数: 159, 频率: 7.87%
# 月线超出Bollinger上轨次数: 50, 频率: 10.75%

# "^SPX.csv"
# 日线超出Bollinger上轨次数: 927, 频率: 4.95%
# 周线超出Bollinger上轨次数: 211, 频率: 5.43%
# 月线超出Bollinger上轨次数: 75, 频率: 8.39%


# 纯数学问题，如果分布是正态分布。超出的概率是多少
# 如果某个变量服从正态分布，那么该变量超出±2标准差范围的总概率是4.55%。
# 单侧超出±2标准差的概率是2.28%。


# fat-tailed distribution
# 金融数据确实具有厚尾（fat tails）的特点，这与标准正态分布有所不同。厚尾分布意味着在分布的两端，即极端值出现的频率比正态分布预期的更高。以下是厚尾现象及其在金融数据中的体现和影响的详细解释。
# 厚尾分布（Fat Tails）
# 定义
# 在统计学中，厚尾分布指的是与标准正态分布相比，分布尾部有更多的概率质量。这意味着在厚尾分布中，极端事件（如极大的收益或亏损）比在正态分布中发生的频率更高。