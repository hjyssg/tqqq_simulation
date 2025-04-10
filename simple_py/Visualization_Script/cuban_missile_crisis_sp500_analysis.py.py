"""
本文件旨在分析古巴导弹危机（1962年10月14日至10月28日）前后美国股市的表现，
通过可视化和数据比较，观察重大地缘政治事件对市场的短期影响。
数据来源为标准普尔500指数（S&P 500），格式为CSV。
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util

# 使用你自定义的函数加载数据
data = _util.load_csv_as_dataframe("^SPX.csv")  # data is a dataframe

# 将日期列转换为datetime类型，并设置为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 筛选古巴导弹危机前后 1962年8月1日 至 1962年12月31日 的数据
crisis_start = "1962-08-01"
crisis_end = "1962-12-31"
crisis_data = data.loc[crisis_start:crisis_end]


# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 可视化Close价格走势
plt.figure(figsize=(12, 6))
plt.plot(crisis_data.index, crisis_data['Close'], label='S&P 500 Close Price', color='blue')
plt.axvline(pd.to_datetime("1962-10-14"), color='red', linestyle='--', label='U-2侦察照片发现导弹（10月14日）')
plt.axvline(pd.to_datetime("1962-10-22"), color='orange', linestyle='--', label='肯尼迪全国演说宣布封锁（10月22日）')
plt.axvline(pd.to_datetime("1962-10-28"), color='green', linestyle='--', label='苏联宣布撤回导弹（10月28日）')
plt.title("古巴导弹危机前后 S&P 500 指数走势（1962年）")
plt.xlabel("日期")
plt.ylabel("收盘价")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

""""
1. 帮我分析，我觉得2025trump的全球关税危机和古巴核弹危机其实很接近。世界一瞬间陷入极大的不确定性。
2. 为了避免confirmation bias,尝试反驳我。


市场结构不同：
    1962年市场远没那么敏感
    当年股市以机构长线投资者为主，交易频率低、信息传递慢，所以古巴危机对市场的冲击其实是温和的。
    你如果看1962年10月那段时间的S&P 500，震荡并没有特别剧烈，甚至略有反弹。
    但2025年你看到的市场波动可能源于：
    高频交易；
    新闻情绪自动化交易；
    ETF结构风险扩散。
    👉 所以我们今天看到的“全球暴跌”，未必是危机本身严重，而是交易结构高度杠杆化后的反应被放大。

"""