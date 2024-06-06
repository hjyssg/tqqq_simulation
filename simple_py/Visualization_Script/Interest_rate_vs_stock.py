import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util

# 加载数据
stock_data = _util.load_csv_as_dataframe("^SPX.csv")  # 假设股票数据文件名为 ^NDX.csv
interest_rate_data = _util.load_etc_csv_as_dataframe("FEDFUNDS.csv")  # 假设利率数据文件名为 FEDFUNDS.csv

# 数据处理
# 转换日期列为日期类型
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
interest_rate_data['Date'] = pd.to_datetime(interest_rate_data['Date'])

# 设置日期为索引并进行重采样
interest_rate_data.set_index('Date', inplace=True)
interest_rate_daily = interest_rate_data['FEDFUNDS'].resample('D').ffill().reset_index()  # 重采样后将 'Date' 重新作为常规列

aligned_data = pd.merge(stock_data, interest_rate_daily, how='left', left_on='Date', right_on='Date')

#----------------------------------------------------------------------------------------------------------------
import mplcursors
from scipy.stats import pearsonr
import numpy as np

def calculate_annual_change(data, value_column, use_absolute_change=False):
    data['Year'] = data['Date'].dt.year
    annual_changes = []
    
    years = sorted(data['Year'].unique())
    for i in range(1, len(years)):
        prev_year = years[i - 1]
        curr_year = years[i]
        
        prev_value = data[data['Year'] == prev_year][value_column].iloc[-1]
        curr_value = data[data['Year'] == curr_year][value_column].iloc[-1]
        
        if use_absolute_change:
            annual_change = curr_value - prev_value
        else:
            annual_change = ((curr_value - prev_value) / prev_value) * 100
            
        annual_changes.append({'Year': curr_year, 'Annual_Change': annual_change})
    
    return pd.DataFrame(annual_changes)

def render_scatter_rate_vs_stock(aligned_data):
    # 计算年度股票变化百分比
    annual_stock_changes = calculate_annual_change(aligned_data, 'Adj Close')
    
    # 计算年度利率变化绝对值
    annual_rate_changes = calculate_annual_change(aligned_data, 'FEDFUNDS', use_absolute_change=True)
    
    # 合并数据
    annual_data = pd.merge(annual_stock_changes, annual_rate_changes, on='Year', suffixes=('_Stock', '_Rate'))
    # 删除包含NaN或inf的行
    annual_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    annual_data.dropna(inplace=True)

    # 绘制散点图
    fig, ax = plt.subplots()
    scatter = ax.scatter(annual_data['Annual_Change_Rate'], annual_data['Annual_Change_Stock'])

    # 计算相关系数  --》 0.01
    correlation, _ = pearsonr(annual_data['Annual_Change_Rate'], annual_data['Annual_Change_Stock'])
    print(f'Pearson correlation coefficient: {correlation:.2f}')

    # 添加标题和标签
    ax.set_title('Annual Change: Stock vs Interest Rate')
    ax.set_xlabel('Annual Interest Rate Change (Absolute Value)')
    ax.set_ylabel('Annual Stock Change (%)')

    # 添加mplcursors tooltip
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Year: {annual_data["Year"].iloc[sel.target.index]}\nRate Change: {annual_data["Annual_Change_Rate"].iloc[sel.target.index]:.2f}\nStock Change: {annual_data["Annual_Change_Stock"].iloc[sel.target.index]:.2f}%'))

    plt.show()

    input("------")

    # 小结论：


render_scatter_rate_vs_stock(aligned_data)

#-------------------------------------------------------------------------------------------------------------------------------
def plot_each_year():
    # 创建输出文件夹
    output_dir = 'temp_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 可视化每年的数据
    unique_years = aligned_data['Date'].dt.year.unique()
    for year in unique_years:
        if year <= 1985:
            continue

        year_data = aligned_data[aligned_data['Date'].dt.year == year]

        # 可视化
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # 主轴：股票价格
        ax1.plot(year_data['Date'], year_data['Adj Close'], color='tab:blue')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Adjusted Close', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # 副轴：利率
        ax2 = ax1.twinx()
        ax2.plot(year_data['Date'], year_data['FEDFUNDS'], color='tab:red')  # 使用日期和利率数据
        ax2.set_ylabel('Fed Funds Rate', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # 设置标题
        plt.title(f'Stock and Interest Rate Changes for the Year {year}')

        # 保存图表
        output_path = os.path.join(output_dir, f'Interest_Stock_Change_{year}.png')
        plt.savefig(output_path)
        plt.close(fig)  # 关闭图表以释放内存
