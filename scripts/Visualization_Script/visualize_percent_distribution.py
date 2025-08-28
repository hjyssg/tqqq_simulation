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
daily_data = data['Close'].pct_change() * 100  # 日涨跌幅
weekly_data = data['Close'].resample('W').last().pct_change() * 100
monthly_data = data['Close'].resample('M').last().pct_change() * 100
year_data = data['Close'].resample('Y').last().pct_change() * 100


# 删除NaN值
daily_data = daily_data.dropna()
weekly_data = weekly_data.dropna()
monthly_data = monthly_data.dropna()
year_data = year_data.dropna()

# 打印统计特征
print("日涨跌幅度统计特征:")
print(daily_data.describe())
print("\n周涨跌幅度统计特征:")
print(weekly_data.describe())
print("\n月涨跌幅度统计特征:")
print(monthly_data.describe())
print("\n年涨跌幅度统计特征:")
print(year_data.describe())

# 打印百分位数（以10%为间隔）
def print_percentiles(data, time_frame):
    print(f"\n{time_frame}涨跌幅度的百分位数（每10%为间隔）：")
    for i in range(10, 101, 10):  # 从10%到100%每10%打印一次
        percentile_value = data.quantile(i / 100)
        print(f"{i}%: {percentile_value:.2f}%")

print_percentiles(daily_data, '日')
print_percentiles(weekly_data, '周')
print_percentiles(monthly_data, '月')
print_percentiles(year_data, '年')



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

# 渲染日、周、月、年的直方图
render_histogram(daily_data, '', '日')
render_histogram(weekly_data, '', '周')
render_histogram(monthly_data, '', '月')
render_histogram(year_data, '', '年')


