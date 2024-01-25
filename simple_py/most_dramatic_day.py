import pandas as pd
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data/1927年开始得^SPX.csv')
df = pd.read_csv(file_path)

# 将日期列转换为datetime类型
df['Date'] = pd.to_datetime(df['Date'])

# 选择1970年及之后的数据
# df = df[df['Date'] >= pd.to_datetime('1970-01-01')].reset_index(drop=True)
df = df[(df['Date'] >= pd.to_datetime('1970-01-01')) & (df['Open'] != 0)].reset_index(drop=True)



# 计算每天的open和close相对于同一天的百分比变化
df['Percent_Change'] = (df['Adj Close'] - df['Open']) / df['Open'] * 100

n_day = 30
# 找出历史中close变动百分比最大的日期，前30天
max_change_date = df.nlargest(n_day, 'Percent_Change')
print("\n历史中上涨变动百分比最大的日期，前30天:")
print(max_change_date[["Date", "Percent_Change"]])

# --------------------- 下跌前20
min_change_date = df.nsmallest(n_day, 'Percent_Change')
print("\n历史中下跌变动百分比最大的日期，前30天:")
print(min_change_date[["Date", "Percent_Change"]])


# 历史中上涨变动百分比最大的日期，前30天:
# Date  Percent_Change
# 2008-10-28       10.789006
# 2008-10-13        9.926045
# 1987-10-21        9.099355
# 2008-11-13        6.817246
# 2009-03-23        6.553066
# 2008-11-24        6.316773
# 2009-03-10        5.935689
# 2008-11-21        5.846476
# 2002-07-24        5.731402
# 2020-03-13        5.487571
# 2002-07-29        5.407813
# 1987-10-20        5.229718
# 2020-03-26        5.148544
# 1997-10-28        5.115222
# 1998-09-08        5.089898
# 2001-01-03        5.009861
# 1987-10-29        4.911922
# 2008-12-16        4.778948
# 2000-03-16        4.763851
# 2002-10-15        4.733554

# 历史中下跌变动百分比最大的日期，前30天:
# Date  Percent_Change
# 1987-10-19      -20.466931
# 2008-10-15       -8.723100
# 2008-09-29       -8.489989
# 1987-10-26       -8.271555
# 2008-12-01       -8.147552
# 2008-10-09       -7.941968
# 1997-10-27       -6.865684
# 1998-08-31       -6.801408
# 1988-01-08       -6.761155
# 2008-11-20       -6.630101
# 2011-08-08       -6.593353
# 1989-10-13       -6.117229
# 2008-11-19       -6.105725
# 2000-04-14       -5.827794
# 2008-10-07       -5.802761
# 2008-10-22       -5.767751
# 2020-03-12       -5.709928
# 2009-01-20       -5.228102
# 2020-03-20       -5.222992
# 1987-10-16       -5.159681


# 提取年份信息
max_change_date['Year'] = max_change_date['Date'].dt.year
min_change_date['Year'] = min_change_date['Date'].dt.year

# 统计每年的次数
max_change_counts = max_change_date['Year'].value_counts().sort_index()
min_change_counts = min_change_date['Year'].value_counts().sort_index()

print(max_change_counts)
print(min_change_counts)


# 可视化
# plt.figure(figsize=(10, 6))
# plt.bar(max_change_counts.index, max_change_counts, label='Largest upward percentage change')
# plt.bar(min_change_counts.index, min_change_counts, label='Largest downward percentage change')
# plt.xlabel('Year')
# plt.ylabel('Count')
# plt.title('Yearly Counts of Dates with the Largest Upward and Downward Percentage Changes')
# plt.legend()
# plt.show()

# 创建两个子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# 绘制上涨变动百分比最大的日期年份次数统计
ax1.bar(max_change_counts.index, max_change_counts, label='Largest upward percentage change')
ax1.set_ylabel('Count')
ax1.set_title('Yearly Counts of Dates with the Largest Upward Percentage Changes')
ax1.set_xlim(1980, max_change_counts.index.max())  # 设置x轴范围

# 绘制下跌变动百分比最大的日期年份次数统计
ax2.bar(min_change_counts.index, min_change_counts, label='Largest downward percentage change', color='orange')
ax2.set_xlabel('Year')
ax2.set_ylabel('Count')
ax2.set_title('Yearly Counts of Dates with the Largest Downward Percentage Changes')
ax2.set_xlim(1980, max_change_counts.index.max())  # 设置x轴范围


# 调整布局
plt.tight_layout()
plt.show()


# 感想
# 熊市波动剧烈，无论上下。
# 深刻地感受到当时2008年股市的波动

print("--------")