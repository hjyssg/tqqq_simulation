import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 导入数据
data = _util.load_csv_as_dataframe("^NDX.csv")  # data is dataframe

# 计算涨跌幅度
data['Pct_Change'] = data['Close'].pct_change() * 100

# 删除首行的NaN值
data = data.dropna()

print(data['Pct_Change'].describe())

def render_histogram(data, title):
    # 可视化设置
    hist_label = f'{title}涨跌幅度分布'
    x_label = '涨跌幅度 (%)'
    y_label = '频率'

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 可视化
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Pct_Change'], kde=True)
    plt.title(hist_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 添加mplcursors的tooltip功能
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'涨跌幅度: {sel.target[0]:.2f}%'))

    # 显示图表
    plt.show()

render_histogram(data, '所有情况')


# 定义牛市和熊市的年份列表
bull_years = [1982, 1983, 1985, 1986, 1987, 1995, 1996, 1997, 1998, 1999]
bear_years = [1973, 1974, 2000, 2001, 2002, 2008, 2009]

# 筛选牛市和熊市的数据
bull_market_data = data[data['Date'].dt.year.isin(bull_years)]
bear_market_data = data[data['Date'].dt.year.isin(bear_years)]

# 绘制牛市和熊市的涨跌幅度分布图
render_histogram(bull_market_data, '牛市')
render_histogram(bear_market_data, '熊市')
