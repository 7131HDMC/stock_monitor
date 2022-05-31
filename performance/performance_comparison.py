import pandas as pd
import investpy as ip
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

countries = ['brazil', 'united states']#n countries
intervals = ['Daily','Weekly','Monthly']

end_date   = datetime.today()
start_date = end_date - timedelta(days=7)

@st.cache
def get_stock(stock, country, from_date, to_date, interval):
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)
def stocks_list(country_select):
    return ip.get_stocks_list(country=country_select)

def get_stocks(stocks, country, from_date, to_date, interval):
    df_arr = []
    for stock in stocks:
        df_arr.append({
            "name": stock,
            "data" : ip.get_stock_historical_data(
                stock=stock,
                country=country,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
        })
    return df_arr

def format_date(dt, format='%d/%m/%Y'):
  return dt.strftime(format)

def plot_candlestick(df,stock='ticket'):
  trace1 = {
      'x':df.index,
      'open': df.Open,
      'close': df.Close,
      'high': df.High,
      'low': df.Low,
      'type': 'candlestick',
      'name': stock,
      'showlegend': True
  }

  return trace1#go.Figure(data= [trace1] ,layout = go.Layout() )


def relative_ret(df):
    rel = df.pct_change()
    cum = ( 1 + rel ).cumprod() -1
    return cum.fillna(0)

def show_relative_return():
    fig = make_subplots(
            rows=2, 
            cols=1, 
            specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
            vertical_spacing=0.133,
            subplot_titles=('Retorno relativo ', ''),
            row_width=[0.2, 0.7],
    )

    for stock_ in stocks:
        fig.add_trace( 
            go.Scatter( 
                x= stock_['data'].index, 
                y= relative_ret( stock_['data'].Close ),
                mode="lines",
                name= stock_['name'] 
            )
        )

        # st.dataframe(stock_['data'])
        # print(stock_['data'].index)

    fig.update_layout(
        template="plotly_dark", 
    )

    st.plotly_chart(fig)

def show_close_price():
    fig = make_subplots(
            rows=2, 
            cols=1, 
            specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
            vertical_spacing=0.133,
            subplot_titles=('Close Price ', ''),
            row_width=[0.2, 0.7],
    )

    for stock_ in stocks:
        fig.add_trace( 
            go.Candlestick( 
                plot_candlestick(stock_['data'], stock_['name'])
            )
        )

    fig.update_layout(
        template="plotly_dark", 
    )

    st.plotly_chart(fig)

st.title('Monitor Financeiro')

sidebar = st.sidebar.empty()

country_select = st.sidebar.selectbox("Selecione o país:", countries)

stocks = stocks_list(country_select)

dropdown = st.sidebar.multiselect("Selecione os ativos: ", stocks)

show_relative_ret = st.sidebar.checkbox('Relative Return')
show_closeprice = st.sidebar.checkbox('Preço de fechamento')

from_date = st.sidebar.date_input("Inicio: ", start_date)
to_date   = st.sidebar.date_input("Fim: ", end_date)

interval_select = st.sidebar.selectbox("Selecione o intervalo:",intervals)

if from_date > to_date:
    st.sidebar.error("Data de ínicio maior que a data final! ")
elif (len(dropdown) > 4):
    st.sidebar.error("Selecione 4 ou menos ativos para comparar! ")
else: 
    try:
        stocks = get_stocks(
                    dropdown, 
                    country_select, 
                    format_date(from_date), 
                    format_date(to_date), 
                    interval_select
                )

        if show_relative_ret:
            show_relative_return()

        if show_closeprice:
            show_close_price()
    except Exception as e:
        st.error(e)

        

