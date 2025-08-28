import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util



# fn = "^SPX.csv"
# fn = "^NDX.csv"
fn = "SOXX.csv"
df_1 = _util.load_csv_as_dataframe(fn)
start_year = 1950
end_year = 2023
df_1 = df_1[(df_1['Date'].dt.year >= start_year) & (df_1['Date'].dt.year <= end_year)]
n_time = 2
data = _util.calculate_n_derivatives(df_1, n_time)

# 初始化最高价格为第一行的收盘价
previous_peak = data.loc[0, 'Close']

# 创建空的DataFrame用于存储日期和腰斩的价格
halvings_data = []

RATIO = 0.5

# 遍历数据集
for index, row in data.iterrows():
    current_close = row['Close']
    
    # 检查当前价格是否低于前高的一半
    if current_close <= previous_peak * RATIO:
        # 记录腰斩信息
        halvings_data.append({'Date': row['Date'], 'Close': current_close})
        # 从这里从新开始
        previous_peak = current_close

    # 不断更新前高值
    previous_peak = max(previous_peak, current_close)

# 将列表转换为DataFrame
halvings = pd.DataFrame(halvings_data)

# 打印腰斩信息的DataFrame
print(halvings)


import matplotlib.pyplot as plt

# 绘制整个数据集的收盘价走势
plt.figure(figsize=(14, 7))  # 设置图表大小
plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')

# 在腰斩点上标记
plt.scatter(halvings['Date'], halvings['Close'], color='red', label='Halving Points', s=50)  # s为点的大小

# 添加一些图表的基本元素
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
plt.title(f'{fn} {n_time} 相对于前高点的腰斩次数')
# plt.title('qld相对于前高点的腰斩次数')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()  # 添加图例
plt.grid(True)  # 添加网格线

# 显示图表
plt.show()

# TODO  https://mplcursors.readthedocs.io/en/stable/
