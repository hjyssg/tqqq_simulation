import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util
df = _util.load_csv_as_dataframe("^SPX.csv")

# 选择1970年及之后的数据
df = df[df['Date'] >= pd.to_datetime('1970-01-01')].reset_index(drop=True)


# 初始化变量，用于跟踪前最高点
previous_high_index = 0
previous_high_price = df['Adj Close'][0]

# 存储历史高点的数据
historical_high_points = {'Date': [], 'Historical_High': []}

# 逐步迭代数据，找到每个数据点相对于之前所有数据的最高点
for index, row in df.iterrows():
    if row['Adj Close'] > previous_high_price:
        # 当前数据点的收盘价高于之前的最高点
        previous_high_index = index
        previous_high_price = row['Adj Close']

        # 存储历史高点的数据
        historical_high_points['Date'].append(row['Date'])
        historical_high_points['Historical_High'].append(previous_high_price)

# 打印历史高点数据
historical_high_df = pd.DataFrame(historical_high_points)
print(historical_high_df)

# 可视化
plt.figure(figsize=(10, 6))
plt.yscale('log')  # 使用对数刻度
plt.plot(df['Date'], df['Adj Close'], label='Close Price')
plt.scatter(historical_high_df['Date'], historical_high_df['Historical_High'], color='red', label='Historical High')

# 在历史高点位置添加日期标签
# for i, date in enumerate(historical_high_df['Date']):
#     plt.annotate(str(date.date()), (date, historical_high_df['Historical_High'][i]), textcoords="offset points", xytext=(0,10), ha='center')

#  控制 Y 轴上标签的数量
plt.yticks([100, 250, 500, 1000, 2000, 5000], ['100', "250", '500', '1000', '2000', '5000'])

plt.title('Stock Price with Historical High Points')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()


print("---")