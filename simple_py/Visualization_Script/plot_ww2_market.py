# 文件名：plot_ww2_market.py
# 文件目的：
# 本脚本用于加载股票指数数据（如标普500），并可视化二战期间（1939-1945年）的市场走势。
# 它还会标记出关键的历史事件时间点，以便观察市场对重大事件的反应。

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from datetime import datetime

# 载入工具模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 加入util.py所在路径
import _util

# 加载数据
data = _util.load_csv_as_dataframe("^SPX.csv")  # data 是一个DataFrame

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 转换日期列为datetime
data['Date'] = pd.to_datetime(data['Date'])

# 过滤二战时间段
start_date = '1939-01-01'
end_date = '1945-12-31'
mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
ww2_data = data.loc[mask]

# 画图
plt.figure(figsize=(14, 7))
plt.plot(ww2_data['Date'], ww2_data['Adj Close'], label='Adj Close')

# 标记重要事件
events = {
    '1939-09-01': '德国入侵波兰（二战爆发）',
    '1940-06-22': '法国投降',
    '1941-12-07': '日本偷袭珍珠港',
    '1942-04-28': '股市触底反弹',
    '1944-06-06': '诺曼底登陆',
    '1945-05-08': '德国投降（欧洲战争结束）',
    '1945-08-15': '日本宣布投降（太平洋战争结束）'
}

for date_str, label in events.items():
    date = pd.to_datetime(date_str)
    plt.axvline(date, color='red', linestyle='--', alpha=0.7)
    plt.text(date, ww2_data['Adj Close'].max()*0.95, label,
         rotation=90, ha='right', va='top', fontsize=9, color='darkred')

# 添加图例与标题
plt.title("二战期间标普500指数走势")
plt.xlabel("日期")
plt.ylabel("调整收盘价")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
