import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

# 加载 util.py 中的自定义函数
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 加载数据
data = _util.load_csv_as_dataframe("^NDX.csv")  # 请替换为实际文件名

# 只在意二战后的数据
data = data[data['Date'].dt.year > 1950]

# 计算每日的涨跌幅
data['Pct_Change'] = data['Adj Close'].pct_change()

# 找出连续五天的轻微上涨
condition = (data['Pct_Change'] > 0.001) & (data['Pct_Change'] <= 0.01)
data['Up_Days'] = condition.astype(int)

# 使用 for 循环累积连续上涨天数
consecutive_up = []
count = 0

for up_day in data['Up_Days']:
    if up_day == 1:
        count += 1
    else:
        count = 0
    consecutive_up.append(count)

data['Consecutive_Up'] = consecutive_up

# 找出连续五天的开始日期
start_dates = data[data['Consecutive_Up'] == 5]['Date'].reset_index(drop=True)

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 创建目录以保存图像
output_dir = 'output_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 可视化
for start_date in start_dates:
    end_date = start_date + pd.Timedelta(days=4)
    plot_start_date = start_date - pd.Timedelta(days=60)
    plot_end_date = end_date + pd.Timedelta(days=60)

    plot_data = data[(data['Date'] >= plot_start_date) & (data['Date'] <= plot_end_date)]

    plt.figure(figsize=(14, 7))
    plt.plot(plot_data['Date'], plot_data['Adj Close'], label='Adjusted Close Price')
    plt.axvline(start_date, color='g', linestyle='--', label='Start of 5-day increase')
    plt.axvline(end_date, color='r', linestyle='--', label='End of 5-day increase')
    plt.title(f'Stock Price Around 5-day Increase Starting on {start_date.date()}')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # 保存图像
    plt.savefig(os.path.join(output_dir, f'{start_date.date()}_stock_price.png'))
    plt.close()
