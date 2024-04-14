import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将util.py所在的目录添加到系统路径中
import _util
df = _util.load_csv_as_dataframe("^SPX.csv")

# 选择1970年及之后的数据
df = df[df['Date'] >= pd.to_datetime('1970-01-01')].reset_index(drop=True)


# 初始化变量，用于跟踪前最高点
previous_high_index = 0
previous_high_price = df['Adj Close'][0]

# 存储历史高点的数据
historical_high_points = {'Date': [], 'Historical_High': []}

# 逐步迭代数据，找到每个数据点相对于之前所有数据的最高点
for index, row in df.iterrows():
    if row['Adj Close'] > previous_high_price:
        # 当前数据点的收盘价高于之前的最高点
        previous_high_index = index
        previous_high_price = row['Adj Close']

        # 存储历史高点的数据
        historical_high_points['Date'].append(row['Date'])
        historical_high_points['Historical_High'].append(previous_high_price)

# # 打印历史高点数据
historical_high_df = pd.DataFrame(historical_high_points)
print(historical_high_df)


import plotly.graph_objs as go
# Assume that historical_high_df and df are already defined from the previous code
# Create a line trace for the closing prices
trace_data = go.Scatter(
    x=df['Date'],
    y=df['Adj Close'],
    mode='lines',
    name='Close Price'
)

# Create a scatter trace for the historical high points
trace_ath = go.Scatter(
    x=historical_high_df['Date'],
    y=historical_high_df['Historical_High'],
    mode='markers',
    marker=dict(color='red', size=5),
    name='Historical High'
)

# Define the layout with a logarithmic scale on the y-axis
layout = go.Layout(
    title='Stock Price with ATH',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Price',
                 tickvals=[100, 250, 500, 1000, 2000, 5000],   
                 autorange=True,
                tickmode='auto'),
    legend=dict(x=0.1, y=0.9),
    xaxis_rangeslider_visible=True
)

# Create the figure with both traces
fig = go.Figure(data=[trace_data, trace_ath], layout=layout)

import dash
import dash_core_components as dcc
import dash_html_components as html
# Set up Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Prices Visualization"),
    dcc.Graph(id='stock-price-graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Specify your port here