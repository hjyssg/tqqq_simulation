import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util


# 读取数据
spy_data = _util.load_csv_as_dataframe("^SPX.csv")
qqq_data = _util.load_csv_as_dataframe("^NDX.csv")

# 设置日期列为索引
spy_data.set_index('Date', inplace=True)
qqq_data.set_index('Date', inplace=True)

spy_data, qqq_data = spy_data.align(qqq_data, join='inner')

# 计算每个月的百分比变化
spy_monthly = spy_data['Close'].resample('M').last().pct_change()
qqq_monthly = qqq_data['Close'].resample('M').last().pct_change()

# 创建一个新的DataFrame来比较这两个股票的月度百分比变化
comparison_df = pd.DataFrame({'SPY': spy_monthly, 'QQQ': qqq_monthly})

# 计算差异
comparison_df['QQQ'] = comparison_df['QQQ'] * 100
comparison_df['SPY'] = comparison_df['SPY'] * 100
comparison_df['Difference'] = comparison_df['QQQ'] - comparison_df['SPY']


# 显示结果





import matplotlib.pyplot as plt

# 筛选出SPY和QQQ都上涨的月份
positive_growth_df = comparison_df[(comparison_df['SPY'] > 0) & (comparison_df['QQQ'] > 0) & (comparison_df['SPY'] > comparison_df['QQQ'])]

# 绘制垂直条形图
positive_growth_df[['SPY', 'QQQ']].plot(kind='bar', figsize=(10, 6))
plt.title('SPY vs QQQ Monthly Growth Where Both Are Positive')
plt.xlabel('Date')
plt.ylabel('Monthly Growth (%)')
plt.legend(title='Stock')
plt.xticks(rotation=45)  # 旋转x轴标签以便更好地显示
plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
plt.show()


print(positive_growth_df)
