import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

start_year = 1997
end_year = 1998
# filename = "^SPX.csv"
filename = "^NDX.csv"


def main():
    df_1 = _util.load_csv_as_dataframe(filename)
    # 筛选时期
    df_1 = df_1[(df_1['Date'].dt.year >= start_year) & (df_1['Date'].dt.year <= end_year)]

    # 试验不同的multiplier值
    best_multiplier = None
    best_return = float('-inf')

    print(f"{filename} From {start_year} To {end_year}")

    for multiplier in range(1, 11):  # 尝试multiplier从1到10
        df_2 = _util.calculate_n_derivatives(df_1, multiplier)
        derived_return = (df_2['Close'].iloc[-1] / df_2['Close'].iloc[0] - 1) * 100

        print(f"Multiplier: {multiplier}, Derived return from {start_year} to {end_year}: {derived_return:.2f}%")

        if derived_return > best_return:
            best_return = derived_return
            best_multiplier = multiplier

    print(f"Best multiplier: {best_multiplier} with a derived return of: {best_return:.2f}%")

if __name__ == "__main__":
    main()
    print("------------")


# ^NDX.csv 1996 1998
# Multiplier: 1, Derived return from 1996 to 1998: 213.34%
# Multiplier: 2, Derived return from 1996 to 1998: 679.02%
# Multiplier: 3, Derived return from 1996 to 1998: 1431.12%
# Multiplier: 4, Derived return from 1996 to 1998: 2263.00%
# Multiplier: 5, Derived return from 1996 to 1998: 2731.70%
# Multiplier: 6, Derived return from 1996 to 1998: 2487.57%
# Multiplier: 7, Derived return from 1996 to 1998: 1648.17%
# Multiplier: 8, Derived return from 1996 to 1998: 722.20%
# Multiplier: 9, Derived return from 1996 to 1998: 129.75%
# Multiplier: 10, Derived return from 1996 to 1998: -88.81%
# Best multiplier: 5 with a derived return of: 2731.70%

# ^SPX.csv From 1996 To 1998
# Multiplier: 1, Derived return from 1996 to 1998: 98.03%
# Multiplier: 2, Derived return from 1996 to 1998: 258.65%
# Multiplier: 3, Derived return from 1996 to 1998: 493.22%
# Multiplier: 4, Derived return from 1996 to 1998: 794.18%
# Multiplier: 5, Derived return from 1996 to 1998: 1124.55%
# Multiplier: 6, Derived return from 1996 to 1998: 1417.07%
# Multiplier: 7, Derived return from 1996 to 1998: 1590.09%
# Multiplier: 8, Derived return from 1996 to 1998: 1578.78%
# Multiplier: 9, Derived return from 1996 to 1998: 1368.22%
# Multiplier: 10, Derived return from 1996 to 1998: 1008.64%
# Best multiplier: 7 with a derived return of: 1590.09%

# ^SPX.csv From 1997 To 1998
# Multiplier: 1, Derived return from 1997 to 1998: 66.79%
# Multiplier: 2, Derived return from 1997 to 1998: 158.02%
# Multiplier: 3, Derived return from 1997 to 1998: 269.77%
# Multiplier: 4, Derived return from 1997 to 1998: 389.87%
# Multiplier: 5, Derived return from 1997 to 1998: 498.19%
# Multiplier: 6, Derived return from 1997 to 1998: 570.55%
# Multiplier: 7, Derived return from 1997 to 1998: 586.00%
# Multiplier: 8, Derived return from 1997 to 1998: 535.21%
# Multiplier: 9, Derived return from 1997 to 1998: 425.86%
# Multiplier: 10, Derived return from 1997 to 1998: 281.75%
# Best multiplier: 7 with a derived return of: 586.00%

# ^NDX.csv From 1997 To 1998
# Multiplier: 1, Derived return from 1997 to 1998: 125.11%
# Multiplier: 2, Derived return from 1997 to 1998: 323.28%
# Multiplier: 3, Derived return from 1997 to 1998: 562.68%
# Multiplier: 4, Derived return from 1997 to 1998: 758.58%
# Multiplier: 5, Derived return from 1997 to 1998: 811.21%
# Multiplier: 6, Derived return from 1997 to 1998: 678.95%
# Multiplier: 7, Derived return from 1997 to 1998: 420.90%
# Multiplier: 8, Derived return from 1997 to 1998: 157.13%
# Multiplier: 9, Derived return from 1997 to 1998: -19.82%
# Multiplier: 10, Derived return from 1997 to 1998: -95.35%
# Best multiplier: 5 with a derived return of: 811.21%