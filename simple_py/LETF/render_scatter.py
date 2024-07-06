import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

# 添加util.py所在的目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 避免中文乱码和负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义文件名和倍数
filename = "^SPX.csv"
multiplier = 3

df = _util.load_csv_as_dataframe(filename)
df['Date'] = pd.to_datetime(df['Date'])  # 确保Date列是日期格式
df = df[df['Date'].dt.year > 1950] # 只在意二战后的数据


def test_single_range(df, start_date, end_date, multiplier):
    # 根据日期范围过滤数据
    df_with_range = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    # 调用_util模块中的函数处理数据
    letf_df = _util.calculate_n_derivatives(df_with_range, multiplier)

    # 计算涨跌百分比
    start_price = df_with_range.iloc[0]['Close']
    end_price = df_with_range.iloc[-1]['Close']
    original_pct_change = ((end_price - start_price) / start_price) * 100

    # 杠杆ETF涨跌百分比为导数结果的一部分 从上面left_df
    leveraged_etf_pct_change = (letf_df['Close'].iloc[-1] / letf_df['Close'].iloc[0] - 1) * 100

    return [start_date, end_date, leveraged_etf_pct_change, original_pct_change]



def render_scatter(results_df):
    x_data = results_df['original_pct_change']
    y_data = results_df['leveraged_etf_pct_change']

    # 使用 NumPy 进行线性回归，计算斜率和截距
    coefficients = np.polyfit(x_data, y_data, 1)  # 1 表示一阶多项式，即线性
    slope, intercept = coefficients

    # 计算拟合线
    y_fit = np.polyval(coefficients, x_data)

    # 绘图
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, label='Data points')
    plt.plot(x_data, y_fit, color='red', label=f'Linear fit: y = {slope:.2f}x + {intercept:.2f}')
    plt.xlabel('原始涨跌百分比')
    plt.ylabel('杠杆ETF的涨跌百分比')
    plt.legend()
    plt.title(f'杠杆etf {filename} {multiplier}')

    import mplcursors
    # 添加mplcursors显示点的数据
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Start: {results_df.iloc[sel.target.index]["start_date"].date()} \n'
        f'End: {results_df.iloc[sel.target.index]["end_date"].date()} \n'
        f'Original Change: {x_data[sel.target.index]:.2f}% \n'
        f'LETF Change: {y_data[sel.target.index]:.2f}%'))

    plt.show()

def main():
    # 初始化存放结果的DataFrame
    results_df = []

    # 假设要随机抽取的区间数
    n_intervals = 50
    # np.random.seed(42)  # 为了结果可复现

    # 遍历随机生成的日期区间
    for _ in range(n_intervals):
        valid_range_found = False
        while not valid_range_found:
            # 随机选择起始日期
            random_index = np.random.randint(0, len(df))
            start_date = df.iloc[random_index]['Date']
            end_date = start_date + pd.DateOffset(days=365)  # 一年后的日期

            # 检查是否超出数据范围
            if end_date <= df['Date'].max():
                valid_range_found = True
                # 计算每个区间的结果
                single_result = test_single_range(df, start_date, end_date, multiplier)
                results_df.append(single_result)


    results_df = pd.DataFrame(results_df, columns=['start_date', 'end_date', 'leveraged_etf_pct_change', 'original_pct_change'])

    # 绘制结果散点图

    render_scatter(results_df)

if __name__ == "__main__":
    main()
