import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
from collections import deque
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')


X = deque(maxlen=50)
Y = deque(maxlen=50)

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite en vivo'),
        html.Div(id='intermediate-value', style={'display': 'none'}),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]

@app.callback(Output('live-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph_scatter(n):
    satellite = Orbital('TERRA')
    tiempo = []
    Latitude = []
    Longitude = []
    Altitude = []
    valor=[]
    v=[]

    X.append(datetime.datetime.now() - datetime.timedelta())
    Y.append(random.randrange(-20,20))   
   #datetime.datetime.now().time()
    for i in range(2*n):
        v=random.randrange(-20,20)
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        lon, lat, alt = satellite.get_lonlatalt(
            time
        )

        Longitude.append(lon)
        Latitude.append(lat)
        Altitude.append(alt)
        tiempo.append(time)
        valor.append(v)
    
    trace1 = go.Scatter(
            x=list(tiempo),
            y=list(Altitude),
            name='Altitud',
            mode= 'lines+markers'
            )



 

    return {'data': [trace1],'layout' : go.Layout(transition={'duration': 1,'easing': 'cubic-in-out'})}




if __name__ == '__main__':
    app.run_server(debug=True)
