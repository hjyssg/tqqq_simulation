# ; 要是把每月8月最后一天卖掉，10月第一天买入。Yearly Growth会怎么样？写一段额外代码，计算看看
import pandas as pd

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")
# data = _util.load_csv_as_dataframe("^SPX.csv")

# 确保数据的日期列已正确地转换为日期格式
data['Date'] = pd.to_datetime(data['Date'])

yearly_segments_growth = []  # 用于存储每年的增长数据

for year in range(data['Date'].dt.year.min(), data['Date'].dt.year.max() + 1):
    yearly_data = data[data['Date'].dt.year == year]
    
    # 计算1月1日到8月最后一天的增长
    jan_to_aug = yearly_data[(yearly_data['Date'].dt.month < 9)]
    if not jan_to_aug.empty:
        start_price_jan = jan_to_aug.iloc[0]['Open']
        end_price_aug = jan_to_aug.iloc[-1]['Close']
        growth_jan_to_aug = ((end_price_aug - start_price_jan) / start_price_jan) * 100 if start_price_jan else 0

    # 计算10月1日到12月31日的增长
    oct_to_dec = yearly_data[(yearly_data['Date'].dt.month > 9)]
    if not oct_to_dec.empty:
        start_price_oct = oct_to_dec.iloc[0]['Open']
        end_price_dec = oct_to_dec.iloc[-1]['Close']
        growth_oct_to_dec = ((end_price_dec - start_price_oct) / start_price_oct) * 100 if start_price_oct else 0

    # 合并这两个增长率作为整年的估计
    if not jan_to_aug.empty and not oct_to_dec.empty:
        yearly_growth = growth_jan_to_aug + growth_oct_to_dec
        yearly_segments_growth.append((year, yearly_growth))

# 转换为DataFrame并显示
growth_df = pd.DataFrame(yearly_segments_growth, columns=['Year', 'Yearly Growth'])
print(growth_df['Yearly Growth'].describe())

# 绘制增长率分布图
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(12, 6))
sns.histplot(growth_df['Yearly Growth'], bins=50, kde=True, color='skyblue')
plt.title('Yearly Growth Rate Distribution for Combined Periods')
plt.xlabel('Yearly Growth Rate (%)')
plt.ylabel('Frequency')
plt.show()


# ndx年化统计
# count    38.000000
# mean     17.290264
# std      25.199917
# min     -33.577457
# 25%       2.910050
# 50%      13.008687
# 75%      30.582673
# max      84.546613
# Name: Yearly Growth, dtype: float64