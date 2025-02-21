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
            expense_inflation = 1 + random.uniform(0, EXPENSE_FLUCTUATION)  # 花费波动
        else:
            rate = RETURN_RATE
            expense_inflation = 1 + INFLATION_RATE
        
        # 每年资产收益并扣除花费
        new_asset = assets[-1] * (1 + rate) - expenses[-1]
        # 每年花费根据通货膨胀调整
        new_expense = expenses[-1] * expense_inflation

        if new_asset < 0:
            print(f"初始资产{init_asset} 在 第{year}年资产为负数，模拟结束！")
            return "failed", year
        
        # 记录新的资产和花费
        assets.append(new_asset)
        expenses.append(new_expense)

    return "passed", None


# 初始化统计数据结构
initial_assets = range(200, 501, 10)  # 200-500万，步长10万
failure_counts = {i:0 for i in initial_assets}
fail_years = []

# 运行模拟
for _ in range(100):  # 每个资产模拟100次
    for asset in initial_assets:
        result, fail_year = simulate_one(asset)
        if result == "failed":
            failure_counts[asset] += 1
            fail_years.append(fail_year)

# 绘制资产-失败概率直方图
assets = list(failure_counts.keys())
failure_rates = [failure_counts[a]/100 for a in assets]


# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

plt.figure(figsize=(12, 6))
plt.bar(assets, failure_rates, width=8, edgecolor='black')
plt.xticks(assets, rotation=45, fontsize=8)
plt.xlabel("初始资产（万）")
plt.ylabel("失败次数")
plt.title("FIRE 失败次数 vs 初始资产 (每组100次模拟)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()



"""
结论：
310万之前的初始资产，FIRE失败概率非常高，380万之后的初始资产，FIRE失败概率非常低。
要400万
"""