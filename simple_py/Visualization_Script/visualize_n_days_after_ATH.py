import pandas as pd
from datetime import datetime, timedelta
import os

# 在股票到达all time high后的股票平均表现百分比。

# 读取CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../../data/^NDX.csv')
df = pd.read_csv(file_path)

# 将日期列转换为datetime类型
df['Date'] = pd.to_datetime(df['Date'])

# 初始化变量，用于跟踪前最高点
previous_high_index = 0
previous_high_price = df['Close'][0]

# 创建一个新的DataFrame用于存储结果
result_df = pd.DataFrame(columns=['Date', 'PerformancePercentage'])


LATER_DAY = 200

# 逐步迭代数据，找到每个数据点相对于之前所有数据的最高点
for index, row in df.iterrows():
    if row['Close'] > previous_high_price:
        # 当前数据点的收盘价高于之前的最高点
        previous_high_index = index
        previous_high_price = row['Close']
    
        # 计算一个月后的日期
        date_later = row['Date'] + timedelta(days=LATER_DAY)

        # 找到一个月后的行
        date_later_row = df[df['Date'] == date_later]


        # 计算平均表现百分比
        if not date_later_row.empty:
            performance_percentage = ((date_later_row['Close'].values[0] - row['Close']) / row['Close']) * 100

            # 将结果添加到新的DataFrame中
            new_row = {'Date': row['Date'],  'PerformancePercentage': performance_percentage}

            assert row['Date'] is not None
            assert performance_percentage is not None

            result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)


print(result_df['PerformancePercentage'].describe())
# count    409.000000
# mean      10.534450
# std       17.012741
# min      -32.042729
# 25%       -0.613834
# 50%       11.317107
# 75%       18.897681
# max       80.832157

import matplotlib.pyplot as plt
import seaborn as sns

# 绘制百分比的分布图
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.histplot(result_df['PerformancePercentage'], bins=30, kde=True, color='skyblue')
plt.title(f'stock performance {LATER_DAY} days after ATH')
plt.xlabel('percentage')
plt.ylabel('time')
plt.show()