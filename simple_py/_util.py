import os
import pandas as pd




def load_csv_as_dataframe(filename):
    """
    Loads a CSV file into a DataFrame and converts the 'Date' column to datetime.

    Args:
    filename (str): The filename of the CSV file to load.

    Returns:
    pandas.DataFrame: A DataFrame containing the data from the CSV file with the 'Date' column as datetime.
    """
    # 获取脚本的目录
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # 创建文件的完整路径
    file_path = os.path.join(script_dir, '../data/', filename)
    # 读取CSV文件
    df = pd.read_csv(file_path)
    # 将日期列转换为datetime类型
    df['Date'] = pd.to_datetime(df['Date'])

    df.sort_values('Date', inplace=True)  # Ensure the data is sorted by date


    # 过滤掉除了日期列以外所有值都为NaN或Null的行
    df = df.dropna(subset=df.columns[df.columns != 'Date'], how='all')


    df['Close'] = pd.to_numeric(df['Close'])
    return df


def load_etc_csv_as_dataframe(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, '../other_data/', filename)
    df = pd.read_csv(file_path)
    # 将日期列转换为datetime类型
    # df['Date'] = pd.to_datetime(df['Date'])
    # df.sort_values('Date', inplace=True)  # Ensure the data is sorted by date
    # 过滤掉除了日期列以外所有值都为NaN或Null的行
    # df = df.dropna(subset=df.columns[df.columns != 'Date'], how='all')
    return df


import pandas as pd

def calculate_n_derivatives(df, n):
    """
    计算原始股票数据的n倍波动衍生品的股价，仅使用基本for循环和数组操作。

    参数:
    df : pandas.DataFrame
        原始股票数据，必须包含 'Close' 列。
    n : float
        波动倍数。
    """
    # 获取Close价格数组
    dates = df['Date'].values
    closes = df['Close'].values
    derived_closes = [closes[0]]  # 起始价格设置为原始股票的起始价格

    # 计算每日的价格变动百分比并应用n倍波动来计算衍生品的价格
    for i in range(1, len(closes)):
        daily_change = (closes[i] - closes[i - 1]) / closes[i - 1]
        new_price = derived_closes[i - 1] * (1 + daily_change * n)
        derived_closes.append(new_price)

    # 创建结果DataFrame，只包含Date和Derived Close
    result_df = pd.DataFrame({
        'Date': dates,
        'Close': derived_closes
    })

    return result_df


