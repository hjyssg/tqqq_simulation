# 1 读取文件。存到一个df。
# 2 分别计算出每年第一周和次年最后一周的百分比。存到另一个df。
# 3. 对第2的df进行统计。

import pandas as pd

# 读取CSV文件
file_path = '../../data/^NDX.csv'  # 替换为你的CSV文件路径

data = pd.read_csv(file_path)

# 将日期列转换为日期时间类型
data['Date'] = pd.to_datetime(data['Date'])

# 提取年份信息
data['Year'] = data['Date'].dt.year

# 创建一个空的DataFrame来存储每年第一周和最后一周的涨跌百分比
yearly_changes = pd.DataFrame(columns=['Year', 'First Week Change', 'Last Week Change'])

# 计算每年第一周和最后一周的涨跌百分比，并存入yearly_changes
for year in data['Year'].unique():
    year_data = data[data['Year'] == year]
    first_week_change = ((year_data.iloc[4]['Close'] - year_data.iloc[0]['Close']) / year_data.iloc[0]['Close']) * 100
    last_week_change = ((year_data.iloc[-1]['Close'] - year_data.iloc[-5]['Close']) / year_data.iloc[-5]['Close']) * 100
    yearly_changes = pd.concat([yearly_changes, pd.DataFrame({'Year': [year], 'First Week Change': [first_week_change], 'Last Week Change': [last_week_change]})], ignore_index=True)

print(yearly_changes)

# 对第二个DataFrame进行统计
stats = yearly_changes.describe()

# 输出结果
print("Statistics for First and Last Weeks of Each Year:")
print(stats)



#     Year  First Week Change  Last Week Change
# 0   1971           1.449997          2.166523
# 1   1972           2.111747          2.021662
# 2   1973           1.032459          3.969780
# 3   1974           1.610286          2.589606
# 4   1975           1.317955          1.636768
# 5   1976           4.599032          2.299328
# 6   1977          -0.163786          1.067925
# 7   1978          -3.653849          0.897976
# 8   1979           3.462324          0.780155
# 9   1980           1.693997          1.099229
# 10  1981          -3.763205          0.071538
# 11  1982          -1.779776         -0.338762
# 12  1983           3.473702          0.744918
# 13  1984           3.472241          0.528886
# 14  1985           0.040669          1.467827
# 15  1986           0.953848         -0.228838
# 16  1987           6.879951         -0.810328
# 17  1988           0.000000          1.086670
# 18  1989           1.769673          2.294193
# 19  1990          -0.130628          0.375938
# 20  1991          -3.546483          6.692632
# 21  1992           4.070252          1.662463
# 22  1993           0.805304          2.068167
# 23  1994           1.580257          1.316377
# 24  1995           1.144465          0.500529
# 25  1996          -2.482410          0.264053
# 26  1997           3.095965          4.722810
# 27  1998          -1.643345          1.370751
# 28  1999           6.175578          2.362797
# 29  2000          -6.015995         -1.847423
# 30  2001           4.540409          0.304454
# 31  2002           3.864595         -2.692952
# 32  2003           1.171244          1.733673
# 33  2004           4.662923          0.985042
# 34  2005          -2.952387         -1.960499
# 35  2006           3.340403          0.587632
# 36  2007           0.853025         -2.256126
# 37  2008          -6.480608          3.418585
# 38  2009          -0.931250         -0.723634
# 39  2010           0.379047         -0.539874
# 40  2011           0.432837         -0.515153
# 41  2012           1.051077          0.229367
# 42  2013          -0.657077          0.509453
# 43  2014           0.544042         -0.783925
# 44  2015           0.198440         -0.813710
# 45  2016          -5.291764         -1.456605
# 46  2017           1.892397         -0.812790
# 47  2018           2.147743          7.142993
# 48  2019           3.466279          0.220261
# 49  2020           0.407490          0.652492
# 50  2021           3.965289         -1.425785
# 51  2022          -5.664819         -0.298917
# 52  2023           2.394054          1.012225

# Statistics for First and Last Weeks of Each Year:
#        First Week Change  Last Week Change
# count          53.000000         53.000000
# mean            0.771578          0.855667
# std             3.023226          1.931625
# min            -6.480608         -2.692952
# 25%            -0.163786         -0.338762
# 50%             1.051077          0.652492
# 75%             3.095965          1.662463
# max             6.879951          7.142993