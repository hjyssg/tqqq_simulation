import pandas as pd

# 计算一段时间内的涨跌幅函数
def calculate_change(begin_row, end_row):
    open_value = begin_row["Open"]
    close_value = end_row["Close"]

    return (close_value - open_value) / open_value

# 读取纳斯达克指数历史数据
df = pd.read_csv('../data/1971年开始的纳斯达克^IXIC.csv', parse_dates=["Date"])

begin_year = df.iloc[0]["Date"].year
end_year =  df.iloc[-1]["Date"].year

# 定义一个函数，统计每年11月和12月的数据
def calculate_month_11_12():
    output_data = []
    for year in range(begin_year, end_year):
        # 筛选出该年份的数据
        year_df = df[df['Date'].dt.year == year]

        early_days = 40
        first_day = year_df.iloc[0] # 该年的第一天
        day_early = year_df.iloc[early_days] # 该年的前40天
        last_day = year_df.iloc[-1] # 该年的最后一天

        # 选择11月份的数据
        sub1 =  year_df[year_df['Date'].dt.month == 11]
        middle_day = sub1.iloc[0] # 该年11月的第一天

        # 计算各项指标的变化率
        year_change = calculate_change(first_day, last_day)
        change_early = calculate_change(first_day, day_early)
        ytd_change = calculate_change(first_day, middle_day)
        rest_change = calculate_change(middle_day, last_day)

        # 将各项指标的结果存储在字典中
        output_data.append({
            "year": year,
            "全年变化百分比":  round(year_change * 100, 2),
            ("年初变化百分比 - " + str(early_days)): round(change_early * 100, 2),
            "前10月变化百分比": round(ytd_change * 100, 2),
            "最后两个月变化百分比": round(rest_change * 100, 2),
            "年初价格": first_day["Open"],
            "年中价格": middle_day["Open"],
            "年尾价格": last_day["Close"]
        })

    # 将结果存储为Excel文件
    output_df = pd.DataFrame.from_dict(output_data)
    output_df.to_excel("简易统计.xlsx", index=False)
