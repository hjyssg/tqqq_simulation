import pandas as pd
import os
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util


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



# 主函数
def main():
    df_1 = _util.load_csv_as_dataframe(filename)
    # 筛选时期
    df_1 = df_1[(df_1['Date'].dt.year >= start_year) & (df_1['Date'].dt.year <= end_year)]

    sim_left = _util.calculate_n_derivatives(df_1, multiplier)

    real_letf = _util.load_csv_as_dataframe(real_left_fn)
    real_letf = real_letf[(real_letf['Date'].dt.year >= start_year) & (real_letf['Date'].dt.year <= end_year)]


    # 计算并打印最终回报率
    original_return = (df_1['Close'].iloc[-1] / df_1['Close'].iloc[0] - 1) * 100
    derived_return = (sim_left['Close'].iloc[-1] / sim_left['Close'].iloc[0] - 1) * 100
    real_left_return = (real_letf['Close'].iloc[-1] / real_letf['Close'].iloc[0] - 1) * 100
    print(f"{filename} return from {start_year} to {end_year}: {original_return:.2f}%")
    print(f"Simulate Derived return from {start_year} to {end_year}: {derived_return:.2f}%")
    print(f"{real_left_fn} return from {start_year} to {end_year}: {real_left_return:.2f}%")



    # 在同一张dash line chart画两组数据，我进行比较
    plt.figure(figsize=(10, 5))
    plt.plot(df_1["Date"], df_1['Close'], label='Original', linestyle='-', marker='')
    plt.plot(sim_left["Date"], sim_left['Close'], label='Derived x' + str(multiplier), linestyle='--', marker='')
    plt.title(f' {filename} VS {multiplier}x Derived From {start_year} to {end_year}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    


    
if __name__ == "__main__":
    main()
    print("------------")