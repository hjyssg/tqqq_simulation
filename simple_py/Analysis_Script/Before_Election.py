import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util

# 载入数据
data = _util.load_csv_as_dataframe("^SPX.csv")

# 确保日期列是datetime格式
data['Date'] = pd.to_datetime(data['Date'])

# 只在意二战后的数据
data = data[data['Date'].dt.year > 1950]

# 选举年份，跳过2008和2000
election_years = [1980, 1984, 1988, 1992, 1996, 2004, 2012, 2016, 2020]

# 分析每年10月15日至11月5日的市场表现
results = []
for year in election_years:
    start_date = pd.Timestamp(f"{year}-10-15")
    end_date = pd.Timestamp(f"{year}-11-15")
    
    spx_nov = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)][['Date', 'Close']]

    if not spx_nov.empty:
        # 计算市场变化百分比
        change = (spx_nov['Close'].iloc[-1] - spx_nov['Close'].iloc[0]) / spx_nov['Close'].iloc[0] * 100
        results.append({'Year': year, 'Change': change})
        
        # 绘制市场走势折线图
        plt.figure(figsize=(16, 8))
        plt.plot(spx_nov['Date'], spx_nov['Close'], marker='o', linestyle='-')
        plt.title(f"SPX Performance from {start_date.date()} to {end_date.date()} ({year})")
        plt.xlabel("Date")
        plt.ylabel("SPX Close Price")
        plt.grid(True)
        
        # 添加选举日的红色竖线（11月的第一个星期二）
        election_day = pd.Timestamp(f"{year}-11-{(2 + (1 + pd.Timestamp(f'{year}-11-01').weekday()) % 7)}")
        if start_date <= election_day <= end_date:
            plt.axvline(x=election_day, color='red', linestyle='--', label='Election Day')
            plt.legend()

        # 创建文件夹保存图片（如不存在）
        output_dir = 'election_year_charts'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存图片
        plt.savefig(f"{output_dir}/spx_performance_{year}.png")
        plt.close()

# 转换为DataFrame
results_df = pd.DataFrame(results)

# 显示统计结果
print(results_df["Change"].describe())

# 打印所有年份的变化百分比
print(results_df)
