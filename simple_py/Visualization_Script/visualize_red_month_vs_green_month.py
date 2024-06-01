import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 导入数据
data = _util.load_csv_as_dataframe("^NDX.csv")  # data is a DataFrame
data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is a datetime object
data = data.set_index('Date')  # Set 'Date' as the index

data = data[data.index.year > 2010]

# 计算周和月的涨跌幅度
weekly_data = data['Close'].resample('W').last().pct_change() * 100
monthly_data = data['Close'].resample('M').last().pct_change() * 100

# 删除NaN值
weekly_data = weekly_data.dropna()
monthly_data = monthly_data.dropna()

print("周涨跌幅度统计特征:")
print(weekly_data.describe())
print("\n月涨跌幅度统计特征:")
print(monthly_data.describe())


# 周涨跌幅度统计特征:
# count    698.000000
# mean       0.336792
# std        2.627321
# min      -12.519540
# 25%       -1.133871
# 50%        0.464701
# 75%        1.916004
# max        9.436903
# Name: Close, dtype: float64

# 月涨跌幅度统计特征:
# count    160.000000
# mean       1.447657
# std        5.002319
# min      -13.368546
# 25%       -1.696964
# 50%        1.845703
# 75%        4.743749
# max       15.191780

#-------------------------------------------------------
# 计算涨跌幅度的分位数
quantiles = monthly_data.quantile([0.25, 0.5, 0.75, 0.95])
print("月度涨跌幅度的主要分位数:")
print(quantiles)

# 特定的涨跌幅度值
specific_value = 6.28  # 涨跌幅度为6.28%
quantile_of_value = monthly_data[monthly_data <= specific_value].count() / monthly_data.count()
print(f"涨跌幅度 {specific_value}% 的月度分位数位置: {quantile_of_value:.2f}")

#------------------------------------------------------------------------------------
def render_histogram(data, title, time_frame):
    # 可视化设置
    hist_label = f'{title}{time_frame}涨跌幅度分布'
    x_label = '涨跌幅度 (%)'
    y_label = '频率'

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 可视化
    plt.figure(figsize=(10, 6))
    sns.histplot(data, kde=True)
    plt.title(hist_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 添加mplcursors的tooltip功能
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f'涨跌幅度: {sel.target[0]:.2f}%'))

    # 显示图表
    plt.show()

# 渲染周和月的直方图
render_histogram(weekly_data, '', '周')
render_histogram(monthly_data, '', '月')



