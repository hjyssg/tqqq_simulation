import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^N225.csv")  # data is dataframe

# 只在意二战后的数据（1950年之后）
data = data[data['Date'].dt.year > 1950]

# 计算每日收盘价的百分比变化
data['Change'] = data['Close'].pct_change() * 100

# 找出跌幅超过10%的天数
large_drops = data[data['Change'] <= -10]

# 输出结果
print("跌幅超过10%的天数: ", len(large_drops))
print(large_drops[['Date', 'Close', 'Change']])

# 可视化跌幅超过10%的天数
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Close'], label='Close Price')
plt.scatter(large_drops['Date'], large_drops['Close'], color='red', label='Drop > 10%')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Stock Price with Drops > 10% Highlighted')
plt.legend()
plt.show()

# 日经跌幅超过10%的天数:  4
# Date         Close     Change
#  1987-10-20  21910.080078 -14.900944  泡沫破灭
#  2008-10-16   8458.450195 -11.406368  世纪金融危机
#  2011-03-15   8605.150391 -10.553930  东日本大地震及其引发的福岛核事故
#  2024-08-05  31458.419922 -12.395758  日本央行加息0.25%  