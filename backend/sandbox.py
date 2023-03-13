# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 19:14:20 2023

@author: Rishi
"""

from funcs import *
import plotly.io as pio


machineData, userData = getData()

userDataAgg = userData.groupby('userName').value.agg('sum')
userDataAgg = userDataAgg.sort_values(ascending = False)

fig = px.bar(userDataAgg, x = userDataAgg.index, y='value', color = userDataAgg.index)
pio.renderers.default='browser'

fig.show()

def aggregateFunc(input_df, group_by, aggregate_on, aggregate_func):
    # takes a df as df, grouping column as string, aggregate target column as string, and aggregate function column as string
    # returns a pandas series of the aggregate target column in DESCENDING order
    aggregation = pd.NamedAgg(column = aggregate_on, aggfunc = aggregate_func)
    output_series = input_df.groupby(group_by).agg(result = aggregation)
    output_series = output_series.sort_values(ascending = False)
    return(output_series) 

