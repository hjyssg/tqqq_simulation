import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
# data = _util.load_csv_as_dataframe("^NDX.csv")
fn = "^SPX.csv"
fn = "^NDX.csv"
data = _util.load_csv_as_dataframe(fn)
import mplcursors

data = data[data["Date"].dt.year > 1950]


def calculate_semiannual_percentage_changes(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    semiannual_changes = {
        'Year': [],
        'H1 Change (%)': [],
        'H2 Change (%)': []
    }
    
    for year in data.index.year.unique():
        year_data = data[data.index.year == year]
        h1_data = year_data[(year_data.index.month >= 1) & (year_data.index.month <= 6)]
        h2_data = year_data[(year_data.index.month >= 7) & (year_data.index.month <= 12)]
        
        if not h1_data.empty and not h2_data.empty:
            h1_start = h1_data.iloc[0]['Adj Close']
            h1_end = h1_data.iloc[-1]['Adj Close']
            h2_start = h2_data.iloc[0]['Adj Close']
            h2_end = h2_data.iloc[-1]['Adj Close']
            
            h1_change = ((h1_end - h1_start) / h1_start) * 100
            h2_change = ((h2_end - h2_start) / h2_start) * 100
            
            semiannual_changes['Year'].append(year)
            semiannual_changes['H1 Change (%)'].append(h1_change)
            semiannual_changes['H2 Change (%)'].append(h2_change)
    
    return pd.DataFrame(semiannual_changes)

def plot_semiannual_changes_relationship(changes_df):
    x = changes_df['H1 Change (%)'].values
    y = changes_df['H2 Change (%)'].values
    
    # 简单线性回归
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    
    y_pred = slope * x + intercept
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x, y, color='green', alpha=0.6, label='Data Points')
    plt.plot(x, y_pred, color='red', label='Regression Line')
    
    plt.xlabel('H1 Change (%)')
    plt.ylabel('H2 Change (%)')
    plt.title(f'Visualization of H1 vs H2 Percentage Changes Relationship of {fn}')
    plt.legend()
    plt.grid(True)
    
    # 显示回归参数
    plt.text(0.05, 0.95, f'y = {slope:.2f}x + {intercept:.2f}', transform=plt.gca().transAxes, 
             fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
    # 添加tooltip功能
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Year: {changes_df.iloc[sel.index]["Year"]}\n'
        f'H1 Change: {changes_df.iloc[sel.index]["H1 Change (%)"]:.2f}%\n'
        f'H2 Change: {changes_df.iloc[sel.index]["H2 Change (%)"]:.2f}%'
    ))

    plt.show()


# 计算每年上半年和下半年的百分比幅度
changes_df = calculate_semiannual_percentage_changes(data)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
print(changes_df)

# 可视化
plot_semiannual_changes_relationship(changes_df)


