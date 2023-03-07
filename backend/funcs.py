# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 23:52:23 2023

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
from dotenv import load_dotenv
import os

# read secrets
def secretFunc():
    load_dotenv()
    global auth_token
    global bearer_token
    global URL
    auth_token = os.getenv('auth_token')
    bearer_token = os.getenv('bearer_token')
    URL = os.getenv('URL')
    
secretFunc()
    
# query relevant GRIT endpoint
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
    
    if(reportType == 'toolReport'):
        machineData = pd.read_json(json.dumps(content[0]))
        userData = pd.read_json(json.dumps(content[1]))
        file1 = open(f'data/machineData_{timeframe}.json', 'w')
        json.dump(machineData.to_dict(), file1)
        file1.close()
        file2 = open(f'data/userData_{timeframe}.json', 'w')
        json.dump(userData.to_dict(), file2)
        file2.close()
        return(machineData, userData)
    
    elif(reportType == 'userReport'):
        userTotal = pd.read_json(json.dumps(content[0]))
        userTools = pd.read_json(json.dumps(content[1]))
        file1 = open(f'data/userTotal_{timeframe}.json', 'w')
        json.dump(userTotal.to_dict(), file1)
        file1.close()
        file2 = open(f'data/userTools_{timeframe}.json', 'w')
        json.dump(userTools.to_dict(), file2)
        file2.close()
        return(userTotal, userTools)
    
    else:
        file = open(f'data/{reportType}_{timeframe}.json', 'w')
        json.dump(content, file)
        file.close()
        return(content)
   

# basic data retrieval - checks for local copy then pulls from API if necessary
# implement stale-data checking or just have manual refresh
def getData(timeframe = 'yesterday', reportType = 'toolReport'):
    
    if reportType == 'toolReport':
        
        try:
            file1 = open(f'data/machineData_{timeframe}.json', 'r')
            machineData = json.load(file1)
            file1.close()
            file2 = open(f'data/userData_{timeframe}.json','r')
            userData = json.load(file2)
            file2.close()
            
            return(machineData, userData)
        
        except:
            machineData, userData = queryGritData(timeframe, reportType)
            return(machineData, userData)
            
    if reportType == 'userReport':
        
        try:
            file1 = open(f'data/machineData_{timeframe}.json', 'r')
            userTotal = json.load(file1)
            file1.close()
            file2 = open(f'data/userData_{timeframe}.json','r')
            userTools = json.load(file2)
            file2.close()
            
            return(userTotal, userTools)
        
        except:
            userTotal, userTools = queryGritData(timeframe, reportType)
            return(userTotal, userTools)
            
    else:
        
        try:
            file = open(f'data/{reportType}_{timeframe}.json', 'r')
            data = json.load(file)
            file.close()
            
            return(data)
        
        except FileNotFoundError:
            data = queryGritData(timeframe, reportType)
            return(data)
        
