import pandas as pd
import os
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("NVDA.csv")  # data is dataframe

# 筛选出2023年1月1日及之后的数据
data = data[data['Date'].dt.year > 2022]

# 计算每日的涨跌幅百分比，使用 pct_change()
data['跌幅百分比'] = data['Close'].pct_change() * 100

# 去掉数据的空值（因为pct_change会导致第一行出现NaN）
data = data.dropna(subset=['跌幅百分比'])

# 按照跌幅百分比降序排列，取前十名（跌幅为负值即为下跌）
top_10_drops = data[['Date', '跌幅百分比']].sort_values(by='跌幅百分比', ascending=True).head(10)

# 输出前十大跌幅
print("2023年1月起最大单日跌幅前十名：")
print(top_10_drops)

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
