import pandas as pd

def calculate_change(begin_row, end_row):
    open_value = begin_row["Open"]
    close_value = end_row["Close"]

    return (close_value - open_value) / open_value

df = pd.read_csv('data/1971年开始的纳斯达克^IXIC.csv', parse_dates=["Date"])

begin_year = df.iloc[0]["Date"].year
end_year =  df.iloc[-1]["Date"].year

# print(df.shape)

# float(df[0:1]["Open"])
# df[df['Date'].dt.year == 2001]

def calculate_month_11_12():
    output_data = []
    for year in range(begin_year, end_year):
        # df[df[Date] == year + "-11-01"]
        year_df = df[df['Date'].dt.year == year]

        early_days = 40
        first_day = year_df.iloc[0]
        day_early = year_df.iloc[early_days]
        last_day = year_df.iloc[-1]
        # print(year_df.head(10))

        # 选择11月
        sub1 =  year_df[year_df['Date'].dt.month == 11]
        middle_day = sub1.iloc[0]

        year_change = calculate_change(first_day, last_day)
        change_early = calculate_change(first_day, day_early)
        ytd_change = calculate_change(first_day, middle_day)
        rest_change = calculate_change(middle_day, last_day)


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


    output_df = pd.DataFrame.from_dict(output_data)
    output_df.to_excel("简易统计.xlsx", index=False)


def do_week_statistic():
    output_data = []
    for year in range(begin_year, end_year):
        year_df = df[df['Date'].dt.year == year]
        for month in range(1, 12+1):
            try:
                month_df = year_df[year_df['Date'].dt.month == month]

                first_day = month_df.iloc[0]
                last_day = month_df.iloc[-1]

                change_month =  calculate_change(first_day, last_day)

                output_data.append({
                    "date": first_day["Date"],
                    "月度变化": round(change_month * 100, 2),
                    "月初价格": first_day["Open"],
                    "月尾价格": last_day["Close"]
                })
            except Exception as e:
                pass

    output_df = pd.DataFrame.from_dict(output_data)
    output_df.to_excel("月度简易统计.xlsx", index=False)


do_week_statistic()