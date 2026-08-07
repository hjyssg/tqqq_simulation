"""
半导体先导信号分析：SMH/SOXX 能否预测 QQQ？
===========================================
分析维度：
1. 滚动相关性：SMH vs QQQ 的1年滚动相关性变化
2. 领先/滞后交叉相关性：SMH 的周涨跌对 QQQ 未来1-4周的预测能力
3. 事件分析：SMH 大跌后 QQQ 的后续表现
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

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

DATA_DIR = Path('data')

def load_data():
    """加载数据，处理不同的列名格式"""
    
    def load_single(path, name):
        df = pd.read_csv(path)
        # 检测第一个列名
        first_col = df.columns[0]
        if first_col == 'Price':
            # 有Ticker行，需要跳过前两行
            df = df.iloc[2:].copy()
            # 重命名列
            df.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
        elif first_col == 'Date':
            pass  # 标准格式
        else:
            raise ValueError(f"Unknown column format for {name}: {first_col}")
        
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)  # 去除时区信息
        df.set_index('Date', inplace=True)
        df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
        return df.sort_index()
    
    # 加载数据
    qqq = load_single(DATA_DIR / 'QQQ.csv', 'QQQ')
    smh = load_single(DATA_DIR / 'SMH.csv', 'SMH')
    soxx = load_single(DATA_DIR / 'SOXX.csv', 'SOXX')
    ndx = load_single(DATA_DIR / '^NDX.csv', 'NDX')
    nvda = load_single(DATA_DIR / 'NVDA.csv', 'NVDA')
    
    # 对齐到共同日期范围
    common_start = max(qqq.index.min(), smh.index.min(), soxx.index.min())
    common_end = min(qqq.index.max(), smh.index.max(), soxx.index.max())
    
    qqq = qqq[qqq.index >= common_start]
    smh = smh[smh.index >= common_start]
    soxx = soxx[soxx.index >= common_start]
    ndx = ndx[ndx.index >= common_start]
    
    return qqq, smh, soxx, ndx, nvda


def calc_weekly_returns(daily_df):
    """计算周收益率"""
    weekly = daily_df['Adj Close'].resample('W-FRI').last()
    weekly_returns = weekly.pct_change() * 100
    return weekly_returns


def calc_rolling_corr(qqq, smh, soxx):
    """计算1年滚动相关性"""
    qqq_ret = qqq['Adj Close'].pct_change() * 100
    smh_ret = smh['Adj Close'].pct_change() * 100
    soxx_ret = soxx['Adj Close'].pct_change() * 100
    
    # 1年滚动相关性（约252个交易日）
    rolling_corr_smh = qqq_ret.rolling(252).corr(smh_ret) * 100
    rolling_corr_soxx = qqq_ret.rolling(252).corr(soxx_ret) * 100
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # 图1：滚动相关性
    ax = axes[0]
    ax.plot(rolling_corr_smh.index, rolling_corr_smh.values, 
            label='SMH vs QQQ 1年滚动相关性', color='#2E86AB', linewidth=1.5)
    ax.plot(rolling_corr_soxx.index, rolling_corr_soxx.values, 
            label='SOXX vs QQQ 1年滚动相关性', color='#A23B72', linewidth=1.5, alpha=0.7)
    ax.axhline(50, color='gray', linestyle='--', alpha=0.5, label='r=0.5')
    ax.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax.set_ylabel('相关性 (%)', fontsize=12)
    ax.set_title('半导体指数 vs QQQ 的1年滚动相关性', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 添加相关性的描述性统计
    stats_text = (
        f"SMH-QQQ平均相关性: {rolling_corr_smh.mean():.1f}%\n"
        f"SOXX-QQQ平均相关性: {rolling_corr_soxx.mean():.1f}%\n"
        f"SMH相关性范围: {rolling_corr_smh.min():.1f}% ~ {rolling_corr_smh.max():.1f}%\n"
        f"SOXX相关性范围: {rolling_corr_soxx.min():.1f}% ~ {rolling_corr_soxx.max():.1f}%"
    )
    ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            verticalalignment='bottom')
    
    # 图2：相关性变化直方图
    ax = axes[1]
    ax.hist(rolling_corr_smh.dropna(), bins=50, alpha=0.6, color='#2E86AB', label='SMH-QQQ', density=True)
    ax.hist(rolling_corr_soxx.dropna(), bins=50, alpha=0.6, color='#A23B72', label='SOXX-QQQ', density=True)
    ax.axvline(rolling_corr_smh.mean(), color='#2E86AB', linestyle='--', linewidth=2, 
               label=f"SMH均值: {rolling_corr_smh.mean():.1f}%")
    ax.axvline(rolling_corr_soxx.mean(), color='#A23B72', linestyle='--', linewidth=2,
               label=f"SOXX均值: {rolling_corr_soxx.mean():.1f}%")
    ax.set_xlabel('相关性 (%)', fontsize=12)
    ax.set_ylabel('概率密度', fontsize=12)
    ax.set_title('滚动相关性分布', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '01_rolling_correlation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 滚动相关性图已保存")
    
    return rolling_corr_smh, rolling_corr_soxx


def calc_cross_correlation(qqq_weekly, smh_weekly, soxx_weekly):
    """计算交叉相关性：SMH领先多少天预测QQQ"""
    
    # 对齐数据
    combined = pd.DataFrame({
        'QQQ': qqq_weekly,
        'SMH': smh_weekly,
        'SOXX': soxx_weekly
    }).dropna()
    
    # 计算不同滞后的相关性
    max_lag = 8  # 最多8周
    results = {}
    
    for name, col in [('SMH', 'SMH'), ('SOXX', 'SOXX')]:
        corrs = []
        for lag in range(-max_lag, max_lag + 1):
            if lag < 0:
                # SMH领先（负滞后：SMH在t+lag预测QQQ在t）
                corr = combined['QQQ'].corr(combined[col].shift(-lag))
            else:
                corr = combined['QQQ'].corr(combined[col].shift(lag))
            corrs.append(corr)
        results[name] = corrs
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    lags = list(range(-max_lag, max_lag + 1))
    labels = [f"SMH领先{w}周" if w < 0 else f"SMH滞后{w}周" if w > 0 else "同时" 
              for w in lags]
    
    ax.bar([l - 0.2 for l in lags], results['SMH'], width=0.35, 
           color='#2E86AB', alpha=0.8, label='SMH vs QQQ')
    ax.bar([l + 0.2 for l in lags], results['SOXX'], width=0.35,
           color='#A23B72', alpha=0.8, label='SOXX vs QQQ')
    
    ax.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax.set_xticks(lags)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Pearson相关系数', fontsize=12)
    ax.set_title('SMH/SOXX 与 QQQ 的滞后交叉相关性分析', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # 标注最强相关性
    max_smh_lag = lags[np.argmax(results['SMH'])]
    max_smh_corr = max(results['SMH'])
    ax.annotate(f'最强: SMH{max_smh_lag:+d}周\nr={max_smh_corr:.3f}',
                xy=(max_smh_lag, max_smh_corr), xytext=(max_smh_lag + 1.5, max_smh_corr + 0.05),
                arrowprops=dict(arrowstyle='->', color='#2E86AB'),
                fontsize=10, color='#2E86AB', fontweight='bold')
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '02_cross_correlation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 交叉相关性图已保存")
    
    return results


def analyze_smh_drop_events(qqq, smh, soxx):
    """分析SMH大跌后QQQ的表现"""
    
    qqq_ret = qqq['Adj Close'].pct_change() * 100
    smh_ret = smh['Adj Close'].pct_change() * 100
    soxx_ret = soxx['Adj Close'].pct_change() * 100
    
    # 找出SMH单日跌幅超过-3%的事件
    smh_drop_events = smh_ret[smh_ret < -3].dropna()
    
    print(f"\n{'='*60}")
    print(f"SMH单日跌幅超过-3%的事件数: {len(smh_drop_events)}")
    print(f"SMH单日跌幅超过-5%的事件数: {len(smh_ret[smh_ret < -5].dropna())}")
    print(f"{'='*60}")
    
    # 对每个事件，查看后续QQQ和半导体表现
    results = []
    for date in smh_drop_events.index:
        try:
            # 找到事件日期在QQQ中的位置
            pos = qqq_ret.index.get_loc(date)
            future_dates = qqq_ret.index[pos:pos+21]  # 后续约1个月（21个交易日）
            
            if len(future_dates) >= 5:
                # 计算后续1天、5天、21天的表现
                qqq_1d = qqq_ret.loc[date] if date in qqq_ret.index else np.nan
                qqq_5d = qqq_ret.loc[future_dates[:5]].sum() if len(future_dates) >= 5 else np.nan
                qqq_21d = qqq_ret.loc[future_dates].sum() if len(future_dates) >= 21 else np.nan
                
                smh_5d = smh_ret.loc[future_dates[:5]].sum() if len(future_dates) >= 5 else np.nan
                
                results.append({
                    'date': date,
                    'smh_drop': smh_ret.loc[date],
                    'qqq_immediate': qqq_1d,
                    'qqq_5d_cum': qqq_5d,
                    'qqq_21d_cum': qqq_21d,
                    'smh_5d_cum': smh_5d
                })
        except (KeyError, IndexError):
            continue
    
    results_df = pd.DataFrame(results)
    if len(results_df) == 0:
        print("没有找到足够的事件数据")
        return results_df
    
    print(f"\nSMH大跌后QQQ的统计:")
    print(f"  事件当天QQQ平均涨跌: {results_df['qqq_immediate'].mean():.2f}%")
    print(f"  后续5天QQQ平均涨跌: {results_df['qqq_5d_cum'].mean():.2f}%")
    print(f"  后续21天QQQ平均涨跌: {results_df['qqq_21d_cum'].mean():.2f}%")
    print(f"  QQQ在5天内跟随下跌的概率: {(results_df['qqq_5d_cum'] < 0).mean()*100:.1f}%")
    
    # 按跌幅大小分组
    results_df['drop_group'] = pd.cut(results_df['smh_drop'], 
                                       bins=[-float('inf'), -7, -5, -3],
                                       labels=['<-7%', '-7%~-5%', '-5%~-3%'])
    
    grouped = results_df.groupby('drop_group')[['qqq_5d_cum', 'qqq_21d_cum']].mean()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # 图1：散点图
    ax = axes[0]
    scatter = ax.scatter(results_df['smh_drop'], results_df['qqq_5d_cum'], 
                         c=results_df['qqq_21d_cum'], cmap='RdYlGn', 
                         s=60, alpha=0.7, edgecolors='black', linewidth=0.5)
    plt.colorbar(scatter, ax=ax, label='后续21天QQQ收益 (%)')
    
    # 添加拟合线
    from numpy.polynomial.polynomial import polyfit
    valid = results_df[['smh_drop', 'qqq_5d_cum']].dropna()
    if len(valid) > 5:
        try:
            b, m = polyfit(valid['smh_drop'], valid['qqq_5d_cum'], 1)
            x_fit = np.linspace(valid['smh_drop'].min(), valid['smh_drop'].max(), 100)
            ax.plot(x_fit, b + m * x_fit, 'r--', alpha=0.6, 
                    label=f'线性拟合 (斜率={m:.3f})')
            ax.legend(fontsize=10)
        except:
            pass
    
    ax.axhline(0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(0, color='gray', linestyle='-', alpha=0.3)
    ax.set_xlabel('SMH当日跌幅 (%)', fontsize=12)
    ax.set_ylabel('QQQ后续5天累计收益 (%)', fontsize=12)
    ax.set_title('SMH大跌日 vs QQQ后续表现', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # 图2：分组柱状图
    ax = axes[1]
    x = np.arange(len(grouped))
    width = 0.35
    ax.bar(x - width/2, grouped['qqq_5d_cum'].values, width, 
           color='#2E86AB', alpha=0.8, label='后续5天平均')
    ax.bar(x + width/2, grouped['qqq_21d_cum'].values, width,
           color='#A23B72', alpha=0.8, label='后续21天平均')
    ax.set_xticks(x)
    ax.set_xticklabels(grouped.index, fontsize=10)
    ax.axhline(0, color='gray', linestyle='-', alpha=0.3)
    ax.set_ylabel('平均累计收益 (%)', fontsize=12)
    ax.set_title('不同跌幅分组下QQQ的后续表现', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '03_smh_drop_events.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] SMH大跌事件分析图已保存")
    
    # 保存详细数据
    results_df.to_csv(OUTPUT_DIR / 'smh_drop_events.csv', index=False)
    
    return results_df


def analyze_nvda_impact(qqq, smh, nvda):
    """分析NVDA在SMH中的权重和影响"""
    
    qqq_ret = qqq['Adj Close'].pct_change() * 100
    smh_ret = smh['Adj Close'].pct_change() * 100
    nvda_ret = nvda['Adj Close'].pct_change() * 100
    
    # 对齐数据
    combined = pd.DataFrame({
        'QQQ': qqq_ret,
        'SMH': smh_ret,
        'NVDA': nvda_ret
    }).dropna()
    
    # 滚动相关性：NVDA vs SMH
    rolling_nvda_smh = combined['NVDA'].rolling(252).corr(combined['SMH']) * 100
    rolling_nvda_qqq = combined['NVDA'].rolling(252).corr(combined['QQQ']) * 100
    
    # 计算NVDA在SMH中的"解释力"
    # 如果SMH涨跌主要由NVDA驱动，那么SMH对QQQ的预测能力可能只是NVDA的镜像
    partial_corr = combined['SMH'].rolling(252).corr(combined['QQQ']) * 100
    
    # 控制NVDA后的偏相关 - 简单方法：看SMH残差 vs QQQ
    # 先对SMH做NVDA的线性回归，取残差
    from numpy.polynomial.polynomial import polyfit
    
    # 滚动窗口计算
    window = 252
    residual_corr = []
    dates = []
    
    for i in range(window, len(combined)):
        chunk = combined.iloc[i-window:i]
        if len(chunk) < window:
            continue
        try:
            # SMH ~ NVDA 回归，取残差
            coeffs = polyfit(chunk['NVDA'], chunk['SMH'], 1)
            smh_residual = chunk['SMH'] - (coeffs[0] + coeffs[1] * chunk['NVDA'])
            # 残差与QQQ的相关性
            corr = smh_residual.corr(chunk['QQQ'])
            residual_corr.append(corr * 100)
            dates.append(chunk.index[-1])
        except:
            continue
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # 图1：相关性对比
    ax = axes[0]
    ax.plot(rolling_nvda_smh.index, rolling_nvda_smh.values, 
            label='NVDA vs SMH 滚动相关性', color='#76B900', linewidth=1.5)  # NVIDIA绿色
    ax.plot(rolling_nvda_qqq.index, rolling_nvda_qqq.values, 
            label='NVDA vs QQQ 滚动相关性', color='#2E86AB', linewidth=1.5, alpha=0.7)
    ax.axhline(50, color='gray', linestyle='--', alpha=0.5)
    ax.set_ylabel('相关性 (%)', fontsize=12)
    ax.set_title('NVDA 与 SMH、QQQ 的滚动相关性', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 图2：控制NVDA后的SMH-QQQ相关性
    ax = axes[1]
    ax.plot(dates, residual_corr, color='#A23B72', linewidth=1.5, 
            label='控制NVDA后 SMH vs QQQ 偏相关')
    # 对比原始相关性
    ax.plot(partial_corr.index, partial_corr.values, color='#2E86AB', linewidth=1.5, alpha=0.5,
            label='原始 SMH vs QQQ 相关性')
    ax.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax.set_ylabel('偏相关系数 (%)', fontsize=12)
    ax.set_title('控制NVDA影响后，SMH对QQQ的独立预测能力', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 添加说明
    if len(residual_corr) > 10:
        avg_residual = np.mean(residual_corr)
        avg_original = partial_corr.mean()
        note = (
            f"原始SMH-QQQ平均相关: {avg_original:.1f}%\n"
            f"控制NVDA后平均相关: {avg_residual:.1f}%\n"
            f"差异: {avg_original - avg_residual:.1f}%\n"
            f"→ NVDA解释了SMH-QQQ相关性的 {(1 - avg_residual/avg_original)*100:.1f}%"
        )
        ax.text(0.02, 0.02, note, transform=ax.transAxes, fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                verticalalignment='bottom')
    
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / '04_nvda_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] NVDA影响分析图已保存")


def main():
    print("=" * 60)
    print("半导体先导信号分析：SMH/SOXX 能否预测 QQQ？")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n[1] 加载数据...")
    qqq, smh, soxx, ndx, nvda = load_data()
    print(f"  QQQ: {qqq.index[0].date()} → {qqq.index[-1].date()} ({len(qqq)}天)")
    print(f"  SMH: {smh.index[0].date()} → {smh.index[-1].date()} ({len(smh)}天)")
    print(f"  SOXX: {soxx.index[0].date()} → {soxx.index[-1].date()} ({len(soxx)}天)")
    print(f"  NVDA: {nvda.index[0].date()} → {nvda.index[-1].date()} ({len(nvda)}天)")
    
    # 2. 滚动相关性
    print("\n[2] 计算滚动相关性...")
    calc_rolling_corr(qqq, smh, soxx)
    
    # 3. 交叉相关性（领先滞后）
    print("\n[3] 计算交叉相关性...")
    qqq_weekly = calc_weekly_returns(qqq)
    smh_weekly = calc_weekly_returns(smh)
    soxx_weekly = calc_weekly_returns(soxx)
    calc_cross_correlation(qqq_weekly, smh_weekly, soxx_weekly)
    
    # 4. SMH大跌事件分析
    print("\n[4] 分析SMH大跌事件...")
    results = analyze_smh_drop_events(qqq, smh, soxx)
    
    # 5. NVDA的影响
    print("\n[5] 分析NVDA对SMH-QQQ关系的影响...")
    analyze_nvda_impact(qqq, smh, nvda)
    
    print(f"\n{'='*60}")
    print("分析完成！所有图表已保存到 output/ 目录")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()