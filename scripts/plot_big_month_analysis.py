"""生成 ^NDX 月度大涨后表现可视化 SVG"""
import math

# 读取数据
INPUT = "data/^NDX_monthly_change.txt"

data = []
with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(", ")
        if len(parts) != 2:
            continue
        pct_str = parts[1]
        if pct_str == "N/A":
            continue
        try:
            pct = float(pct_str.replace("%", ""))
        except ValueError:
            continue
        data.append(pct)

# 找出大涨月及下月
big_months = []
following = []
for i in range(len(data) - 1):
    if data[i] > 8.0:
        big_months.append(data[i])
        following.append(data[i + 1])

total = len(big_months)
positive = sum(1 for p in following if p > 0)

# ───── SVG 参数 ─────
W = 800
H = 900
M = 65   # margin (加大给Y轴标签)
chart_w = W - 2 * M
chart_h = 380

# 计算直方图 bins
bins = [(-30, -10), (-10, -5), (-5, -2), (-2, 0), (0, 2), (2, 5), (5, 10), (10, 30)]
bin_labels = ["≤-10%", "-10%~-5%", "-5%~-2%", "-2%~0%", "0%~2%", "2%~5%", "5%~10%", "≥10%"]
bin_counts = [sum(1 for p in following if lo < p <= hi) for lo, hi in bins]
max_count = max(bin_counts) if max(bin_counts) > 0 else 1

bar_w = chart_w / len(bins)
colors_bar = ["#c0392b","#e74c3c","#e67e22","#f39c12","#2ecc71","#27ae60","#1abc9c","#16a085"]

# ─── 散点图数据范围 ───
min_y_range = min(following)
max_y_range = max(following)

# 构建 SVG
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Arial, sans-serif">')
svg.append('<rect width="100%" height="100%" fill="#fafafa"/>')

# 标题
svg.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">^NDX 月度涨幅>8% 后下月表现分布</text>')
svg.append(f'<text x="{W/2}" y="48" text-anchor="middle" font-size="13" fill="#7f8c8d">数据区间: 1985~2026 | 共 {total} 次大涨 | 下月平均 +{(sum(following)/total):.2f}% | 上涨概率 {positive/total*100:.1f}%</text>')

# ─── 直方图 ───
x0 = M
y0 = 75
hist_bottom = y0 + chart_h

# Y轴
max_y = max_count + 1
y_scale = chart_h / max_y

for i in range(max_y + 1):
    y = y0 + chart_h - i * y_scale
    svg.append(f'<line x1="{x0-3}" y1="{y}" x2="{W-M+3}" y2="{y}" stroke="#ecf0f1" stroke-width="1"/>')
    svg.append(f'<text x="{x0-8}" y="{y+4}" text-anchor="end" font-size="11" fill="#95a5a6">{i}</text>')

svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{hist_bottom}" stroke="#bdc3c7" stroke-width="1"/>')
svg.append(f'<line x1="{x0}" y1="{hist_bottom}" x2="{W-M}" y2="{hist_bottom}" stroke="#bdc3c7" stroke-width="1"/>')

# 柱子
for i, (cnt, label) in enumerate(zip(bin_counts, bin_labels)):
    x = x0 + i * bar_w + 2
    bar_h = cnt * y_scale
    y = y0 + chart_h - bar_h
    svg.append(f'<rect x="{x}" y="{y}" width="{bar_w-4}" height="{max(bar_h, 1)}" fill="{colors_bar[i]}" rx="3" opacity="0.85"/>')
    if cnt > 0:
        svg.append(f'<text x="{x + (bar_w-4)/2}" y="{y-6}" text-anchor="middle" font-size="13" font-weight="bold" fill="{colors_bar[i]}">{cnt}</text>')
    svg.append(f'<text x="{x + (bar_w-4)/2}" y="{hist_bottom+16}" text-anchor="middle" font-size="11" fill="#555">{label}</text>')

svg.append(f'<text x="{x0 + chart_w/2}" y="{hist_bottom+36}" text-anchor="middle" font-size="13" fill="#7f8c8d">下月涨跌幅区间</text>')

# ─── 散点图 ───
scatter_y0 = hist_bottom + 60
scatter_h = 200
scatter_w = chart_w

svg.append(f'<text x="{W/2}" y="{scatter_y0-8}" text-anchor="middle" font-size="15" font-weight="bold" fill="#2c3e50">当月涨幅 vs 下月涨幅 (散点图)</text>')

# Y轴
svg.append(f'<line x1="{x0}" y1="{scatter_y0}" x2="{x0}" y2="{scatter_y0+scatter_h}" stroke="#bdc3c7" stroke-width="1"/>')

# 0%虚线
zero_y = scatter_y0 + scatter_h - (0 - min_y_range) / (max_y_range - min_y_range) * scatter_h if max_y_range > min_y_range else scatter_y0 + scatter_h/2
svg.append(f'<line x1="{x0}" y1="{zero_y}" x2="{W-M}" y2="{zero_y}" stroke="#e74c3c" stroke-width="1" stroke-dasharray="5,4" opacity="0.5"/>')

# Y轴刻度（自动按10%步长）
tick_start = int(min_y_range / 10) * 10
tick_end = int(max_y_range / 10) * 10 + 10
for tv in range(tick_start, tick_end, 10):
    ty = scatter_y0 + scatter_h - (tv - min_y_range) / (max_y_range - min_y_range) * scatter_h
    label = f"{tv:+.0f}%"
    svg.append(f'<line x1="{x0-4}" y1="{ty}" x2="{x0}" y2="{ty}" stroke="#bdc3c7" stroke-width="1"/>')
    svg.append(f'<text x="{x0-8}" y="{ty+4}" text-anchor="end" font-size="10" fill="#7f8c8d">{label}</text>')

# 0%特殊标注
if 0 not in range(tick_start, tick_end, 10):
    svg.append(f'<line x1="{x0-4}" y1="{zero_y}" x2="{x0}" y2="{zero_y}" stroke="#e74c3c" stroke-width="2"/>')
    svg.append(f'<text x="{x0-8}" y="{zero_y+4}" text-anchor="end" font-size="10" fill="#e74c3c" font-weight="bold">0%</text>')

# 散点
max_x_range = max(big_months)
for bx, fx in zip(big_months, following):
    if max_x_range > 8:
        sx = x0 + (bx - 8) / (max_x_range - 8) * scatter_w
    else:
        sx = x0 + scatter_w / 2
    sy = scatter_y0 + scatter_h - (fx - min_y_range) / (max_y_range - min_y_range) * scatter_h
    color = "#27ae60" if fx > 0 else "#e74c3c"
    svg.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.5" fill="{color}" opacity="0.7"/>')

# X轴标题
svg.append(f'<text x="{x0 + scatter_w/2}" y="{scatter_y0+scatter_h+18}" text-anchor="middle" font-size="11" fill="#7f8c8d">当月涨幅 →</text>')

# Y轴标题
svg.append(f'<text x="{x0-8}" y="{scatter_y0-6}" text-anchor="middle" font-size="11" fill="#7f8c8d">下月</text>')
svg.append(f'<text x="{x0-8}" y="{scatter_y0+scatter_h+6}" text-anchor="middle" font-size="11" fill="#7f8c8d">涨跌</text>')

# 图例
legend_y = scatter_y0 + scatter_h + 35
svg.append(f'<circle cx="{x0+10}" cy="{legend_y}" r="4.5" fill="#27ae60"/>')
svg.append(f'<text x="{x0+22}" y="{legend_y+4}" font-size="11" fill="#555">上涨</text>')
svg.append(f'<circle cx="{x0+90}" cy="{legend_y}" r="4.5" fill="#e74c3c"/>')
svg.append(f'<text x="{x0+102}" y="{legend_y+4}" font-size="11" fill="#555">下跌</text>')

svg.append('</svg>')

output = "\n".join(svg)
OUTPUT_SVG = "data/^NDX_分析_大涨后表现.svg"
with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
    f.write(output)

print(f"SVG 已保存到 {OUTPUT_SVG}")
print(f"文件大小: {len(output)} bytes")