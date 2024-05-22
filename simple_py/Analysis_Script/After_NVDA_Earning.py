import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")

# 定义英伟达财报日期
earnings_dates = {
    "Q4 2024": "2023-02-22",
    "Q1 2024": "2023-05-24",
    "Q2 2024": "2023-08-23",
    "Q3 2024": "2023-11-21",
    "Q4 2024": "2024-02-21",
    # "Q1 2025": "2024-05-22"
}

# 解析日期并计算财报发布后的第二天
for quarter, date_str in earnings_dates.items():
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_day = date + timedelta(days=1)
    
    # 获取财报发布前一天和发布后第二天的收盘价
    day_before = data[data['Date'] == date]['Close'].values[0]
    day_after = data[data['Date'] == next_day]['Close'].values[0]
    
    # 计算变动幅度
    change = ((day_after - day_before) / day_before) * 100
    
    # 输出结果
    print(f"{date_str}: 财报发布前标普500收盘价 = {day_before}, 财报发布后第二天标普500收盘价 = {day_after}, 变动幅度 = {change:.2f}%")
