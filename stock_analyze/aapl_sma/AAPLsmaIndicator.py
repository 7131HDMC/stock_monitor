#!/usr/bin/env python
# coding: utf-8

# # Create SMA with Python

# Import libraries

# In[1]:


import numpy as np
import pandas as pd
import investpy as ip
# import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.express as px


# Get historical data from stock name

# In[10]:


#Define function to egt historical data with investpy
def get_stock_df(stock, country, from_date, to_date, interval):
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)
#historical data from 5 yeasr ago#get Aaple 
aapl = get_stock_df("AAPL", 'united states', '13/04/2017', '22/04/2022', 'daily')

aapl.head()

#Visual representation
# In[12]:


aapl["Close"].plot(grid=True)


# Define a simple moving average from 30 and 100 entries window

# In[130]:


# Define FIRST AND SECOND sma intervals
st_sma_interval = 30
nd_sma_interval = 50
#DEFINE FIRST AND SECOND  SMA INTERVALS NAME
st_sma_name = "sma"+str(st_sma_interval)
nd_sma_name = "sma"+str(nd_sma_interval)

st_sma  = pd.DataFrame()
nd_sma = pd.DataFrame()

st_sma["close_price"] = aapl["Close"].rolling(window = st_sma_interval).mean()
nd_sma["close_price"] = aapl["Close"].rolling(window = nd_sma_interval).mean()


# View new DataFrame TAIL

# In[131]:


print(st_sma.tail())
print(nd_sma.tail())


# Create a simple graph with both sma and aapl close price

# In[132]:


aapl["Close"].plot(grid=True)
st_sma["close_price"].plot(grid=True)
nd_sma["close_price"].plot(grid=True)


# Create function to return a dataframe with sma cross signal of buy or sell

# In[133]:


#buy and sell definitions
buy  = 1
sell = 0

def sma_signals(data):
    flag = -1
    
    data["signal"] = np.nan
    
    for i in range(len(data)):
        if data[st_sma_name][i] > data[nd_sma_name][i]:# if first sma cross second is a buy signal
            if flag != buy:
                data["signal"][i] = buy
                flag = buy
        elif data[st_sma_name][i] < data[nd_sma_name][i]:# if second sma cross first is a sell signal
            if flag != sell:
                data["signal"][i] = sell
                flag = sell
    
    return data.copy()


# Prepare data with copy from AAPL

# In[134]:


#Copy dataframe
aapl_ = aapl.copy()

#delete some columns
aapl_ = aapl_.drop(['High', 'Open', 'Low', 'Currency'], axis=1)

aapl_[st_sma_name] = st_sma["close_price"]
aapl_[nd_sma_name] = nd_sma["close_price"]
print(aapl_.tail())


# In[135]:


aapl_ = sma_signals(aapl_)
aapl_.tail()


# In[138]:


aapl_.loc[ aapl_["signal"] == 1 ,"signal"]


# Create functioon to show a graph from dataframe with two sma cross

# In[140]:


def show_sma_signals(data):
    ## Make subplot with Title
    fig = make_subplots(
            rows=2, 
            cols=1, 
            shared_xaxes=True, 
            specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
            vertical_spacing=0.03,
            subplot_titles=(' AAPL close price history buy and sell signal ', ' Daily interval '),
            row_width=[0.2, 0.7],
    )

    ## Add Close datal as yAXIS
    fig.add_trace( 
        go.Scatter( 
            x=data.index, 
            y=data["Close"],
            mode="lines",
            name="Close"
        )
    )

    ## Add st_sma_name alongside Close data
    fig.add_trace(
        go.Scatter(
            x=data[st_sma_name].index, 
            y=data[st_sma_name],
            mode="lines",
            line_color="orange",
            name=st_sma_name,
            opacity=0.72
    )
    ,row=1, col=1)

    ## Add nd_sma_name alongside Close data
    fig.add_trace(
        go.Scatter(
            x=data[nd_sma_name].index, 
            y=data[nd_sma_name],
            mode="lines",
            name=nd_sma_name,
            line_color="yellow",
            opacity=0.72
    )
    ,row=1, col=1)

    #Add sell marker at firts cross second based on signal pre calculated
    fig.add_trace(
        go.Scatter(
            x=data[data["signal"] == sell].index, 
            y=data[data["signal"] == sell]["Close"],
            mode="markers",
            name="Sell",
            marker_color="red",
            marker_symbol="arrow-down-open",
            marker_size=7,
    )
    ,row=1, col=1)


    #Add sell marker at firts cross second based on signal pre calculated
    fig.add_trace(
        go.Scatter(
            x=data[data["signal"] == buy].index, 
            y=data[data["signal"] == buy]["Close"],
            mode="markers",
            name="Buy",
            marker_color="springgreen",
            marker_symbol="arrow-up-open",
            marker_size=7,
    )
    ,row=1, col=1)
    
    #change template
    fig.update_layout(
        template="plotly_dark", 
        xaxis_rangeslider_visible=True,
        height=700
    )

    fig.show()


# In[139]:


show_sma_signals(aapl_.copy())

