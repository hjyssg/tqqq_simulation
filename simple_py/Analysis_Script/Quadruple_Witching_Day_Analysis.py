import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 导入数据
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")  # data is dataframe

data = data[data['Date'].dt.year > 1950]

# 计算四巫日的涨跌百分比
# 四巫日为每年3月、6月、9月和12月的第三个周五
def is_quadruple_witching_day(date):
    month = date.month
    if month not in [3, 6, 9, 12]:
        return False
    day = date.day
    weekday = date.weekday()
    # Check if the date is the third Friday
    return day >= 15 and day <= 21 and weekday == 4

data['Date'] = pd.to_datetime(data['Date'])
data['Return'] = data['Close'].pct_change() * 100  # 计算每日涨跌百分比
data['Amplitude'] = (data['High'] - data['Low']) / data['Low'] * 100  # 计算每日振幅百分比

quadruple_witching_days = data[data['Date'].apply(is_quadruple_witching_day)]

# 打印统计特征
print("四巫日涨跌百分比统计特征：")
print(quadruple_witching_days['Return'].describe())
print("\n四巫日振幅百分比统计特征：")
print(quadruple_witching_days['Amplitude'].describe())

# 可视化涨跌幅度分布
plt.figure(figsize=(10, 6))
sns.histplot(quadruple_witching_days['Return'], kde=True, bins=30)
plt.title('四巫日涨跌幅度分布')
plt.xlabel('涨跌百分比')
plt.ylabel('频数')
cursor = mplcursors.cursor(hover=True)

# 让工具提示显示x和y的值
@cursor.connect("add")
def on_add(sel):
    sel.annotation.set(text=f"{sel.target[0]:.2f}, {sel.target[1]:.2f}")

plt.show()

# 可视化振幅分布
plt.figure(figsize=(10, 6))
sns.histplot(quadruple_witching_days['Amplitude'], kde=True, bins=30)
plt.title('四巫日振幅分布')
plt.xlabel('振幅百分比')
plt.ylabel('频数')
cursor = mplcursors.cursor(hover=True)

# 让工具提示显示x和y的值
@cursor.connect("add")
def on_add(sel):
    sel.annotation.set(text=f"{sel.target[0]:.2f}, {sel.target[1]:.2f}")

plt.show()
