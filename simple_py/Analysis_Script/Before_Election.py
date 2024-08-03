import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^NDX.csv")  # data is dataframe

# 只在意二战后的数据
data = data[data['Date'].dt.year > 1950]

# 选举年份
election_years = [2004, 2012, 2016, 2020]

# 分析11月上半月的市场表现
results = []
for year in election_years:
    start_date = pd.Timestamp(f"{year}-11-01")
    end_date = pd.Timestamp(f"{year}-11-15")
    
    spx_nov = data.loc[start_date:end_date]['Close']
    
    if len(spx_nov) > 1:
        change = (spx_nov.iloc[-1] - spx_nov.iloc[0]) / spx_nov.iloc[0] * 100
        results.append({'Year': year, '11 Days Change (%)': change})
    else:
        results.append({'Year': year, '11 Days Change (%)': None})

# 转换为DataFrame
results_df = pd.DataFrame(results)

# 显示结果
print(results_df)
