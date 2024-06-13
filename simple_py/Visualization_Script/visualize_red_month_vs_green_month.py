import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 导入数据
fn = "^SPX.csv"
data = _util.load_csv_as_dataframe(fn)  # data is a DataFrame
data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is a datetime object
data = data.set_index('Date')  # Set 'Date' as the index

data = data[data.index.year > 1950]

# 计算周和月的涨跌幅度
weekly_data = data['Close'].resample('W').last().pct_change() * 100
monthly_data = data['Close'].resample('M').last().pct_change() * 100
year_data = data['Close'].resample('Y').last().pct_change() * 100


# 删除NaN值
weekly_data = weekly_data.dropna()
monthly_data = monthly_data.dropna()
year_data = year_data.dropna()


print("周涨跌幅度统计特征:")
print(weekly_data.describe())
print("\n月涨跌幅度统计特征:")
print(monthly_data.describe())






#------------------------------------------------------------------------------------
def render_histogram(data, title, time_frame):
    # 过滤掉前1%和后1%的极端值
    lower_bound = data.quantile(0.01)
    upper_bound = data.quantile(0.99)
    data = data[(data >= lower_bound) & (data <= upper_bound)]

    # 可视化设置
    hist_label = f'{fn} {title}{time_frame}涨跌幅度分布'
    x_label = '涨跌幅度 (%)'
    y_label = '频率'

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 可视化
    plt.figure(figsize=(10, 6))
    sns.histplot(data, kde=True)
    plt.title(hist_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    
    plt.legend()  # 显示图例

    # 添加mplcursors的tooltip功能
    # cursor = mplcursors.cursor(hover=True)
    # cursor.connect("add", lambda sel: sel.annotation.set_text(f'涨跌幅度: {sel.target[0]:.2f}%'))

    plt.savefig(hist_label+".jpg")

    # 显示图表
    plt.show()

# 渲染周和月的直方图
render_histogram(weekly_data, '', '周')
render_histogram(monthly_data, '', '月')
render_histogram(year_data, '', '年')




# 周涨跌幅度统计特征:
# count    698.000000
# mean       0.336792
# std        2.627321
# min      -12.519540
# 25%       -1.133871
# 50%        0.464701
# 75%        1.916004
# max        9.436903
# Name: Close, dtype: float64

# 月涨跌幅度统计特征:
# count    160.000000
# mean       1.447657
# std        5.002319
# min      -13.368546
# 25%       -1.696964
# 50%        1.845703
# 75%        4.743749
# max       15.191780


