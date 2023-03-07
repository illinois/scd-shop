# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

from funcs import *

machineData, userData = getData()

app = Dash(__name__, external_stylesheets=[
           dbc.themes.SPACELAB], title='SCD Shop Dashboard')

app.layout = html.Div([
    html.H1('Test Application'),
    html.Div(children='Woah, a subtitle!'),
    dcc.Dropdown( options = timeframeDict,
        value = 'yesterday',
        id = 'timeframe-dropdown'),
    dcc.Graph(id = 'machineData-figure')
])

@app.callback(
    Output('machineData-figure', 'figure'),
    Input('timeframe-dropdown', 'value'))

def update_figure(selected_timeframe):
    machineData, userData = getData(timeframe = selected_timeframe)
    
    fig = px.bar(machineData, x='deviceName', y='value', color='deviceName')
    
    fig.update_layout(transition_duration = 250)
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
