import pandas as pd
import os
import sys

# 将util.py所在的目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

def calculate_changes(df):
    df = df.copy()  # 创建副本
    first_day_open = df.iloc[0]['Open']
    last_day_close = df.iloc[-1]['Close']
    change = (last_day_close - first_day_open) / first_day_open * 100
    return change

def compute_yearly_and_top5_changes(file_path):
    # 加载数据
    data = _util.load_csv_as_dataframe(file_path)
    
    # 将日期列转换为日期类型
    data['Date'] = pd.to_datetime(data['Date'])
    
    # 获取数据的年份列表
    years = data['Date'].dt.year.unique()
    
    top5_changes = {}
    yearly_changes = {}
    
    # 计算每年前五天的涨跌比和全年涨跌百分比的闭市
    for year in years:
        yearly_data = data[data['Date'].dt.year == year]
        yearly_data = yearly_data.reset_index(drop=True)
        
        # 计算每年前五天的涨跌比
        top5_data = yearly_data.head(5)
        top5_changes[year] = calculate_changes(top5_data)
        
        # 计算全年涨跌百分比的闭市
        yearly_changes[year] = calculate_changes(yearly_data)
    
    # 将字典转换为DataFrame
    df_top5_changes = pd.DataFrame(top5_changes.items(), columns=['Year', 'First_5_Changes'])
    df_yearly_changes = pd.DataFrame(yearly_changes.items(), columns=['Year', 'Yearly_Changes'])
    
    # 合并两个DataFrame
    merged_df = pd.merge(df_top5_changes, df_yearly_changes, on='Year')
    
    return merged_df

# 调用计算函数
file_path = "^NDX.csv"
merged_df = compute_yearly_and_top5_changes(file_path)

print(merged_df)



import matplotlib.pyplot as plt

def visualize_changes(merged_df):
    # # 散点图显示Top5_Changes和Yearly_Changes之间的关系
    # plt.figure(figsize=(12, 6))
    # plt.scatter(merged_df['First_5_Changes'], merged_df['Yearly_Changes'], color='blue', label='All Data')
    # plt.xlabel('Top 5 Days Changes (%)')
    # plt.ylabel('Yearly Changes (%)')
    # plt.title('Scatter Plot of Top 5 Days Changes vs Yearly Changes')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # 可视化开门黑和开门红的情况
    negative_top5_changes = merged_df[merged_df['First_5_Changes'] < 0]
    positive_top5_changes = merged_df[merged_df['First_5_Changes'] > 0]

    plt.figure(figsize=(12, 6))
    plt.scatter(negative_top5_changes['First_5_Changes'], negative_top5_changes['Yearly_Changes'], color='red', label='Negative Top 5 Changes')
    plt.scatter(positive_top5_changes['First_5_Changes'], positive_top5_changes['Yearly_Changes'], color='green', label='Positive Top 5 Changes')
    plt.xlabel('Top 5 Days Changes (%)')
    plt.ylabel('Yearly Changes (%)')
    plt.title('Scatter Plot of Top 5 Days Changes vs Yearly Changes (Positive and Negative)')
    plt.legend()
    plt.grid(True)
    plt.show()

# 调用可视化函数
visualize_changes(merged_df)


# 一年能发生很多事情，前五天预测一年其实有点搞笑。没啥统计意义