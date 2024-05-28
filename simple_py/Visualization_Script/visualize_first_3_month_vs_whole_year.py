import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

data = _util.load_csv_as_dataframe("^NDX.csv")

# 将日期列转换为 datetime 格式
data['Date'] = pd.to_datetime(data['Date'])

# 过滤掉年份小于或等于 1950 的数据
data = data[data['Date'].dt.year > 1950]

def calculate_annual_performance(data):
    result = []  # 用于存储结果的列表

    for year in range(data['Date'].dt.year.min(), data['Date'].dt.year.max() + 1):
        yearly_data = data[data['Date'].dt.year == year]  # 筛选出该年份的数据
        begin_data = yearly_data[yearly_data['Date'].dt.month.isin([1, 2, 3])]  # 筛选出1月、2月和3月的数据
        if not begin_data.empty:
            start_price = begin_data.iloc[0]['Open']  # 全年的起始价格
            if start_price == 0:
                start_price = begin_data.iloc[0]['Close']  # 全年的起始价格

            end_price = begin_data.iloc[-1]['Close']  # 结束价格
            begin_growth = ((end_price - start_price) / start_price) * 100  # 计算1月、2月和3月的涨幅
            
            end_year_price = yearly_data.iloc[-1]['Close']  # 全年的结束价格
            yearly_growth = ((end_year_price - start_price) / start_price) * 100  # 计算全年的涨幅
            result.append((year, begin_growth, yearly_growth))  # 添加到结果列表
        else:
            result.append((year, np.nan, np.nan))  # 如果没有数据，填充NaN

    return pd.DataFrame(result, columns=['Year', 'Begin Growth (%)', 'Yearly Growth (%)'])

def plot_annual_performance_relationship(df):
    df = df.dropna()  # 去除包含NaN的行
    x = df['Begin Growth (%)'].values
    y = df['Yearly Growth (%)'].values
    
    # 简单线性回归
    coefficients = np.polyfit(x, y, 1)
    polynomial = np.poly1d(coefficients)
    y_pred = polynomial(x)
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x, y, color='green', alpha=0.6, label='Data Points')
    plt.plot(np.sort(x), polynomial(np.sort(x)), color='red', linestyle='-', label='Regression Line')
    
    plt.xlabel('Begin Growth (%)')
    plt.ylabel('Yearly Growth (%)')
    plt.title('Yearly Start vs. Yearly Growth')
    plt.legend()
    plt.grid(True)
    
    # 显示回归参数
    plt.text(0.05, 0.95, f'y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}', transform=plt.gca().transAxes, 
             fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
    # 添加tooltip功能
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Year: {df.iloc[sel.index]["Year"]}\n'
        f'Begin Growth: {df.iloc[sel.index]["Begin Growth (%)"]:.2f}%\n'
        f'Yearly Growth: {df.iloc[sel.index]["Yearly Growth (%)"]:.2f}%'
    ))

    plt.show()

# 计算年初几个月和全年表现的关系
annual_performance_df = calculate_annual_performance(data)

# 可视化
plot_annual_performance_relationship(annual_performance_df)
