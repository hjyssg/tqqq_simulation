"""目的：量化 QLD、TQQQ、SPXL 在 300 个交易日内的每日再平衡杠杆 decay。

本脚本从 NDX / SPX 的历史日收益率中抽取连续 5 日区块，并将区块拼接成大量
随机市场路径（block bootstrap Monte Carlo）。每条路径上比较每日复利的 2x / 3x
杠杆产品，与“标的期末总收益 × 杠杆倍数”的静态杠杆基准。

decay = 每日复利杠杆收益 - 静态杠杆基准收益。
负值代表震荡、回撤等路径依赖导致的波动损耗；正值可能出现在强单边趋势路径。
结果是基于历史收益分布的情景分析，不是未来收益预测，也不包含基金费率、融资成本
或实际 ETF 跟踪误差（尤其 SPXL 为基于 SPX 的理论 3x 模拟）。

示例：
    python scripts/LETF/monte_carlo_decay.py  # 默认模拟 300 个交易日
    python scripts/LETF/monte_carlo_decay.py --paths 50000 --years 3 --block-size 10

这里的 decay 定义为：逐日复利杠杆 ETF 的期末收益率，减去“期末标的累计收益
乘以杠杆倍数”的静态倍数收益率。它不是基金费率或真实 ETF 的 tracking error。
"""

import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util


ASSETS = (
    ("QLD", "^NDX.csv", 2.0),
    ("TQQQ", "^NDX.csv", 3.0),
    ("SPXL", "^SPX.csv", 3.0),
)


def load_returns(filename: str, start_date: str | None) -> tuple[np.ndarray, pd.DataFrame]:
    """读取并清洗标的指数的收盘价日收益率。"""
    frame = _util.load_csv_as_dataframe(filename)
    if start_date:
        frame = frame[frame["Date"] >= pd.Timestamp(start_date)]
    returns = frame["Close"].pct_change().dropna().to_numpy(dtype=float)
    if len(returns) < 252:
        raise ValueError(f"{filename} 可用日收益率不足一年：{len(returns)}")
    return returns, frame


def ytd_trading_days(frame: pd.DataFrame) -> int:
    """以数据中最后一个交易日所在年份为准，返回其 YTD 已完成的日收益率个数。"""
    last_date = frame["Date"].iloc[-1]
    ytd_prices = frame[frame["Date"].dt.year == last_date.year]
    days = len(ytd_prices) - 1
    if days <= 0:
        raise ValueError("数据中没有足够的 YTD 交易日")
    return days


def block_bootstrap_paths(
    returns: np.ndarray,
    paths: int,
    days: int,
    block_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """抽取连续历史收益块，保留短期波动聚集；返回形状为 (paths, days)。"""
    blocks_needed = int(np.ceil(days / block_size))
    starts = rng.integers(0, len(returns), size=(paths, blocks_needed))
    offsets = np.arange(block_size)
    indices = (starts[..., None] + offsets) % len(returns)
    return returns[indices].reshape(paths, -1)[:, :days]


def simulate_asset(
    name: str,
    returns: np.ndarray,
    leverage: float,
    paths: int,
    days: int,
    block_size: int,
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, np.ndarray]:
    """模拟标的与其每日杠杆产品，返回汇总统计与每条路径的 decay。"""
    sampled = block_bootstrap_paths(returns, paths, days, block_size, rng)
    underlying_nav = np.cumprod(1.0 + sampled, axis=1)
    leveraged_nav = np.cumprod(1.0 + leverage * sampled, axis=1)

    underlying_return = underlying_nav[:, -1] - 1.0
    leveraged_return = leveraged_nav[:, -1] - 1.0
    static_return = leverage * underlying_return
    decay = leveraged_return - static_return
    outperform_probability = float(np.mean(decay > 0))

    summary = {
        "asset": name,
        "leverage": leverage,
        "paths": paths,
        "trading_days": days,
        "underlying_return_median": np.median(underlying_return),
        "leveraged_return_median": np.median(leveraged_return),
        "static_leverage_return_median": np.median(static_return),
        "decay_median": np.median(decay),
        "decay_mean": np.mean(decay),
        "decay_p05": np.quantile(decay, 0.05),
        "decay_p95": np.quantile(decay, 0.95),
        "probability_decay_negative": float(np.mean(decay < 0)),
        "probability_beats_static_leverage": outperform_probability,
    }
    return pd.DataFrame([summary]), decay


def save_charts(results: pd.DataFrame, decay_samples: dict[str, np.ndarray], days: int, output_dir: str) -> None:
    """画出每只产品自己的 decay 分布，避免重叠路径图难以阅读。"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)
    for axis, (_, row) in zip(axes, results.iterrows()):
        name = row["asset"]
        values = decay_samples[name] * 100
        axis.hist(values, bins=80, color="#4C78A8", edgecolor="white", alpha=0.9)
        axis.axvline(0, color="#333333", linewidth=1, linestyle="--", label="No decay")
        axis.axvline(row["decay_median"] * 100, color="#E45756", linewidth=2, label="Median")
        axis.axvspan(row["decay_p05"] * 100, row["decay_p95"] * 100, color="#F2CF5B", alpha=0.25, label="5th–95th pct")
        axis.set_title(f"{name} ({row['leverage']:.0f}x)")
        axis.set_xlabel("Decay vs. static leverage (percentage points)")
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=8)
        axis.text(
            0.02,
            0.97,
            f"Median: {row['decay_median'] * 100:.2f} pp\n"
            f"Negative: {row['probability_decay_negative'] * 100:.1f}%",
            transform=axis.transAxes,
            va="top",
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
        )
    axes[0].set_ylabel("Number of simulated paths")
    fig.suptitle(f"{days}-day Monte Carlo: daily-reset leveraged ETF decay\n"
                 "Decay = leveraged daily-compounded return − (underlying total return × leverage)", y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "monte_carlo_decay.png"), dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="QLD、TQQQ、SPXL 的 block-bootstrap 蒙特卡洛 decay 分析")
    parser.add_argument("--paths", type=int, default=20_000, help="每个品种的模拟路径数（默认 20000）")
    duration = parser.add_mutually_exclusive_group()
    duration.add_argument("--years", type=float, help="模拟年数，按每年 252 个交易日计算")
    duration.add_argument("--days", type=int, help="直接指定模拟交易日数（默认 300）")
    duration.add_argument("--ytd", action="store_true", help="按指数数据最后日期所在年份的 YTD 交易日数模拟")
    parser.add_argument("--block-size", type=int, default=5, help="连续抽样块长度（交易日，默认 5）")
    parser.add_argument("--start-date", default="2000-01-01", help="历史样本起始日期（默认 2000-01-01）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子（默认 42）")
    args = parser.parse_args()
    if args.paths <= 0 or args.block_size <= 0 or (args.years is not None and args.years <= 0) or (args.days is not None and args.days <= 0):
        parser.error("paths、years、days 和 block-size 必须为正数")

    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "output", "LETF")
    os.makedirs(output_dir, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    summaries, decay_samples = [], {}
    cached_data: dict[str, tuple[np.ndarray, pd.DataFrame]] = {}

    for _, filename, _ in ASSETS:
        if filename not in cached_data:
            cached_data[filename] = load_returns(filename, args.start_date)

    if args.ytd:
        days = ytd_trading_days(cached_data["^NDX.csv"][1])
        duration_label = "YTD"
    elif args.days is not None:
        days = args.days
        duration_label = f"{days} trading days"
    elif args.years is not None:
        days = round(args.years * 252)
        duration_label = f"{args.years:g} year(s)"
    else:
        days = 300
        duration_label = "300 trading days (default)"
    print(f"模拟期限: {duration_label} ({days} 个交易日); 历史样本起点: {args.start_date}; block size: {args.block_size}")

    for name, filename, leverage in ASSETS:
        historical_returns, _ = cached_data[filename]
        result, decay = simulate_asset(name, historical_returns, leverage, args.paths, days, args.block_size, rng)
        summaries.append(result)
        decay_samples[name] = decay
        print(f"{name}: 使用 {len(historical_returns)} 个历史日收益率，模拟 {args.paths:,} 条 {days} 日路径")

    results = pd.concat(summaries, ignore_index=True)
    csv_path = os.path.join(output_dir, "monte_carlo_decay_summary.csv")
    results.to_csv(csv_path, index=False, float_format="%.8f")
    save_charts(results, decay_samples, days, output_dir)

    show = results.copy()
    percent_columns = [col for col in show.columns if "return" in col or "decay" in col or "probability" in col]
    show[percent_columns] *= 100
    print("\n=== Monte Carlo decay 汇总（百分比）===")
    print(show.to_string(index=False, float_format=lambda value: f"{value:.2f}"))
    print(f"\nCSV: {csv_path}")
    print(f"图表: {os.path.join(output_dir, 'monte_carlo_decay.png')}")


if __name__ == "__main__":
    main()