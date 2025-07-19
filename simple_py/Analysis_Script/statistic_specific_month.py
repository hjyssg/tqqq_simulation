import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")
data = data[data["Date"].dt.year > 1950]

# 筛选特定月份的数据
target_month = 3


def get_data_by_month(target_month):
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year
    
    # 获取上个月的年份和月份
    def get_previous_month(year, month):
        if month == 1:
            return year - 1, 12  # 前一个月是上一年的12月
        else:
            return year, month - 1  # 前一个月是当前年的前一个月

    # 按年份分组并计算百分比变化
    def calculate_change(year):
        # 获取当前月份的数据
        current_month = data[(data['Year'] == year) & (data['Month'] == target_month)] 
        
        # 获取前一个月的年份和月份
        prev_year, prev_month = get_previous_month(year, target_month)

        # 获取前一个月的数据
        prev_month_data = data[(data['Year'] == prev_year) & (data['Month'] == prev_month)]

        if not prev_month_data.empty and not current_month.empty:
            previous_close = prev_month_data['Close'].iloc[-1]
            current_close = current_month['Close'].iloc[-1]
            return (current_close - previous_close) / previous_close * 100
        else:
            return None

    # 计算每一年的变化
    monthly_changes = data['Year'].unique()
    monthly_changes = {year: calculate_change(year) for year in monthly_changes}
    monthly_changes = pd.Series(monthly_changes).dropna()

    print(monthly_changes.describe())

    return monthly_changes


monthly_changes = get_data_by_month(target_month)

# print("置信区间", _util.calculate_confidence_interval(monthly_changes, 3.6))


# 画出直方图
import seaborn as sns
sns.histplot(monthly_changes, bins=30, kde=True, kde_kws={'bw_adjust': 0.5},   color='skyblue', edgecolor='black')
plt.title('Monthly Percentage Change Histogram')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(True)

output_path = os.path.join(f'{target_month} performance.png')
plt.savefig(output_path)
plt.show()

# print("--")
