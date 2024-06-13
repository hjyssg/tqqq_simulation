import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 导入数据
# fn = "^N225.csv"
# fn = "^SPX.csv"
fn = "^NDX.csv"
# fn = "^HSI.csv"
data = _util.load_csv_as_dataframe(fn)  # data is dataframe

data = data[data["Date"].dt.year > 1950]
data['Pct_Change'] = data['Close'].pct_change() * 100  # 计算涨跌幅度


# 删除首行的NaN值
data = data.dropna()
print(data['Pct_Change'].describe())

# 过滤掉前1%和后1%的极端值
lower_bound = data['Pct_Change'].quantile(0.01)
upper_bound = data['Pct_Change'].quantile(0.99)
filtered_data = data[(data['Pct_Change'] >= lower_bound) & (data['Pct_Change'] <= upper_bound)]
print("lower", lower_bound)
print("up", upper_bound)

#---------------------------------------------
def render_histogram(data, title):
    # 可视化设置
    hist_label = f'{title} {fn} 日涨跌幅度分布'
    x_label = '涨跌幅度 (%)'
    y_label = '频率'

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 可视化
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Pct_Change'], kde=True)
    plt.title(hist_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    

    # 添加mplcursors的tooltip功能
    # cursor = mplcursors.cursor(hover=True)
    # cursor.connect("add", lambda sel: sel.annotation.set_text(f'涨跌幅度: {sel.target[0]:.2f}%'))

    # 保存图表
    # filename = f"{hist_label}.png"
    # plt.savefig(filename, bbox_inches='tight')

    # 显示图表
    plt.show()

# render_histogram(data, '')
render_histogram(filtered_data, '过滤掉极端值的')



# 定义牛市和熊市的年份列表
# bull_years = [1982, 1983, 1985, 1986, 1987, 1995, 1996, 1997, 1998, 1999]
# bear_years = [1973, 1974, 2000, 2001, 2002, 2008, 2009]

# # 筛选牛市和熊市的数据
# bull_market_data = data[data['Date'].dt.year.isin(bull_years)]
# bear_market_data = data[data['Date'].dt.year.isin(bear_years)]
# # 绘制牛市和熊市的涨跌幅度分布图
# render_histogram(bull_market_data, '牛市')
# render_histogram(bear_market_data, '熊市')


# 结论：移除极端值后是正态分布


def shapiro_wilk_test(data, alpha=0.05):
    from scipy.stats import shapiro
    """
    进行Shapiro-Wilk正态性检验。
    
    参数:
    data (pd.Series): 要检验的数据。
    alpha (float): 显著性水平。默认值为0.05。
    
    返回:
    tuple: (统计量, p值, 检验结果)。
    """
    stat, p = shapiro(data)
    result = '数据服从正态分布 (fail to reject H0)' if p > alpha else '数据不服从正态分布 (reject H0)'
    return stat, p, result


# stat, p, result = shapiro_wilk_test(data['Pct_Change'])
stat, p, result = shapiro_wilk_test(filtered_data['Pct_Change'])
print(f'Statistics={stat}, p={p}')
print(result)



#---------------------------------------------