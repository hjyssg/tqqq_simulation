import pandas as pd
import os

current_file_path = os.path.abspath(__file__)
parent_folder_path = os.path.dirname(os.path.dirname(current_file_path))

# 读取CSV文件
tqqq_data = pd.read_csv(os.path.join(parent_folder_path,  "data", "tqqq.csv"))
voo_data = pd.read_csv(os.path.join(parent_folder_path,  "data", "voo.csv"))

# 筛选起始时间
start_date = '2010-02-11'

# 重命名列
tqqq_data = tqqq_data.rename(columns={'Close/Last': 'Close'})
voo_data = voo_data.rename(columns={'Close/Last': 'Close'})


# 将日期列转换为日期时间格式
tqqq_data['Date'] = pd.to_datetime(tqqq_data['Date'])
voo_data['Date'] = pd.to_datetime(voo_data['Date'])



# 筛选起始时间之后的数据
tqqq_data = tqqq_data[tqqq_data['Date'] >= start_date]
voo_data = voo_data[voo_data['Date'] >= start_date]

# 合并两个数据集，并设置日期作为索引
merged_data = pd.merge(tqqq_data, voo_data, on='Date', suffixes=('_tqqq', '_voo'))
merged_data.set_index('Date', inplace=True)


# 排序日期索引
merged_data.sort_index(inplace=True)

# 筛选起始时间之后的数据
merged_data = merged_data.loc[start_date:]

def test_one(merged_data, tqqq_percentage, voo_percentage, test_start_date, test_duration_days):
    # 初始化投资金额和股票持有量
    investment = 10000  # 初始投资金额
    
    # 筛选测试起始时间之后的数据
    test_end_date = pd.to_datetime(test_start_date) + pd.DateOffset(days=test_duration_days)
    test_data = merged_data.loc[test_start_date:test_end_date]
 
    # 计算初始股票持有量
    initial_tqqq_price = test_data.iloc[0]['Close_tqqq']
    initial_voo_price = test_data.iloc[0]['Close_voo']

    tqqq_shares = (investment * tqqq_percentage) / initial_tqqq_price
    voo_shares = (investment * voo_percentage) / initial_voo_price

    # 循环遍历数据，模拟投资策略
    for index, row in test_data.iterrows():
        # 每30天调整一次持仓占比
        if (index - pd.to_datetime(start_date)).days % 30 == 0 and index != pd.to_datetime(start_date):
            total_value = tqqq_shares * row['Close_tqqq'] + voo_shares * row['Close_voo']
            tqqq_shares = total_value * tqqq_percentage / row['Close_tqqq']
            voo_shares = total_value * voo_percentage / row['Close_voo']

    # 计算最终收益
    final_value = tqqq_shares * test_data.iloc[-1]['Close_tqqq'] + voo_shares * test_data.iloc[-1]['Close_voo']
    profit = final_value - investment
    profit_percentage = (final_value - investment) / investment * 100

    # print(f"初始投资金额：${investment:.2f}")
    # print(f"最终价值：${final_value:.2f}")
    # print(f"收益：${profit:.2f}")
    # print(f"收益率：{profit_percentage:.2f}%")

    return profit_percentage


# test_one(merged_data, tqqq_percentage=0.5, voo_percentage=0.5, test_start_date='2012-08-14', test_duration_days=360)
# ------------------------------


import random

def find_optimal_percentage(merged_data, test_duration_days):
    results = []  # 保存每个占比组合和对应的收益率

    random_test_dates = random.sample(list(merged_data.index), 60)  # 从测试数据中随机选择 100 个起始日期

    tqqq_range = range(30, 80, 10)  # 将 TQQQ 的占比从 0% 到 80% 之间试验
    
    for test_start_date in random_test_dates:
        for tqqq in tqqq_range:
            tqqq_percentage = tqqq / 100  # 将 tqqq 转换为占比形式
            voo_percentage = 1 - tqqq_percentage  # VOO 占比为剩余的比例

            profit_percentage = test_one(merged_data, tqqq_percentage, voo_percentage, test_start_date, test_duration_days)
            
            # 将每个占比组合和对应的收益率保存到结果列表中
            results.append({
                'TQQQ_Percentage': tqqq_percentage,
                'VOO_Percentage': voo_percentage,
                'Profit_Percentage': profit_percentage
            })

    # 将结果列表转换为 pandas DataFrame
    results_df = pd.DataFrame(results)

    # 按 'TQQQ_Percentage' 和 'VOO_Percentage' 分组，并计算统计量（如平均值、最大值等）
    grouped_results = results_df.groupby(['TQQQ_Percentage', 'VOO_Percentage']).agg({
        'Profit_Percentage': ['mean', 'max', 'min', 'std', 'count']
    }).reset_index()

    # 输出分组后的统计结果
    print(grouped_results)


# 调用函数寻找最佳比例
find_optimal_percentage(merged_data, test_duration_days=450)


#----------------------300 天-------------------------------------------------------------
#   TQQQ_Percentage VOO_Percentage Profit_Percentage
#                                               mean         max        min        std count
# 0             0.0            1.0          8.202464   29.060521 -24.053148  10.741117    60
# 1             0.1            0.9         10.942094   41.019575 -32.113200  14.222532    60
# 2             0.2            0.8         13.726870   53.669786 -39.461645  17.904616    60
# 3             0.3            0.7         16.550247   66.364136 -46.148619  21.686186    60
# 4             0.4            0.6         19.405151   78.992247 -52.221624  25.520771    60
# 5             0.5            0.5         22.283950   91.432332 -57.725619  29.382946    60
# 6             0.6            0.4         25.178431  103.550705 -62.703106  33.256949    60
# 7             0.7            0.3         28.079765  115.201298 -67.194217  37.132577    60

#   TQQQ_Percentage VOO_Percentage Profit_Percentage
#                                               mean         max        min        std count
# 0            0.30           0.70         23.762283   82.820130 -31.254381  21.751089    60
# 1            0.35           0.65         25.940655   91.401733 -33.991369  23.807756    60
# 2            0.40           0.60         28.125813  100.306514 -36.664191  25.898458    60
# 3            0.45           0.55         30.315360  109.543825 -39.272646  28.018214    60


# ----------450天----------------------
#   TQQQ_Percentage VOO_Percentage Profit_Percentage
#                                               mean         max        min        std count
# 0             0.3            0.7         28.865254   71.160715 -37.272097  25.210051    60
# 1             0.4            0.6         34.043291   87.041047 -43.208663  30.409734    60
# 2             0.5            0.5         39.320775  103.554863 -48.802607  35.760664    60
# 3             0.6            0.4         44.679958  120.651558 -54.046998  41.236581    60
# 4             0.7            0.3         50.100565  138.272874 -58.939282  46.819738    60

# 总结：
# 过去十年长牛，闭眼全仓tqqq。比例越高越好。
# 但2022年超级熊市，越低越好。