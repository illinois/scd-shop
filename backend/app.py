# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

from funcs import *

machineData, userData = getData() # pre-load yesterday's data

app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], title='SCD Shop Dashboard')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H1('Test Application'),
            html.Div(children='Woah, a subtitle!'),
            dcc.Dropdown( options = timeframeDict,
                value = 'yesterday',
                id = 'timeframe-dropdown'),
            dcc.Graph(id = 'machineData-figure')
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Machine Data"),
        dbc.Tab(tab2_content, label="???"),
        dbc.Tab(
            "This tab's content is never seen", label="Live Dashboard (coming soon!)", disabled=True
        ),
    ]
)

app.layout = dbc.Container(tabs, fluid = True)

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
