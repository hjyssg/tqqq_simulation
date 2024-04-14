import pandas as pd
import mplfinance as mpf
import os

# 读取CSV文件
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../../data/^NDX.csv')
df = pd.read_csv(file_path)


# 将日期列转换为日期时间格式
df['Date'] = pd.to_datetime(df['Date'])

# 将日期设置为索引
df.set_index('Date', inplace=True)

# 计算周线数据
df_weekly = df.resample('W-Fri').last()

# 计算20周移动平均
df_weekly['MA20'] = df_weekly['Close'].rolling(window=20).mean()

# 计算布林带指标
rolling_std = df_weekly['Close'].rolling(window=20).std()
df_weekly['UpperBand'] = df_weekly['MA20'] + 2 * rolling_std
df_weekly['MiddleBand'] = df_weekly['MA20']
df_weekly['LowerBand'] = df_weekly['MA20'] - 2 * rolling_std

# 将数据准备为mplfinance所需的格式
ohlc_data = df_weekly[['Open', 'High', 'Low', 'Close', 'Volume']]

# 设置布林带的显示参数
bollinger_bands = mpf.make_addplot(df_weekly[['UpperBand', 'MiddleBand', 'LowerBand']], secondary_y=False)

# 绘制股票图表
mpf.plot(ohlc_data, type='candle', addplot=bollinger_bands, title='Weekly Stock Price with Bollinger Bands', ylabel='Price', ylabel_lower='Volume', style='yahoo')
