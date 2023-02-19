import pandas as pd
import os
# https://stackoverflow.com/questions/54876404/unable-to-import-sqlite3-using-anaconda-python
import sqlite3


def create_percent(x):
    return (x["Close"] - x["Open"])/x["Open"]*100


csv_file_path = os.path.join('data', 'AAPL.csv')
baseName = os.path.basename(csv_file_path).split(".")[0]
baseName = baseName.strip()
db_fn =  os.path.join("output_db", baseName + ".db")
df = pd.read_csv(csv_file_path, parse_dates=["Date"])
df["change_percent"] = df.apply(create_percent, axis=1)

# print(df.head(20))
subdf = df[df['change_percent'] > 5]
print(subdf[["Date", 'change_percent']])

con = sqlite3.connect(db_fn)
df.to_sql("daily_table", con, schema=None, if_exists='replace', index=False)


# ------------------ 常用SQL
# select Date, change_percent From daily_table where change_percent >= 8.2 ORDER BY Date DESC
