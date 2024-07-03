import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
fn = "^SPX.csv"
data = _util.load_csv_as_dataframe(fn)
data = data[data["Date"].dt.year > 1950]

# 设置 'Date' 列为索引
data.set_index('Date', inplace=True)

# 将数据按月重新取样
monthly_data = data.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Adj Close': 'last', 'Volume': 'sum'})


# 如果open是0或者null，使用第一个close
monthly_data['Open'] = monthly_data.apply(
    lambda row: row['Close'] if pd.isnull(row['Open']) or row['Open'] == 0 else row['Open'], axis=1
)


# 计算每个月的涨幅百分比
monthly_data['Increase Percentage'] = ((monthly_data['Close'] - monthly_data['Open']) / monthly_data['Open']) * 100


# 计算每个月的平均涨幅百分比
monthly_avg_increase = {}
for month in range(1, 13):
    month_data = monthly_data[monthly_data.index.month == month]
    monthly_avg_increase[month] = month_data['Increase Percentage'].mean()

# 打印每个月的平均涨幅百分比
print("每个月的平均涨幅百分比：")
for month, avg_increase in monthly_avg_increase.items():
    print(f"{month}月的平均涨幅百分比为: {avg_increase:.2f}%")

import matplotlib.pyplot as plt

monthly_avg_increase_df = pd.DataFrame(list(monthly_avg_increase.items()), columns=['Month', 'Average Increase'])

# 绘制每个月的平均涨幅百分比
plt.figure(figsize=(10, 6))
bars = plt.bar(monthly_avg_increase_df['Month'], monthly_avg_increase_df['Average Increase'], color='skyblue')
plt.xlabel('Month')
plt.ylabel('Average Increase Percentage')
plt.title(f'{fn} Montyly Return')
plt.xticks(range(1, 13))  # 设置x轴刻度为月份
plt.grid(axis='y')  # 显示水平网格线

# 在每个bar上显示monthly return
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}%', ha='center', va='bottom')

plt.show()


# 1月的平均涨幅百分比为: 0.71% 
# 2月的平均涨幅百分比为: 0.07% 
# 3月的平均涨幅百分比为: 0.86% 
# 4月的平均涨幅百分比为: 1.10% 
# 5月的平均涨幅百分比为: 0.63% 
# 6月的平均涨幅百分比为: 0.36% 
# 7月的平均涨幅百分比为: 1.11% 
# 8月的平均涨幅百分比为: -0.12%
# 9月的平均涨幅百分比为: -0.76%
# 10月的平均涨幅百分比为: 0.71%
# 11月的平均涨幅百分比为: 1.40%
# 12月的平均涨幅百分比为: 1.14%


