import pandas as pd
import os
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
df = _util.load_csv_as_dataframe("^SPX.csv")

df = df[df['Date'].dt.year > 1950]


# 设置日期为索引
df.set_index('Date', inplace=True)

# 将数据重采样到周线级别，计算每周的第一个开盘价和最后一个收盘价
weekly_df = df.resample('W').agg({'Open': 'first', 'Close': 'last'})

# 计算每周的涨跌百分比
weekly_df['Weekly Return'] = ((weekly_df['Close'] - weekly_df['Open']) / weekly_df['Open']) * 100

# 找出所有开盘到收盘下跌超过5%的周
drop_value_min = -2
drop_value_max = -3
decline_weeks = weekly_df[(weekly_df['Weekly Return'] <= drop_value_min) & (weekly_df['Weekly Return'] >= drop_value_max)]

# 找出下一周的涨跌百分比
next_week_return = weekly_df.loc[decline_weeks.index + pd.DateOffset(weeks=1), 'Weekly Return']

# 结果输出
print(f"下跌超过{drop_value_min}%的周后，下一周的涨跌百分比:")
print(next_week_return.describe())
print(len(next_week_return))


# 将结果导出到CSV文件
next_week_return.to_csv('decline_weeks.csv', index=True)  # index=True保留日期索引


#----------------------------------------------------

