# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

# import helper functions
from funcs import *

# import tabs
from tabs.reports import *
from tabs.toolmap import *

# pre-load yesterday's data
machineData, userData = getData()

# load shop geoJSON
geoJSON = 'data/features.geojson'
with open(geoJSON) as file:
    shopGEOJSON = json.load(file)
    file.close()


app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], title='SCD Shop Dashboard')

disabled_tab = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Secret tab...')
            # when implementing this tab follow the same structure as others
            ]
        )
    )

leftTabs = dbc.Tabs(
    [
        dbc.Tab(machine_function(), label="Machine Data"),
        dbc.Tab(user_function(), label="User Data"),
        dbc.Tab(disabled_tab, label="More Data...", disabled=True),
        dbc.Tab(toolMap_function(), label='Tool Map')
    ]
)

rightTabs = dbc.Tabs(
    [
     dbc.Tab()
     ]
)

layout = dbc.Container([
    html.Br(),
    html.H2("a silly goofy website"),
    html.Div('a silly goofy subtitle'),
    html.Br(),
    dbc.Alert("This dashboard is under development :)", color='info'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(leftTabs)),
                    dbc.Col(html.Div("Thar be tabs ahead..."))
                ])
        ])
],
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
                 title='Usage by Machine',
                 labels={
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
                 title='Usage by User',
                 labels={
                     'userName': 'User',
                     'value': 'Cumulative Runtime (minutes)'},
                 color=userDataAgg.index)
    fig.update_layout(transition_duration=250)

    return fig


@app.callback(
    Output('toolMap-figure', 'figure'),
    Input('toolMap-button', 'n_clicks'))
def updateToolMap(n=0):

    dashInfo = toolMapData()

    fig = px.choropleth(dashInfo, geojson=shopGEOJSON,
                        locations='data.id', featureidkey='properties.uid',
                        color='statusColor',
                        color_discrete_map={'#fd7e14': '#fd7e14',  # inUse
                                            '#20c997': '#20c997',  # available
                                            '#adb5bd': '#adb5bd'})  # broken

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
