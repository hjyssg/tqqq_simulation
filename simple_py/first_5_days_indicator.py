import pandas as pd

# 帮我写个脚本，统计每年前五天的涨跌比和全年涨跌百分比的关闭。

# 读取CSV文件
file_path = '../data/1985年开始的纳斯达克100^NDX.csv'  # 替换为你的CSV文件路径
data = pd.read_csv(file_path)

# 将日期列转换为日期时间格式
data['Date'] = pd.to_datetime(data['Date'])

# 获取数据的年份列表
years = data['Date'].dt.year.unique()

# 定义函数计算前五天的涨跌比和全年涨跌百分比的闭市
def calculate_changes(df):
    # df['Change'] = df['Close'].pct_change()
    # return df

    df = df.copy()  # 创建副本
    df['Change'] = df['Close'].pct_change()
    return df

top5_changes = {}
yearly_changes = {}

# 计算每年前五天的涨跌比和全年涨跌百分比的闭市
for year in years:
    yearly_data = data[data['Date'].dt.year == year]
    yearly_data = yearly_data.reset_index(drop=True)
    
    # 计算每年前五天的涨跌比
    top5_data = yearly_data.head(5)
    top5_data = calculate_changes(top5_data)
    top5_changes[year] = top5_data['Change'].sum()
    
    # 计算全年涨跌百分比的闭市
    yearly_data = calculate_changes(yearly_data)
    yearly_changes[year] = yearly_data['Change'].sum()

# print("每年前五天的涨跌比：")
# print(top5_changes)
# print("\n全年涨跌百分比的闭市：")
# print(yearly_changes)
    

# 将字典转换为DataFrame
df_top5_changes = pd.DataFrame(top5_changes.items(), columns=['Year', 'Top5_Changes'])
df_yearly_changes = pd.DataFrame(yearly_changes.items(), columns=['Year', 'Yearly_Changes'])

# 合并两个DataFrame
merged_df = pd.merge(df_top5_changes, df_yearly_changes, on='Year')
print(merged_df)



correlation = merged_df['Top5_Changes'].corr(merged_df['Yearly_Changes'])
print(f"整体而言, Top5_Changes 和 Yearly_Changes 的相关系数为: {correlation}")

negative_top5_changes = merged_df[merged_df['Top5_Changes'] < 0]
# print(negative_top5_changes)
correlation = negative_top5_changes['Top5_Changes'].corr(negative_top5_changes['Yearly_Changes'])
print(f"开门黑的时候, Top5_Changes 和 Yearly_Changes 的相关系数为: {correlation}")

positive_top5_changes = merged_df[merged_df['Top5_Changes'] > 0]
correlation = positive_top5_changes['Top5_Changes'].corr(positive_top5_changes['Yearly_Changes'])
print(f"开门红的时候,Top5_Changes 和 Yearly_Changes 的相关系数为: {correlation}")
