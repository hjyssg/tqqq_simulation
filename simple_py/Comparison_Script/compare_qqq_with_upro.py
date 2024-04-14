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

# 计算每月末的市值
def calculate_monthly_values(df, initial_investment):
    monthly_values = []
    # 计算每月末的收盘价
    monthly_close = df['Close'].resample('M').last()
    num_shares = initial_investment / monthly_close.iloc[0]
    for price in monthly_close:
        monthly_values.append(num_shares * price)
    return pd.Series(monthly_values, index=monthly_close.index)

# 生成可视化结果
def visualize_returns(monthly_values_1, monthly_values_2):
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_values_1.index, monthly_values_1.values, label='QQQ', color='blue')
    plt.plot(monthly_values_2.index, monthly_values_2.values, label='UPRO', color='orange')
    # plt.title(f"Portfolio Value Comparison since {year_after}")
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

# 主函数
def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path_1 = os.path.join(script_dir, '../data/^NDX.csv')
    file_path_2 = os.path.join(script_dir, '../data/upro.csv')

    # 读取数据
    df_1 = read_data(file_path_1)
    df_2 = read_data(file_path_2)

    df_1, df_2 = df_1.align(df_2, join='inner')

    # 初始投资金额
    initial_investment = 10000

    # 计算每月末的市值
    monthly_values_1 = calculate_monthly_values(df_1, initial_investment)
    monthly_values_2 = calculate_monthly_values(df_2, initial_investment)

    # 生成可视化结果
    visualize_returns(monthly_values_1, monthly_values_2)

if __name__ == "__main__":
    main()



    print("------------")