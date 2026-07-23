import os
import pandas as pd



def load_csv_as_dataframe(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, '../data/', filename)
    # 如果文件不存在，抛出异常
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found")
    
    # 尝试加载
    df = pd.read_csv(file_path)
    
    # 检测奇葩格式：Price, Adj Close, Close ... (第一行)
    # Ticker, ^NDX, ^NDX ... (第二行)
    # Date, , , ... (第三行)
    if 'Price' in df.columns and any('Ticker' in str(val) for val in df.iloc[0]):
        # 这种格式下，第三行索引为1的是真正的列名，但包含大量空值
        # 实际上真正的列名是第一行，只是 Date 被错放到了第三行第一列
        df = pd.read_csv(file_path, skiprows=[1, 2])
        if 'Price' in df.columns:
            df.rename(columns={'Price': 'Date'}, inplace=True)
    
    # 清洗列名
    df.columns = [str(c).strip().replace('"', '').replace("'", "") for c in df.columns]
    
    # 确保 Date 存在
    if 'Date' not in df.columns:
        # 尝试暴力搜索
        for i in range(min(5, len(df))):
           if 'Date' in str(df.iloc[i, 0]):
               df = pd.read_csv(file_path, skiprows=i+1)
               df.columns = [str(c).strip().replace('"', '').replace("'", "") for c in df.columns]
               break

    # 过滤掉无效行
    df = df.dropna(subset=['Date'], how='any')
    df = df[df['Date'].astype(str).str.contains(r'\d{4}')] # 必须包含年份

    df['Date'] = pd.to_datetime(df['Date'])
    
    # Ensure the data is sorted by date
    df.sort_values('Date', inplace=True) 
    # 过滤掉除了日期列以外所有值都为NaN或Null的行
    df = df.dropna(subset=df.columns[df.columns != 'Date'], how='all')

    df['Close'] = pd.to_numeric(df['Close'])
    return df

# date as index
def load_csv_as_dataframe_v2(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, '../data/', filename)
    # 如果文件不存在，抛出异常
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found")
    
    df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    # df = df.dropna(subset=df.columns[df.columns != 'Date'], how='all')
    # df['Close'] = pd.to_numeric(df['Close'])
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



import numpy as np
def calculate_and_print_percentiles(data):
    # 计算从5%到100%的分位数，步长为5%
    percentiles = np.percentile(data, np.arange(5, 101, 5))
    for i, percentile in enumerate(percentiles, start=1):
        print(f"{i * 5}% percentile: {percentile}")



import pandas as pd
import scipy.stats as stats
def calculate_confidence_interval_normal(series, value):
    """
    计算给定值在正态分布中的置信区间。
    """
    mean = series.mean()
    std = series.std()
    
    z_score = (value - mean) / std
    
    # Calculate the cumulative probability of the z_score
    # 在正态分布中，累积分布函数用于计算一个特定值落在某个范围内的概率。例如，给定一个标准正态分布（均值为 0，标准差为 1）
    cumulative_prob = stats.norm.cdf(z_score)
    
    # Determine the confidence interval based on cumulative probability
    if cumulative_prob < 0.5:
        lower_prob = 1 - 2 * cumulative_prob
    else:
        lower_prob = 2 * (1 - cumulative_prob)
    
    confidence_interval = 100 * lower_prob
    return confidence_interval


import matplotlib.pyplot as plt

def init_plotting():
    """
    初始化绘图设置，支持中文显示和负号显示。
    """
    # 尝试多种常用的中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    try:
        plt.style.use('seaborn-v0_8-whitegrid') # 设置一个美观的风格
    except:
        plt.style.use('ggplot')

def show_plot(title=None, xlabel=None, ylabel=None):
    """
    设置标题和标签，整理布局并显示图表。
    """
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()


def calculate_confidence_interval_for_far_tail(series, value):
    """
    计算给定值在厚尾分布中的置信区间。
    """
    mean = series.mean()
    std = series.std()
    n = len(series)
    
    # 使用t分布计算置信区间
    t_score = (value - mean) / (std / (n ** 0.5))
    
    # Calculate the cumulative probability of the t_score
    cumulative_prob = stats.t.cdf(t_score, df=n-1)
    
    # Determine the confidence interval based on cumulative probability
    if cumulative_prob < 0.5:
        lower_prob = 1 - 2 * cumulative_prob
    else:
        lower_prob = 2 * (1 - cumulative_prob)
    
    confidence_interval = 100 * lower_prob
    return confidence_interval