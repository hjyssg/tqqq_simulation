import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 读取数据
# data = _util.load_csv_as_dataframe("^SPX.csv")
# data = _util.load_csv_as_dataframe("^NDX.csv")
data = _util.load_csv_as_dataframe("^HSI.csv")



# 确保日期列为datetime格式，并按照日期排序
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by='Date')

# 计算10天的百分比变化
data['10d_change'] = data['Adj Close'].pct_change(periods=10) * 100

# 找出10天内涨幅超过25%的行
significant_rise = data[data['10d_change'] > 20]

# 输出结果
print("历史上10天内上涨超过25%的期间：")
print(significant_rise[['Date', 'Adj Close', '10d_change']])

# 1932
# 1933
# 1938
# 2001