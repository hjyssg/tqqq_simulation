import pandas as pd
import os
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 随机测试杠杆ETF多年return

# Usage example:
filename = "^SPX.csv"
df_1 = _util.load_csv_as_dataframe(filename)

def calculate_returns(df, start_year, end_year, multiplier):
    # Filter dataframe based on start_year and end_year
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
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
        start_year = random.randint(1950, 2020)
        end_year = start_year + 5  # Random 3-year period
        multiplier = random.choice([3])
        result = calculate_returns(df, start_year, end_year, multiplier)
        results.append(result)
    return results

# Perform random testing
results = random_test(df_1)

# Convert results list to pandas Series
results_series = pd.Series(results)
summary_stats = results_series.describe()
print(summary_stats)

# Visualize the distribution of results
plt.hist(results, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Derived Return to Original Return Ratio')
plt.ylabel('Frequency')
plt.title('Distribution of Return Ratios')
plt.grid()
plt.show()
