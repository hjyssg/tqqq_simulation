import pandas as pd
import os
import matplotlib.pyplot as plt

# 读取数据
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../../data/^NDX.csv')
df = pd.read_csv(file_path)

# 将 'Date' 列转换为日期时间类型
df['Date'] = pd.to_datetime(df['Date'])

# df = df[df['Date'].dt.year > 2012]

# 计算涨跌幅度
df['Change'] = df['Close'].pct_change()

# 计算当日高低点波动
df['High_Low_Volatility'] = (df['High'] - df['Low']) / df['Open']

# 找出涨跌幅度小于 0.1% 且高低点波动小于 0.5% 的日期
filtered_dates = df[(abs(df['Change']) < 0.001) & (abs(df['High_Low_Volatility']) < 0.005)]

# 输出结果
print("Dates with change less than 0.1% and high-low volatility less than 1%:")
print(filtered_dates)

# # 画出价格变动的折线图
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='Close Price')

# 标记低波动日子的红色点
plt.scatter(filtered_dates['Date'], filtered_dates['Close'], color='red', label='Low Volatility Days')

plt.title('Price Movement on Low Volatility Days')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()


# 结论： 低波动的日子对未来没有什么指引性