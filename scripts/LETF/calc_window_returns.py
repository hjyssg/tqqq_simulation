# -*- coding: utf-8 -*-
"""
统计不同时间窗口下 QQQ / SPY 及各衍生品（杠杆 ETF）的涨跌百分比。

数据来源：data/ 下的 yfinance 真实历史收盘价（Adj Close 复权价）。

时间窗口：
    - YTD     年初至今
    - 1M / 3M / 6M   过去 1/3/6 个月
    - 1Y / 3Y / 5Y   过去 1/3/5 年
    - Max     自上市至今

输出：一个自包含的 HTML（图表 + 表格 + 文字）到 output/ 目录。
"""
import os
import sys
import base64
import io

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无显示环境，直接输出图片
import matplotlib.pyplot as plt

# 复用项目工具的加载函数 & 绘图初始化
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
ETFS = [
    # (文件名, 显示名, 分组, 杠杆倍数)
    ("QQQ.csv",  "QQQ",  "纳指", 1),
    ("QLD.csv",  "QLD",  "纳指", 2),
    ("TQQQ.csv", "TQQQ", "纳指", 3),
    ("SPY.csv",  "SPY",  "标普", 1),
    ("SSO.csv",  "SSO",  "标普", 2),
    ("UPRO.csv", "UPRO", "标普", 3),
    ("SPXL.csv", "SPXL", "标普", 3),
    ("SMH.csv",  "SMH",  "半导体", 1),
]

# 窗口定义：(显示名, pd.DateOffset 或 None 表示 YTD/Max 特殊处理)
WINDOWS = [
    ("YTD",    None),
    ("1M",     pd.DateOffset(months=1)),
    ("3M",     pd.DateOffset(months=3)),
    ("6M",     pd.DateOffset(months=6)),
    ("1Y",     pd.DateOffset(years=1)),
    ("3Y",     pd.DateOffset(years=3)),
    ("5Y",     pd.DateOffset(years=5)),
    ("10Y",    pd.DateOffset(years=10)),
    ("Max",    None),
]

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_SCRIPT_DIR, "..", "..", "data")   # repo_root/data
_OUTDIR = os.path.join(_SCRIPT_DIR, "..", "..", "output")   # repo_root/output


def load_adj_close(filename):
    """加载 Adj Close 复权价序列（以 Date 为索引）。"""
    path = os.path.join(_DATA_DIR, filename)
    df = pd.read_csv(path)
    # 兼容 yfinance 的多级表头格式
    if "Price" in df.columns and any("Ticker" in str(v) for v in df.iloc[0]):
        df = pd.read_csv(path, skiprows=[1, 2])
        df.rename(columns={"Price": "Date"}, inplace=True)
    df.columns = [str(c).strip().replace('"', "").replace("'", "") for c in df.columns]
    df = df[df["Date"].astype(str).str.contains(r"\d{4}")]
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    df = df.dropna(subset=["Adj Close"])
    return df.set_index("Date")["Adj Close"].astype(float)


def window_return(series, window_name, latest_dt, latest_val):
    """返回该 ETF 在指定窗口的收益率（百分比, 可为 None 表示数据不足）。"""
    if window_name == "YTD":
        start = pd.Timestamp(year=latest_dt.year, month=1, day=1)
        start_val = series[series.index <= start]
        if start_val.empty:
            return None
        start_val = start_val.iloc[-1]
    elif window_name == "Max":
        start_val = series.iloc[0]
    else:
        offset = dict(WINDOWS)[window_name]
        start = latest_dt - offset
        start_val = series[series.index <= start]
        if start_val.empty:
            return None
        start_val = start_val.iloc[-1]

    if start_val == 0 or np.isnan(start_val):
        return None
    return (latest_val / start_val - 1) * 100.0


def chart_img_to_base64(fig):
    """把 matplotlib figure 保存为 PNG 并转 base64，返回可嵌入 HTML 的字符串。"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def apply_chinese_font():
    """配置 matplotlib 中文字体，避免图表中文显示为方框。"""
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun',
                                       'PingFang SC', 'Arial Unicode MS',
                                       'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def build_bar_chart(returns_df, latest_dt):
    """按窗口分组的条形图：各 ETF 在各窗口的涨跌。"""
    colors = {"纳指": "#2E86DE", "标普": "#E67E22", "半导体": "#27AE60"}
    show_windows = ["YTD", "1M", "3M", "6M", "1Y", "3Y", "5Y"]

    data = {}
    names = {}
    for w, _ in WINDOWS:
        data[w] = []
        names[w] = []
        for etf in ETFS:
            name = etf[1]
            r = returns_df.loc[name, w]
            data[w].append(r if r is not None else 0.0)
            names[w].append(name if r is not None else "")

    fig, axes = plt.subplots(2, 4, figsize=(16, 9))
    axes = axes.flatten()

    def draw(ax, w, is_max=False):
        vals = data[w]
        nms = names[w]
        bar_colors = [colors[etf[2]] for etf in ETFS]
        bars = ax.barh(nms, vals, color=bar_colors, edgecolor="black", linewidth=0.3)
        ax.axvline(0, color="gray", linewidth=0.8)
        title = "Max(上市至今)" if is_max else w
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.tick_params(labelsize=9)
        for b in bars:
            v = b.get_width()
            if v >= 0:
                ax.text(v * 1.02, b.get_y() + b.get_height() / 2,
                        f"{v:+.1f}%", va="center", fontsize=8, fontweight="bold")
            else:
                ax.text(v * 1.02 - 1.5, b.get_y() + b.get_height() / 2,
                        f"{v:+.1f}%", va="center", fontsize=8, fontweight="bold")
        lo = min(vals) * 1.25 if vals and min(vals) < 0 else -1
        hi = 1.25 * max(vals) if vals else 1
        ax.set_xlim(lo, hi)

    for ax, w in zip(axes, show_windows):
        draw(ax, w, is_max=False)
    draw(axes[7], "Max", is_max=True)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors["纳指"], label="纳指系 (QQQ/QLD/TQQQ)"),
                       Patch(facecolor=colors["标普"], label="标普系 (SPY/SSO/UPRO/SPXL)"),
                       Patch(facecolor=colors["半导体"], label="半导体 (SMH)")]
    fig.legend(handles=legend_elements, loc="lower center", ncol=3, fontsize=11,
               framealpha=1, edgecolor="gray")
    fig.suptitle(f"各 ETF 不同时间窗口涨跌幅（截至 {latest_dt:%Y-%m-%d}）",
                 fontsize=16, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    return chart_img_to_base64(fig)


def build_growth_chart(series_dict, latest_dt):
    """自共同起点（覆盖全部衍生品）的归一化复权净值曲线（对数刻度）。"""
    start = pd.Timestamp("2010-02-01")
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = {"QQQ": "#2E86DE", "QLD": "#1ABC9C", "TQQQ": "#E74C3C",
              "SPY": "#F39C12", "SSO": "#9B59B6", "UPRO": "#E67E22",
              "SPXL": "#C0392B", "SMH": "#27AE60"}
    for name, s in series_dict.items():
        s = s[s.index >= start]
        if s.empty:
            continue
        norm = s / s.iloc[0] * 100  # 起点=100
        ax.plot(norm.index, norm, label=f"{name}", linewidth=1.6,
                color=colors.get(name))
    ax.set_yscale("log")
    ax.axhline(100, color="gray", linestyle="--", linewidth=0.8)
    ax.set_title(f"复权净值归一化曲线（起点=100, 对数刻度, 截至 {latest_dt:%Y-%m-%d}）",
                 fontsize=15, fontweight="bold")
    ax.set_ylabel("归一化净值（起点=100）")
    ax.grid(alpha=0.3)
    ax.legend(ncol=8, fontsize=10, loc="upper left")
    return chart_img_to_base64(fig)


def build_html(returns_df, cagr_df, latest_dt, bar_b64, growth_b64, years_listed):
    """生成自包含 HTML 字符串。"""
    def fmt(v):
        if v is None:
            return '<td class="na">N/A</td>'
        color = "#c0392b" if v < 0 else "#1e8449"
        return f'<td style="color:{color};font-weight:600">{v:+.2f}%</td>'

    thead = "<tr><th>ETF</th><th>分组</th><th>杠杆</th><th>上市年限</th>" + \
            "".join(f"<th>{w}</th>" for w, _ in WINDOWS if w != "Max") + \
            "<th>Max(上市)</th></tr>"
    trows = ""
    for etf in ETFS:
        name, group, lev = etf[1], etf[2], etf[3]
        yl = years_listed.get(name, None)
        yl_str = f"{yl:.1f}年" if yl is not None else "N/A"
        trows += f'<tr><td><b>{name}</b></td><td>{group}</td><td>{lev}x</td><td>{yl_str}</td>'
        for w, _ in WINDOWS[:-1]:
            trows += fmt(returns_df.loc[name, w])
        trows += fmt(returns_df.loc[name, "Max"])
        trows += "</tr>"

    thead2 = "<tr><th>ETF</th><th>3年 CAGR</th><th>5年 CAGR</th><th>10年 CAGR</th></tr>"
    trows2 = ""
    for etf in ETFS:
        name = etf[1]
        trows2 += f"<tr><td><b>{name}</b></td>"
        for w in ["3Y", "5Y", "10Y"]:
            v = cagr_df.loc[name, w]
            if v is None:
                trows2 += '<td class="na">N/A</td>'
            else:
                color = "#c0392b" if v < 0 else "#1e8449"
                trows2 += f'<td style="color:{color};font-weight:600">{v:+.2f}%</td>'
        trows2 += "</tr>"

    asof = f"{latest_dt:%Y-%m-%d}"

    notes = []
    for etf in ETFS:
        name = etf[1]
        ytd = returns_df.loc[name, "YTD"]
        y1 = returns_df.loc[name, "1Y"]
        y3 = returns_df.loc[name, "3Y"]
        y5 = returns_df.loc[name, "5Y"]
        note = f"{name}：YTD {ytd:+.2f}%，近1年 {y1:+.2f}%，近3年 {y3:+.2f}%，近5年 {y5:+.2f}%"
        notes.append(note)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ETF 各时间窗口涨跌幅统计 - {asof}</title>
<style>
  body {{ font-family: "Microsoft YaHei","PingFang SC","Segoe UI",sans-serif;
        background: #f4f6f8; margin:0; color:#2c3e50; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:24px; }}
  h1 {{ color:#1a1a2e; border-bottom:3px solid #3498db; padding-bottom:10px; }}
  h2 {{ color:#34495e; margin-top:8px; }}
  .card {{ background:#fff; border-radius:10px; padding:20px 24px;
          box-shadow:0 2px 8px rgba(0,0,0,.08); margin:18px 0; }}
  .asof {{ color:#7f8c8d; font-size:14px; margin-top:-6px; }}
  table {{ border-collapse:collapse; width:100%; background:#fff;
          border-radius:8px; overflow:hidden; }}
  th,td {{ border:1px solid #ecf0f1; padding:9px 12px; text-align:center; font-size:14px; }}
  th {{ background:#3498db; color:#fff; font-weight:600; }}
  tr:nth-child(even) {{ background:#f8fafb; }}
  td.na {{ color:#bdc3c7; }}
  .note {{ line-height:2.0; color:#34495e; }}
  .legend {{ color:#7f8c8d; font-size:13px; }}
  img {{ max-width:100%; border-radius:8px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>📊 QQQ / SPY 及相关杠杆 ETF · 各时间窗口涨跌幅</h1>
  <p class="asof">数据截至：<b>{asof}</b> ｜ 基于 Adj Close 复权价 ｜ 来源: yfinance</p>

  <div class="card">
    <h2>① 涨跌幅汇总表</h2>
    <table>
      <thead>{thead}</thead>
      <tbody>{trows}</tbody>
    </table>
    <p class="legend">注：YTD=年初至今；1M/3M/6M=近1/3/6个月；1Y/3Y/5Y=近1/3/5年；
      Max=自该 ETF 上市以来的累计涨幅。绿=上涨，红=下跌。</p>
  </div>

  <div class="card">
    <h2>② 年化收益率（CAGR）</h2>
    <table>
      <thead>{thead2}</thead>
      <tbody>{trows2}</tbody>
    </table>
    <p class="legend">CAGR = (期末/期初)^(1/年数) - 1，剔除持有年限差异后更能反映真实年化回报。</p>
  </div>

  <div class="card">
    <h2>③ 各窗口涨跌幅对比图</h2>
    <img src="data:image/png;base64,{bar_b64}" alt="窗口涨跌对比">
  </div>

  <div class="card">
    <h2>④ 复权净值归一化曲线</h2>
    <img src="data:image/png;base64,{growth_b64}" alt="净值曲线">
    <p class="legend">以 2010 年 2 月起为共同起点（起点=100），对数刻度展示长期财富增长差异。</p>
  </div>

  <div class="card">
    <h2>⑤ 文字速览</h2>
    <p class="note">{'<br>'.join(notes)}</p>
  </div>
</div>
</body>
</html>"""
    return html


def main():
    """主流程：加载数据 -> 计算窗口收益 -> 生成图表 -> 输出 HTML。"""
    series_dict = {}
    for fn, name, _, _ in ETFS:
        series_dict[name] = load_adj_close(fn)

    latest_dt = max(s.index.max() for s in series_dict.values())
    latest_val = {n: s.loc[s.index <= latest_dt].iloc[-1]
                  for n, s in series_dict.items()}

    returns_df = pd.DataFrame(index=[e[1] for e in ETFS], columns=[w for w, _ in WINDOWS])
    cagr_df = pd.DataFrame(index=[e[1] for e in ETFS], columns=["3Y", "5Y", "10Y"])

    for etf in ETFS:
        name = etf[1]
        s = series_dict[name]
        for w, _offset in WINDOWS:
            r = window_return(s, w, latest_dt, latest_val[name])
            returns_df.loc[name, w] = r
        for w, years in [("3Y", 3), ("5Y", 5), ("10Y", 10)]:
            total = returns_df.loc[name, w]
            if total is not None:
                cagr = ((1 + total / 100) ** (1 / years) - 1) * 100
                cagr_df.loc[name, w] = cagr
            else:
                cagr_df.loc[name, w] = None

    apply_chinese_font()
    bar_b64 = build_bar_chart(returns_df, latest_dt)
    growth_b64 = build_growth_chart(series_dict, latest_dt)

    # 上市年限（自首个交易日至今，单位：年）
    years_listed = {}
    for name, s in series_dict.items():
        first = s.index.min()
        years_listed[name] = (latest_dt - first).days / 365.25

    html = build_html(returns_df, cagr_df, latest_dt, bar_b64, growth_b64, years_listed)

    outdir = os.path.abspath(_OUTDIR)
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, f"etf_window_returns_{latest_dt:%Y%m%d}.html")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)

    # 控制台预览
    print("数据截至:", latest_dt)
    print("\n=== 各窗口涨跌幅 (%) ===")
    print(returns_df.to_string())
    print("\n=== 年化 CAGR (%) ===")
    print(cagr_df.to_string())
    print(f"\n✅ 已生成 HTML: {outfile}")
    print(f"   大小: {os.path.getsize(outfile)/1024:.1f} KB")


if __name__ == "__main__":
    main()

