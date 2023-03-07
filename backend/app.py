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
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

# read secrets

keys = open('keys.txt', 'r')
auths = keys.readlines()
auth_token = auths[0].strip()
bearer_token = auths[1].strip()
URL = auths[2].strip()
keys.close()

### query API function ###

def queryGritData(timeframe = 'yesterday', reportType = 'toolReport', authToken = auth_token, bearerToken = bearer_token, URL = URL):
    
    # make a dictionary for each of the endpoint lookups using the timeframe var
    
    endpointDict = {'fullReport': f'{URL}/report/activity/{timeframe}/',
                    'runtimeReport': f'{URL}/report/activity/{timeframe}/runtime/',
                    'trackReport': f'{URL}/report/activity/{timeframe}/track/',
                    'statusReport': f'{URL}/report/activity/{timeframe}/deviceStatus/',
                    'signonReport': f'{URL}/report/signon/{timeframe}/',
                    'assetReport': f'{URL}/report/asset/{timeframe}/',
                    'toolReport': f'{URL}/report/trigger/all/runtime/{timeframe}/',
                    'userReport': f'{URL}/report/user/all/runtime/{timeframe}/'}
    
    r = requests.get(endpointDict[f"{reportType}"], 
               data = {'auth_token': auth_token})

    # save raw data
    
    content = json.loads(r.text)
    content.append(f'{reportType}')
    dump = json.dumps(content)
    with open(f'data/{reportType}_{timeframe}.json', 'w') as output:
        output.write(dump)
        output.close()
    return(content)

def getData(timeframe = 'yesterday', reportType = 'toolReport'):
    try:
        file = open(f'data/{reportType}_{timeframe}.json', 'r')
        content = pd.read_json(file)
        file.close()
        
    except FileNotFoundError:
        content = queryGritData(timeframe, reportType)
        
    except:
        print('oh shit lol')
        exit(-1)
            
        if(content[-1] == 'toolReport'):
            machineData = content[0]
            userData = content[1]
            return(machineData, userData)
        
        elif(content[-1] == 'userReport'):
            userTotal = content[0]
            userTools = content[1]
            return(userTotal, userTools)
        
        else:
            return(content)
        

# reportType = 'toolReport'
# timeframe = 'yesterday'
    
machineData, userData = getData()

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB], title = 'Test Application')

fig1 = px.bar(machineData, x = 'deviceName', y = 'value', color = 'deviceName')

app.layout = html.Div(children=[
    html.H1(
        children='Test Application'),

    html.Div(children='Dash: A web application framework for your data.'),

    dcc.Graph(
        id='example-graph-2',
        figure=fig1
    )
])

             
# if __name__ == '__main__':
#     app.run_server(debug=False)

