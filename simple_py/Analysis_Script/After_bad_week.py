import pandas as pd
import os
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
df = _util.load_csv_as_dataframe("^NDX.csv")

# df = df[df['Date'].dt.year > 2010]


# 设置日期为索引
df.set_index('Date', inplace=True)

# 将数据重采样到周线级别，计算每周的第一个开盘价和最后一个收盘价
weekly_df = df.resample('W').agg({'Open': 'first', 'Close': 'last'})

# 计算每周的涨跌百分比
weekly_df['Weekly Return'] = ((weekly_df['Close'] - weekly_df['Open']) / weekly_df['Open']) * 100

# 找出所有开盘到收盘下跌超过5%的周
decline_weeks = weekly_df[(weekly_df['Weekly Return'] <= -5) & (weekly_df['Weekly Return'] >= -8)]

# 找出下一周的涨跌百分比
next_week_return = weekly_df.loc[decline_weeks.index + pd.DateOffset(weeks=1), 'Weekly Return']

# 结果输出
print("下跌超过5%的周及其下一周的涨跌百分比:")
print(next_week_return.describe())
print(len(next_week_return))


# 将结果导出到CSV文件
next_week_return.to_csv('decline_weeks.csv', index=True)  # index=True保留日期索引


#----------------------------------------------------
# import matplotlib.pyplot as plt

# # 设置图表大小和分辨率
# plt.figure(figsize=(14, 7))

# # 创建线形图显示下一周的涨跌百分比
# plt.subplot(2, 1, 1)  # 2行1列的第1个
# plt.plot(next_week_return.index, next_week_return.values, label='Next Week Return')
# plt.title('Next Week\'s Return After a 5-6% Decline')
# plt.xlabel('Date')
# plt.ylabel('Percentage')
# plt.grid(True)
# plt.legend()

# # 创建直方图显示下一周的涨跌百分比
# plt.subplot(2, 1, 2)  # 2行1列的第2个
# plt.hist(next_week_return.dropna(), bins=20, alpha=0.75, color='blue')
# plt.title('Histogram of Next Week\'s Return After a 5-6% Decline')
# plt.xlabel('Return Percentage')
# plt.ylabel('Frequency')
# plt.grid(True)

# # 显示图表
# plt.tight_layout()
# plt.show()
