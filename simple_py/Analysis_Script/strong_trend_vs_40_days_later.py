import pandas as pd
import os

# 找出所有40个交易日内涨幅超过10%的区间。
# 并且统计那之后10个交易日的涨跌百分比。


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
df = _util.load_csv_as_dataframe("^NDX.csv")

# # 找出所有40个交易日内涨幅
window_size = 40
# # 统计之后10个交易日的涨跌百分比
days_after = 10

# 初始化 'range_change' 列和 'Future_Return' 列
df['range_change'] = 0.0
df['Future_Return'] = 0.0

# 循环计算 'range_change'
for i in range(window_size, len(df)):
    current_row = df.iloc[i]
    past_row = df.iloc[i - window_size]
    range_change = (current_row['Adj Close'] / past_row['Adj Close'] - 1) * 100
    df.iloc[i, df.columns.get_loc('range_change')] = range_change

# 循环计算 'Future_Return'
for i in range(len(df) - days_after):
    current_row = df.iloc[i]
    future_row = df.iloc[i + days_after]
    future_return = (future_row['Adj Close'] / current_row['Adj Close'] - 1) * 100
    df.iloc[i, df.columns.get_loc('Future_Return')] = future_return

# 过滤
df = df[df['range_change'].notna() & df['Future_Return'].notna()]
# 收益率大于
gain_pct = 10
significant_returns = df[df['range_change'] > gain_pct].reset_index()


# 打印结果
# print(f"所有{window_size}个交易日内涨幅超过{days_after}%的区间:")
# print(significant_returns[['Date', 'range_change', "Future_Return"]])
print(significant_returns[["Future_Return"]].describe())

# output_file_path = 'output_file.csv'
# significant_returns[['Date', 'range_change', "Future_Return"]].to_csv(output_file_path, index=False)

# -----------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# 绘制10个交易日的涨跌百分比分布直方图
plt.figure(figsize=(10, 6))
sns.histplot(significant_returns['Future_Return'].dropna(), bins=30, kde=True, color='skyblue')
plt.title(f' {days_after} days after a gain of more than {gain_pct}% within a {window_size}-day period')
plt.xlabel('Future Return (%)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

print("------------")