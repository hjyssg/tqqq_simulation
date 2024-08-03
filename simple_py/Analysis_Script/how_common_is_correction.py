import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util


fn = "^NDX.csv"
df_1 = _util.load_csv_as_dataframe(fn)
start_year = 1950
end_year = 1999
df_1 = df_1[(df_1['Date'].dt.year >= start_year) & (df_1['Date'].dt.year <= end_year)]
data = df_1

# 初始化最高价格为第一行的收盘价
previous_peak = data.loc[0, 'Close']

# 创建空的DataFrame用于存储日期和下跌一定程度的价格
correction_data = []

# 下跌百分比
RATIO = 0.89


# 遍历数据集
for index, row in data.iterrows():
    current_close = row['Close']
    
    # 检查当前价格是否低于前高的ratio
    if current_close <= previous_peak * RATIO:
        # 记录下跌一定程度信息
        correction_data.append({'Date': row['Date'], 'Close': current_close})
        # 从这里从新开始
        previous_peak = current_close

    # 不断更新前高值
    previous_peak = max(previous_peak, current_close)

# 将列表转换为DataFrame
correction = pd.DataFrame(correction_data)

# 打印下跌一定程度信息的DataFrame
print(correction)

#-----------------------------------------
# 算一下平均一年几次
total_corrections = correction.shape[0]
# 确定data中的年份范围
years_covered = data['Date'].dt.year.max() - data['Date'].dt.year.min() + 1
# 计算平均每年下跌的次数
average_corrections_per_year = total_corrections / years_covered
print(f"平均每年下跌至特定水平的次数为：{average_corrections_per_year:.2f}次")
# NDX  平均每年下跌至特定水平的次数为：1.80次

#-------------------------------------------
import matplotlib.pyplot as plt

# 绘制整个数据集的收盘价走势
plt.figure(figsize=(14, 7))  # 设置图表大小
plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')

# 在下跌一定程度点上标记
plt.scatter(correction['Date'], correction['Close'], color='red', label='Correction Points', s=50)  # s为点的大小

# 添加一些图表的基本元素
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
plt.title(f'{fn}  相对于前高点的下跌{100-RATIO*100}%次数')
# plt.title('qld相对于前高点的下跌一定程度次数')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()  # 添加图例
plt.grid(True)  # 添加网格线

# 显示图表
plt.show()


