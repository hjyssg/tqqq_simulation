import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")

# 筛选特定月份的数据
target_month = 4  
data['Month'] = data['Date'].dt.month
monthly_data = data[data['Month'] == target_month]

# 计算每年该月的百分比变化
monthly_data['Year'] = monthly_data['Date'].dt.year
monthly_changes = monthly_data.groupby('Year').apply(lambda x: (x['Close'].iloc[-1] - x['Open'].iloc[0]) / x['Open'].iloc[0] * 100)

# print(monthly_changes.head(10))
print(monthly_changes.describe())

# 画出直方图
plt.figure(figsize=(10, 6))
monthly_changes.hist(bins=20)
plt.title('March Monthly Percentage Change Histogram')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

print("--")