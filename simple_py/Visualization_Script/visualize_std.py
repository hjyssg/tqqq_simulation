import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util
df = _util.load_csv_as_dataframe("^NDX.csv")

df = df[(df['Date'] >= pd.to_datetime('1970-01-01')) & (df['Close'] != 0)].reset_index(drop=True)

# 提取年份并添加到数据框中
df['Year'] = df['Date'].dt.year

# 计算每日收益率
df['Daily_Return'] = df['Close'].pct_change()

# 提取年份并添加到数据框中
df['Year'] = df['Date'].dt.year

# 计算每年的波动率（使用收益率的标准差）
volatility_by_year = df.groupby('Year')['Daily_Return'].std()

# 找到波动率最大的前10个年份
top_volatility_years = volatility_by_year.nlargest(20).index

# 可视化每年的波动率，并标红最大的前10个年份
plt.figure(figsize=(10, 6))
colors = ['red' if year in top_volatility_years else 'skyblue' for year in volatility_by_year.index]
volatility_by_year.plot(kind='bar', color=colors)
plt.title('Annual Volatility of Daily Returns')
plt.xlabel('Year')
plt.ylabel('Volatility')
plt.show()