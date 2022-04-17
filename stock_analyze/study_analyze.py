""" 
#IMport libraries
"""
import numpy as np
import pandas as pd
import investpy as ip
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

import seaborn as sns
from scipy.signal import argrelextrema

"""# Define intervals and countries"""
countries = ['brazil', 'united states']#n countries
intervals = ['Daily','Weekly','Monthly']

def search_stocks(stock, country, from_date, to_date, interval):
    print("stock =>",stock)
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)

aapl = search_stocks("AAPL", countries[1], '13/04/2020', '13/04/2022', intervals[0])

print("Head :: ",aapl.head())
print("Tail :: ",aapl.tail())

print("Describe :: ",aapl.describe())