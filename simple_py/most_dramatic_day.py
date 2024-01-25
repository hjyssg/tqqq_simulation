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
df['Percent_Change'] =  df['Close'].pct_change() * 100 #(df['Adj Close'] - df['Open']) / df['Open'] * 100

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
# 2008-10-13       11.580037
# 2008-10-28       10.789006
# 2020-03-24        9.382774
# 2020-03-13        9.287125
# 1987-10-21        9.099355
# 2009-03-23        7.075755
# 2020-04-06        7.033132
# 2008-11-13        6.921271
# 2008-11-24        6.472253
# 2009-03-10        6.366302
# 2008-11-21        6.324760
# 2020-03-26        6.241416
# 2020-03-17        5.995485
# 2002-07-24        5.732729
# 2022-11-10        5.543448
# 2008-09-30        5.417467
# 2002-07-29        5.407813
# 1987-10-20        5.332684
# 2008-12-16        5.136027
# 1997-10-28        5.115222
# 1998-09-08        5.089898
# 2001-01-03        5.009861
# 2018-12-26        4.959374
# 2020-03-10        4.939631
# 1987-10-29        4.925414
# 2008-10-20        4.768490
# 2000-03-16        4.764604
# 1982-08-17        4.755505
# 2011-08-09        4.740685

# 历史中下跌变动百分比最大的日期，前30天:
# Date  Percent_Change
# 1987-10-19      -20.466931
# 2020-03-16      -11.984055
# 2020-03-12       -9.511268
# 2008-10-15       -9.034978
# 2008-12-01       -8.929524
# 2008-09-29       -8.806776
# 1987-10-26       -8.278947
# 2008-10-09       -7.616710
# 2020-03-09       -7.596970
# 1997-10-27       -6.865684
# 1998-08-31       -6.801408
# 1988-01-08       -6.768304
# 2008-11-20       -6.712293
# 2011-08-08       -6.663446
# 1989-10-13       -6.117229
# 2008-11-19       -6.115558
# 2008-10-22       -6.101247
# 2020-06-11       -5.894406
# 2000-04-14       -5.827794
# 2008-10-07       -5.739484
# 2009-01-20       -5.281610
# 2008-11-05       -5.267709
# 2008-11-12       -5.189390
# 2020-03-18       -5.183076
# 1987-10-16       -5.159681
# 2008-11-06       -5.026398
# 2001-09-17       -4.921560
# 2009-02-10       -4.912120
# 2020-03-11       -4.886844
# 1986-09-11       -4.808551


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