import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")
data = data[data["Date"].dt.year > 1950]

# 筛选特定月份的数据
target_month = 7


def get_data_by_month(target_month):
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year

    # 计算每年目标月份与上个月的收盘价比较的百分比变化
    monthly_data = data[data['Month'] == target_month]
    monthly_data = monthly_data.sort_values(by='Date')
    
    # 获取上个月的数据
    previous_month = target_month - 1 if target_month > 1 else 12
    previous_month_data = data[data['Month'] == previous_month].sort_values(by='Date')

    # 按年份分组并计算百分比变化
    def calculate_change(year):
        current_month = monthly_data[monthly_data['Year'] == year]
        prev_month = previous_month_data[previous_month_data['Year'] == year if previous_month != 12 else year - 1]
        
        if not prev_month.empty and not current_month.empty:
            previous_close = prev_month['Close'].iloc[-1]
            current_close = current_month['Close'].iloc[-1]
            return (current_close - previous_close) / previous_close * 100
        else:
            return None

    monthly_changes = monthly_data['Year'].unique()
    monthly_changes = {year: calculate_change(year) for year in monthly_changes}
    monthly_changes = pd.Series(monthly_changes).dropna()

    print(monthly_changes.describe())
    print("偏度", monthly_changes.skew())


    return monthly_changes

monthly_changes = get_data_by_month(target_month)

# print("置信区间", _util.calculate_confidence_interval(monthly_changes, 3.6))


# 画出直方图
import seaborn as sns
# Assuming 'results' is your dataset
# sns.histplot(monthly_changes, bins=30, kde=True, kde_kws={'bw_adjust': 0.5},  color='skyblue', edgecolor='black')
sns.histplot(monthly_changes, bins=30, kde=True, kde_kws={'bw_adjust': 0.5}, stat='density',  color='skyblue', edgecolor='black')
# plt.figure(figsize=(10, 6))
plt.title('Monthly Percentage Change Histogram')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(True)


plt.show()

print("--")
