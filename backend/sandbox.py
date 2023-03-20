# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 19:14:20 2023

@author: Rishi

"""

from funcs import *
import plotly.io as pio
pio.renderers.default='browser'

geoJSON = 'data/features.geojson'
with open(geoJSON) as file:
    shopGEOJSON = json.load(file)

# test_data = px.data.election()
# test_geojson = px.data.election_geojson()

def dashboardFunc():
    # queries GRIT for the current status of all RFID-associated devices
    # returns a pandas dataframe containing the device name, id, last updated time, online status, and current signed-in user (nan if none) 

    r = requests.get(f'{URL}/sse/data', 
        data={'auth_token': auth_token},
        headers = {'Authorization': 'Bearer ' + bearer_token})

    # save raw data
    
    def statusCheck(row):
        inUse = '#fd7e14' # tool is in use, orange
        available = '#20c997' # tool is available, teal
        broken = '#adb5bd' # tool is locked out, gray
        
        if(row['data.lockout']):
            return(broken)
        elif(pd.isna(row['data.userName'])):
            return(available)
        else:
            return(inUse)
        
    content = json.loads(r.text)
    content = pd.json_normalize(content, max_level = 1)
    output = content.iloc[[0]]
    output = pd.concat([output, content.query('type == "rfid"')], 
                       ignore_index = True)
    output = output[['data.name', 'data.id', 
                        'data.pingAt', 'data.isOnline',
                        'data.userId', 'data.userName', 'data.lockout']]
    
    output['statusColor'] = output.apply(statusCheck, axis = 1)
        
    return(output)

# [content["type"] == 'rfid']


    
dashInfo = dashboardFunc()



# draw the shop outline as a separate, non-interactable trace then layer the machines on top
# would allow for some different colored background

shop_outline = px.choropleth(dashInfo.iloc[0], geojson = shopGEOJSON,
                             locations = 'data.id', featureidkey = 'properties.uid')
shop_outline.update_geos(fitbounds="locations", visible=False)
shop_outline.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
shop_outline.show()

fig = px.choropleth(dashInfo, geojson = shopGEOJSON,
                    locations = 'data.id', featureidkey = 'properties.uid',
                    color = 'statusColor')

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()