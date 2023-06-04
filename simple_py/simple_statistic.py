import pandas as pd
import sqlite3

# 计算一段时间内的涨跌幅函数
def calculate_change(begin_row, end_row):
    open_value = begin_row["Open"]
    close_value = end_row["Close"]

    return (close_value - open_value) / open_value

# 读取纳斯达克指数历史数据
df = pd.read_csv('../data/1971年开始的纳斯达克^IXIC.csv', parse_dates=["Date"])

begin_year = df.iloc[0]["Date"].year
end_year =  df.iloc[-1]["Date"].year

# 定义一个函数，统计每个月份的数据
def do_month_statistic():
    output_data = []
    for year in range(begin_year, end_year):
        year_df = df[df['Date'].dt.year == year]
        for month in range(1, 12+1):
            try:
                month_df = year_df[year_df['Date'].dt.month == month]

                first_day = month_df.iloc[0] # 该月的第一天
                last_day = month_df.iloc[-1] # 该月的最后一天

                change_month =  calculate_change(first_day, last_day) # 计算该月的涨跌幅

                # 将各项指标的结果存储在字典中
                output_data.append({
                    "date": first_day["Date"],
                    "月度变化": round(change_month * 100, 2),
                    "月初价格": first_day["Open"],
                    "月尾价格": last_day["Close"]
                })
            except Exception as e:
                pass

    # 将结果存储为Excel文件和SQLite数据库文件
    output_df = pd.DataFrame.from_dict(output_data)
    output_df.to_excel("月度简易统计.xlsx", index=False)
    
    # 连接SQLite数据库
    conn = sqlite3.connect('nasdaq.db')
    
    # 将DataFrame数据写入到SQLite数据库中的表格nasdaq中
    output_df.to_sql('nasdaq', conn, if_exists='replace', index=False)

# 调用函数进行月度统计，并将结果输出到Excel和SQLite数据库文件中
do_month_statistic()
