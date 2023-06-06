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
    

''' What useful information does each kind of report contain?

* full reports - completely overkill, contains all state updates, 
    logins & audits, etc
* runtime reports - provide aggregation within the selected timeframe grouped by 
    tool and user. too simple.
* track reports - provides rfid activation / deactivation and all user 
    sign-in/outs. will be useful to find sign-ons in last week for lockers 
    and storage purposes
* signon reports - provides signin, signout time, and duration 
    of time in raw and pretty-print
* asset reports - provides userId, updatedByUserId, and timestamp
* tool reports - provides aggregation on the selected timeframe by tool use time, 
    and usage information grouped by tool, user, and day
* user reports - provides aggregation on the selected timeframe by user tool use time,
    and also usage information grouped by tool, user, and day


'''
    
# takes a df as df, grouping column as string, aggregate target column as string, and aggregate function column as string
# returns a pandas series of the aggregate target column in DESCENDING order
def aggregateFunc(input_df, group_by, aggregate_on, aggregate_func):
    
    aggregation = pd.NamedAgg(column = aggregate_on, aggfunc = aggregate_func)
    
    output_series = input_df.groupby(group_by).agg(result = aggregation)
    
    if(group_by == 'userName' and aggregate_on == 'value'):
        output_series = output_series.sort_values(by = 'result', ascending = False)
        
    return(output_series) 

# implement POSTing freshly queried data to Mongo
# cronjob to run relatively frequently
# seed database with all-time information for each collection initially,
# then defaults to last-7 for day-to-day unless specifically updated

def mongoUpdate(timeframe = 'last-7', reportType = 'toolReport'):
    # mongo_URI
    client = MongoClient(mongo_URI, server_api=ServerApi('1'))
    db = client['SCD-SHOP-DEV']
    
    # since the collections are time-agnostic, we have to ignore the time 
    # aggregations that GRIT performs and do our own aggregation for each 
    
    collection = db[f'{reportType}']
    payload = queryGritData('last-7', reportType)[1]
    collection.insert_many(payload.to_dict(orient = 'records'))
    # inserting is not ideal since it will create many duplicates rapidly
    # work on implementing upserting
    print(f'{reportType} updated successfully.')
        
    return
    

# implement retrieving data from Mongo for easier aggregation