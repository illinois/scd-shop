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

