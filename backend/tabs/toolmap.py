# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:51:42 2023

@author: Rishi
"""

from funcs import *

def toolMap_function():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3('Tool Map'),
                html.Div(children='Can you believe it? Another subtitle!'),
                html.Br(),
                html.Div(children=[
                    dbc.Button("Refresh Data", color="primary",
                               id='toolMap-button', n_clicks=0,
                               className='me-2')],
                         className='d-flex flex-row'),
                dcc.Graph(id='toolMap-figure')
            ]
        ),
        className="mt-3")