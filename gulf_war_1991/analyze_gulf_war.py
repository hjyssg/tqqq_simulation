import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def load_stock_data(ticker):
    """加载股票数据"""
    file_path = os.path.join(os.path.dirname(__file__), f"../data/{ticker}.csv")
    df = pd.read_csv(file_path, skiprows=[1, 2])
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.set_index('Date', inplace=True)
    df = df.dropna(how='all')
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def analyze_gulf_war():
    """分析1991年海湾战争期间美股表现"""
    
    print("="*80)
    print("1991年海湾战争期间美股表现分析")
    print("Gulf War Stock Market Analysis (1990-1991)")
    print("="*80)
    
    # 加载数据分析标普500
    print("\n正在加载数据...")
    spx_data = load_stock_data("^SPX")
    ndx_data = load_stock_data("^NDX")  # 保留用于文本分析
    
    # 定义分析时间段：从入侵前2个月到战争结束后2个月
    start_date = '1990-06-01'
    end_date = '1991-04-30'
    
    spx_period = spx_data[start_date:end_date].copy()
    ndx_period = ndx_data[start_date:end_date].copy()
    
    print(f"SPX数据点数: {len(spx_period)}")
    
    # 创建单Y轴图表
    fig, ax1 = plt.subplots(figsize=(18, 10))
    
    # 绘制SPX
    color_spx = 'steelblue'
    ax1.plot(spx_period.index, spx_period['Close'], color=color_spx, linewidth=2.5, label='标普500 (SPX)', alpha=0.9)
    ax1.set_xlabel('日期', fontsize=14, fontweight='bold')
    ax1.set_ylabel('标普500指数', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='y', labelsize=11)
    ax1.tick_params(axis='x', labelsize=11)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # 标注关键历史事件
    events = [
        ('1990-08-02', '伊拉克入侵科威特\n油价暴涨 股市下跌', 'red', 0.95),
        ('1991-01-17', '沙漠风暴行动开始\n空袭阶段', 'orange', 0.85),
        ('1991-02-24', '地面进攻开始', 'purple', 0.75),
        ('1991-02-28', '战争结束\n(100小时地面战)', 'green', 0.65)
    ]
    
    y_min, y_max = ax1.get_ylim()
    for date, label, color, y_pos in events:
        ax1.axvline(pd.Timestamp(date), color=color, linestyle='--', linewidth=2, alpha=0.7)
        ax1.text(pd.Timestamp(date), y_min + (y_max - y_min) * y_pos, label, 
                rotation=0, verticalalignment='top', horizontalalignment='center',
                fontsize=10, color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=color, alpha=0.9))
    
    # 设置标题
    plt.title('1991年海湾战争期间标普500走势\nS&P 500 Performance during Gulf War (1990-1991)', 
              fontsize=16, fontweight='bold', pad=20)
    
    # 设置图例
    ax1.legend(loc='upper left', fontsize=12, framealpha=0.9)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "gulf_war_stock_performance.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ 图表已保存到: {output_path}")
    
    # ==================== 统计分析 ====================
    print("\n" + "="*80)
    print("详细统计分析")
    print("="*80)
    
    # 定义关键时间点
    invasion_date = '1990-08-02'
    air_strike_date = '1991-01-17'
    ground_war_date = '1991-02-24'
    war_end_date = '1991-02-28'
    
    # 获取各时间点的价格
    def get_closest_price(df, date):
        """获取最接近指定日期的价格"""
        target = pd.Timestamp(date)
        idx = df.index.get_indexer([target], method='nearest')[0]
        return df.iloc[idx]['Close'], df.index[idx]
    
    # SPX关键价格点
    spx_pre_invasion, spx_pre_invasion_date = get_closest_price(spx_period, '1990-08-01')
    spx_invasion, spx_invasion_date = get_closest_price(spx_period, invasion_date)
    spx_air_strike, spx_air_strike_date = get_closest_price(spx_period, air_strike_date)
    spx_ground_war, spx_ground_war_date = get_closest_price(spx_period, ground_war_date)
    spx_war_end, spx_war_end_date = get_closest_price(spx_period, war_end_date)
    spx_post_war, spx_post_war_date = get_closest_price(spx_period, '1991-03-31')
    
    # NDX关键价格点
    ndx_pre_invasion, _ = get_closest_price(ndx_period, '1990-08-01')
    ndx_invasion, _ = get_closest_price(ndx_period, invasion_date)
    ndx_air_strike, _ = get_closest_price(ndx_period, air_strike_date)
    ndx_ground_war, _ = get_closest_price(ndx_period, ground_war_date)
    ndx_war_end, _ = get_closest_price(ndx_period, war_end_date)
    ndx_post_war, _ = get_closest_price(ndx_period, '1991-03-31')
    
    # 打印SPX分析
    print("\n【标普500指数 (SPX) 表现】")
    print("-" * 80)
    print(f"入侵前 ({spx_pre_invasion_date.date()}): {spx_pre_invasion:.2f}")
    print(f"入侵时 ({spx_invasion_date.date()}): {spx_invasion:.2f}")
    print(f"空袭开始 ({spx_air_strike_date.date()}): {spx_air_strike:.2f}")
    print(f"地面战开始 ({spx_ground_war_date.date()}): {spx_ground_war:.2f}")
    print(f"战争结束 ({spx_war_end_date.date()}): {spx_war_end:.2f}")
    print(f"战后一个月 ({spx_post_war_date.date()}): {spx_post_war:.2f}")
    
    print(f"\n阶段涨跌幅：")
    print(f"  入侵后初期反应 (8月-12月): {((spx_air_strike / spx_invasion) - 1) * 100:+.2f}%")
    print(f"  空袭阶段 (1月17日-2月24日): {((spx_ground_war / spx_air_strike) - 1) * 100:+.2f}%")
    print(f"  地面战期间 (2月24日-2月28日): {((spx_war_end / spx_ground_war) - 1) * 100:+.2f}%")
    print(f"  战争结束后一个月: {((spx_post_war / spx_war_end) - 1) * 100:+.2f}%")
    print(f"\n整体表现：")
    print(f"  入侵到战争结束: {((spx_war_end / spx_invasion) - 1) * 100:+.2f}%")
    print(f"  空袭开始到战争结束: {((spx_war_end / spx_air_strike) - 1) * 100:+.2f}%")
    
    # 打印NDX分析
    print("\n【纳斯达克100指数 (NDX) 表现】")
    print("-" * 80)
    print(f"入侵前: {ndx_pre_invasion:.2f}")
    print(f"入侵时: {ndx_invasion:.2f}")
    print(f"空袭开始: {ndx_air_strike:.2f}")
    print(f"地面战开始: {ndx_ground_war:.2f}")
    print(f"战争结束: {ndx_war_end:.2f}")
    print(f"战后一个月: {ndx_post_war:.2f}")
    
    print(f"\n阶段涨跌幅：")
    print(f"  入侵后初期反应 (8月-12月): {((ndx_air_strike / ndx_invasion) - 1) * 100:+.2f}%")
    print(f"  空袭阶段 (1月17日-2月24日): {((ndx_ground_war / ndx_air_strike) - 1) * 100:+.2f}%")
    print(f"  地面战期间 (2月24日-2月28日): {((ndx_war_end / ndx_ground_war) - 1) * 100:+.2f}%")
    print(f"  战争结束后一个月: {((ndx_post_war / ndx_war_end) - 1) * 100:+.2f}%")
    print(f"\n整体表现：")
    print(f"  入侵到战争结束: {((ndx_war_end / ndx_invasion) - 1) * 100:+.2f}%")
    print(f"  空袭开始到战争结束: {((ndx_war_end / ndx_air_strike) - 1) * 100:+.2f}%")
    
    # 验证"战争期间上涨约10%"的说法
    print("\n" + "="*80)
    print("【验证结论】")
    print("="*80)
    
    spx_war_period_change = ((spx_war_end / spx_air_strike) - 1) * 100
    ndx_war_period_change = ((ndx_war_end / ndx_air_strike) - 1) * 100
    
    print(f"\n从空袭开始(1991-01-17)到战争结束(1991-02-28)：")
    print(f"  SPX涨幅: {spx_war_period_change:+.2f}%")
    print(f"  NDX涨幅: {ndx_war_period_change:+.2f}%")
    
    if spx_war_period_change > 8 and spx_war_period_change < 12:
        print(f"\n✓ 验证通过：SPX在战争期间确实上涨约10%")
    else:
        print(f"\n✗ 与预期有差异：SPX实际涨幅为{spx_war_period_change:.2f}%")
    
    # 找出最低点
    spx_min_idx = spx_period.loc[invasion_date:war_end_date]['Close'].idxmin()
    spx_min_value = spx_period.loc[spx_min_idx]['Close']
    spx_max_drawdown = ((spx_min_value / spx_invasion) - 1) * 100
    
    print(f"\n【风险分析】")
    print(f"SPX最大回撤: {spx_max_drawdown:.2f}% (发生在 {spx_min_idx.date()})")
    print(f"从最低点到战争结束的反弹: {((spx_war_end / spx_min_value) - 1) * 100:+.2f}%")
    
    print("\n" + "="*80)
    print("分析完成！")
    print("="*80)
    
    # 保存分析报告
    report_path = os.path.join(output_dir, "分析报告.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 1991年海湾战争美股表现分析报告\n\n")
        f.write("## Gulf War Stock Market Analysis Report\n\n")
        f.write("---\n\n")
        
        f.write("## 📅 关键时间线\n\n")
        f.write("| 日期 | 事件 |\n")
        f.write("|------|------|\n")
        f.write("| 1990年8月2日 | 伊拉克入侵科威特，油价暴涨，股市下跌 |\n")
        f.write("| 1991年1月17日 | 沙漠风暴行动开始（空袭阶段） |\n")
        f.write("| 1991年2月24日 | 地面进攻开始 |\n")
        f.write("| 1991年2月28日 | 战争结束（100小时地面战） |\n\n")
        
        f.write("## 📊 标普500指数 (SPX) 表现\n\n")
        f.write(f"- **入侵前** ({spx_pre_invasion_date.date()}): {spx_pre_invasion:.2f}\n")
        f.write(f"- **入侵时** ({spx_invasion_date.date()}): {spx_invasion:.2f}\n")
        f.write(f"- **空袭开始** ({spx_air_strike_date.date()}): {spx_air_strike:.2f}\n")
        f.write(f"- **地面战开始** ({spx_ground_war_date.date()}): {spx_ground_war:.2f}\n")
        f.write(f"- **战争结束** ({spx_war_end_date.date()}): {spx_war_end:.2f}\n")
        f.write(f"- **战后一个月** ({spx_post_war_date.date()}): {spx_post_war:.2f}\n\n")
        
        f.write("### 阶段涨跌幅\n\n")
        f.write(f"- 入侵后初期反应 (8月-1月): **{((spx_air_strike / spx_invasion) - 1) * 100:+.2f}%**\n")
        f.write(f"- 空袭阶段 (1月17日-2月24日): **{((spx_ground_war / spx_air_strike) - 1) * 100:+.2f}%**\n")
        f.write(f"- 地面战期间 (2月24日-2月28日): **{((spx_war_end / spx_ground_war) - 1) * 100:+.2f}%**\n")
        f.write(f"- 战争结束后一个月: **{((spx_post_war / spx_war_end) - 1) * 100:+.2f}%**\n\n")
        
        f.write("### 整体表现\n\n")
        f.write(f"- 入侵到战争结束: **{((spx_war_end / spx_invasion) - 1) * 100:+.2f}%**\n")
        f.write(f"- 空袭开始到战争结束: **{((spx_war_end / spx_air_strike) - 1) * 100:+.2f}%**\n\n")
        
        f.write("## 📈 纳斯达克100指数 (NDX) 表现\n\n")
        f.write(f"- **入侵前**: {ndx_pre_invasion:.2f}\n")
        f.write(f"- **入侵时**: {ndx_invasion:.2f}\n")
        f.write(f"- **空袭开始**: {ndx_air_strike:.2f}\n")
        f.write(f"- **地面战开始**: {ndx_ground_war:.2f}\n")
        f.write(f"- **战争结束**: {ndx_war_end:.2f}\n")
        f.write(f"- **战后一个月**: {ndx_post_war:.2f}\n\n")
        
        f.write("### 阶段涨跌幅\n\n")
        f.write(f"- 入侵后初期反应 (8月-1月): **{((ndx_air_strike / ndx_invasion) - 1) * 100:+.2f}%**\n")
        f.write(f"- 空袭阶段 (1月17日-2月24日): **{((ndx_ground_war / ndx_air_strike) - 1) * 100:+.2f}%**\n")
        f.write(f"- 地面战期间 (2月24日-2月28日): **{((ndx_war_end / ndx_ground_war) - 1) * 100:+.2f}%**\n")
        f.write(f"- 战争结束后一个月: **{((ndx_post_war / ndx_war_end) - 1) * 100:+.2f}%**\n\n")
        
        f.write("### 整体表现\n\n")
        f.write(f"- 入侵到战争结束: **{((ndx_war_end / ndx_invasion) - 1) * 100:+.2f}%**\n")
        f.write(f"- 空袭开始到战争结束: **{((ndx_war_end / ndx_air_strike) - 1) * 100:+.2f}%**\n\n")
        
        f.write("## ✅ 验证结论\n\n")
        f.write(f"**从空袭开始(1991-01-17)到战争结束(1991-02-28)：**\n\n")
        f.write(f"- SPX涨幅: **{spx_war_period_change:+.2f}%**\n")
        f.write(f"- NDX涨幅: **{ndx_war_period_change:+.2f}%**\n\n")
        
        if spx_war_period_change > 8 and spx_war_period_change < 12:
            f.write(f"✓ **验证通过**：SPX在战争期间确实上涨约10%\n\n")
        else:
            f.write(f"✗ **与预期有差异**：SPX实际涨幅为{spx_war_period_change:.2f}%\n\n")
        
        f.write("## ⚠️ 风险分析\n\n")
        f.write(f"- SPX最大回撤: **{spx_max_drawdown:.2f}%** (发生在 {spx_min_idx.date()})\n")
        f.write(f"- 从最低点到战争结束的反弹: **{((spx_war_end / spx_min_value) - 1) * 100:+.2f}%**\n\n")
        
        f.write("## 💡 关键发现\n\n")
        f.write("1. **初期恐慌**：伊拉克入侵科威特后，市场出现明显下跌\n")
        f.write("2. **战争开始后反转**：当美军开始空袭后，市场信心恢复\n")
        f.write("3. **快速结束利好**：100小时地面战的快速胜利提振了市场\n")
        f.write("4. **不确定性消除**：战争结束后，市场继续上涨\n\n")
        
        f.write("---\n\n")
        f.write("*分析基于历史数据，仅供参考*\n")
    
    print(f"✓ 分析报告已保存到: {report_path}")
    
    plt.show()

if __name__ == "__main__":
    analyze_gulf_war()
