from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import dash_auth

USERNAME_PASSWORD_PAIRS=[['username', 'password'], ['helloworld', 'goodbyeworld']]

app = Dash(__name__)
dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

server = app.server

nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace = True)

options = []
for tic in nsdq.index:
    #{'label': 'user sees','value':'script sees'}
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name']+''+tic # Apple Co. AAPL
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
            html.H1('Stock Ticker Dashboard'),
            html.Div([html.H3('Enter a stock symbol:', style = {'paddingRight':'30px'}), # the text above dropdown
            #Changing Input to be a dropdown
            #dcc.Input(id = 'my_stock_picker',
                      #value = 'TSLA',
                      #style = {'fontSize':24, 'width':75}
            dcc.Dropdown(id = 'my_ticker_symbol',
                         options = options,
                         value = ['TSLA'],
                         multi = True # !Allows us to choose more than just one option in a dropdown menu.
            )], style = {'display':'iline-block', 'color': '#49678d', 'verticalAlign':'top', 'width':'40%'}),#width to have more space to chose
            html.Div([html.H3('Select a start and end date:'),
                      dcc.DatePickerRange(id = 'my_date_picker',
                                          initial_visible_month=datetime.today(),  # Needed for MCOS
                                          min_date_allowed='2015-1-1',
                                          max_date_allowed=datetime.today(),
                                          start_date='2020-1-1', # default date
                                          end_date=datetime.today(), # default date
                                          with_portal=True  # Needed for MCOS
                                          )
                      ], style = {'display':'inline-block'}),
            html.Div([
                    html.Button(id = 'submit-button',
                                          n_clicks = 0,
                                          children = 'Submit!',
                                          style = {'fontSize': 24,'color':'white', 'background': '#49678d', 'marginLeft': '30px'}
                                          )
                      ]),
                      dcc.Graph(id = 'my_graph',
                                figure = {'data':[
                                    {'x':[1,2], 'y':[3,1]}
                        ], 'layout': {'title':'Default Title'}})])

@app.callback(Output('my_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my_ticker_symbol', 'value'),
               State('my_date_picker','start_date'),
               State('my_date_picker','end_date')
            ])
            # Step5. We keep the 'value', 'start_date', 'end_date' registered in its state, but don't send it
            # to update graph until we click on the submit button.
def update_graph(n_clicks, stock_ticker, start_date, end_date): #don't forget the date parameters, in the correct order
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')


    # Step 6. We need to edit our function to take in those stocks coming from dropdown menu -
    # to create traces for each ticker in the list.
    traces = []
    for tic in stock_ticker:
        data = yf.download(tic, start, end) # data is a df
        traces.append({'x': data.index,'y': data['Close'], 'name': tic})
    fig = {
        'data': traces,
        'layout': {'title': stock_ticker}
    }
    return fig
# Now the input box is interacting with the title.

if __name__ == '__main__':
    app.run(debug = True)

#1 Failed download:
#['DISCK']: YFTzMissingError('$%ticker%: possibly delisted; No timezone found')