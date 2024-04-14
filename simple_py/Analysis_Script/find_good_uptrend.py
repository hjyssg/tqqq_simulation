# 帮我写一个python脚本，找出20个交易日上涨超过20%的时段。

import pandas as pd
import os

# 读取CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../../data/^NDX.csv')
data = pd.read_csv(file_path)

# 将日期列转换为日期时间类型
data['Date'] = pd.to_datetime(data['Date'])

# 计算涨跌幅度
data['Daily_Return'] = data['Close'].pct_change() * 100

# 找出涨幅超过20%的时间段
window = 20  # 窗口大小为20天
threshold = 20  # 涨幅阈值为20%

# 使用滑动窗口计算涨幅
data['Over_20_percent'] = data['Daily_Return'].rolling(window=window).sum()
result = data[data['Over_20_percent'] > threshold]

# 输出结果
print("任意20天时间段内涨幅超过20%的情况：")
for index, row in result.iterrows():
    start_date = row['Date'] - pd.Timedelta(days=window - 1)  # 计算窗口的起始日期
    end_date = row['Date']  # 窗口的结束日期
    print(f"起始日期: {start_date}, 结束日期: {end_date}")



# 1991年，美联储进行了多次降息。在那一年，美国经历了经济衰退，美联储采取了一系列的货币政策来刺激经济增长和降低利率。从1990年7月到1992年9月，美联储进行了数次利率调整，逐步降低联邦基金利率（即银行之间短期借贷利率）

#  让chatgpt写了一个脚本，发现上次美股涨这么狠的的日期是
#  1991-01-18
#  1998-10-16
#  1999-10-28 
#  2000-06-02 
#  2001-01-04 
#  2001-04-12 
#  2002-10-16 
#  2009-03-14 
#  2020-03-26 

# 除了2000和2001，最终都提供了惊人的回报。 结论：坚定持有

