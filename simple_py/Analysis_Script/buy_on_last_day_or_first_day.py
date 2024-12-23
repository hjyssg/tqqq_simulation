import pandas as pd
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt

"""
帮我找出spx是一年最后一个交易日加仓好还是一年第一、第二个交易日加仓比较好
"""

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 加载数据
df = _util.load_csv_as_dataframe("^SPX.csv")

# 过滤数据
df = df[df['Date'].dt.year > 1985]

# 设置日期为索引
df.set_index('Date', inplace=True)

# 初始化一个列表来存储每年的最低值位置
min_positions = []

# 遍历每一年
for year in df.index.year.unique():
    # 获取当前年的最后一个交易日
    last_day = df[df.index.year == year].tail(1)
    
    # 获取下一年的前七个交易日
    next_year_days = df[df.index.year == year + 1].head(7)
    
    # 合并这八个交易日
    combined_days = pd.concat([last_day, next_year_days])
    
    # 找到最低值的位置
    min_position = combined_days['Close'].idxmin()
    
    # 将日期转换为标签
    if min_position == last_day.index[0]:
        min_positions.append('Last Day')
    else:
        day_index = (next_year_days.index == min_position).argmax() + 1
        min_positions.append(f'Day {day_index}')

# 将最低值位置转换为DataFrame
min_positions_df = pd.DataFrame(min_positions, columns=['Min Position'])

# 定义明确的顺序
categories = ['Last Day', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']

# 将 'Min Position' 列转换为有序类别
min_positions_df['Min Position'] = pd.Categorical(
    min_positions_df['Min Position'], 
    categories=categories, 
    ordered=True
)


# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 可视化结果
plt.figure(figsize=(12, 6))

# 最后一个交易日和前七个交易日的最低值位置分布
sns.histplot(min_positions_df['Min Position'], discrete=True, kde=False, color='blue', label='Min Position')

plt.title('跨年最低值位置分布')
plt.xlabel('Day')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

plt.show()

input()