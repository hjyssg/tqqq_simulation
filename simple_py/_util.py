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

    df['Close'] = pd.to_numeric(df['Close'])
    return df

