import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 导入数据
df = _util.load_csv_as_dataframe("^NDX.csv")

def visualize_stock_with_historical_highs(df, historical_high_df):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')  # 使用对数刻度
    plt.plot(df['Date'], df['Adj Close'], label='Close Price')
    plt.scatter(historical_high_df['Date'], historical_high_df['Historical_High'], color='red', label='Historical High')

    # 控制 Y 轴上标签的数量
    plt.yticks([100, 250, 500, 1000, 2000, 5000, 10000], ['100', "250", '500', '1000', '2000', '5000', '10000'])

    plt.title('Stock Price with Historical High Points')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

def calculate_days_between_ath(historical_high_df):
    historical_high_df['Date'] = pd.to_datetime(historical_high_df['Date'])
    historical_high_df['Days_Between'] = historical_high_df['Date'].diff().dt.days
    return historical_high_df[['Date', 'Historical_High', 'Days_Between']]

def visualize_ath_intervals(historical_high_df_with_intervals):
    historical_high_df_with_intervals['Year'] = historical_high_df_with_intervals['Date'].dt.year
    yearly_intervals = historical_high_df_with_intervals.groupby('Year')['Days_Between'].mean().dropna()

    threshold = yearly_intervals.quantile(0.95)
    yearly_intervals = yearly_intervals[yearly_intervals < threshold]

    plt.figure(figsize=(10, 6))
    plt.bar(yearly_intervals.index, yearly_intervals.values, color='blue')
    plt.title('Average Days Between All-Time Highs by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Days Between ATH')
    plt.show()

# 初始化变量，用于跟踪前最高点
previous_high_price = df['Adj Close'][0]

# 存储历史高点的数据
historical_high_points = {'Date': [], 'Historical_High': []}

# 逐步迭代数据，找到每个数据点相对于之前所有数据的最高点
for index, row in df.iterrows():
    if row['Adj Close'] > previous_high_price:
        # 当前数据点的收盘价高于之前的最高点
        previous_high_price = row['Adj Close']

        # 存储历史高点的数据
        historical_high_points['Date'].append(row['Date'])
        historical_high_points['Historical_High'].append(previous_high_price)

# 转换历史高点数据为 DataFrame
historical_high_df = pd.DataFrame(historical_high_points)

# 计算刷新历史高点的间隔天数
historical_high_df_with_intervals = calculate_days_between_ath(historical_high_df)
print(historical_high_df_with_intervals)

# 可视化每年刷新历史高点的间隔天数
visualize_ath_intervals(historical_high_df_with_intervals)

# 可视化
visualize_stock_with_historical_highs(df, historical_high_df)
