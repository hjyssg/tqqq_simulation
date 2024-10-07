import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")  # data is dataframe
data = data[data['Date'].dt.year > 1950]

# 定义总统选举的年份
election_years = [1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]

# 计算大选后的涨跌幅
result = []
for year in election_years:
    start_date = pd.Timestamp(f"{year}-11-01")
    end_date = pd.Timestamp(f"{year + 1}-05-31")
    df_filtered = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    if not df_filtered.empty:
        start_price = df_filtered.iloc[0]['Adj Close']
        end_price = df_filtered.iloc[-1]['Adj Close']
        pct_change = (end_price - start_price) / start_price * 100
        result.append({"Year": year, "Pct Change": pct_change})

# 转换为DataFrame
result_df = pd.DataFrame(result)

# 打印统计特征
print(result_df.describe())
print(result_df)

# import seaborn as sns
# import matplotlib.pyplot as plt
# import mplcursors
# # 可视化部分
# def visualize_percentage_changes(df):
#     plt.figure(figsize=(10, 6))
#     sns.histplot(df['Pct Change'], kde=True, color="blue")
    
#     # 设置图表动态标题和标签
#     title = "Percentage Change in Stock Prices After U.S. Elections (Post-WWII)"
#     xlabel = "Percentage Change"
#     ylabel = "Frequency"
    
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)

#     # mplcursors 用于显示tooltip
#     mplcursors.cursor(hover=True)
#     plt.show()

# # 调用可视化函数
# visualize_percentage_changes(result_df)
