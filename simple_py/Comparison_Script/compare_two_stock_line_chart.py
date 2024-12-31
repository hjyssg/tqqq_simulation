import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 读取数据
f1 = "sso.csv"
f2 = "upro.csv"
spy_data = _util.load_csv_as_dataframe(f1)
qqq_data = _util.load_csv_as_dataframe(f2)

# 设置日期列为索引，并确保日期列为timezone-naive
spy_data['Date'] = pd.to_datetime(spy_data['Date']).dt.tz_localize(None)
qqq_data['Date'] = pd.to_datetime(qqq_data['Date']).dt.tz_localize(None)

spy_data.set_index('Date', inplace=True)
qqq_data.set_index('Date', inplace=True)

# 对齐数据
spy_data, qqq_data = spy_data.align(qqq_data, join='inner')

# 计算每个月的百分比变化
spy_monthly = spy_data['Close'].resample('ME').last().pct_change()
qqq_monthly = qqq_data['Close'].resample('ME').last().pct_change()

# 计算相同初始投资的最终收益百分比
initial_investment = 10000  # 初始投资金额
spy_final_value = initial_investment * (1 + spy_monthly).cumprod().iloc[-1]
qqq_final_value = initial_investment * (1 + qqq_monthly).cumprod().iloc[-1]

spy_return_percentage = (spy_final_value - initial_investment) / initial_investment * 100
qqq_return_percentage = (qqq_final_value - initial_investment) / initial_investment * 100

print(f"{f1}最终收益百分比: {spy_return_percentage:.2f}%")
print(f"{f2}最终收益百分比: {qqq_return_percentage:.2f}%")

# 绘制走势图
plt.figure(figsize=(14, 7))
plt.plot((1 + spy_monthly).cumprod(), label=f1)
plt.plot((1 + qqq_monthly).cumprod(), label=f2)
plt.title(f'{f1} vs {f2} Investment Growth')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)
plt.show()