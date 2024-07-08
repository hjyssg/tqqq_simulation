import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import mplcursors

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the directory containing _util.py to the system path
import _util


# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# Load the stock data
data = _util.load_csv_as_dataframe("^NDX.csv")
data['Date'] = pd.to_datetime(data['Date'])
data = data[data['Date'].dt.year > 1950]  # Consider only data after 1950

# Calculate the daily percentage change in 'Close' prices
data['Change'] = data['Close'].pct_change() * 100

# Define CPI release dates from 2023-01 to 2024-06
cpi_dates = pd.to_datetime([
    "2023-01-11", "2023-02-13", "2023-03-12", "2023-04-10", "2023-05-15", "2023-06-12",
    "2023-07-11", "2023-08-14", "2023-09-11", "2023-10-10", "2023-11-13", "2023-12-11",
    "2024-01-11", "2024-02-13", "2024-03-12", "2024-04-10", "2024-05-15", "2024-06-12"
])

# Filter data for these CPI release dates
cpi_data = data[data['Date'].isin(cpi_dates)]

# Visualize the results
plt.figure(figsize=(12, 6))
plt.bar(cpi_data['Date'].dt.strftime('%Y-%m-%d'), cpi_data['Change'], color='blue')
plt.xlabel('日期')
plt.ylabel('日股价变化率 (%)')
plt.title('CPI发布日期的股票价格日变化率')
plt.xticks(rotation=45)
plt.tight_layout()

# Add mplcursors for interactive tooltips
mplcursors.cursor(hover=True)

# Display statistical features using describe
print(cpi_data['Change'].describe())

plt.show()


input("-")