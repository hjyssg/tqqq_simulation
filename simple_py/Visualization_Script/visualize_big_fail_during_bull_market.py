import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 导入数据
df = _util.load_csv_as_dataframe("^NDX.csv")

def visualize_stock_with_drops(df, drop_df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Adj Close'], label='Close Price')
    plt.scatter(drop_df['Date'], drop_df['Adj Close'], color='red', label='Drop > 3.5% Days')

    plt.title('Stock Price with Drops Exceeding 3.5% (1996-01-01 to 2000-01-01)')
    plt.xlabel('Date')
    plt.ylabel('Adj Close Price')
    plt.legend()
    plt.show()

# 将 'Date' 列转换为日期时间类型
df['Date'] = pd.to_datetime(df['Date'])

# 过滤日期范围
df_filtered = df[(df['Date'] >= '1996-01-01') & (df['Date'] <= '2000-01-01')]

# 计算涨跌幅度
df_filtered['Change'] = df_filtered['Adj Close'].pct_change()

# 找出单日下跌超过 3.5% 的日期
drop_dates = df_filtered[df_filtered['Change'] < -0.035]

# 可视化
visualize_stock_with_drops(df_filtered, drop_dates)