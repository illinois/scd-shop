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
    
    r = requests.get(f'{URL}/sse/data', 
        data={'auth_token': auth_token},
        headers = {'Authorization': 'Bearer ' + bearer_token})

    # save raw data
    content = json.loads(r.text)
    content = pd.json_normalize(content, max_level = 1)
    RFID = content[['data.name', 'data.id', 
                        'data.pingAt', 'data.isOnline',
                        'data.userId', 'data.userName']]
    return(RFID)

# [content["type"] == 'rfid']
dashInfo = dashboardFunc()

fig = px.choropleth(dashInfo, geojson = shopGEOJSON,
                    locations = 'data.id', featureidkey = 'properties.uid',
                    color = 'data.name')

# for some weird reason the map just shows up blank
# maybe because not all data entries have matches between the JSON and regular dataset?
# needs attention


fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


def aggregateFunc(input_df, group_by, aggregate_on, aggregate_func):
    # takes a df as df, grouping column as string, aggregate target column as string, and aggregate function column as string
    # returns a pandas series of the aggregate target column in DESCENDING order
    aggregation = pd.NamedAgg(column = aggregate_on, aggfunc = aggregate_func)
    output_series = input_df.groupby(group_by).agg(result = aggregation)
    if(group_by == 'userName' and aggregate_on == 'value'):
        output_series = output_series.sort_values(by = 'result', ascending = False)
    return(output_series) 


machineData, userData = getData()
userDataAgg = aggregateFunc(userData, 'userName', 'value', 'sum')
# fig = px.bar(userDataAgg, x = userDataAgg.index, y='result', color = userDataAgg.index)
# fig.show()
