"""
用python写脚本。
假设现在我一年花20万，年平均通货膨胀率是2.2%（中国的cpi平均值）
我的资产每年收益率是10%，（SPY的平均年回报）现在资产是300万
接下来是40年，每年我不工作进行消费，那么40年后我的资产是多少？
假设值全部用大写字母表示，如INITIAL_EXPENSE表示初始花费。
可视化资产、花费随时间的变化。
"""

import numpy as np
import matplotlib.pyplot as plt



# 定义变量
INITIAL_ASSET = 300  # 初始资产 单位   万元
INITIAL_EXPENSE = 20  # 初始花费 单位   万元
INFLATION_RATE = 0.022  # 年通货膨胀率
RETURN_RATE = 0.1  # 年资产收益率
YEARS = 40  # 模拟时间，单位：年

# 初始化资产和花费数组
assets = [INITIAL_ASSET]
expenses = [INITIAL_EXPENSE]

# 模拟40年内的资产变化
for year in range(1, YEARS + 1):
    # 每年资产收益
    new_asset = assets[-1] * (1 + RETURN_RATE) - expenses[-1]
    # 每年花费增长
    new_expense = expenses[-1] * (1 + INFLATION_RATE)
    
    # 记录新的资产和花费
    assets.append(new_asset)
    expenses.append(new_expense)

# 输出CSV文件
import csv
with open('资产和花费变化.csv', mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['年份', '资产', '花费'])
    for year in range(YEARS + 1):
        writer.writerow([year, assets[year], expenses[year]])

print("资产和花费数据已保存为 '资产和花费变化.csv'")

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 画图
plt.figure(figsize=(10, 6))
plt.plot(range(YEARS + 1), assets, label="资产", color='b')
plt.plot(range(YEARS + 1), expenses, label="花费", color='r', linestyle='--')

# 标注图表
plt.title('40年后的资产和花费变化')
plt.xlabel('年份')
plt.ylabel('金额 (万元)')
plt.legend()
plt.grid(True)

# 显示图表
plt.show()

# 输出40年后的资产
print(f"40年后的资产为: {assets[-1]:,.2f}万元")


