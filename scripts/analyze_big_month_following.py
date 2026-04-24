"""分析 ^NDX 月涨幅>8% 后下一个月的表现"""
import csv

INPUT = "data/^NDX_monthly_change.txt"
OUTPUT = "data/^NDX_分析_大涨后表现.txt"

data = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(", ")
        if len(parts) != 2:
            continue
        ym = parts[0]
        pct_str = parts[1]
        if pct_str == "N/A":
            continue
        try:
            pct = float(pct_str.replace("%", ""))
        except ValueError:
            continue
        data.append((ym, pct))

# 找出月涨幅 > 8% 的月份，以及下个月
big_months = []
following_months = []
for i in range(len(data) - 1):
    ym, pct = data[i]
    if pct > 8.0:
        next_ym, next_pct = data[i + 1]
        big_months.append((ym, pct, next_ym, next_pct))
        following_months.append(next_pct)

total = len(big_months)

if total == 0:
    output = "无月涨幅>8%的记录"
else:
    positive = sum(1 for p in following_months if p > 0)
    negative = sum(1 for p in following_months if p < 0)
    avg_next = sum(following_months) / total
    max_next = max(following_months)
    min_next = min(following_months)

    lines = []
    lines.append("=" * 60)
    lines.append("^NDX 月度涨幅>8% 后下个月表现统计")
    lines.append(f"数据区间: {data[0][0]} ~ {data[-1][0]}")
    lines.append(f"总月数: {len(data)}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"月涨幅>8% 共出现: {total} 次")
    lines.append(f"下个月平均涨跌: {avg_next:+.2f}%")
    lines.append(f"下个月中位数涨跌: {sorted(following_months)[len(following_months)//2]:+.2f}%")
    lines.append(f"下个月最大涨幅: {max_next:+.2f}%")
    lines.append(f"下个月最大跌幅: {min_next:+.2f}%")
    lines.append(f"下个月上涨次数: {positive} ({positive/total*100:.1f}%)")
    lines.append(f"下个月下跌次数: {negative} ({negative/total*100:.1f}%)")
    lines.append("")
    lines.append("-" * 60)
    lines.append("详细清单 (当月涨幅>8%  -> 下月涨跌):")
    lines.append("-" * 60)

    for ym, pct, next_ym, next_pct in big_months:
        arrow = "🟢" if next_pct > 0 else "🔴"
        lines.append(f"{ym} ({pct:+.2f}%)  ->  {next_ym} {arrow} {next_pct:+.2f}%")

    lines.append("")
    lines.append("-" * 60)
    lines.append("下个月涨跌幅分布:")
    lines.append("-" * 60)

    buckets = [(-100, -10), (-10, -5), (-5, -2), (-2, 0), (0, 2), (2, 5), (5, 10), (10, 100)]
    for lo, hi in buckets:
        cnt = sum(1 for p in following_months if lo < p <= hi)
        bar = "█" * cnt
        lo_str = f"{lo:>+5}%" if lo > -100 else " <=-10%"
        hi_str = f"{hi:>+4}%"
        if lo <= -100:
            range_str = f" <=-10%"
        else:
            range_str = f"{lo:>+5.0f}% ~ {hi:>+4.0f}%"
        lines.append(f"{range_str}: {cnt:>2d}次 {bar}")

    output = "\n".join(lines)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(output + "\n")

print(f"已输出到 {OUTPUT}")
print(output)