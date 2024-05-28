import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")


# 获取数据的年份列表
years = data['Date'].dt.year.unique()

# 定义函数计算前五天的涨跌比和全年涨跌百分比的闭市
def calculate_changes(df):
    # df = df.copy()  # 创建副本
    # df['Change'] = (df['Close'] - df['Open']) / df['Open']  # 考虑开盘价和收盘价之间的涨跌幅
    # return df
    df = df.copy()  # 创建副本
    first_day_open = df.iloc[0]['Open']
    last_day_close = df.iloc[-1]['Close']
    change = (last_day_close - first_day_open) / first_day_open * 100
    return change

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

# https://www.nasdaq.com/articles/the-stock-markets-first-5-days-indicator-heres-the-truth-for-better-or-worse.
#     Year  Top5_Changes  Yearly_Changes
#     1985     -2.187675       19.594101
#     1986     -0.857927        6.886127
#     1987     10.102191       10.498215
#     1988      1.244804       13.542403
#     1989      0.140924       26.175318
#     1990     -0.131800      -10.411690
#     1991     -4.208848       64.990282
#     1992      4.060690        8.864906
#     1993      1.486739       10.576510
#     1994      1.637119        1.509059
#     1995     -0.183044       42.535928
#     1996     -2.269919       42.540307
#     1997      3.863110       20.632857
#     1998      0.378482       85.305817
#     1999      7.497237      101.950428
#     2000     -6.021181      -37.650105
#     2001     -2.551595      -32.641545
#     2002      4.769568      -38.117569
#     2003      4.708530       47.434818
#     2004      3.832012        9.969064
#     2005     -3.925706        1.009974
#     2006      5.289563        6.196242
#     2007      1.492750       17.844585
#     2008     -8.400746      -41.902058
#     2009      3.280178       53.397272
#     2010      0.525845       17.802728
#     2011      1.699233        1.749715
#     2012      1.183302       14.539250
#     2013     -0.328117       31.687488
#     2014     -0.225418       18.477449
#     2015     -0.423855        7.858684
#     2016     -4.777646        8.440468
#     2017      2.531190       30.516539
#     2018      3.809945       -1.580008
#     2019      5.697502       40.885964
#     2020      1.251393       46.420797
#     2021      1.196740       26.021646
#     2022     -4.899630      -33.275879
#     2023      0.634423       52.430600
#     2024     -0.104586       --
# 整体而言, Top5_Changes 和 Yearly_Changes 的相关系数为: 0.35958507496592723
# 开门黑的时候, Top5_Changes 和 Yearly_Changes 的相关系数为: 0.4741643281686757
# 开门红的时候,Top5_Changes 和 Yearly_Changes 的相关系数为: 0.0036342671552026477