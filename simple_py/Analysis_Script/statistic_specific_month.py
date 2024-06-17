import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")
data = data[data["Date"].dt.year > 1950]

# 筛选特定月份的数据
target_month = 6 

def get_data_by_month(target_month):
    data['Month'] = data['Date'].dt.month
    monthly_data = data[data['Month'] == target_month]

    # 计算每年该月的百分比变化
    monthly_data['Year'] = monthly_data['Date'].dt.year
    monthly_changes = monthly_data.groupby('Year').apply(lambda x: (x['Close'].iloc[-1] - x['Open'].iloc[0]) / x['Open'].iloc[0] * 100)

    # print(monthly_changes.head(10))
    print(monthly_changes.describe())

    return monthly_changes


monthly_changes = get_data_by_month(target_month)

# 画出直方图
import seaborn as sns
# Assuming 'results' is your dataset
sns.histplot(monthly_changes, bins=30, kde=True, color='skyblue', edgecolor='black')
# plt.figure(figsize=(10, 6))
plt.title('Monthly Percentage Change Histogram')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(True)

# import mplcursors
# cursor = mplcursors.cursor(hover=True)
# cursor.connect(
#     "add", 
#     lambda sel: sel.annotation.set_text(
#         f'{sel.target[0]:.2f}%\n {sel.target[1]:.0f}'
#     )
# )

plt.show()

print("--")