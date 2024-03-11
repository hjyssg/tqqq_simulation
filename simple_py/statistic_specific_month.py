import pandas as pd
import matplotlib.pyplot as plt
import os

# 读取CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data/1985年开始的纳斯达克100^NDX.csv')
data = pd.read_csv(file_path)

# 将 'Date' 列转换为日期时间类型
data['Date'] = pd.to_datetime(data['Date'])

# 筛选特定月份的数据
target_month = 3  # 3月
data['Month'] = data['Date'].dt.month
monthly_data = data[data['Month'] == target_month]

# 计算每年该月的百分比变化
monthly_data['Year'] = monthly_data['Date'].dt.year
monthly_changes = monthly_data.groupby('Year').apply(lambda x: (x['Close'].iloc[-1] - x['Open'].iloc[0]) / x['Open'].iloc[0] * 100)

# 画出直方图
plt.figure(figsize=(10, 6))
monthly_changes.hist(bins=20)
plt.title('March Monthly Percentage Change Histogram')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()
