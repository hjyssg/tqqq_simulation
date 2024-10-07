import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 读取数据
data = _util.load_csv_as_dataframe("^SPX.csv")

# 确保日期列为datetime格式，并按照日期排序
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by='Date')

# 筛选1932年的数据
data_1932 = data[(data['Date'] >= '1931-01-01') & (data['Date'] <= '1934-12-31')]

# 可视化1932年的股票走势
plt.figure(figsize=(18, 10))  # 设置图表大小为 1800x1000 像素
plt.plot(data_1932['Date'], data_1932['Adj Close'], label='Adjusted Close Price in 1932')

# 设置标签和标题
plt.xlabel('Date')
plt.ylabel('Adjusted Close Price')
plt.title('Stock Trends After 1929')

# 旋转x轴标签以避免重叠
plt.xticks(rotation=45)

# 显示图例
plt.legend()

# 显示图表
plt.show()
