import pandas as pd
import os

def calculate_cagr(file_path):
    # 读取CSV文件
    data = pd.read_csv(file_path)
    # 将 'Date' 列转换为日期时间类型
    data['Date'] = pd.to_datetime(data['Date'])

    # data = data[data['Date'].dt.year > 1985]
    # data = data[data['Date'].dt.year > 2009]


    # 确保数据是按日期排序的
    data.sort_values('Date', inplace=True)
    # 计算投资期初和期末的价格
    initial_price = data.iloc[0]['Open']
    final_price = data.iloc[-1]['Open']
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
    plt.title('平均年回报率')
    # 添加网格线
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# 替换下面的路径为你的文件夹路径
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data')
process_files(file_path)


# ^SPX.csv: 开始日期: 1986-01-02, 结束日期: 2024-01-24, 平均年回报率: 8.60%
# 纳斯达克^IXIC.csv: 开始日期: 1986-01-02, 结束日期: 2023-12-21, 平均年回报率: 10.61%
# 纳斯达克100^NDX.csv: 开始日期: 1986-01-02, 结束日期: 2024-01-08, 平均年回报率: 13.51%
# 罗素 ^RUT.csv: 开始日期: 1987-09-10, 结束日期: 2022-10-21, 平均年回报率: 6.84%
# AAPL.csv: 开始日期: 1986-01-02, 结束日期: 2022-10-27, 平均年回报率: 21.99%
# BTC-USD.csv: 开始日期: 2014-09-17, 结束日期: 2024-02-22, 平均年回报率: 64.81%
# IBM.csv: 开始日期: 1986-01-02, 结束日期: 2024-01-19, 平均年回报率: 4.10%
# qyld.csv: 开始日期: 2013-12-12, 结束日期: 2022-08-12, 平均年回报率: -3.43%
# soxl.csv: 开始日期: 2012-08-15, 结束日期: 2022-08-12, 平均年回报率: 44.61%
# SOXX.csv: 开始日期: 2001-07-13, 结束日期: 2024-03-28, 平均年回报率: 10.35%
# SPYD.csv: 开始日期: 2015-10-22, 结束日期: 2024-03-28, 平均年回报率: 3.53%
# sqqq.csv: 开始日期: 2012-08-15, 结束日期: 2022-08-12, 平均年回报率: -52.80%
# tqqq.csv: 开始日期: 2010-02-11, 结束日期: 2023-12-22, 平均年回报率: 41.63%
# upro.csv: 开始日期: 2009-06-25, 结束日期: 2024-03-26, 平均年回报率: 32.30%
# VXUS.csv: 开始日期: 2011-01-28, 结束日期: 2024-03-28, 平均年回报率: 1.41%