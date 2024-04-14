import pandas as pd
import os
import numpy as np
# 统计年初几个月和全年表现得关系
import os
import sys
# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")

data = data[data['Date'].dt.year > 1950]

result = []  # 用于存储结果的列表

for year in range(data['Date'].dt.year.min(), data['Date'].dt.year.max() + 1):
    yearly_data = data[data['Date'].dt.year == year]  # 筛选出该年份的数据
    begin_data = yearly_data[yearly_data['Date'].dt.month.isin([1, 2, 3])]  # 筛选出1月、2月和3月的数据
    if not begin_data.empty:
        start_price = begin_data.iloc[0]['Open']  # 全年的起始价格
        if start_price == 0:
            start_price = begin_data.iloc[0]['Close']  # 全年的起始价格


        end_price = begin_data.iloc[-1]['Close']  # 结束价格
        begin_growth = ((end_price - start_price) / start_price) * 100  # 计算1月、2月和3月的涨幅
        
        end_year_price = yearly_data.iloc[-1]['Close']  # 全年的结束价格
        yearly_growth = ((end_year_price - start_price) / start_price) * 100  # 计算全年的涨幅
        result.append((year, begin_growth, yearly_growth))  # 添加到结果列表

        print((year, begin_growth, yearly_growth) )
    else:
        print(year)

# 帮我用scatter，x是begin_growth， y是yearly_growth。
import matplotlib.pyplot as plt

# 分别提取年份、年初涨幅和全年涨幅
years, begin_growths, yearly_growths = zip(*result)

# plt.figure(figsize=(10, 6))  # 设置图形大小
# plt.scatter(begin_growths, yearly_growths)  # 创建散点图

# plt.title('Yearly Start vs. Yearly Growth')  # 设置标题
# plt.xlabel('Begin Growth (%)')  # 设置x轴标签
# plt.ylabel('Yearly Growth (%)')  # 设置y轴标签

# # 在每个点旁边添加年份标签
# for i, year in enumerate(years):
#     plt.text(begin_growths[i], yearly_growths[i], str(year))

# plt.grid(True)  # 显示网格
# plt.show()  # 显示图形


# 计算线性回归拟合
coefficients = np.polyfit(begin_growths, yearly_growths, 1)
polynomial = np.poly1d(coefficients)

plt.figure(figsize=(10, 6))  # 设置图形大小
plt.scatter(begin_growths, yearly_growths)  # 创建散点图

# 绘制多项式回归曲线
x_values = np.linspace(min(begin_growths), max(begin_growths), 100)
y_values = polynomial(x_values)
plt.plot(x_values, y_values, color='red', linestyle='-')


plt.title('Yearly Start vs. Yearly Growth')  # 设置标题
plt.xlabel('Begin Growth (%)')  # 设置x轴标签
plt.ylabel('Yearly Growth (%)')  # 设置y轴标签

# 在每个点旁边添加年份标签
for i, year in enumerate(years):
    plt.text(begin_growths[i], yearly_growths[i], str(year))

plt.grid(True)  # 显示网格
plt.show()  # 显示图形