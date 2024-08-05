import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 读取CSV文件
spx_fn = "^SPX.csv"
spx_data = _util.load_csv_as_dataframe(spx_fn)

n225_fn = "^N225.csv"
n225_data = _util.load_csv_as_dataframe(n225_fn)

# 将Date列转换为日期格式
spx_data['Date'] = pd.to_datetime(spx_data['Date'])
n225_data['Date'] = pd.to_datetime(n225_data['Date'])

# 写死跌幅超过10%的日期数组
drop_dates = ['1987-10-20', '2008-10-16', '2011-03-15']

# 将字符串数组转换为日期格式
drop_dates = pd.to_datetime(drop_dates)

observation_period = 20

# 为每个大跌日生成独立的图表并保存
for drop_date in drop_dates:
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    start_date = drop_date - pd.Timedelta(days=observation_period)
    end_date = drop_date + pd.Timedelta(days=observation_period)
    
    spx_preceding_data = spx_data[(spx_data['Date'] >= start_date) & (spx_data['Date'] <= end_date)]
    n225_preceding_data = n225_data[(n225_data['Date'] >= start_date) & (n225_data['Date'] <= end_date)]
    
    # 用竖线标红发生的日期
    ax1.axvline(x=drop_date, color='red', linestyle='--', label='Drop Date')
    
    # 绘制美国股市的图表
    ax1.plot(spx_preceding_data['Date'], spx_preceding_data['Close'], label="SPX Close Price", color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('SPX Close Price', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # 创建第二个Y轴并绘制日本股市的图表
    ax2 = ax1.twinx()
    ax2.plot(n225_preceding_data['Date'], n225_preceding_data['Close'], label="N225 Close Price", color='green')
    ax2.set_ylabel('N225 Close Price', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title(f'SPX and N225 Performance around {drop_date.date()}')
    
    fig.tight_layout()  # 确保标签不会重叠
    
    # 保存图表为图片
    file_name = f'{drop_date.date()}_spx_n225_performance.png'
    plt.savefig(file_name)
    
    # 关闭当前图表
    plt.close()

print("图片已保存。")
