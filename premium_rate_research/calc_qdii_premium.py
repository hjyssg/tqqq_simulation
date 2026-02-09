from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


@dataclass
class AssetConfig:
    name: str
    index_path: Path
    qdii_candidates: list[Path]
    fx_path: Path
    calibration_date: str
    known_premium: float
    output_dir: Path
    daily_output_name: str


def read_close_series(path: Path) -> pd.DataFrame:
    """读取 csv 并统一输出列: date, close（升序、去重）。"""
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    # 尝试识别中文列（如 data/qdii/513100.csv）
    sample = pd.read_csv(path, nrows=5)
    cols = list(sample.columns)
    zh_date_col = next((c for c in cols if "日期" in c), None)
    zh_close_col = next((c for c in cols if c.startswith("關閉")), None)

    if zh_date_col and zh_close_col:
        df = pd.read_csv(path)
        df = df.rename(columns={zh_date_col: "date", zh_close_col: "close"})
        df["date"] = pd.to_datetime(df["date"], format="%Y年%m月%d日", errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
    else:
        # 兼容 yfinance 双表头格式：
        # 第 1 行: Price,Adj Close,Close...
        # 第 2 行: Ticker,...
        # 第 3 行: Date,...
        try:
            df = pd.read_csv(path, skiprows=[1])
        except Exception:
            df = pd.read_csv(path)

        first_col = df.columns[0]
        close_col = "Close" if "Close" in df.columns else None

        if close_col is None:
            raise ValueError(f"无法识别 Close 列: {path}")

        df = df.rename(columns={first_col: "date", close_col: "close"})
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df = df[["date", "close"]].dropna(subset=["date", "close"])
    df = df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


def pick_qdii_source(candidates: Iterable[Path], calibration_date: pd.Timestamp) -> tuple[Path, pd.DataFrame]:
    """优先挑选含校验日的 QDII 数据；若都不含，使用首个可读文件。"""
    first_valid: tuple[Path, pd.DataFrame] | None = None
    for path in candidates:
        if not path.exists():
            continue
        try:
            df = read_close_series(path)
        except Exception:
            continue

        if first_valid is None:
            first_valid = (path, df)
        if (df["date"] == calibration_date).any():
            return path, df

    if first_valid is not None:
        return first_valid
    raise FileNotFoundError("所有候选 QDII 文件均不可用")


def build_daily_premium(asset: AssetConfig) -> tuple[pd.DataFrame, float, Path]:
    calibration_date = pd.Timestamp(asset.calibration_date)

    index_df = read_close_series(asset.index_path).rename(columns={"close": "index_close"})
    fx_df = read_close_series(asset.fx_path).rename(columns={"close": "fx_close"})
    qdii_path, qdii_df = pick_qdii_source(asset.qdii_candidates, calibration_date)
    qdii_df = qdii_df.rename(columns={"close": "qdii_close"})

    # 以 QDII 交易日为锚，对 index/fx 做 backward(asof) 对齐
    aligned = qdii_df[["date", "qdii_close"]].sort_values("date").copy()
    aligned = pd.merge_asof(
        aligned,
        index_df.sort_values("date"),
        on="date",
        direction="backward",
    )
    aligned = pd.merge_asof(
        aligned,
        fx_df.sort_values("date"),
        on="date",
        direction="backward",
    )

    aligned = aligned.dropna(subset=["qdii_close", "index_close", "fx_close"]).copy()

    calibration_row = aligned.loc[aligned["date"] == calibration_date]
    if calibration_row.empty:
        raise ValueError(
            f"{asset.name} 在校验日 {asset.calibration_date} 没有可用的 QDII 交易数据，"
            f"当前选择文件: {qdii_path}"
        )

    q = calibration_row.iloc[0]
    k = q["qdii_close"] / (q["index_close"] * q["fx_close"] * (1 + asset.known_premium))

    aligned["theoretical_nav"] = aligned["index_close"] * aligned["fx_close"] * k
    aligned["premium"] = aligned["qdii_close"] / aligned["theoretical_nav"] - 1
    aligned["premium_pct"] = aligned["premium"] * 100
    return aligned, k, qdii_path


def save_trend_plot(df: pd.DataFrame, asset_name: str, output_path: Path) -> None:
    monthly = (
        df.set_index("date")["premium"]
        .resample("ME")
        .mean()
        .dropna()
        .rename("monthly_premium")
    )

    # 过滤初期异常区间：默认从 2016 年开始
    monthly = monthly.loc[monthly.index >= pd.Timestamp("2016-01-01")]

    plt.figure(figsize=(12, 5))
    plt.plot(monthly.index, monthly.values * 100, linewidth=1.8)
    plt.axhline(0, color="red", linestyle="--", linewidth=1)
    plt.title(f"{asset_name} Monthly Premium Trend")
    plt.xlabel("Date")
    plt.ylabel("Premium (%)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def save_distribution_plot(df: pd.DataFrame, asset_name: str, output_path: Path) -> pd.DataFrame:
    end_date = df["date"].max()
    start_date = end_date - pd.DateOffset(years=3)
    window = df.loc[df["date"] >= start_date, ["date", "premium"]].copy()

    plt.figure(figsize=(8, 5))
    plt.hist(window["premium"] * 100, bins=40, edgecolor="black", alpha=0.75)
    plt.axvline(window["premium"].mean() * 100, color="red", linestyle="--", linewidth=1, label="Mean")
    plt.axvline(window["premium"].median() * 100, color="green", linestyle="--", linewidth=1, label="Median")
    plt.title(f"{asset_name} Premium Distribution (Last 3 Years)")
    plt.xlabel("Premium (%)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

    return window


def make_report(
    asset: AssetConfig,
    daily_df: pd.DataFrame,
    three_year_df: pd.DataFrame,
    k: float,
    qdii_path: Path,
    output_path: Path,
) -> None:
    calib_date = pd.Timestamp(asset.calibration_date)
    calib_row = daily_df.loc[daily_df["date"] == calib_date].iloc[0]
    recalculated_premium = calib_row["premium"]

    p = three_year_df["premium"]
    quantiles = p.quantile([0.1, 0.25, 0.75, 0.9])

    in_range_ratio = ((p >= 0.02) & (p <= 0.05)).mean()
    has_discount = (p < 0).any()

    # 断层检测：日变化绝对值超过 99.5% 分位点
    diff_abs = daily_df["premium"].diff().abs().dropna()
    jump_threshold = diff_abs.quantile(0.995) if len(diff_abs) else 0.0
    jump_count = int((diff_abs > jump_threshold).sum()) if jump_threshold > 0 else 0

    lines = [
        f"资产: {asset.name}",
        f"QDII 数据源: {qdii_path}",
        f"校验日: {asset.calibration_date}",
        f"已知溢价率: {asset.known_premium * 100:.2f}%",
        f"回算溢价率: {recalculated_premium * 100:.2f}%",
        f"常数因子 K: {k:.12e}",
        "",
        f"最近三年区间: {three_year_df['date'].min().date()} ~ {three_year_df['date'].max().date()}",
        f"样本数（日频）: {len(three_year_df)}",
        "",
        "统计量（最近三年）:",
        f"  均值: {p.mean() * 100:.2f}%",
        f"  中位数: {p.median() * 100:.2f}%",
        f"  P10: {quantiles.loc[0.1] * 100:.2f}%",
        f"  P25: {quantiles.loc[0.25] * 100:.2f}%",
        f"  P75: {quantiles.loc[0.75] * 100:.2f}%",
        f"  P90: {quantiles.loc[0.9] * 100:.2f}%",
        "",
        "Sanity Check:",
        f"  落在 +2%~+5% 的比例: {in_range_ratio * 100:.2f}%",
        f"  是否存在折价（<0）: {'是' if has_discount else '否'}",
        f"  断层检测阈值(|Δpremium|): {jump_threshold * 100:.2f}%",
        f"  疑似断层点数量: {jump_count}",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")


def run_for_asset(asset: AssetConfig) -> None:
    asset.output_dir.mkdir(parents=True, exist_ok=True)

    daily_df, k, qdii_path = build_daily_premium(asset)
    daily_csv_path = asset.output_dir / asset.daily_output_name
    daily_df.to_csv(daily_csv_path, index=False, encoding="utf-8-sig")

    trend_png = asset.output_dir / "溢价率走势.png"
    dist_png = asset.output_dir / "溢价率分布.png"
    report_txt = asset.output_dir / "report.txt"

    save_trend_plot(daily_df, asset.name, trend_png)
    three_year_df = save_distribution_plot(daily_df, asset.name, dist_png)
    make_report(asset, daily_df, three_year_df, k, qdii_path, report_txt)

    print(f"[{asset.name}] 完成")
    print(f"  - 日度结果: {daily_csv_path}")
    print(f"  - 走势图:   {trend_png}")
    print(f"  - 分布图:   {dist_png}")
    print(f"  - 报告:     {report_txt}")


def main() -> None:
    root = Path(__file__).resolve().parent

    assets = [
        AssetConfig(
            name="SPX QDII",
            index_path=root / "spx" / "^SPX.csv",
            # 优先按任务目标找 513100；若无可用校验日数据则 fallback 到现有 513650.SS
            qdii_candidates=[
                root / "spx" / "513100.SS.csv",
                root / "spx" / "513100.csv",
                root.parent / "data" / "qdii" / "513100.csv",
                root / "spx" / "513650.SS.csv",
            ],
            fx_path=root / "CNY=X.csv",
            calibration_date="2026-02-09",
            known_premium=0.0294,
            output_dir=root / "spx" / "output",
            daily_output_name="spx_qdii_daily_premium.csv",
        ),
        AssetConfig(
            name="NDX QDII",
            index_path=root / "ndx" / "^NDX.csv",
            qdii_candidates=[root / "ndx" / "159941.SZ.csv"],
            fx_path=root / "CNY=X.csv",
            calibration_date="2026-02-09",
            known_premium=0.0469,
            output_dir=root / "ndx" / "output",
            daily_output_name="ndx_qdii_daily_premium.csv",
        ),
    ]

    for asset in assets:
        run_for_asset(asset)


if __name__ == "__main__":
    main()
