"""
日经 vs 纳指：如果美国也经历"失去的三十年"
===========================================
分析维度：
1. 路径对齐：N225从1989年高点 vs NDX从2021年高点
2. 如果NDX复制日经路径，TQQQ会怎样？
3. 估值对比：两个时期的基本面差异
4. TQQQ在日经路径下的模拟表现
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR = Path('data')


def load_data():
    """加载日经和纳指数据"""
    
    def load_index(path, name):
        df = pd.read_csv(path)
        first_col = df.columns[0]
        if first_col == 'Price':
            df = df.iloc[2:].copy()
            df.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        elif first_col == 'Date':
            pass
        else:
            raise ValueError(f"Unknown column format for {name}: {first_col}")
        
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        df.set_index('Date', inplace=True)
        df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
        return df.sort_index()
    
    # 加载数据
    n225 = load_index(DATA_DIR / '^N225.csv', 'N225')
    ndx = load_index(DATA_DIR / '^NDX.csv', 'NDX')
    spx = load_index(DATA_DIR / '^SPX.csv', 'SPX')
    tqqq = load_index(DATA_DIR / 'TQQQ.csv', 'TQQQ')
    qqq = pd.read_csv(DATA_DIR / 'QQQ.csv')
    qqq = qqq.iloc[2:].copy()
    qqq.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    qqq['Date'] = pd.to_datetime(qqq['Date'])
    qqq.set_index('Date', inplace=True)
    qqq['Adj Close'] = pd.to_numeric(qqq['Adj Close'], errors='coerce')
    qqq = qqq.sort_index()
    
    return n225, ndx, spx, tqqq, qqq


def align_paths(n225, ndx):
    """
    路径对齐：将日经从1989年高点开始的路径，对齐到纳指从2021年高点
    """
    # 日经高点：1989-12-29
    n225_peak = n225.loc['1989-01-01':'1990-12-31']['Adj Close'].max()
    n225_peak_date = n225.loc['1989-01-01':'1990-12-31']['Adj Close'].idxmax()
    print(f"日经高点: {n225_peak_date.date()} @ {n225_peak:.0f}")
    
    # 纳指高点：2021-11-19（约）
    ndx_peak_date = '2021-11-19'
    ndx_peak = ndx.loc[ndx_peak_date]['Adj Close']
    print(f"纳指高点: {ndx_peak_date} @ {ndx_peak:.0f}")
    
    # 日经从高点后的数据
    n225_after = n225.loc[n225_peak_date:].copy()
    n225_after['normalized'] = n225_after['Adj Close'] / n225_peak * 100
    
    # 纳指从高点后的数据  
    ndx_after = ndx.loc[ndx_peak_date:].copy()
    ndx_after['normalized'] = ndx_after['Adj Close'] / ndx_peak * 100
    
    # 计算时间对齐（交易日）
    n225_days = (n225_after.index - n225_peak_date).days
    ndx_days = (ndx_after.index - pd.Timestamp(ndx_peak_date)).days
    
    n225_after['days_since_peak'] = n225_days
    ndx_after['days_since_peak'] = ndx_days
    
    print(f"\n日经从高点至今: {n225_after.index[-1].date()} ({n225_after['normalized'].iloc[-1]:.1f}% of peak)")
    print(f"纳指从高点至今: {ndx_after.index[-1].date()} ({ndx_after['normalized'].iloc[-1]:.1f}% of peak)")
    
    # 日经的"失去的十年"（1989→1999）
    n225_decade = n225_after[n225_after['days_since_peak'] <= 3650]  # 10年
    # 日经的"失去的三十年"（1989→2019）
    n225_three_decades = n225_after[n225_after['days_since_peak'] <= 10950]  # 30年
    
    return n225_after, ndx_after, n225_peak, ndx_peak, n225_peak_date, ndx_peak_date


def plot_path_comparison(n225_after, ndx_after, n225_peak_date, ndx_peak_date):
    """绘制路径对比图"""
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 14))
    
    # 图1：按天数对齐
    ax = axes[0]
    ax.plot(n225_after['days_since_peak'] / 365, n225_after['normalized'], 
            color='#D32F2F', linewidth=1.5, label='日经225 (1989→)')
    ax.plot(ndx_after['days_since_peak'] / 365, ndx_after['normalized'], 
            color='#1976D2', linewidth=1.5, label='纳斯达克100 (2021→)', alpha=0.8)
    ax.axhline(100, color='gray', linestyle='--', alpha=0.5, label='峰值')
    ax.axhline(50, color='red', linestyle=':', alpha=0.3, label='腰斩线')
    
    # 标注关键位置
    ax.annotate('日经峰值\n1989', xy=(0, 100), xytext=(0.5, 105),
                fontsize=9, color='#D32F2F', fontweight='bold')
    bottom_x = (n225_after['normalized'].idxmin() - n225_after.index[0]).days / 365
    bottom_y = n225_after['normalized'].min()
    ax.annotate('日经底部\n(2009年3月)', 
                xy=(bottom_x, bottom_y),
                fontsize=9, color='#D32F2F')
    
    # 在横轴上标注时间
    for year in range(0, 35, 5):
        ax.axvline(year, color='gray', linestyle=':', alpha=0.2)
    
    ax.set_xlabel('从峰值经过的年数', fontsize=12)
    ax.set_ylabel('峰值百分比 (%)', fontsize=12)
    ax.set_title('日经失去的三十年 vs 纳指当前路径', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, max(n225_after['days_since_peak'].max() / 365, 
                       ndx_after['days_since_peak'].max() / 365))
    
    # 图2：按日历时间
    ax = axes[1]
    
    # 日经数据
    n225_plot = n225_after.copy()
    n225_plot.index = n225_peak_date + pd.to_timedelta(n225_plot['days_since_peak'], unit='D')
    ax.plot(n225_plot.index, n225_plot['normalized'], 
            color='#D32F2F', linewidth=1.5, label='日经225 (1989→2019, 峰值对齐)')
    
    # 纳指数据（实际时间）
    ax.plot(ndx_after.index, ndx_after['normalized'], 
            color='#1976D2', linewidth=1.5, label='纳斯达克100 (实际时间)')
    
    ax.axhline(100, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(50, color='red', linestyle=':', alpha=0.3)
    
    # 标注关键事件
    events = [
        (pd.Timestamp('1990-01-01'), '泡沫破裂', '#D32F2F'),
        (pd.Timestamp('1997-01-01'), '亚洲金融\n危机', '#FF9800'),
        (pd.Timestamp('2000-01-01'), '互联网\n泡沫', '#FF9800'),
        (pd.Timestamp('2008-01-01'), '全球金融\n危机', '#D32F2F'),
        (pd.Timestamp('2011-01-01'), '福岛\n核灾', '#FF9800'),
        (pd.Timestamp('2022-01-01'), '美联储\n加息', '#1976D2'),
    ]
    for date, label, color in events:
        ax.axvline(date, color=color, linestyle=':', alpha=0.3)
        ax.text(date, 5, label, fontsize=7, color=color, ha='center', rotation=90)
    
    ax.set_xlabel('日历时间', fontsize=12)
    ax.set_ylabel('峰值百分比 (%)', fontsize=12)
    ax.set_title('当日经路径"平移"到纳指时间轴上', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '01_path_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 路径对比图已保存")


def simulate_tqqq_on_japan_path(n225_after, ndx, tqqq, qqq, ndx_peak, ndx_peak_date):
    """
    如果NDX复制日经路径，模拟TQQQ的表现
    """
    
    # 日经从峰值开始的累计涨跌幅（对数）
    n225_cumret = n225_after['Adj Close'] / n225_after['Adj Close'].iloc[0]
    
    # 纳指从2021-11-19开始的模拟路径
    # 将日经的累计收益映射到纳指
    ndx_simulated = ndx_peak * n225_cumret.values
    ndx_simulated = pd.Series(ndx_simulated, index=n225_after.index)
    # 将时间索引改为从2021-11-19开始
    ndx_sim_dates = pd.date_range(ndx_peak_date, periods=len(ndx_simulated), freq='B')
    ndx_simulated.index = ndx_sim_dates[:len(ndx_simulated)]
    
    # 模拟TQQQ在日经路径下的表现
    # 计算日经每日涨跌幅
    daily_ret = n225_after['Adj Close'].pct_change().dropna()
    
    # TQQQ日收益 = 3x 日经日收益（考虑衰减）
    # 但这里我们直接用日经路径模拟，所以TQQQ = 3x 日经的日收益复利
    tqqq_sim = [1.0]
    for ret in daily_ret.values:
        tqqq_sim.append(tqqq_sim[-1] * (1 + 3 * ret))
    tqqq_sim = pd.Series(tqqq_sim[1:], index=daily_ret.index)
    # 将时间索引重新映射
    tqqq_sim.index = ndx_sim_dates[:len(tqqq_sim)]
    
    # 归一化到100
    ndx_sim_norm = ndx_simulated / ndx_simulated.iloc[0] * 100
    tqqq_sim_norm = tqqq_sim / tqqq_sim.iloc[0] * 100
    
    # 实际NDX和TQQQ表现
    ndx_actual = ndx.loc[ndx_peak_date:].copy()
    ndx_actual_norm = ndx_actual['Adj Close'] / ndx_actual['Adj Close'].iloc[0] * 100
    
    tqqq_actual = tqqq.loc[ndx_peak_date:].copy()
    tqqq_actual_norm = tqqq_actual['Adj Close'] / tqqq_actual['Adj Close'].iloc[0] * 100
    
    # 对齐到天数
    ndx_sim_days = np.arange(len(ndx_sim_norm))
    ndx_actual_days = np.arange(len(ndx_actual_norm))
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))
    
    # 图1：NDX模拟 vs 实际
    ax = axes[0]
    ax.plot(ndx_sim_days, ndx_sim_norm.values, color='#D32F2F', linewidth=1.5, 
            label='NDX 模拟 (复制日经路径)')
    ax.plot(ndx_actual_days, ndx_actual_norm.values, color='#1976D2', linewidth=1.5, 
            label='NDX 实际', alpha=0.8)
    ax.axhline(100, color='gray', linestyle='--', alpha=0.5, label='起始点')
    ax.set_xlabel('从峰值经过的交易日', fontsize=12)
    ax.set_ylabel('归一化价格 (起点=100)', fontsize=12)
    ax.set_title('如果真的失去三十年：NDX实际 vs 日经路径模拟', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 标注最终结果
    final_sim = ndx_sim_norm.iloc[-1]
    final_actual = ndx_actual_norm.iloc[-1]
    ax.text(0.98, 0.95, f"模拟终点: {final_sim:.1f}\n实际终点: {final_actual:.1f}", 
            transform=ax.transAxes, fontsize=10, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 图2：TQQQ模拟 vs 实际
    ax = axes[1]
    
    # 确保长度一致用于绘图
    min_len = min(len(tqqq_sim_norm), len(tqqq_actual_norm))
    ax.plot(range(min_len), tqqq_sim_norm.values[:min_len], color='#D32F2F', linewidth=1.5,
            label='TQQQ 模拟 (3x日经路径)')
    ax.plot(range(min_len), tqqq_actual_norm.values[:min_len], color='#2E86AB', linewidth=1.5,
            label='TQQQ 实际', alpha=0.8)
    ax.axhline(100, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(0, color='black', linestyle='-', alpha=0.3)
    
    # 标注腰斩线
    for level, label in [(50, '-50%'), (25, '-75%'), (10, '-90%')]:
        ax.axhline(level, color='red', linestyle=':', alpha=0.2)
        ax.text(0, level, label, fontsize=8, color='red')
    
    ax.set_xlabel('从峰值经过的交易日', fontsize=12)
    ax.set_ylabel('归一化价格 (起点=100)', fontsize=12)
    ax.set_title('TQQQ在日经路径下的模拟表现', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 关键数字
    if len(tqqq_sim_norm) > 0 and len(tqqq_actual_norm) > 0:
        tqqq_final_sim = tqqq_sim_norm.iloc[-1]
        tqqq_final_actual = tqqq_actual_norm.iloc[-1]
        tqqq_min_sim = tqqq_sim_norm.min()
        tqqq_min_actual = tqqq_actual_norm.min()
        
        stats = (
            f"【模拟日经路径】\n"
            f"TQQQ最终: {tqqq_final_sim:.1f} (较起点{tqqq_final_sim-100:.1f}%)\n"
            f"最大回撤: {tqqq_min_sim-100:.1f}%\n\n"
            f"【实际表现】\n"
            f"TQQQ最终: {tqqq_final_actual:.1f} (较起点{tqqq_final_actual-100:.1f}%)\n"
            f"最大回撤: {tqqq_min_actual-100:.1f}%"
        )
        ax.text(0.98, 0.05, stats, transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '02_tqqq_simulation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] TQQQ模拟图已保存")
    
    return ndx_simulated, tqqq_sim, ndx_actual, tqqq_actual


def compare_valuation(n225, ndx):
    """对比估值和宏观环境"""
    
    # 日本1989年泡沫数据
    # 日本1989年：PE ~60x, PB ~5x, GDP增长率 ~5%
    # 美国2021年：NDX PE ~35x, 但2022加息后已大幅调整
    
    japan_bubble = {
        'period': '日本泡沫 1989',
        'peak_pe': 60,
        'peak_pb': 5.0,
        'gdp_growth': 5.0,
        'interest_rate': 6.0,
        'inflation': 3.0,
        'demographics': '老龄化加速',
        'global_position': '世界第二大经济体'
    }
    
    us_current = {
        'period': '美国现在 2021-2022',
        'peak_pe': 35,
        'peak_pb': 4.0,
        'gdp_growth': 5.7,
        'interest_rate': 0.25,
        'inflation': 7.0,
        'demographics': '相对健康',
        'global_position': '世界第一大经济体'
    }
    
    # 当前纳指从高点回撤情况
    ndx_peak = ndx.loc['2021-11-19']['Adj Close'] if '2021-11-19' in ndx.index else ndx.max()
    ndx_current = ndx['Adj Close'].iloc[-1]
    drawdown = (ndx_current / ndx_peak - 1) * 100
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # 图1：估值对比雷达图（简化版，用柱状图）
    ax = axes[0]
    categories = ['峰值PE', '峰值PB', 'GDP增速', '利率', '通胀']
    japan_vals = [japan_bubble['peak_pe'], japan_bubble['peak_pb'], 
                  japan_bubble['gdp_growth'], japan_bubble['interest_rate'],
                  japan_bubble['inflation']]
    us_vals = [us_current['peak_pe'], us_current['peak_pb'],
               us_current['gdp_growth'], us_current['interest_rate'],
               us_current['inflation']]
    
    x = np.arange(len(categories))
    width = 0.35
    bars1 = ax.bar(x - width/2, japan_vals, width, color='#D32F2F', alpha=0.8, label='日本1989')
    bars2 = ax.bar(x + width/2, us_vals, width, color='#1976D2', alpha=0.8, label='美国2021-22')
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylabel('数值', fontsize=12)
    ax.set_title('泡沫时期宏观指标对比', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # 在柱子上标注数值
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.0f}', ha='center', va='bottom', fontsize=9, color='#D32F2F')
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.0f}', ha='center', va='bottom', fontsize=9, color='#1976D2')
    
    # 图2：关键差异
    ax = axes[1]
    differences = [
        'PE: 日本60x vs 美国35x\n(日本几乎翻倍)',
        '人口: 日本老龄化加速\nvs 美国相对健康',
        '利率: 日本6% vs 美国0.25%\n(日本紧缩刺破泡沫)',
        '全球地位: 日本当时\n第二大 vs 美国第一大',
        '产业: 日本地产+金融\nvs 美国科技+AI'
    ]
    y_pos = np.arange(len(differences))
    
    # 用颜色块表示"危险程度"
    danger_levels = [0.8, 0.6, 0.3, 0.2, 0.4]  # 0=不危险, 1=很危险
    colors = plt.cm.RdYlGn_r(danger_levels)
    
    bars = ax.barh(y_pos, [1]*len(differences), color=colors, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(differences, fontsize=9)
    ax.set_xlim(0, 1.5)
    ax.set_title('美国 vs 日本泡沫：关键差异与危险程度', fontsize=14, fontweight='bold')
    ax.set_xticks([])
    
    # 添加图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=plt.cm.RdYlGn_r(0.2), alpha=0.7, label='低风险'),
        Patch(facecolor=plt.cm.RdYlGn_r(0.4), alpha=0.7, label='中等风险'),
        Patch(facecolor=plt.cm.RdYlGn_r(0.8), alpha=0.7, label='高风险'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '03_valuation_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 估值对比图已保存")
    
    # 打印关键数据
    print(f"\n{'='*60}")
    print("关键数据对比")
    print(f"{'='*60}")
    print(f"日本1989泡沫峰值PE: ~{japan_bubble['peak_pe']}x")
    print(f"美国2021 NDX峰值PE: ~{us_current['peak_pe']}x")
    print(f"纳指从2021年高点至今回撤: {drawdown:.1f}%")
    print(f"日经从1989年高点最大回撤: ~80%")
    print(f"日经从1989年高点用时34年才回本")
    print(f"{'='*60}")
    
    return japan_bubble, us_current


def plot_n225_historical_phases(n225):
    """绘制日经225的完整历史阶段，标注关键时期"""
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    data = n225['Adj Close'].copy()
    ax.plot(data.index, data.values, color='#333', linewidth=1.5, label='日经225')
    
    # 标注关键时期
    phases = [
        ('1985-09-01', '1989-12-31', '泡沫膨胀', '#D32F2F', 0.15),
        ('1990-01-01', '2003-04-30', '失去的十年', '#FF9800', 0.15),
        ('2003-05-01', '2007-12-31', '短暂复苏', '#4CAF50', 0.15),
        ('2008-01-01', '2012-12-31', '金融危机+地震', '#D32F2F', 0.15),
        ('2013-01-01', '2024-08-05', '安倍经济学', '#1976D2', 0.15),
    ]
    
    for start, end, label, color, alpha in phases:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), 
                   alpha=alpha, color=color, label=label)
    
    # 标注峰值和低点
    peak = data.loc['1989-01-01':'1990-12-31'].max()
    peak_date = data.loc['1989-01-01':'1990-12-31'].idxmax()
    trough = data.loc['1990-01-01':'2012-12-31'].min()
    trough_date = data.loc['1990-01-01':'2012-12-31'].idxmin()
    
    ax.scatter([peak_date], [peak], color='red', s=100, zorder=5, marker='^')
    ax.scatter([trough_date], [trough], color='green', s=100, zorder=5, marker='v')
    ax.annotate(f'峰值: {peak_date.year}\n{peak:.0f}', xy=(peak_date, peak),
                xytext=(pd.Timestamp('1992-01-01'), peak*0.8),
                arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')
    ax.annotate(f'底部: {trough_date.year}\n{trough:.0f}', xy=(trough_date, trough),
                xytext=(pd.Timestamp('2004-01-01'), trough*1.5),
                arrowprops=dict(arrowstyle='->', color='green'), fontsize=10, color='green')
    
    # 标注回本时间
    recovery_date = data.loc['2019-01-01':'2024-08-05'][data > peak].index[0] if any(data > peak) else None
    if recovery_date:
        ax.axhline(peak, color='red', linestyle='--', alpha=0.3)
        ax.annotate(f'回本: {recovery_date.year}', xy=(recovery_date, peak),
                    xytext=(pd.Timestamp('2015-01-01'), peak*0.9),
                    arrowprops=dict(arrowstyle='->', color='purple'), fontsize=10, color='purple')
    
    ax.set_ylabel('日经225指数', fontsize=12)
    ax.set_title('日经225完整历史：1989→2024', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=9, ncol=3)
    ax.grid(True, alpha=0.3)
    
    # 格式化x轴
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '04_n225_historical_phases.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 日经历史阶段图已保存")


def main():
    print("=" * 60)
    print("日经 vs 纳指：如果美国也经历'失去的三十年'")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n[1] 加载数据...")
    n225, ndx, spx, tqqq, qqq = load_data()
    print(f"  日经225: {n225.index[0].date()} → {n225.index[-1].date()} ({len(n225)}天)")
    print(f"  纳斯达克100: {ndx.index[0].date()} → {ndx.index[-1].date()} ({len(ndx)}天)")
    print(f"  TQQQ: {tqqq.index[0].date()} → {tqqq.index[-1].date()} ({len(tqqq)}天)")
    
    # 2. 路径对齐
    print("\n[2] 路径对齐...")
    n225_after, ndx_after, n225_peak, ndx_peak, n225_peak_date, ndx_peak_date = align_paths(n225, ndx)
    
    # 3. 路径对比图
    print("\n[3] 绘制路径对比图...")
    plot_path_comparison(n225_after, ndx_after, n225_peak_date, ndx_peak_date)
    
    # 4. TQQQ模拟
    print("\n[4] 模拟TQQQ在日经路径下的表现...")
    ndx_sim, tqqq_sim, ndx_actual, tqqq_actual = simulate_tqqq_on_japan_path(
        n225_after, ndx, tqqq, qqq, ndx_peak, ndx_peak_date)
    
    # 5. 估值对比
    print("\n[5] 估值对比...")
    compare_valuation(n225, ndx)
    
    # 6. 日经历史阶段
    print("\n[6] 日经历史阶段分析...")
    plot_n225_historical_phases(n225)
    
    print(f"\n{'='*60}")
    print("分析完成！所有图表已保存到 output/ 目录")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()