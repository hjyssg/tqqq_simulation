import pandas as pd
from datetime import datetime, timedelta
import os

# all_time_high.py 的随机对照组

# 读取CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data/1985年开始的纳斯达克100^NDX.csv')
df = pd.read_csv(file_path)


# 将日期列转换为datetime类型
df['Date'] = pd.to_datetime(df['Date'])

# 随机抽取200个数据点
random_sample = df.sample(n=600)

# 创建一个新的DataFrame用于存储结果
random_sample_result_df = pd.DataFrame(columns=['Date', 'PerformancePercentage'])

LATER_DAY = 200


# 逐步迭代随机抽取的数据点，找到每个数据点相对于之前所有数据的最高点
for index, row in random_sample.iterrows():
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

        random_sample_result_df = pd.concat([random_sample_result_df, pd.DataFrame([new_row])], ignore_index=True)

print(random_sample_result_df['PerformancePercentage'].describe())

# count    309.000000
# mean       7.435062
# std       18.486876
# min      -42.459678
# 25%       -3.419026
# 50%        8.816449
# 75%       17.608205
# max       84.246207

# all_time_high投资效果甚至比随机略好

import matplotlib.pyplot as plt
import seaborn as sns
# 绘制随机抽取数据点的百分比分布图
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.histplot(random_sample_result_df['PerformancePercentage'], bins=30, kde=True, color='orange')
plt.title(f'Stock Performance {LATER_DAY} Days After ATH (Random Sample)')
plt.xlabel('Percentage')
plt.ylabel('Frequency')
plt.show()
