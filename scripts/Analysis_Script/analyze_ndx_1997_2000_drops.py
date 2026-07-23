import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# 添加脚本目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from _util import load_csv_as_dataframe, init_plotting, show_plot

def analyze_drops():
    # 1. 加载数据
    filename = '^NDX.csv'
    df = load_csv_as_dataframe(filename)
    
    # 2. 筛选 1997 ~ 2000 互联网泡沫牛市顶点前的区间
    start_date = '1997-01-01'
    end_date = '2000-03-24'  # NDX 泡沫顶点大约在 2000年3月
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    df_bull = df.loc[mask].copy()
    
    if df_bull.empty:
        print("未找到指定日期范围内的数据")
        return

    # 3. 计算收益率
    df_bull['Daily_Return'] = df_bull['Close'].pct_change() * 100
    
    # 4. 统计不同幅度的下跌
    drop_thresholds = [-2, -3, -5]
    print(f"--- 1997-01-01 至 {end_date} 期间下跌统计 ---")
    total_days = len(df_bull)
    print(f"总交易天数: {total_days}")
    
    for t in drop_thresholds:
        count = len(df_bull[df_bull['Daily_Return'] <= t])
        pct = (count / total_days) * 100
        print(f"单日跌幅超过 {abs(t)}% 的天数: {count} 天 ({pct:.2f}%)")

    # 5. 画图验证
    init_plotting()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # 上图：收盘价
    ax1.plot(df_bull['Date'], df_bull['Close'], label='NDX Close Price', color='blue')
    
    # 标注跌幅 > 2% 的点
    big_drops = df_bull[df_bull['Daily_Return'] <= -2]
    ax1.scatter(big_drops['Date'], big_drops['Close'], color='red', label='Daily Drop > 2%', zorder=5)
    ax1.set_title('NDX Bull Market Price Action and Major Drops (1997-2000)')
    ax1.set_ylabel('Points')
    ax1.legend()

    # 下图：每日波动
    ax2.bar(df_bull['Date'], df_bull['Daily_Return'], color='gray', alpha=0.5, label='Daily Return %')
    ax2.axhline(y=-2, color='red', linestyle='--', label='-2% Threshold')
    ax2.set_ylabel('Daily Change (%)')
    ax2.set_ylim(-15, 15)  # 限制范围以便观察
    ax2.legend()

    plt.xlabel('Date')
    
    # 保存结果
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'screenshot', 'ndx_bull_market_drops.png')
    plt.savefig(output_path)
    print(f"分析图表已保存至: {output_path}")
    plt.show()

if __name__ == "__main__":
    analyze_drops()
