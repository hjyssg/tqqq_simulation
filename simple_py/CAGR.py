import pandas as pd
import os

def calculate_cagr(file_path):
    # 读取CSV文件
    data = pd.read_csv(file_path)
    # 将 'Date' 列转换为日期时间类型
    data['Date'] = pd.to_datetime(data['Date'])

    # data = data[data['Date'].dt.year > 1985]

    # 确保数据是按日期排序的
    data.sort_values('Date', inplace=True)
    # 计算投资期初和期末的价格
    initial_price = data.iloc[0]['Open']
    final_price = data.iloc[-1]['Open']
    # 计算总的投资年数
    years = (data.iloc[-1]['Date'] - data.iloc[0]['Date']).days / 365.25
    # 计算CAGR
    CAGR = (final_price / initial_price) ** (1 / years) - 1
    return CAGR

def process_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    cagr = calculate_cagr(file_path)
                    print(f"{file}: 平均年回报率: {cagr * 100:.2f}%")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

# 替换下面的路径为你的文件夹路径
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data')
process_files(file_path)
