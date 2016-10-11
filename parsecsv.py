
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from datetime import datetime
get_ipython().magic(u'matplotlib inline')


# In[10]:

df = pd.read_csv('weather_20160307.csv', parse_dates=[0,16,17])
df['Dew'] = df.Dew.round(decimals=2)
df['Feel'] = df.Feel.round(decimals=2)
df['Temp'] = df.Temp.round(decimals=2)
df['WS'] = df.WS.round(decimals=2)
df['Press'] = df['Press'].astype(int)
df['WD'] = df['WD'].astype(int)
df['Tmin'] = df['Tmin'].astype(int)
df['Tmax'] = df['Tmax'].astype(int)
df['Sunrise'] = df.Sunrise.dt.strftime('%H:%M:%S')
df['Sunset'] = df.Sunset.dt.strftime('%H:%M:%S')


# In[11]:

df.sort_values(by=['Date','City'], ascending=[False,True]).head()


# In[4]:

wmed = df.groupby('City')['City','Temp','Feel','Press','WS','Cloud'].median().round(2).copy()
wavg = df.groupby('City')['City','Temp','Feel','Press','WS','Cloud'].mean().round(2).copy()


# In[5]:

i = 1
for c in wavg.columns:
    wmed.insert(list(wmed.columns).index(c)+1,c+'Avg',wavg[c])


# In[6]:

for i in ['Temp','Feel','Press','WS','Cloud']:
    #wmed.columns[list(wmed.columns).index(i)]= i+'Med'
    wmed = wmed.rename(columns={i: i+'Med'})


# In[7]:

wmed


# In[8]:

#wmed.plot(y=['TempMed', 'TempAvg'], color=['black','red'], style='x', figsize=(16,8))
wmed.plot(y=['TempMed', 'TempAvg'], style=['x','.'], figsize=(16,8), sort_columns='TempMed')


# In[167]:



