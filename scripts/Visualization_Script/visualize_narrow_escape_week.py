import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
import numpy as np

fn = "^NDX.csv"
data = _util.load_csv_as_dataframe(fn)

# 找出有惊无险的周。

# 将 'Date' 列转换为日期时间类型，并设置为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 根据周来重采样数据，计算每周的第一个开盘价和最后一个收盘价
weekly_data = data.resample('W-MON').agg({'Open': 'first', 'Close': 'last'})

# 重采样以找到每周的最低价
weekly_data['weekly_low'] = data['Low'].resample('W-MON').min()

# 计算从周一开盘到周中任何一天的最低价的最大跌幅百分比
weekly_data['max_weekly_drop'] = ((weekly_data['weekly_low'] - weekly_data['Open']) / weekly_data['Open']) * 100

# 计算每周的最终涨幅百分比
weekly_data['weekly_change'] = ((weekly_data['Close'] - weekly_data['Open']) / weekly_data['Open']) * 100

# 筛选条件：周内最大跌幅超过2%，周的最终涨幅在0.5%到1.5%之间
# filtered_weeks = weekly_data[  (weekly_data['max_weekly_drop'] >= -4) & 
#                     (weekly_data['max_weekly_drop'] < -2) & 
#                      (weekly_data['weekly_change'] >= 0.5) & 
#                      (weekly_data['weekly_change'] <= 1.5)]

filtered_weeks = weekly_data[  (weekly_data['max_weekly_drop'] >= -4) & 
                    (weekly_data['max_weekly_drop'] < -2) & 
                     (weekly_data['weekly_change'] >= 0.5) ]

# 打印结果
# print(filtered_weeks)

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_later_performance():
    # 计算满足条件周后20周的涨跌幅
    target_changes = []
    for date in filtered_weeks.index:
        if date + pd.DateOffset(weeks=20) in weekly_data.index:
            initial_close = weekly_data.loc[date, 'Close']
            future_close = weekly_data.loc[date + pd.DateOffset(weeks=20), 'Close']
            change = ((future_close - initial_close) / initial_close) * 100
            target_changes.append(change)

    # 随机选择20周期间计算涨跌幅
    random_changes = []
    for _ in range(200):  # 生成100个随机20周期间的涨跌幅数据
        random_start = np.random.randint(0, len(weekly_data) - 20)
        initial_close = weekly_data.iloc[random_start]['Close']
        future_close = weekly_data.iloc[random_start + 20]['Close']
        change = ((future_close - initial_close) / initial_close) * 100
        random_changes.append(change)

    # 使用Seaborn绘制两组数据的直方图和KDE
    # plt.figure(figsize=(12, 6))
    # sns.histplot(target_changes, kde=True, color='blue', label='Specific Criteria 20-Week Changes', binwidth=2)
    # sns.histplot(random_changes, kde=True, color='red', label='Random 20-Week Changes', binwidth=2)
    # plt.title('Comparison of 20-Week Price Changes')
    # plt.xlabel('Percentage Change')
    # plt.ylabel('Frequency')
    # plt.legend()
    # plt.show()

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12), gridspec_kw={'hspace': 0.3})
    sns.histplot(target_changes, kde=True, color='blue', label='Specific Criteria 20-Week Changes', binwidth=2, ax=axes[0])
    axes[0].set_title('周中跌最后收涨的周的后续表现')
    axes[0].set_xlabel('Percentage Change')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()
    # 设置x轴的详细刻度
    axes[0].set_xticks(np.arange(min(target_changes), max(target_changes)+1, 5))

    sns.histplot(random_changes, kde=True, color='red', label='Random 20-Week Changes', binwidth=2, ax=axes[1])
    axes[1].set_title('随便挑的周的后续表现')
    axes[1].set_xlabel('Percentage Change')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    # 设置x轴的详细刻度
    axes[1].set_xticks(np.arange(min(random_changes), max(random_changes)+1, 5))

    plt.tight_layout()
    plt.show()

visualize_later_performance()

# 
# 画出每个年份发生这种周的次数，没有的周也要显示在x轴
def plot_by_year():
    # 按年统计满足条件的周的数量
    annual_counts = filtered_weeks.resample('Y').size()

    # 将年份格式化为YYYY格式
    annual_counts.index = annual_counts.index.year

    # 获取数据涵盖的所有年份
    all_years = range(annual_counts.index.min(), annual_counts.index.max() + 1)

    # 创建一个新的Series，确保每个年份都有数据，没有数据的年份用0填充
    full_annual_counts = pd.Series(index=all_years).fillna(0).add(annual_counts, fill_value=0)

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    full_annual_counts.plot(kind='bar', color='skyblue')
    plt.title('有惊无险周')
    plt.xlabel('Year')
    plt.ylabel('Number of Weeks')
    plt.grid(True)
    plt.show()
