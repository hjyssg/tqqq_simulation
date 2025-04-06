import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

data = _util.load_csv_as_dataframe("^SPX.csv")  # data is dataframe

# 只在意二战后的数据
data = data[data['Date'].dt.year > 1950]

# 排除 2000、2001、2002、2003、2008 年的数据
data = data[~data['Date'].dt.year.isin([2000, 2001, 2002, 2003, 2008])]

# 计算每日涨跌幅度（百分比）
data['Return'] = data['Close'].pct_change() * 100

# 找出单日跌幅超过4%的日期
significant_drops = data[data['Return'] < -4]

# 只保留每年第一次暴跌的记录
# significant_drops['Year'] = significant_drops['Date'].dt.year
# significant_drops = significant_drops.groupby('Year').first().reset_index()

# 打印统计特征
# print(significant_drops['Return'].describe())
# print(significant_drops)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

drop_dates = significant_drops['Date']  # 用日期来表示
returns_after_drops = []

for drop_date in drop_dates:
    # 找到暴跌发生日期对应的索引
    drop_idx = data[data['Date'] == drop_date].index[0]  # 使用日期找到对应的索引
    
    if drop_idx + 20 < len(data):
        future_return = (data.loc[drop_idx + 20, 'Close'] / data.loc[drop_idx, 'Close'] - 1) * 100
        returns_after_drops.append((drop_date, data.loc[drop_idx, 'Return'], future_return))
# 将结果保存为DataFrame
returns_after_drops_df = pd.DataFrame(returns_after_drops, columns=['Drop Date', 'Drop Return', 'Return After 20 Days'])

returns_after_drops_df.to_csv('returns_after_drops.csv', index=False)

# # 绘制散点图
# plt.figure(figsize=(12, 6))
# sns.scatterplot(x=returns_df['Drop Percentage'], y=returns_df['20-Day Return'], color='red', alpha=0.6)
# plt.xlabel("单日跌幅（%）")
# plt.ylabel("20天后累计涨跌幅（%）")
# plt.title("单日暴跌 vs 20天后涨跌幅")
# plt.grid(True)
# plt.show()
