#!/usr/bin/env python
# coding: utf-8

# Define intervals and countries

# In[1]:



import numpy as np
import pandas as pd
import investpy as ip
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import seaborn as sns
from scipy.signal import argrelextrema


# Define intervals and countries

# In[2]:


countries = ['brazil', 'united states']#n countries
intervals = ['Daily','Weekly','Monthly']


# Define datetime to filter

# In[3]:


end_date   = datetime.today()
start_date = end_date - timedelta(days=7)


# In[4]:



def search_stocks(stock, country, from_date, to_date, interval):
    print("stock =>",stock)
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)


# In[5]:


def format_date(dt, format='%d/%m/%Y'):
  return dt.strftime(format)


# In[6]:
country_select = countries[0]

#sidebar = st.sidebar.empty()
stocks = ip.get_stocks_list(country=country_select)

# In[7]:


# from_date = end_date#st.sidebar.date_input("De: ", start_date)
# to_date   = #st.sidebar.date_input("Para: ", end_date)
# format_date(end_date)


# In[23]:


stock = "ALPA4"
df_result = {}
# print("STocks :: ", stocks)

for stock in stocks:
    try:
        df = search_stocks(stock, country_select, '13/04/2020', '13/04/2022', intervals[0])
    # df
    except:
        continue

    # 

    # In[9]:


    min_local_range = 5


    # In[10]:


    df_ = df.copy()
    # df_


    # In[11]:


    df_["i"] = np.arange(len(df_))

    # df_["i"]


    # In[12]:


    local_min_idx = argrelextrema(df_.values, np.less, order = min_local_range, mode = "wrap")[0]
    local_max_idx = argrelextrema(df_.values, np.greater, order = min_local_range, mode = "wrap")[0]

    # print(local_min_idx)
    # print(local_max_idx)


    # In[13]:


    local_min_idx = np.array(local_min_idx)
    local_max_idx = np.array(local_max_idx)

    # print(local_min_idx)
    # print(local_max_idx)


    # In[14]:


    local_min=[]
    local_max=[]

    for loc in local_min_idx:
        # print(loc)
        local_min.append(df_.Low[loc])
        
    for loc in local_max_idx:
        # print(loc)
        local_max.append(df_.High[loc])
        
    local_min = np.array(local_min)
    local_max = np.array(local_max)
        
    df_["local_min"] = 0
    df_["local_max"] = 0

    df_.loc[ df_["i"].isin(local_min_idx), "local_min"] = 1
    df_.loc[ df_["i"].isin(local_max_idx), "local_max"] = 1


    # 

    # In[29]:


    dt_start = datetime(2020, 5, 3, 9, 52)
    dt_end = datetime(2022, 4, 13, 18, 15)

    df_2 = df_[(df_.index >= dt_start) & (df_.index <= dt_end)].copy()

    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
        vertical_spacing=0.03,
        subplot_titles=(stock+' OHLC', intervals[1]),
        row_width=[0.2, 0.7])

    fig.add_trace(go.Candlestick(
        x=df_2.index, 
        open=df_2['Open'], 
        high=df_2['High'], 
        low=df_2['Low'], 
        close=df_2['Close']), 
                row=1, 
                col=1)

    fig.add_trace(
        go.Scatter(
            x=df_2[df_2["local_min"] == 1].index,
            y=df_2[df_2["local_min"] == 1]["Low"],
            mode="markers",
            marker_color="cyan",
            marker_symbol="x",
            marker_size=10,
            opacity=0.5
    )
    ,row=1, col=1)


    fig.update_layout(
        template="plotly_dark", 
        xaxis_rangeslider_visible=False,
        height=700
    )

    # fig.show()


    # 

    # In[16]:


    vol_window_size = 100
    step_v = 3
    window_stoch = 25


    # In[17]:


    df_["roll_vol"]      = df_["Volume"].rolling(window=3).sum()# acção em janela passada definida em parametro
    df_["roll_vol_mean"] = df_["roll_vol"].rolling(window=vol_window_size).mean()
    df_["roll_vol_std"]  = df_["roll_vol_mean"].rolling(window=vol_window_size).std()

    # print(df_["roll_vol"] )
    # print(df_["roll_vol_mean"])
    # print(df_["roll_vol_std"])


    # 

    # In[18]:


    df_["last_min_price"] = np.nan
    df_.loc[df_["local_min"] == 1, "last_min_price"] =  df_.loc[df_["local_min"] == 1,"Low"]
    df_["last_min_price"] = df_["last_min_price"].ffill()

    # df_
    df_["rol_min"] = df_["Low"].rolling(window=vol_window_size).min() #minima de volume de janela definida em parametro
    df_["s_rol_min"] = df_["Low"].rolling(window=window_stoch).min() #minima estocastica de valor de janela definida em parametro
    df_["s_rol_max"] = df_["High"].rolling(window=window_stoch).max()#maxima estocastica de valor de janela definida em parametro
    #
    df_["stoch"] = (df_["Close"] - df_["s_rol_min"]) / (df_["s_rol_max"] - df_["s_rol_min"])#definição de estocastico
    df_["candle_side"] = np.sign(df_["Close"] - df_["Open"])#define a opeção
    # df_


    # 

    # In[19]:


    ppvi_bool = df_["local_min"] == 1


    up_d1 = (df_["Close"] < df_["Close"].shift(step_v)) & (df_["Close"].shift(step_v) < df_["Close"].shift(step_v * 2)) & (df_["Close"].shift(2 * step_v) < df_["Close"].shift(step_v * 3))
    up_d2 = (df_["Close"] < df_["Close"].shift(step_v-1)) & (df_["Close"].shift(step_v-1) < df_["Close"].shift(step_v * 2 - 1)) & (df_["Close"].shift(2 * step_v - 1) < df_["Close"].shift(step_v * 3 - 1))
    ppvi_bool = (up_d1 | up_d2) & (ppvi_bool)


    up_p1 = (df_["Close"] < df_["Close"].shift(-step_v)) & (df_["Close"].shift(-step_v) < df_["Close"].shift(-step_v * 2)) & (df_["Close"].shift(-2*step_v) < df_["Close"].shift(-step_v * 3))
    up_p2 = (df_["Close"] < df_["Close"].shift(-step_v+1)) & (df_["Close"].shift(-step_v+1) < df_["Close"].shift(-step_v * 2 + 1)) & (df_["Close"].shift(-2*step_v + 1) < df_["Close"].shift(-step_v * 3 + 1))
    ppvi_bool = (up_p1 | up_p2) & (ppvi_bool)


    ppvi_bool = (df_["rol_min"] == df_["last_min_price"]) & (ppvi_bool)


    ppvi_bool = (df_["roll_vol"] > df_["roll_vol_mean"] + 2 * df_["roll_vol_std"]) & (ppvi_bool)

    df_["v_pattern"] = 0
    df_.loc[ppvi_bool, "v_pattern"] = 1


    # 

    # In[20]:


    df_["v_pattern_near"] = df_["v_pattern"].rolling(window=window_stoch).sum() - df_["v_pattern"].rolling(window=step_v*3 + 1).sum()
    df_["ppvi"] = (df_["v_pattern_near"] >= 1) & (df_["stoch"] > 0.1) & (df_["stoch"] < 0.3) & (df_["Close"] > df_["last_min_price"]) & (df_["candle_side"] == -1)

    df_["rolling_ppvi"] = df_["ppvi"].rolling(window=window_stoch).sum()
    df_.loc[(df_["rolling_ppvi"] > 1) & (df_["ppvi"] == 1), "ppvi"] = 0

    df_["ret_n"] = df_["Close"].shift(-5) - df_["Close"]
    df_[df_["ppvi"] == 1]["ret_n"].mean()
    

    # 

    # In[21]:


    print("Contagem de ocorrências: ", df_[df_["ppvi"] == 1]["ret_n"].count())


    # In[ ]:





    # In[22]:


    # print("Media de retornos: ", df_[df_["ppvi"] == 1]["ret_n"].mean())
    # print("STD de retornos: ", df_[df_["ppvi"] == 1]["ret_n"].std())
    # sns.histplot(df_[df_["ppvi"] == 1]["ret_n"], bins=15)
    df_result[stock] = { 
        "ppvi_ret_n_std" : df_[df_["ppvi"] == 1]["ret_n"].std(),
         "ppvi_ret_n_mean" : df_[df_["ppvi"] == 1]["ret_n"].mean()
         }
    

print("DF RESULT ", df_result)
