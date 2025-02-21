import numpy as np
import matplotlib.pyplot as plt
import random

"""
模拟存在随机波动情况下，fire生活破产的可能性。
"""

def simulate_one(init_asset):
    # 定义常量
    INITIAL_EXPENSE = 20  # 初始花费：20万（单位：元）
    INFLATION_RATE = 0.022  # 年通货膨胀率：2.2%
    RETURN_RATE = 0.10  # 年资产收益率：10%（SPY的年回报）
    YEARS = 40  # 模拟时间：40年

    # 随机波动控制（设置为True时，允许收益率和花费波动）
    RANDOM_ON = True
    RATE_FLUCTUATION = 0.1  # 收益率波动范围±10%
    EXPENSE_FLUCTUATION = 0.1  # 花费波动范围±10%

    # 初始化资产和花费列表
    assets = [init_asset]
    expenses = [INITIAL_EXPENSE]

    # 模拟40年内的资产变化
    for year in range(1, YEARS + 1):
        # 随机波动
        if RANDOM_ON:
            rate = RETURN_RATE * (1 + random.uniform(-RATE_FLUCTUATION, RATE_FLUCTUATION))  # 收益率波动
            expense_inflation = 1 + random.uniform(-EXPENSE_FLUCTUATION, EXPENSE_FLUCTUATION)  # 花费波动
        else:
            rate = RETURN_RATE
            expense_inflation = 1 + INFLATION_RATE
        
        # 每年资产收益并扣除花费
        new_asset = assets[-1] * (1 + rate) - expenses[-1]
        # 每年花费根据通货膨胀调整
        new_expense = expenses[-1] * expense_inflation

        if new_asset < 0:
            print(f"初始资产{init_asset} 在 第{year}年资产为负数，模拟结束！")
            break
        
        # 记录新的资产和花费
        assets.append(new_asset)
        expenses.append(new_expense)


for time in range(100): # 模拟100次
    for i in range(200, 500, 10): # 初始资产范围：200万到500万
        simulate_one(i)


"""
初始资产较低（200万至250万）时，通常无法支撑超过20-30年的模拟，
因为资产在模拟的早期就已经因为每年固定花费和较低的收益率波动而变为负数。即使是初始资产为250万的情况下，在某些情况下也会在30年内变为负数。
"""