"""
可视化一下如果股价完全不动，期权的下跌
比如一个期权离到期还有16个月，横盘了3个月。损失多少价格
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Black-Scholes 期权定价公式
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# 参数设定
def visualize_option_price_decay(S, K, r, sigma, option_type, start_months, end_months):
    # 将月份转换为年，从大到小
    times = np.linspace(start_months / 12, end_months / 12, 100)[::-1]  # 从大到小排列时间
    prices = [black_scholes(S, K, T, r, sigma, option_type) for T in times]
    
    # 可视化
    plt.plot(times * 12, prices)
    plt.title(f'Option Price Decay from {start_months} to {end_months} Months')
    plt.xlabel('Months to Expiration')
    plt.ylabel('Option Price')
    plt.gca().invert_xaxis()  # 反转x轴方向，使得时间从大到小
    plt.grid(True)
    plt.show()

# 可配置的输入参数
S = 100  # 股价
K = 100  # 行权价
r = 0.05  # 无风险利率
sigma = 0.2  # 波动率
option_type = 'call'  # 期权类型 ('call' 或 'put')

# 起始月份和结束月份参数
start_months = 16  # 从16个月开始
end_months = 1     # 到1个月结束

# 调用函数
visualize_option_price_decay(S, K, r, sigma, option_type, start_months, end_months)
