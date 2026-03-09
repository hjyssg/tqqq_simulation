import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def analyze_post_embargo():
    """分析1973-1976年禁运结束后的市场走势"""
    
    # 数据路径
    spx_file = os.path.join(os.path.dirname(__file__), '..', 'data', '^SPX.csv')
    oil_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'WTISPLC Spot Crude Oil Price West Texas Intermediate (WTI) (WTISPLC).csv')
    
    # 读取数据
    spx_df = pd.read_csv(spx_file, header=2)
    spx_df.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    oil_df = pd.read_csv(oil_file)
    
    # 转换日期
    spx_df['Date'] = pd.to_datetime(spx_df['Date'])
    oil_df['observation_date'] = pd.to_datetime(oil_df['observation_date'])
    
    # 筛选1973-1976年数据
    start_date = '1973-01-01'
    end_date = '1976-12-31'
    
    spx_period = spx_df[(spx_df['Date'] >= start_date) & (spx_df['Date'] <= end_date)].copy()
    oil_period = oil_df[(oil_df['observation_date'] >= start_date) & (oil_df['observation_date'] <= end_date)].copy()
    
    # 关键日期
    embargo_start = datetime(1973, 10, 17)
    embargo_end = datetime(1974, 3, 18)
    
    # 计算关键点位
    spx_at_start = spx_period.iloc[0]['Close']
    spx_at_embargo_start = spx_period[spx_period['Date'] >= embargo_start].iloc[0]['Close']
    spx_at_embargo_end = spx_period[spx_period['Date'] >= embargo_end].iloc[0]['Close']
    spx_at_end = spx_period.iloc[-1]['Close']
    
    oil_at_start = oil_period.iloc[0]['WTISPLC']
    oil_at_embargo_start = oil_period[oil_period['observation_date'] >= embargo_start].iloc[0]['WTISPLC']
    oil_at_embargo_end = oil_period[oil_period['observation_date'] >= embargo_end].iloc[0]['WTISPLC']
    oil_at_end = oil_period.iloc[-1]['WTISPLC']
    
    # 找到SPX最低点
    spx_min_idx = spx_period['Close'].idxmin()
    spx_min_date = spx_period.loc[spx_min_idx, 'Date']
    spx_min_value = spx_period.loc[spx_min_idx, 'Close']
    
    # 创建图表
    fig, ax1 = plt.subplots(figsize=(16, 9))
    
    # 绘制SPX
    color1 = '#2E86AB'
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('标普500指数', color=color1, fontsize=12)
    ax1.plot(spx_period['Date'], spx_period['Close'], color=color1, linewidth=2, label='SPX')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    # 创建第二个Y轴用于原油价格
    ax2 = ax1.twinx()
    color2 = '#A23B72'
    ax2.set_ylabel('原油价格 (美元/桶)', color=color2, fontsize=12)
    ax2.plot(oil_period['observation_date'], oil_period['WTISPLC'], color=color2, linewidth=2, label='WTI原油', alpha=0.7)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 标记关键事件
    ax1.axvline(x=embargo_start, color='red', linestyle='--', linewidth=2, alpha=0.7, label='禁运开始')
    ax1.axvline(x=embargo_end, color='green', linestyle='--', linewidth=2, alpha=0.7, label='禁运结束')
    ax1.axvline(x=spx_min_date, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='SPX最低点')
    
    # 添加阴影区域表示禁运期
    ax1.axvspan(embargo_start, embargo_end, alpha=0.2, color='red', label='禁运期')
    
    # 标注关键点位
    ax1.annotate(f'禁运开始\nSPX: {spx_at_embargo_start:.2f}',
                xy=(embargo_start, spx_at_embargo_start),
                xytext=(10, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax1.annotate(f'禁运结束\nSPX: {spx_at_embargo_end:.2f}',
                xy=(embargo_end, spx_at_embargo_end),
                xytext=(10, -40), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax1.annotate(f'最低点\n{spx_min_date.strftime("%Y-%m-%d")}\nSPX: {spx_min_value:.2f}',
                xy=(spx_min_date, spx_min_value),
                xytext=(10, -60), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='orange', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # 设置标题
    plt.title('1973-1976年石油危机与标普500走势\n禁运结束后的市场表现', fontsize=16, fontweight='bold', pad=20)
    
    # 格式化X轴日期
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    # 添加图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'spx_oil_1973_1976.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存: {output_file}")
    
    # 打印统计数据
    print("\n" + "="*60)
    print("1973-1976年市场表现分析")
    print("="*60)
    
    print(f"\n【原油价格】")
    print(f"1973年初: ${oil_at_start:.2f}/桶")
    print(f"禁运开始 (1973-10-17): ${oil_at_embargo_start:.2f}/桶")
    print(f"禁运结束 (1974-03-18): ${oil_at_embargo_end:.2f}/桶")
    print(f"1976年底: ${oil_at_end:.2f}/桶")
    print(f"涨幅: {((oil_at_end / oil_at_start - 1) * 100):.1f}%")
    
    print(f"\n【标普500指数】")
    print(f"1973年初: {spx_at_start:.2f}点")
    print(f"禁运开始 (1973-10-17): {spx_at_embargo_start:.2f}点")
    print(f"禁运结束 (1974-03-18): {spx_at_embargo_end:.2f}点")
    print(f"最低点 ({spx_min_date.strftime('%Y-%m-%d')}): {spx_min_value:.2f}点")
    print(f"1976年底: {spx_at_end:.2f}点")
    
    print(f"\n【关键阶段表现】")
    embargo_decline = ((spx_at_embargo_end / spx_at_embargo_start - 1) * 100)
    print(f"禁运期间 (1973-10 至 1974-03): {embargo_decline:.1f}%")
    
    bottom_to_embargo_end = ((spx_min_value / spx_at_embargo_end - 1) * 100)
    print(f"禁运结束到最低点: {bottom_to_embargo_end:.1f}%")
    
    recovery = ((spx_at_end / spx_min_value - 1) * 100)
    print(f"从最低点到1976年底: {recovery:.1f}%")
    
    total_change = ((spx_at_end / spx_at_start - 1) * 100)
    print(f"整个时期 (1973-1976): {total_change:.1f}%")
    
    # 计算恢复到禁运前水平的时间
    recovery_date = spx_period[spx_period['Close'] >= spx_at_embargo_start].iloc[0]['Date']
    days_to_recover = (recovery_date - embargo_start).days
    print(f"\n【恢复时间】")
    print(f"恢复到禁运前水平: {recovery_date.strftime('%Y-%m-%d')}")
    print(f"用时: {days_to_recover}天 ({days_to_recover/365:.1f}年)")
    
    print("\n" + "="*60)
    
    plt.show()

if __name__ == "__main__":
    analyze_post_embargo()
