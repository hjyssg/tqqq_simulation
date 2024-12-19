# 写一个python脚本，
# 我想比较的是2022,2023，2024实际三年涨幅百分比和历史上任意连续三年涨幅百分比。对象是1945年后的^SPX


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 定义函数计算涨幅百分比
def calculate_annual_returns(data):
    returns = (data['Adj Close'].resample('Y').last().pct_change() * 100).dropna()
    returns.name = 'Annual Return (%)'
    return returns

# 下载数据
start_date = "1945-01-01"
end_date = "2024-12-31"
spx = yf.download("^SPX", start=start_date, end=end_date)

# 确保数据按照日期排序
spx = spx.sort_index()

# 计算年化收益率
annual_returns = calculate_annual_returns(spx)

# 提取目标年份的收益率
target_years = [2022, 2023, 2024]
target_returns = annual_returns.loc[annual_returns.index.year.isin(target_years)]

# 计算连续三年的收益率和目标三年的涨幅
rolling_three_year_returns = (
    (1 + annual_returns / 100).rolling(3).apply(lambda x: (x.prod() - 1) * 100, raw=True)
).dropna()
target_three_year_return = (1 + target_returns / 100).prod() - 1

print(rolling_three_year_returns)

print(target_three_year_return)