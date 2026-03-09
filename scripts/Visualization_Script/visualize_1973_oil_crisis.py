import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def load_data(filename):
    """加载CSV数据文件"""
    current_script_path = os.path.dirname(__file__)
    data_dir = os.path.join(current_script_path, "../../data")
    file_path = os.path.join(data_dir, filename)
    
    # 读取CSV文件，跳过Ticker行和Date标签行（第2行和第3行，索引为1和2）
    df = pd.read_csv(file_path, skiprows=[1, 2])
    
    # 第一列是Price列，实际上包含了日期数据
    # 重命名第一列为Date
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    
    # 转换Date列为datetime并设置为索引
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.set_index('Date', inplace=True)
    
    # 删除可能存在的空行
    df = df.dropna(how='all')
    
    # 转换数值列为float类型
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def analyze_1973_oil_crisis():
    """分析1973年石油危机期间原油价格与SPX的关系"""
    
    # 加载数据
    print("正在加载数据...")
    spx_data = load_data("^SPX.csv")
    oil_data = load_data("CL=F.csv")
    
    # 检查数据时间范围
    print(f"\nSPX数据时间范围: {spx_data.index.min()} 到 {spx_data.index.max()}")
    print(f"原油数据时间范围: {oil_data.index.min()} 到 {oil_data.index.max()}")
    
    # 筛选1973年数据
    spx_1973 = spx_data[spx_data.index.year == 1973].copy()
    oil_1973 = oil_data[oil_data.index.year == 1973].copy()
    
    if len(spx_1973) == 0:
        print("\n警告: SPX数据不包含1973年的数据")
        return
    
    if len(oil_1973) == 0:
        print("\n警告: 原油期货数据不包含1973年的数据")
        print("注意: WTI原油期货于1983年才在NYMEX上市，因此yfinance无法获取1973年的原油期货数据")
        print("建议使用历史原油现货价格数据进行分析")
        
        # 仍然可视化SPX在1973年的表现
        visualize_spx_1973(spx_1973)
        return
    
    # 如果有数据，进行对比分析
    visualize_oil_spx_comparison(oil_1973, spx_1973)

def visualize_spx_1973(spx_1973):
    """可视化1973年SPX的表现"""
    
    # 计算归一化价格（以年初为100）
    spx_normalized = (spx_1973['Close'] / spx_1973['Close'].iloc[0]) * 100
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 图1: SPX价格走势
    ax1.plot(spx_1973.index, spx_1973['Close'], 'b-', linewidth=2, label='SPX收盘价')
    ax1.set_title('1973年标普500指数走势\n(第一次石油危机期间)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('价格', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # 标注关键事件
    # 1973年10月6日 - 赎罪日战争爆发
    # 1973年10月17日 - OPEC宣布石油禁运
    ax1.axvline(pd.Timestamp('1973-10-06'), color='r', linestyle='--', alpha=0.7, label='赎罪日战争(10/6)')
    ax1.axvline(pd.Timestamp('1973-10-17'), color='darkred', linestyle='--', alpha=0.7, label='石油禁运(10/17)')
    ax1.legend(fontsize=10)
    
    # 图2: 归一化走势
    ax2.plot(spx_1973.index, spx_normalized, 'b-', linewidth=2, label='SPX (年初=100)')
    ax2.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('1973年标普500归一化走势 (年初=100)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('日期', fontsize=12)
    ax2.set_ylabel('归一化价格', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    
    # 标注关键事件
    ax2.axvline(pd.Timestamp('1973-10-06'), color='r', linestyle='--', alpha=0.7)
    ax2.axvline(pd.Timestamp('1973-10-17'), color='darkred', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.join(os.path.dirname(__file__), "../../screenshot")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "1973_oil_crisis_spx.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图表已保存到: {output_path}")
    
    # 计算统计数据
    print("\n=== 1973年SPX统计数据 ===")
    print(f"年初价格: {spx_1973['Close'].iloc[0]:.2f}")
    print(f"年末价格: {spx_1973['Close'].iloc[-1]:.2f}")
    year_return = ((spx_1973['Close'].iloc[-1] / spx_1973['Close'].iloc[0]) - 1) * 100
    print(f"全年回报率: {year_return:.2f}%")
    
    # 计算石油危机前后的表现
    pre_crisis = spx_1973[spx_1973.index < '1973-10-06']
    post_crisis = spx_1973[spx_1973.index >= '1973-10-06']
    
    if len(pre_crisis) > 0 and len(post_crisis) > 0:
        pre_return = ((pre_crisis['Close'].iloc[-1] / pre_crisis['Close'].iloc[0]) - 1) * 100
        post_return = ((post_crisis['Close'].iloc[-1] / post_crisis['Close'].iloc[0]) - 1) * 100
        print(f"\n危机前回报率 (1月-10月初): {pre_return:.2f}%")
        print(f"危机后回报率 (10月初-年末): {post_return:.2f}%")
    
    plt.show()

def visualize_oil_spx_comparison(oil_1973, spx_1973):
    """可视化原油价格与SPX的对比"""
    
    # 计算归一化价格（以年初为100）
    oil_normalized = (oil_1973['Close'] / oil_1973['Close'].iloc[0]) * 100
    spx_normalized = (spx_1973['Close'] / spx_1973['Close'].iloc[0]) * 100
    
    # 创建图表
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # 图1: 原油价格走势
    axes[0].plot(oil_1973.index, oil_1973['Close'], 'orange', linewidth=2, label='WTI原油')
    axes[0].set_title('1973年WTI原油价格走势', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('价格 (美元/桶)', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=10)
    
    # 图2: SPX价格走势
    axes[1].plot(spx_1973.index, spx_1973['Close'], 'b-', linewidth=2, label='SPX')
    axes[1].set_title('1973年标普500指数走势', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('价格', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(fontsize=10)
    
    # 图3: 归一化对比
    axes[2].plot(oil_normalized.index, oil_normalized, 'orange', linewidth=2, label='原油 (年初=100)')
    axes[2].plot(spx_normalized.index, spx_normalized, 'b-', linewidth=2, label='SPX (年初=100)')
    axes[2].axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    axes[2].set_title('1973年原油与SPX归一化对比 (年初=100)', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('日期', fontsize=12)
    axes[2].set_ylabel('归一化价格', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    output_dir = os.path.join(os.path.dirname(__file__), "../../screenshot")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "1973_oil_vs_spx.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图表已保存到: {output_path}")
    
    # 计算相关性
    correlation = oil_normalized.corr(spx_normalized)
    print(f"\n1973年原油与SPX的相关系数: {correlation:.4f}")
    
    plt.show()

if __name__ == "__main__":
    analyze_1973_oil_crisis()
