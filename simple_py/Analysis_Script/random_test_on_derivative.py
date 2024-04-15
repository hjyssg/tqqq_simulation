import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 随机测试杠杆ETF多年return

# Usage example:
filename = "^SPX.csv"
df_1 = _util.load_csv_as_dataframe(filename)
multiplier = 3


def calculate_returns(df, start_date, end_date, multiplier):
    # Filter dataframe based on start_year and end_year
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # Calculate n-derivatives
    df_2 = _util.calculate_n_derivatives(df, multiplier)
    
    # Calculate original return
    original_return = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
    
    # Calculate derived return
    derived_return = (df_2['Close'].iloc[-1] / df_2['Close'].iloc[0] - 1) * 100
    
    # Return derived return / original return
    # return derived_return / original_return
    return derived_return 


import random
# Define a function for random testing
def random_test(df, num_tests=100):
    results = []
    for _ in range(num_tests):
        # Randomly select a start date between 1950-01-01 and 2020-12-31
        start_date = datetime.datetime(1950, 1, 1) + datetime.timedelta(days=random.randint(0, (2020 - 1950) * 365))
        # Calculate the end date based on the selected start date
        end_date = start_date + datetime.timedelta(days=365 * 3)  # 4-year period


        result = calculate_returns(df, start_date, end_date, multiplier)
        results.append(result)

        if result > 1000:
            print(start_date, end_date, result)


    return results

# Perform random testing
results = random_test(df_1)

# Convert results list to pandas Series
results_series = pd.Series(results)
summary_stats = results_series.describe()
print(summary_stats)

# Visualize the distribution of results
plt.hist(results, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Percent')
plt.ylabel('Frequency')
plt.title(f'${filename} ${multiplier} return distribution')
plt.grid()
plt.show()
