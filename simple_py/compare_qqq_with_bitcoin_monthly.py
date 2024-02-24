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

# 主函数
def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path_1 = os.path.join(script_dir, '../data/1985年开始的纳斯达克100^NDX.csv')
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
    visualize_returns(monthly_returns_1, monthly_returns_2)

if __name__ == "__main__":
    main()



