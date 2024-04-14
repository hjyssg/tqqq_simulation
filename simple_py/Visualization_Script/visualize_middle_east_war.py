import pandas as pd
import os
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import timedelta

app = Dash(__name__)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")

# Define the date ranges for war periods


war_periods = {
    'Suez Crisis (1956) 苏伊士危机': ('1956-10-29', '1956-11-07'),
    'Six-Day War (1967) 六日战争': ('1967-06-05', '1967-06-10'),
    'Yom Kippur War (1973) 赎罪日战争': ('1973-10-06', '1973-10-25'),
    'Lebanon War (1982) 第五次中东战争': ('1982-06-06', '1982-09-30'),
    'Lebanon War (2006) 黎巴嫩战争': ('2006-07-12', '2006-08-14')
}

def calculate_price_changes(df, periods):
    results = []
    for war, (start, end) in periods.items():
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        
        # Adjusting the period to get 10 days before and after
        adjusted_start = start_date - timedelta(days=10)
        adjusted_end = end_date + timedelta(days=10)
        
        # Filter the dataframe for the adjusted date range
        mask = (df['Date'] >= adjusted_start) & (df['Date'] <= adjusted_end)
        filtered_data = df[mask]
        
        if not filtered_data.empty:
            start_price = filtered_data.iloc[0]['Close']
            end_price = filtered_data.iloc[-1]['Close']
            price_change = ((end_price - start_price) / start_price) * 100
            results.append({
                'War': war,
                'Price Change (%)': price_change,
                'Adjusted Start Date': adjusted_start.date(),
                'Adjusted End Date': adjusted_end.date(),
                'Start Price': start_price,
                'End Price': end_price
               
            })
        else:
            results.append({
                'War': war,
                'Price Change (%)': 'N/A',
                'Adjusted Start Date': adjusted_start.date(),
                'Adjusted End Date': adjusted_end.date(),
                'Start Price': 'N/A',
                'End Price': 'N/A'
            })
    
    return pd.DataFrame(results)

# Precompute the price changes
price_changes_df = calculate_price_changes(data, war_periods)

app.layout = html.Div([
    html.H1("Stock Price Analysis During Wars"),
    dcc.Graph(id='war-graph'),
    html.P("Select a war to view stock data:"),
    dcc.Dropdown(
        id='war-dropdown',
        options=[{'label': war, 'value': war} for war in war_periods],
        value='Suez Crisis (1956) 苏伊士危机'  # Default value
    ),
    html.H2("Price Changes Around War Periods"),
    dash_table.DataTable(
        id='price-change-table',
        columns=[{"name": i, "id": i} for i in price_changes_df.columns],
        data=price_changes_df.to_dict('records'),
        style_table={'overflowX': 'auto'}
    )
])

@app.callback(
    Output('war-graph', 'figure'),
    [Input('war-dropdown', 'value')]
)
def update_graph(selected_war):
    start, end = war_periods[selected_war]
    mask = (data['Date'] >= pd.to_datetime(start)) & (data['Date'] <= pd.to_datetime(end))
    war_data = data.loc[mask]

    fig = go.Figure(data=[
        go.Scatter(x=war_data['Date'], y=war_data['Close'], mode='lines+markers')
    ])

    fig.update_layout(
        title=f'{selected_war} (Stock Price)',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis_rangeslider_visible=True
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
