# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

from funcs import *

machineData, userData = getData()

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB], title = 'SCD Shop Dashboard')

fig1 = px.bar(machineData, x = 'deviceName', y = 'value', color = 'deviceName')

app.layout = html.Div(children=[
    html.H1(
        children='Test Application'),

    html.Div(children='Woah, a subtitle!'),

    dcc.Graph(
        id='example-graph',
        figure=fig1
    )
])

             
if __name__ == '__main__':
    app.run_server(debug=False)

