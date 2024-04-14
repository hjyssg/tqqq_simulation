import pandas as pd
import os
import matplotlib.pyplot as plt

# 读取数据
def read_data(file_path):
    df = pd.read_csv(file_path)
    # 将日期列解析为日期时间对象
    df['Date'] = pd.to_datetime(df['Date'])
    # 设置日期作为索引
    df.set_index('Date', inplace=True)
    return df

# 计算百分比涨跌幅
def calculate_monthly_returns(df):
    # 计算每月末的收盘价
    monthly_close = df['Close'].resample('M').last()
    # 计算每月末的收益率
    monthly_returns = monthly_close.pct_change() * 100
    return monthly_returns

# 生成可视化结果
def visualize_returns(monthly_returns_1, monthly_returns_2):
    plt.figure(figsize=(10, 6))
    # 画柱状图
    plt.bar(monthly_returns_1.index, monthly_returns_1.values, width=20, label='QQQ', color='blue', alpha=0.7)
    plt.bar(monthly_returns_2.index, monthly_returns_2.values, width=20, label='Bitcoin', color='orange', alpha=0.7)
    
    plt.title('Monthly Returns Comparison')
    plt.xlabel('Date')
    plt.ylabel('Monthly Returns (%)')
    plt.legend()
    plt.grid(True)
    plt.show()


import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

def compare_and_regress(monthly_returns_1, monthly_returns_2):
    # Drop NaN values from both Series to ensure clean data
    monthly_returns_1 = monthly_returns_1.dropna()
    monthly_returns_2 = monthly_returns_2.dropna()

    # Ensure both Series have the same dates after dropping NaNs
    monthly_returns_1, monthly_returns_2 = monthly_returns_1.align(monthly_returns_2, join='inner')
    
    # Check if there are enough data points
    if len(monthly_returns_1) < 2:
        print("Insufficient data for regression analysis.")
        return

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(monthly_returns_1, monthly_returns_2)

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(monthly_returns_1.values, monthly_returns_2.values)

    print(slope, intercept, r_value, p_value, std_err)
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(monthly_returns_1.values, monthly_returns_2.values, color='green', alpha=0.5)
    
    # Plot regression line
    line = slope * monthly_returns_1.values + intercept
    plt.plot(monthly_returns_1.values, line, 'r', label=f'y={slope:.2f}x+{intercept:.2f}\nR²={r_value**2:.2f}')
    
    plt.title('Monthly Returns: Bitcoin vs. Nasdaq')
    plt.xlabel('Nasdaq Monthly Returns (%)')
    plt.ylabel('Bitcoin Monthly Returns (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Optionally, you can return the regression results if you want to use them later
    return slope, intercept, r_value, p_value, std_err



# 主函数
def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path_1 = os.path.join(script_dir, '../data/^NDX.csv')
    file_path_2 = os.path.join(script_dir, '../data/BTC-USD.csv')

    # 读取数据
    df_1 = read_data(file_path_1)
    df_2 = read_data(file_path_2)

    # 选择2015年及以后的数据
    df_1 = df_1['2015':]
    df_2 = df_2['2015':]

    # 计算百分比涨跌幅
    monthly_returns_1 = calculate_monthly_returns(df_1)
    monthly_returns_2 = calculate_monthly_returns(df_2)

    # 生成可视化结果
    # visualize_returns(monthly_returns_1, monthly_returns_2)

    compare_and_regress(monthly_returns_1, monthly_returns_2)

if __name__ == "__main__":
    main()



print("--------")