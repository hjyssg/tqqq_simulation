import pandas as pd
import os

begin_year = 1980

def calculate_cagr(file_path):
    # 读取CSV文件
    data = pd.read_csv(file_path)
    # 将 'Date' 列转换为日期时间类型
    data['Date'] = pd.to_datetime(data['Date'])

    data = data[data['Date'].dt.year >= begin_year]
    # data = data[data['Date'].dt.year > 2009]

    # 过滤掉除了日期列以外所有值都为NaN或Null的行
    data = data.dropna(subset=data.columns[data.columns != 'Date'], how='all')

    # 确保数据是按日期排序的
    data.sort_values('Date', inplace=True)
    # 计算投资期初和期末的价格
    initial_price = data.iloc[0]['Open'] if not pd.isnull(data.iloc[0]['Open']) and data.iloc[0]['Open'] != 0  else data.iloc[0]['Close']
    final_price = data.iloc[-1]['Open'] if not pd.isnull(data.iloc[-1]['Open']) and data.iloc[-1]['Open'] != 0 else data.iloc[-1]['Close']
    # 计算总的投资年数
    years = (data.iloc[-1]['Date'] - data.iloc[0]['Date']).days / 365.25
    # 计算CAGR
    CAGR = (final_price / initial_price) ** (1 / years) - 1


    start_date = data.iloc[0]['Date']
    end_date = data.iloc[-1]['Date']

    return CAGR, start_date, end_date

def process_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                # if not file.startswith("^"): 
                #     continue
                file_path = os.path.join(root, file)
                try:
                    cagr, start_date, end_date = calculate_cagr(file_path)
                    # print(f"{file}: 平均年回报率: {cagr * 100:.2f}%")
                    results.append((file, cagr))
                    print(f"{file}: 开始日期: {start_date.date()}, 结束日期: {end_date.date()}, 平均年回报率: {cagr * 100:.2f}%")
                except Exception as e:
                    print(f"Error processing {file}: {e}")


    # 根据CAGR排序
    results.sort(key=lambda x: x[1])

    # 分解文件名和CAGR用于可视化
    files, cagrs = zip(*results)

    import matplotlib.pyplot as plt
    # 设置matplotlib的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    # 创建条形图
    plt.figure(figsize=(10, 8))
    plt.barh(files, [cagr * 100 for cagr in cagrs], color='skyblue')
    plt.xlabel('平均年回报率 (%)')
    plt.title(f"""{begin_year}年起的平均年回报率""")

    bars = plt.barh(files, [cagr * 100 for cagr in cagrs], color='skyblue')
    # 为每个条形图添加文本标签
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.2f}%", va='center')


    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# 替换下面的路径为你的文件夹路径
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data')
process_files(file_path)


# AAPL.csv: 开始日期: 2001-01-02, 结束日期: 2024-04-01, 平均年回报率: 32.09%
# BTC-USD.csv: 开始日期: 2014-09-17, 结束日期: 2024-02-22, 平均年回报率: 64.81%
# IBM.csv: 开始日期: 2001-01-02, 结束日期: 2024-01-19, 平均年回报率: 3.30%
# MSFT.csv: 开始日期: 2001-01-02, 结束日期: 2024-03-28, 平均年回报率: 13.53%
# NVDA.csv: 开始日期: 2001-01-02, 结束日期: 2024-04-01, 平均年回报率: 32.19%
# QLD.csv: 开始日期: 2008-01-02, 结束日期: 2024-03-28, 平均年回报率: 22.86%
# qyld.csv: 开始日期: 2013-12-12, 结束日期: 2024-04-01, 平均年回报率: -3.19%
# soxl.csv: 开始日期: 2010-03-11, 结束日期: 2024-04-01, 平均年回报率: 35.65%
# SOXX.csv: 开始日期: 2001-07-13, 结束日期: 2024-03-28, 平均年回报率: 10.35%
# SPYD.csv: 开始日期: 2015-10-22, 结束日期: 2024-03-28, 平均年回报率: 3.53%
# sqqq.csv: 开始日期: 2010-02-11, 结束日期: 2024-04-01, 平均年回报率: -53.45%
# tqqq.csv: 开始日期: 2010-02-11, 结束日期: 2024-04-01, 平均年回报率: 42.69%
# upro.csv: 开始日期: 2009-06-25, 结束日期: 2024-03-26, 平均年回报率: 32.30%
# VXUS.csv: 开始日期: 2011-01-28, 结束日期: 2024-03-28, 平均年回报率: 1.41%
# YINN.csv: 开始日期: 2009-12-03, 结束日期: 2024-03-28, 平均年回报率: -23.14%
# ^N225.csv: 开始日期: 2001-01-04, 结束日期: 2024-04-02, 平均年回报率: 4.64%
# ^NDX.csv: 开始日期: 2001-01-02, 结束日期: 2024-04-01, 平均年回报率: 9.24%
# ^RUT.csv: 开始日期: 2001-01-02, 结束日期: 2024-04-01, 平均年回报率: 6.58%
# ^SPX.csv: 开始日期: 2001-01-02, 结束日期: 2024-04-01, 平均年回报率: 6.13%