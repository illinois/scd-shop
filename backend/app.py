# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

from funcs import *

# pre-load yesterday's data
machineData, userData = getData()

# load shop geoJSON
geoJSON = 'data/features.geojson'
with open(geoJSON) as file:
    shopGEOJSON = json.load(file)
    file.close()


app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], title='SCD Shop Dashboard')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Per-machine Runtime'),
            html.Div(children='Woah, a subtitle!'),
            html.Br(),
            html.Div(children=[
                html.Div(children=[
                    dcc.Dropdown(options=timeframeDict,
                                 value='yesterday',
                                 id='machineTime-dropdown',
                                 className='me-2')],
                         className='col col-lg-2'),
                html.Div(children=[
                    dbc.Button("Refresh Data", color="primary",
                               id='machineRefresh-button', n_clicks=0,
                               className='me-2')],
                         className='col-md-auto')],
                     className='d-flex flex-row'),
            dcc.Graph(id='machineData-figure'),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Per-user Runtime'),
            html.Div(children='Woah, another subtitle!'),
            html.Br(),
            html.Div(children=[
                html.Div(children=[
                    dcc.Dropdown(options=timeframeDict,
                                 value='yesterday',
                                 id='userTime-dropdown',
                                 className='me-2')],
                         className='col col-lg-2'),
                html.Div(children=[
                    dbc.Button("Refresh Data", color="primary",
                               id='userRefresh-button', n_clicks=0,
                               className='me-2')],
                         className='col-md-auto')],
                     className='d-flex flex-row'),
            dcc.Graph(id='userData-figure'),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Secret tab...')]))

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Live Dashboard'),
            html.Div(children='Can you believe it? Another subtitle!'),
            html.Br(),
            html.Div(children=[
                dbc.Button("Refresh Data", color="primary",
                           id='liveRefresh-button', n_clicks=0,
                           className='me-2')],
                     className='d-flex flex-row'),
            dcc.Graph(id='liveDash-figure')
            ]
        ),
    className="mt-3")

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Machine Data"),
        dbc.Tab(tab2_content, label="User Data"),
        dbc.Tab(tab3_content, label="More Data...", disabled = True),
        dbc.Tab(tab4_content, label = 'Live Status Dashboard')
    ]
)

layout = dbc.Container([
    html.Br(),
    html.H2("a silly goofy website"),
    html.Div('a silly goofy subtitle'),
    html.Br(),
    dbc.Alert("This dashboard is under development :)", color='info'),
    html.Br(),
    tabs],
    fluid=True)

app.layout = dbc.Container(layout, fluid=True)


@app.callback(
    Output('machineData-figure', 'figure'),
    Input('machineTime-dropdown', 'value'),
    Input('machineRefresh-button', 'n_clicks'))
def update_machine_figure(selected_timeframe='', n=0):

    if n > 0:
        machineData, userData = queryGritData(timeframe=selected_timeframe)
    else:
        machineData, userData = getData(timeframe=selected_timeframe)
        
    machineData['value'] = machineData['value'] / 60

    fig = px.bar(machineData, x='deviceName', y='value', 
                 title = 'Usage by Machine',
                 labels = {
                     'deviceName': 'Machine',
                     'value': 'Cumulative Runtime (minutes)'},
                 color='deviceName')

    fig.update_layout(transition_duration=250)

    return fig


@app.callback(
    Output('userData-figure', 'figure'),
    Input('userTime-dropdown', 'value'),
    Input('userRefresh-button', 'n_clicks'))
def update_user_figure(selected_timeframe='', n=0):

    if n > 0:
        machineData, userData = queryGritData(timeframe=selected_timeframe)
    else:
        machineData, userData = getData(timeframe=selected_timeframe)
    userDataAgg = userData.groupby('userName').value.agg('sum')
    userDataAgg = userDataAgg.sort_values(ascending=False)
    
    userDataAgg = userDataAgg / 60
    
    fig = px.bar(userDataAgg, x=userDataAgg.index,
                 y='value',
                 title = 'Usage by User', 
                 labels = {
                     'userName': 'User',
                     'value': 'Cumulative Runtime (minutes)'},
                 color=userDataAgg.index)
    fig.update_layout(transition_duration=250)

    return fig


@app.callback(
    Output('liveDash-figure', 'figure'),
    Input('liveRefresh-button', 'n_clicks'))
def updateDash(n = 0):

    dashInfo = dashboardFunc()

    fig = px.choropleth(dashInfo, geojson=shopGEOJSON,
                        locations='data.id', featureidkey='properties.uid',
                        color='statusColor',
                        color_discrete_map = {'#fd7e14': '#fd7e14',  # inUse
                                              '#20c997': '#20c997',  # available
                                              '#adb5bd': '#adb5bd'}) # broken

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
