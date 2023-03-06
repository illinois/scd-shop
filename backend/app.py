# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 17:11:34 2023

@author: Rishi
"""

# imports

import requests
import pandas as pd
import json
from dash import Dash, html, dcc
import plotly.express as px
import numpy as np


r = requests.get('http://128.174.109.12/api/report/trigger/all/runtime/yesterday', 
           data = {'auth_token': 'grit_a9448704457346bf95eb4e27b66d2bd0'})

content = json.loads(r.text)[:2]

machineData = pd.DataFrame.from_records(content[0])
userData = pd.DataFrame.from_records(content[1])

app = Dash(__name__)


fig1 = px.bar(machineData, x = 'deviceName', y = 'value', color = 'deviceName')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig1
    )
])
             
if __name__ == '__main__':
    app.run_server(debug=False)

