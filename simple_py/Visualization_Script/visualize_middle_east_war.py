import pandas as pd
import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util
data = _util.load_csv_as_dataframe("^SPX.csv")

# Define the date ranges for war periods
war_periods = {
    'Suez Crisis (1956)': ('1956-10-29', '1956-11-07'),
    'Six-Day War (1967)': ('1967-06-05', '1967-06-10'),
    'Yom Kippur War (1973)': ('1973-10-06', '1973-10-25'),
    'Lebanon War (1982)': ('1982-06-06', '1982-09-30'),
    'Lebanon War (2006)': ('2006-07-12', '2006-08-14')
}

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Stock Price Analysis During Wars"),
    dcc.Graph(id='war-graph'),
    html.P("Select a war to view stock data:"),
    dcc.Dropdown(
        id='war-dropdown',
        options=[{'label': war, 'value': war} for war in war_periods],
        value='Suez Crisis (1956)'  # Default value
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
