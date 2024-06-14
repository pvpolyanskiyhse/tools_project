import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd

nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace = True)

options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic
    mydict['value'] = tic
    options.append(mydict)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Enter a stock symbol:'),
       
        dcc.Dropdown(id = 'my_ticker_symbol',
                     options = options,
                     multi = True)
        
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': "40%"}),
    html.Div([
        html.H3('Select dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            initial_visible_month=datetime.today(),
            min_date_allowed='2015-1-1',
            max_date_allowed=datetime.today(),
            start_date = '2020-1-1',
            end_date = datetime.today(),
            with_portal=True
        )
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 24, 'marginLeft': '30px'}
        )
    ]),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1, 2], 'y': [3, 1]}
            ],
            'layout': {'title': 'Default'}
        }
    )
])




@app.callback(Output('my_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my_ticker_symbol', 'value'),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], "%Y-%m-%d")#'2020-1-1'
    end = datetime.strptime(end_date[:10], "%Y-%m-%d") #'2021-1-1'
    
    traces = []
    
    for tic in stock_ticker:

        data = yf.download(tic, start, end)
        traces.append({'x': data.index, 'y': data['Close']})

    fig = {
        'data': traces,
        'layout': {'title': stock_ticker}
    }

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

#python src/app.py
