import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")

# 设置 'Date' 列为索引
data.set_index('Date', inplace=True)

# 将数据按月重新取样
monthly_data = data.resample('M').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Adj Close': 'last', 'Volume': 'sum'})

# 计算每个月的涨跌情况
monthly_data['Up'] = monthly_data['Close'] > monthly_data['Open']

# 统计每个月的上涨和下跌次数
monthly_stats = monthly_data.groupby(monthly_data.index.month)['Up'].value_counts().unstack().fillna(0)



# 计算每个月的上涨和下跌概率
monthly_stats['Total'] = monthly_stats[True] + monthly_stats[False]
monthly_stats['Up Probability'] = monthly_stats[True] / monthly_stats['Total']
monthly_stats['Down Probability'] = monthly_stats[False] / monthly_stats['Total']

# 打印结果
print("每个月的上涨和下跌次数及概率：")
print(monthly_stats[[ 'Up Probability', 'Down Probability']])


#-----------------
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
plt.bar(monthly_avg_increase_df['Month'], monthly_avg_increase_df['Average Increase'], color='skyblue')
plt.xlabel('Month')
plt.ylabel('Average Increase Percentage')
plt.title('Average Monthly Increase Percentage')
plt.xticks(range(1, 13))  # 设置x轴刻度为月份
plt.grid(axis='y')  # 显示水平网格线
plt.show()


# 每个月的上涨和下跌次数及概率：
# Up    Up Probability  Down Probability
# Date
# 1           0.653846          0.346154
# 2           0.490566          0.509434
# 3           0.603774          0.396226
# 4           0.679245          0.320755
# 5           0.584906          0.415094
# 6           0.547170          0.452830
# 7           0.584906          0.415094
# 8           0.547170          0.452830
# 9           0.547170          0.452830
# 10          0.547170          0.452830
# 11          0.698113          0.301887
# 12          0.547170          0.452830
# 每个月的平均涨幅百分比：
# 1月的平均涨幅百分比为: 2.31%
# 2月的平均涨幅百分比为: 0.36%
# 3月的平均涨幅百分比为: 0.67%
# 4月的平均涨幅百分比为: 1.58%
# 5月的平均涨幅百分比为: 0.93%
# 6月的平均涨幅百分比为: 0.72%
# 7月的平均涨幅百分比为: 0.88%
# 8月的平均涨幅百分比为: 0.20%
# 9月的平均涨幅百分比为: -0.93%
# 10月的平均涨幅百分比为: 0.68%
# 11月的平均涨幅百分比为: 1.90%
# 12月的平均涨幅百分比为: 1.40%