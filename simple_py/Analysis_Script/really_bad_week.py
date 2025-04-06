# ----------------------------------------------------------
# 脚本功能：
# 分析股票数据，找出每周下跌超过8%的情况，并查看接下来一个交易周的周一涨跌幅。
# 输出包括：
# - 每个大跌周的结束日期和跌幅
# - 下一周周一的开盘和收盘涨跌幅（相对于上周五）
# - 输出结果为 CSV 文件
# - 绘制下一周周一收盘涨跌幅的分布直方图
# ----------------------------------------------------------

import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# 固定导入方式，导入自定义的 _util 模块加载数据
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 加载数据
data = _util.load_csv_as_dataframe("^SPX.csv")  # 返回一个 DataFrame

# 日期格式转换，并设置为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
data = data.sort_index()  # 确保时间顺序

# 每周重采样，按周五（W-FRI）聚合数据
weekly = data.resample('W-FRI').agg({
    'Open': 'first',        # 一周的第一个交易日开盘价
    'High': 'max',          # 一周最高价
    'Low': 'min',           # 一周最低价
    'Close': 'last',        # 一周收盘价（周五）
    'Adj Close': 'last',    # 一周调整收盘价
    'Volume': 'sum'         # 一周成交量
})

# 计算每周的收盘涨跌幅（相对上周）
weekly['pct_change'] = weekly['Close'].pct_change()

# 筛选出下跌超过 8% 的周
big_drop_weeks = weekly[weekly['pct_change'] < -0.08]

results = []

# 遍历每个下跌周，分析其后一周周一的表现
for drop_date in big_drop_weeks.index:
    week_start = drop_date - pd.Timedelta(days=4)  # 当前周的周一（用于参考）
    week_data = data[week_start:drop_date]         # 当前周的完整数据（可选）

    # 获取下一周的周一（+3天）
    next_monday = drop_date + pd.Timedelta(days=3)
    if next_monday not in data.index:
        continue  # 如果那天不是交易日，跳过

    monday_data = data.loc[next_monday]
    prev_close = weekly.loc[drop_date, 'Close']

    # 计算开盘涨跌幅（相对于上周五收盘）
    open_pct = (monday_data['Open'] - prev_close) / prev_close * 100
    # 计算收盘涨跌幅（相对于上周五收盘）
    close_pct = (monday_data['Close'] - prev_close) / prev_close * 100

    results.append({
        'Drop Week End': drop_date.strftime('%Y-%m-%d'),
        'Drop %': weekly.loc[drop_date, 'pct_change'] * 100,
        'Next Monday': next_monday.strftime('%Y-%m-%d'),
        'Monday Open %': open_pct,
        'Monday Close %': close_pct
    })

# 将结果转换为 DataFrame 并导出为 CSV 文件
result_df = pd.DataFrame(results)
result_df.to_csv('drop_weeks_next_monday.csv', index=False)

print(result_df["Monday Open %"].describe())

# 绘制下一周周一收盘涨跌幅的分布直方图
plt.figure(figsize=(10,6))
plt.hist(result_df['Monday Close %'], bins=20, edgecolor='black')
plt.title('Next Monday Close % After >8% Weekly Drop')
plt.xlabel('Monday Close %')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('monday_close_pct_histogram.png')
plt.show()

# 防止运行后窗口直接关闭
input()
