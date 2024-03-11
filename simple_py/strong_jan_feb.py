import pandas as pd
import os


# 读取股票数据CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data/1985年开始的纳斯达克100^NDX.csv')
df = pd.read_csv(file_path)

data = df

# 1. 转换日期列，这一步已完成
data['Date'] = pd.to_datetime(data['Date'])

# 确保 'Close' 列是数字类型
data['Close'] = pd.to_numeric(data['Close'])

# 2. 计算每年1月和2月的涨幅以及全年的涨幅
result = []  # 用于存储结果的列表

for year in range(data['Date'].dt.year.min(), data['Date'].dt.year.max() + 1):
    yearly_data = data[data['Date'].dt.year == year]  # 筛选出该年份的数据
    jan_feb_data = yearly_data[yearly_data['Date'].dt.month.isin([1, 2])]  # 筛选出1月和2月的数据
    if not jan_feb_data.empty:
        start_price = jan_feb_data.iloc[0]['Open']  # 1月的起始价格
        end_price = jan_feb_data.iloc[-1]['Close']  # 2月的结束价格
        jan_feb_growth = ((end_price - start_price) / start_price) * 100  # 计算1月和2月的涨幅
        
        if jan_feb_growth > 5:  # 如果1月和2月的涨幅超过5%
            start_year_price = yearly_data.iloc[0]['Open']  # 全年的起始价格
            end_year_price = yearly_data.iloc[-1]['Close']  # 全年的结束价格
            yearly_growth = ((end_year_price - start_year_price) / start_year_price) * 100  # 计算全年的涨幅
            result.append((year, jan_feb_growth, yearly_growth))  # 添加到结果列表

# 输出结果
for year, jan_feb_growth, yearly_growth in result:
    print(f"Year: {year}, Jan-Feb Growth: {jan_feb_growth:.2f}%, Yearly Growth: {yearly_growth:.2f}%")
