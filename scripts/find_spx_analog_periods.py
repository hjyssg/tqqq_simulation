"""
目的：从标普 500（SPX）历史价格中检索与当前阶段走势形态相近的时期。

本脚本将当前窗口与历史非重叠窗口的累计对数收益路径进行波动率标准化，
按路径相关性、RMSE 和摘要特征的综合得分筛选相似时期；随后展示这些时期
结束后的真实路径，作为有限历史条件样本的情景研究。

重要限制：结果不是价格预测、投资建议或事件因果证明。历史样本很少且市场
制度会变化；请结合多窗口参数运行，而不要只根据某一个相似时期做决策。

示例：
    python scripts/find_spx_analog_periods.py
    python scripts/find_spx_analog_periods.py --window 126 --top-n 8
"""

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
import _util  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="检索 SPX 历史相似走势并输出图表。")
    parser.add_argument("--symbol-file", default="^SPX.csv", help="data 目录中的价格 CSV 文件名")
    parser.add_argument("--window", type=int, default=189, help="待匹配窗口长度（交易日，默认 189）")
    parser.add_argument("--top-n", type=int, default=5, help="输出的非重叠相似时期数量（默认 5）")
    parser.add_argument("--forward-days", type=int, default=126, help="统计后续路径长度（交易日，默认 126）")
    parser.add_argument("--min-history-years", type=int, default=5, help="候选结束日距当前至少的年数")
    return parser.parse_args()


def normalized_log_path(prices):
    """把价格转为起点为 0、窗口内波动率为 1 的累计对数收益路径。"""
    log_path = np.log(prices / prices.iloc[0]).to_numpy()
    daily_returns = np.diff(log_path)
    volatility = np.std(daily_returns, ddof=1)
    return log_path / max(volatility * np.sqrt(len(daily_returns)), 1e-12)


def window_features(prices):
    """提供用于相似度轻量校正的方向、回撤与波动特征。"""
    returns = prices.pct_change().dropna()
    drawdown = prices / prices.cummax() - 1
    late_start = int(len(prices) * 0.67)
    late_drawdown = prices.iloc[late_start:] / prices.iloc[late_start:].cummax() - 1
    return np.array([
        np.log(prices.iloc[-1] / prices.iloc[0]),
        drawdown.min(),
        late_drawdown.min(),
        returns.std(ddof=1) * np.sqrt(252),
    ])


def score_candidates(prices, window, forward_days, min_history_years):
    """生成候选窗口并计算综合距离；候选不与当前窗口重叠且有足够的后续数据。"""
    target = prices.iloc[-window:]
    target_path = normalized_log_path(target)
    target_features = window_features(target)
    feature_scale = np.array([0.20, 0.15, 0.12, 0.20])
    latest_allowed_end = len(prices) - window - forward_days - min_history_years * 252
    candidates = []

    for start_idx in range(0, latest_allowed_end + 1):
        candidate = prices.iloc[start_idx:start_idx + window]
        candidate_path = normalized_log_path(candidate)
        correlation = np.corrcoef(target_path, candidate_path)[0, 1]
        rmse = np.sqrt(np.mean((target_path - candidate_path) ** 2))
        feature_penalty = np.mean(np.abs((window_features(candidate) - target_features) / feature_scale))
        score = 0.55 * (1 - correlation) + 0.35 * rmse + 0.10 * feature_penalty
        candidates.append({
            "start_idx": start_idx,
            "end_idx": start_idx + window - 1,
            "start_date": candidate.index[0],
            "end_date": candidate.index[-1],
            "score": score,
            "correlation": correlation,
            "rmse": rmse,
            "window_return": candidate.iloc[-1] / candidate.iloc[0] - 1,
            "max_drawdown": (candidate / candidate.cummax() - 1).min(),
        })
    return pd.DataFrame(candidates), target


def select_non_overlapping(candidates, top_n, spacing):
    """由低分到高分选择；各入选窗口起点至少相距 spacing 个交易日。"""
    selected = []
    for _, row in candidates.sort_values("score").iterrows():
        if all(abs(row.start_idx - item["start_idx"]) >= spacing for item in selected):
            selected.append(row.to_dict())
            if len(selected) == top_n:
                break
    return pd.DataFrame(selected)


def add_forward_statistics(selected, prices, forward_days):
    records = []
    paths = []
    for row in selected.itertuples(index=False):
        future = prices.iloc[row.end_idx + 1:row.end_idx + 1 + forward_days]
        if len(future) != forward_days:
            continue
        relative_path = future / prices.iloc[row.end_idx] - 1
        paths.append(relative_path.to_numpy())
        record = row._asdict()
        for days in (21, 63, forward_days):
            path = relative_path.iloc[:days]
            record[f"forward_{days}d_return"] = path.iloc[-1]
            record[f"forward_{days}d_max_drawdown"] = (1 + path).div((1 + path).cummax()).sub(1).min()
        records.append(record)
    return pd.DataFrame(records), np.asarray(paths)


def save_plots(target, selected, prices, forward_paths, output_dir, forward_days):
    _util.init_plotting()
    target_norm = target / target.iloc[0] * 100
    days = np.arange(len(target_norm))

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(days, target_norm, color="black", linewidth=3, label=f"当前：{target.index[0].date()} 至 {target.index[-1].date()}")
    for rank, row in enumerate(selected.itertuples(index=False), 1):
        history = prices.iloc[row.start_idx:row.end_idx + 1]
        ax.plot(days, history / history.iloc[0] * 100, linewidth=1.5,
                label=f"#{rank} {row.start_date.date()} 至 {row.end_date.date()}（得分 {row.score:.3f}）")
    ax.set(title="SPX 当前走势与历史相似时期（起点=100）", xlabel="窗口内交易日", ylabel="归一化价格")
    ax.legend(fontsize=9, loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "current_vs_analogs.png", dpi=160)
    plt.close(fig)

    panels = len(selected) + 1
    fig, axes = plt.subplots(panels, 1, figsize=(14, 3.2 * panels), sharex=True)
    axes[0].plot(days, target_norm, color="black", linewidth=2.5)
    axes[0].set_title(f"当前窗口：{target.index[0].date()} 至 {target.index[-1].date()}")
    for rank, row in enumerate(selected.itertuples(index=False), 1):
        history = prices.iloc[row.start_idx:row.end_idx + 1]
        axes[rank].plot(days, history / history.iloc[0] * 100, linewidth=2)
        axes[rank].set_title(f"#{rank}：{row.start_date.date()} 至 {row.end_date.date()} | 相关={row.correlation:.3f}，得分={row.score:.3f}")
    for axis in axes:
        axis.axhline(100, color="gray", alpha=0.45, linestyle="--")
        axis.set_ylabel("起点=100")
        axis.grid(alpha=0.3)
    axes[-1].set_xlabel("窗口内交易日")
    fig.suptitle("SPX 当前窗口与每段历史相似时期", y=1.002, fontsize=15)
    fig.tight_layout()
    fig.savefig(output_dir / "analog_period_panels.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    horizon = np.arange(1, forward_days + 1)
    fig, ax = plt.subplots(figsize=(14, 7))
    for rank, path in enumerate(forward_paths, 1):
        ax.plot(horizon, path * 100, linewidth=1.2, alpha=0.7, label=f"历史样本 #{rank}")
    median = np.median(forward_paths, axis=0) * 100
    low, high = np.percentile(forward_paths, [25, 75], axis=0) * 100
    ax.fill_between(horizon, low, high, color="tab:blue", alpha=0.16, label="历史样本 25%–75% 区间")
    ax.plot(horizon, median, color="black", linewidth=2.5, label="历史样本中位数")
    ax.axhline(0, color="gray", alpha=0.6, linestyle="--")
    ax.set(title="相似时期结束后的实际路径（历史条件样本，非预测）", xlabel="相似窗口结束后的交易日", ylabel="累计收益率（%）")
    ax.legend(ncol=2, fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "forward_paths.png", dpi=160)
    plt.close(fig)


def main():
    args = parse_args()
    if args.window < 21 or args.top_n < 1 or args.forward_days < 21:
        raise ValueError("window 至少为 21、top-n 至少为 1、forward-days 至少为 21。")

    data = _util.load_csv_as_dataframe(args.symbol_file).set_index("Date")
    prices = data["Close"].dropna().astype(float)
    candidates, target = score_candidates(prices, args.window, args.forward_days, args.min_history_years)
    selected = select_non_overlapping(candidates, args.top_n, args.window)
    selected, forward_paths = add_forward_statistics(selected, prices, args.forward_days)
    if selected.empty:
        raise RuntimeError("没有足够的候选窗口；请减小 window、forward-days 或 min-history-years。")

    output_dir = PROJECT_DIR / "output" / "spx_analog_periods"
    output_dir.mkdir(parents=True, exist_ok=True)
    selected.insert(0, "rank", range(1, len(selected) + 1))
    selected.to_csv(output_dir / "analog_periods.csv", index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")

    summary_rows = []
    for days in (21, 63, args.forward_days):
        returns = selected[f"forward_{days}d_return"]
        summary_rows.append({"horizon_trading_days": days, "sample_count": len(returns), "positive_ratio": (returns > 0).mean(),
                             "min_return": returns.min(), "p25_return": returns.quantile(.25), "median_return": returns.median(),
                             "p75_return": returns.quantile(.75), "max_return": returns.max()})
    pd.DataFrame(summary_rows).to_csv(output_dir / "forward_return_summary.csv", index=False, encoding="utf-8-sig")
    save_plots(target, selected, prices, forward_paths, output_dir, args.forward_days)

    print(f"数据：{args.symbol_file}，当前窗口：{target.index[0].date()} 至 {target.index[-1].date()}（{args.window} 个交易日）")
    print("\n相似时期（得分越低越相似）：")
    print(selected[["rank", "start_date", "end_date", "score", "correlation", "window_return", "max_drawdown",
                    f"forward_{args.forward_days}d_return"]].to_string(index=False, float_format=lambda x: f"{x:.3%}"))
    print(f"\n已输出到：{output_dir}")


if __name__ == "__main__":
    main()