import pandas as pd
import os
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
import numpy as np

# start_year = 1995
# end_year = 1998
# multiplier = 5
# filename = "^SPX.csv"

start_year = 2012
end_year = 2023

# multiplier = 2
# filename = "^NDX.csv"
# real_left_fn = "QLD.csv"

multiplier = 3
filename = "^SPX.csv"
real_left_fn = "upro.csv"

def compare_sim_with_real(sim_left, real_letf):
    # 比较sim_left和real_letf的数据 按日比较
    # 画一张scatter plot，x轴是real_letf的涨跌幅，y轴是sim_left的涨跌幅

    # Ensure both dataframes have the same date range
    common_dates = sim_left['Date'].isin(real_letf['Date'])
    sim_left = sim_left[common_dates]
    real_letf = real_letf[real_letf['Date'].isin(sim_left['Date'])]

    # Calculate daily percentage change
    sim_left['Pct_Change'] = sim_left['Close'].pct_change()
    real_letf['Pct_Change'] = real_letf['Close'].pct_change()

    # Drop NaN values resulting from pct_change
    sim_left = sim_left.dropna(subset=['Pct_Change'])
    real_letf = real_letf.dropna(subset=['Pct_Change'])

    # Create scatter plot
    plt.scatter(real_letf['Pct_Change'], sim_left['Pct_Change'])
   # Perform linear regression using numpy
    X = real_letf['Pct_Change'].values
    y = sim_left['Pct_Change'].values
    A = np.vstack([X, np.ones(len(X))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]

    # Plot regression line
    m_formatted = f"{m:.2f}"
    c_formatted = f"{c:.2f}"
    # Plot regression line with formatted label
    plt.plot(X, m*X + c, color='red', label=f'Regression Line {m_formatted}x + {c_formatted}')

    plt.xlabel('Real LETF Daily Percentage Change')
    plt.ylabel('Simulated Daily Percentage Change')
    plt.title('Comparison of Simulated vs Real LETF Daily Percentage Change')
    plt.legend()
    plt.grid(True)
    plt.show()
 

# 主函数
def main():
    df_1 = _util.load_csv_as_dataframe(filename)
    # 筛选时期
    df_1 = df_1[(df_1['Date'].dt.year >= start_year) & (df_1['Date'].dt.year <= end_year)]

    sim_left = _util.calculate_n_derivatives(df_1, multiplier)

    real_letf = _util.load_csv_as_dataframe(real_left_fn)
    real_letf = real_letf[(real_letf['Date'].dt.year >= start_year) & (real_letf['Date'].dt.year <= end_year)]
    compare_sim_with_real(sim_left, real_letf)



if __name__ == "__main__":
    main()
    print("------------")