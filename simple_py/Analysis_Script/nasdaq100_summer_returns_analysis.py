"""
文件名: nasdaq100_summer_returns_analysis.py

文件目的:
本脚本用于分析纳斯达克100指数 (NASDAQ-100, 代码 ^NDX) 或标普500指数 (S&P 500, 代码 ^SPX) 在夏季（6月至8月）的历史回报率表现。
主要功能包括：
1. 加载指定指数的历史价格数据（通过自定义模块 _util）
2. 计算每年夏季（6-8月）的回报率
3. 统计并打印近5年、10年、20年的平均回报、波动率、最佳/最差年份
4. 绘制夏季回报率柱状图
5. 保存分析结果为CSV文件

使用说明:
- 需预先准备好指数的历史数据CSV文件（例如 ^SPX.csv 或 ^NDX.csv），并放置在项目目录下。
- 使用 _util.load_csv_as_dataframe() 加载CSV数据。
- 支持中文显示，适合在中国地区使用（已设置字体为黑体）。

"""

import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

data = _util.load_csv_as_dataframe("^NDX.csv")  
data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = data['Date'].dt.tz_localize(None)

# 避免中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 计算每年夏季（6-8月）的回报率
summer_returns = {}

for year in range(2004, 2025):  # 根据数据年份调整
    try:
        start_date = pd.Timestamp(f"{year}-06-01")
        end_date = pd.Timestamp(f"{year}-08-31")
        summer_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
        if summer_data.empty:
            continue
        start_price = summer_data['Adj Close'].iloc[0]
        end_price = summer_data['Adj Close'].iloc[-1]
        summer_return = (end_price - start_price) / start_price
        summer_returns[year] = summer_return * 100
    except Exception as e:
        print(f"{year} 数据处理出错: {e}")
        continue

# 转为 DataFrame
summer_df = pd.DataFrame.from_dict(summer_returns, orient='index', columns=['夏季回报率 (%)'])
summer_df = summer_df.round(2)

# 获取summer_df中的最新年份
current_year = summer_df.index.max()

def analyze_period(years):
    cutoff = current_year - years + 1  # 包含最近years年
    subset = summer_df.loc[summer_df.index >= cutoff]
    if subset.empty:
        print(f"\n⚠️ 没有找到最近 {years} 年的夏季回报数据，请检查数据！")
        return
    avg_return = subset['夏季回报率 (%)'].mean()
    std_return = subset['夏季回报率 (%)'].std()
    best_year = subset['夏季回报率 (%)'].idxmax()
    worst_year = subset['夏季回报率 (%)'].idxmin()
    print(f"\n📊 最近 {years} 年夏季回报统计 (截至 {current_year} 年):")
    print(f"平均回报率: {avg_return:.2f}%")
    print(f"标准差: {std_return:.2f}%")
    print(f"最佳年份: {best_year}年 ({subset.loc[best_year,'夏季回报率 (%)']}%)")
    print(f"最差年份: {worst_year}年 ({subset.loc[worst_year,'夏季回报率 (%)']}%)")


print("\n📈 夏季回报分析结果:")
analyze_period(5)
analyze_period(10)
analyze_period(20)

# 绘制柱状图
plt.figure(figsize=(12,6))
colors = ['green' if x > 0 else 'red' for x in summer_df['夏季回报率 (%)']]
plt.bar(summer_df.index, summer_df['夏季回报率 (%)'], color=colors)
plt.axhline(0, color='black', linestyle='--')
plt.title('每年夏季（6-8月）回报率')
plt.xlabel('年份')
plt.ylabel('回报率 (%)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 保存结果
output_file = 'summer_returns_result.csv'
summer_df.to_csv(output_file, encoding='utf-8-sig')
print(f"\n✅ 夏季回报率结果已保存至 {output_file}")


input()