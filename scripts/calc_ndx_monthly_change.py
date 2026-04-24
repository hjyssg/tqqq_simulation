"""计算 ^NDX 每月涨跌百分比"""
import csv
from collections import OrderedDict

INPUT = "data/^NDX.csv"
OUTPUT = "data/^NDX_monthly_change.txt"

with open(INPUT, "r", encoding="utf-8") as f:
    # 跳过前 3 行元数据 (Price, Ticker, Date)
    for _ in range(3):
        next(f)
    reader = csv.reader(f)
    # 按年月存放最后一个交易日的收盘价
    monthly_close: OrderedDict[str, float] = OrderedDict()
    for row in reader:
        date_str = row[0].strip()
        price_str = row[2].strip() # 使用 Close 列 (索引2)
        if not date_str or not price_str:
            continue
        try:
            price = float(price_str)
        except ValueError:
            continue
        year_month = date_str[:7]  # "1985-10"
        monthly_close[year_month] = price  # 后面的覆盖前面的，最终保留该月最后一个

# 计算涨跌幅
results = []
prev_price = None
for ym, price in monthly_close.items():
    if prev_price is not None:
        pct = (price - prev_price) / prev_price * 100
        results.append(f"{ym}, {pct:+.2f}%")
    else:
        results.append(f"{ym}, N/A")  # 首月无环比
    prev_price = price

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(results) + "\n")

print(f"已输出 {len(results)} 个月的数据到 {OUTPUT}")