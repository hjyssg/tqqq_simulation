import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

def calculate_max_drawdown(prices):
    """计算最大回撤"""
    cummax = np.maximum.accumulate(prices)
    drawdown = (prices - cummax) / cummax
    return drawdown.min()

def run_simulation(start_date, end_date):
    # 参数设置
    filename = "^NDX.csv"
    
    # 1. 加载数据
    df_ndx = _util.load_csv_as_dataframe(filename)
    df_filtered = df_ndx[(df_ndx['Date'] >= start_date) & (df_ndx['Date'] <= end_date)].reset_index(drop=True)
    
    if df_filtered.empty:
        print(f"Error: No data found for {filename} between {start_date} and {end_date}")
        return

    # 2. 模拟杠杆 ETF
    df_qld = _util.calculate_n_derivatives(df_filtered, 2)
    df_tqqq = _util.calculate_n_derivatives(df_filtered, 3)
    
    # 3. 计算指标
    results = []
    assets = [("NDX (1x)", df_filtered), ("QLD (Sim 2x)", df_qld), ("TQQQ (Sim 3x)", df_tqqq)]
    for name, df in assets:
        prices = df['Close'].values
        initial_price = prices[0]
        
        final_return = (prices[-1] / initial_price - 1) * 100
        peak_return = (np.max(prices) / initial_price - 1) * 100
        mdd = calculate_max_drawdown(prices) * 100
        
        results.append({
            "Name": name,
            "TotalReturn": final_return,
            "PeakReturn": peak_return,
            "MaxDrawdown": mdd
        })

    # 4. 打印结果
    print(f"\nSimulation Results ({start_date} to {end_date}):")
    print("-" * 85)
    print(f"{'Name':<15} | {'Total Return':<15} | {'Peak Return':<15} | {'Max Drawdown':<15}")
    print("-" * 85)
    for res in results:
        print(f"{res['Name']:<15} | {res['TotalReturn']:>13.2f}% | {res['PeakReturn']:>13.2f}% | {res['MaxDrawdown']:>13.2f}%")
    print("-" * 85)

    # 5. 可视化
    plt.figure(figsize=(12, 7))
    
    # 归一化，以便从100开始比较
    plt.plot(df_filtered['Date'], df_filtered['Close'] / df_filtered['Close'].iloc[0] * 100, label='NDX (1x)', linewidth=1.5)
    plt.plot(df_qld['Date'], df_qld['Close'] / df_qld['Close'].iloc[0] * 100, label='QLD (Sim 2x)', linewidth=1.1)
    plt.plot(df_tqqq['Date'], df_tqqq['Close'] / df_tqqq['Close'].iloc[0] * 100, label='TQQQ (Sim 3x)', linewidth=0.8)
    
    plt.yscale('log') # 使用对数坐标轴，因为波动巨大
    plt.title(f'Dotcom Bubble Simulation: NDX vs QLD vs TQQQ ({start_date} to {end_date})')
    plt.xlabel('Date')
    plt.ylabel('Relative Price (Log Scale, Start=100)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    # 保存结果图表
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'screenshot', 'LETF')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    start_year = start_date.split('-')[0]
    filename_out = f'dotcom_bubble_{start_year}_start.png'
    plt.savefig(os.path.join(output_dir, filename_out))
    print(f"图表已保存至: {os.path.join(output_dir, filename_out)}")
    plt.close()

def main():
    _util.init_plotting()
    periods = [
        ('1997-01-01', '2002-12-31'),
        ('1998-01-01', '2002-12-31'),
        ('1999-01-01', '2002-12-31')
    ]
    
    for start, end in periods:
        run_simulation(start, end)

if __name__ == "__main__":
    main()
