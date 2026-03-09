import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def load_spx_data():
    """加载SPX数据"""
    file_path = os.path.join(os.path.dirname(__file__), "../data/^SPX.csv")
    df = pd.read_csv(file_path, skiprows=[1, 2])
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.set_index('Date', inplace=True)
    df = df.dropna(how='all')
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def load_oil_data():
    """加载FRED原油数据"""
    file_path = os.path.join(os.path.dirname(__file__), "../data/WTISPLC Spot Crude Oil Price West Texas Intermediate (WTI) (WTISPLC).csv")
    df = pd.read_csv(file_path)
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    df.set_index('observation_date', inplace=True)
    return df

def analyze_oil_crisis_1972_1974():
    """分析1972-1974年石油危机期间原油价格与SPX的关系"""
    
    print("正在加载数据...")
    spx_data = load_spx_data()
    oil_data = load_oil_data()
    
    # 筛选1973年5月-1974年3月数据（包含禁运结束）
    start_date = '1973-05-01'
    end_date = '1974-03-31'
    
    spx_period = spx_data[start_date:end_date].copy()
    oil_period = oil_data[start_date:end_date].copy()
    
    print(f"\nSPX数据点数: {len(spx_period)}")
    print(f"原油数据点数: {len(oil_period)}")
    
    # 创建单Y轴图表 - 只显示SPX
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 绘制SPX
    color_spx = 'steelblue'
    ax.plot(spx_period.index, spx_period['Close'], color=color_spx, linewidth=3, label='标普500指数')
    ax.set_xlabel('日期', fontsize=14, fontweight='bold')
    ax.set_ylabel('标普500指数', fontsize=14, fontweight='bold')
    ax.tick_params(axis='both', labelsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 标注关键历史事件 - 调整位置避免重叠
    events = [
        ('1973-10-06', '赎罪日战争', 'red', 0.92),
        ('1973-10-17', 'OPEC石油禁运', 'darkred', 0.85),
        ('1974-03-18', '石油禁运结束', 'green', 0.78)
    ]
    
    y_min, y_max = ax.get_ylim()
    for date, label, color, y_pos in events:
        ax.axvline(pd.Timestamp(date), color=color, linestyle='--', linewidth=2, alpha=0.7)
        # 使用不同的y位置避免重叠
        ax.text(pd.Timestamp(date), y_min + (y_max - y_min) * y_pos, label, 
                rotation=0, verticalalignment='top', horizontalalignment='center',
                fontsize=11, color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=color, alpha=0.9))
    
    # 设置标题
    plt.title('1973年石油危机期间标普500指数走势\n(1973年5月-1974年3月)', 
              fontsize=16, fontweight='bold', pad=20)
    
    # 图例
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "oil_spx_dual_axis_1972_1974.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图表已保存到: {output_path}")
    
    # 计算统计数据
    print("\n" + "="*60)
    print("统计分析 (1973年5月-1974年1月)")
    print("="*60)
    
    # 原油价格变化
    oil_period_start = oil_period.iloc[0]['WTISPLC']
    oil_1973_oct = oil_period.loc['1973-10-01', 'WTISPLC']
    oil_1974_jan = oil_period.loc['1974-01-01', 'WTISPLC']
    oil_period_end = oil_period.iloc[-1]['WTISPLC']
    
    print(f"\n【原油价格】")
    print(f"1973年5月: ${oil_period_start:.2f}/桶")
    print(f"1973年10月(禁运前): ${oil_1973_oct:.2f}/桶")
    print(f"1974年1月: ${oil_1974_jan:.2f}/桶")
    print(f"\n5月到10月涨幅: {((oil_1973_oct / oil_period_start) - 1) * 100:.1f}%")
    print(f"禁运期间涨幅(10月-1月): {((oil_1974_jan / oil_1973_oct) - 1) * 100:.1f}%")
    print(f"整体涨幅(5月-1月): {((oil_period_end / oil_period_start) - 1) * 100:.1f}%")
    
    # SPX变化
    spx_period_start = spx_period.iloc[0]['Close']
    spx_1973_oct = spx_period.loc[spx_period.index <= '1973-10-06'].iloc[-1]['Close']
    spx_1974_jan = spx_period.iloc[-1]['Close']
    
    print(f"\n【标普500指数】")
    print(f"1973年5月: {spx_period_start:.2f}")
    print(f"1973年10月(禁运前): {spx_1973_oct:.2f}")
    print(f"1974年1月: {spx_1974_jan:.2f}")
    print(f"\n5月到10月变化: {((spx_1973_oct / spx_period_start) - 1) * 100:.1f}%")
    print(f"禁运期间跌幅(10月-1月): {((spx_1974_jan / spx_1973_oct) - 1) * 100:.1f}%")
    print(f"整体跌幅(5月-1月): {((spx_1974_jan / spx_period_start) - 1) * 100:.1f}%")
    
    # 计算相关性（使用月度数据）
    # 重采样为月度数据以匹配原油数据频率
    spx_monthly = spx_period['Close'].resample('MS').last()
    oil_monthly = oil_period['WTISPLC'].resample('MS').last()
    
    # 对齐数据
    common_dates = spx_monthly.index.intersection(oil_monthly.index)
    spx_aligned = spx_monthly.loc[common_dates]
    oil_aligned = oil_monthly.loc[common_dates]
    
    # 计算收益率
    spx_returns = spx_aligned.pct_change().dropna()
    oil_returns = oil_aligned.pct_change().dropna()
    
    # 对齐收益率数据
    common_return_dates = spx_returns.index.intersection(oil_returns.index)
    correlation = spx_returns.loc[common_return_dates].corr(oil_returns.loc[common_return_dates])
    
    print(f"\n【相关性分析】")
    print(f"月度收益率相关系数: {correlation:.4f}")
    if correlation < -0.3:
        print("结论: 原油价格上涨与股市下跌呈现明显负相关")
    elif correlation > 0.3:
        print("结论: 原油价格上涨与股市上涨呈现正相关")
    else:
        print("结论: 原油价格与股市相关性较弱")
    
    print("\n" + "="*60)
    
    plt.show()

if __name__ == "__main__":
    analyze_oil_crisis_1972_1974()
