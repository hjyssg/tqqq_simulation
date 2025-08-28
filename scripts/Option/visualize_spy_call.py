import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# Black-Scholes公式
def black_scholes_call(S, K, T, r, sigma):
    """" 
    S (float): 标的资产的当前价格 (现价)。
    K (float): 期权的执行价格 (行权价)。
    T (float): 距离到期日的时间，以年为单位 (例如1年、0.5年)。
    r (float): 无风险利率，作为一个百分比的小数形式 (例如0.03表示3%)。
    sigma (float): 标的资产的波动率，作为百分比的小数形式 (例如0.2表示20%)。 
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 加载CSV文件
# data = _util.load_csv_as_dataframe("^SPX.csv")  
data = _util.load_csv_as_dataframe("^NDX.csv")  


# 假设：利率r = 0.03，波动率sigma = 0.2，期权到期时间2025年6月
r = 0.03
sigma = 0.2
expiry_date = pd.to_datetime("2025-06-30")
current_date = pd.to_datetime("2024-01-01")
strike_price = data.iloc[0]['Adj Close'] * 1.01

data = data[data['Date'] >= current_date]

# 计算期权价格
data['Days_to_Expiry'] = (expiry_date - data['Date']).dt.days / 365.0
data['Call_Price'] = data.apply(lambda row: black_scholes_call(row['Adj Close'], strike_price, row['Days_to_Expiry'], r, sigma), axis=1)

# 可视化期权价格变化
plt.figure(figsize=(10, 6))
plt.plot(data['Date'], data['Call_Price'], label=f'SPY Call (Strike {strike_price})')
plt.title('SPY Call Option Price Change (2023 - 2025 June)')
plt.xlabel('Date')
plt.ylabel('Call Option Price')
plt.grid(True)
plt.legend()

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

plt.show()
