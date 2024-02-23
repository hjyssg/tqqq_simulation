import pandas as pd
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, '../data/1985年开始的纳斯达克100^NDX.csv')
data = pd.read_csv(file_path)
data['Date'] = pd.to_datetime(data['Date'])
data['Close'] = pd.to_numeric(data['Close'])

yearly_growth_rates = []  # 用于存储每年的涨幅

for year in range(data['Date'].dt.year.min(), data['Date'].dt.year.max() + 1):
    yearly_data = data[data['Date'].dt.year == year]
    if not yearly_data.empty:
        start_price = yearly_data.iloc[0]['Open']
        end_price = yearly_data.iloc[-1]['Close']
        yearly_growth = ((end_price - start_price) / start_price) * 100
        yearly_growth_rates.append((year, yearly_growth))

# 将列表转换为DataFrame
growth_df = pd.DataFrame(yearly_growth_rates, columns=['Year', 'Yearly Growth'])
print(growth_df['Yearly Growth'].describe())

# 找出涨幅超过60%的年份
high_growth_years = growth_df[growth_df['Yearly Growth'] > 40]
print("Years with Growth Over 60%:")
print(high_growth_years)



import matplotlib.pyplot as plt
import seaborn as sns

# 绘制百分比的分布图
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.histplot(growth_df['Yearly Growth'], bins=30, kde=True, color='skyblue')
plt.title('Yearly Growth Rate Distribution')
plt.xlabel('Yearly Growth Rate (%)')
plt.ylabel('Frequency')
plt.show()


print("--------")

# 年化统计
# mean      17.315052
# std       31.301710
# min      -41.902058
# 25%        1.689551
# 50%       14.040826
# 75%       33.987107
# max      101.950428


# Years with Growth Over 60%:
#     Year  Yearly Growth
#     1991      64.990282
#     1995      42.535928
#     1996      42.540307
#     1998      85.305817
#     1999     101.950428
#     2003      47.434818
#     2009      53.397272
#     2019      40.885964
#     2020      46.420797
#     2023      52.430600