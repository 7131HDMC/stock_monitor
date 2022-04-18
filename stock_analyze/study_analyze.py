#!/usr/bin/env python
# coding: utf-8

# ## Import libraries

# In[2]:


import numpy as np
import pandas as pd
import investpy as ip
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import seaborn as sns
from scipy.signal import argrelextrema


# ## Define intervals and countries

# In[3]:


countries = ['brazil', 'united states']#n countries
intervals = ['Daily','Weekly','Monthly']


# ## Function to get historical data from investpy

# In[4]:


def search_stocks(stock, country, from_date, to_date, interval):
    print("stock =>",stock)
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)


# ## Get AAPL records and test

# In[5]:


aapl = search_stocks("AAPL", countries[1], '13/04/2020', '13/04/2022', intervals[0])


# ### Test .head .desxcribe and .tail

# Head

# In[6]:


aapl.head()


# Tail

# In[7]:


aapl.tail()


# Describe

# In[9]:


aapl.describe()


# In[13]:


print(aapl.columns)
print(aapl.index)


# In[14]:


#Last 10
aapl["Close"][-10:]


# In[24]:


## loc usage
# print(aapl.loc[ pd.Timestamp("2020-11-01") : pd.Timestamp("2020-12-31") ].head())
## First rows fromgiven date
# print(aapl.loc["2020"].head())
## iloc usage
# print(aapl.iloc[22:43])# from index x(22) to index y(43)


# In[25]:


aapl.sample(20)


# In[27]:


aapl.resample('M').mean()


# In[32]:


aapl.asfreq('M', method="bfill")


# In[ ]:





# In[39]:


aapl['Diff'] = aapl.Open - aapl.Close
aapl['Diff']


# In[46]:


aapl["Diff"].plot(grid=True)
aapl["Close"].plot(grid=True)


# In[ ]:




