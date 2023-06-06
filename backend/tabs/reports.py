# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:25:39 2023

@author: Rishi
"""

from funcs import *

def machine_function():
    return dbc.Card(
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

def user_function():
    return dbc.Card(
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
