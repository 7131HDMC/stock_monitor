
import pandas as pd
import investpy as ip
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime, timedelta

countries = ['brazil', 'united states']#n countries
intervals = ['Daily','Weekly','Monthly']

end_date   = datetime.today()
start_date = end_date - timedelta(days=7)

@st.cache
def search_stocks(stock, country, from_date, to_date, interval):
    return ip.get_stock_historical_data(stock=stock,
                                  country=country,
                                  from_date=from_date,
                                  to_date=to_date,
                                  interval=interval)

def format_date(dt, format='%d/%m/%Y'):
  return dt.strftime(format)

def plot_candlestick(df,acao='ticket'):
  trace1 = {
      'x':df.index,
      'open': df.Open,
      'close': df.Close,
      'high': df.High,
      'low': df.Low,
      'type': 'candlestick',
      'name': acao,
      'showlegend': True
  }

  return go.Figure(data= [trace1] ,layout = go.Layout() )

sidebar = st.sidebar.empty()

country_select = st.sidebar.selectbox("Selecione o país:", countries)

stocks = ip.get_stocks_list(country=country_select)

stock_select = st.sidebar.selectbox("Selecione o ativo:", stocks)

from_date = st.sidebar.date_input("De: ", start_date)
to_date   = st.sidebar.date_input("Para: ", end_date)

interval_select = st.sidebar.selectbox("Selecione o intervalo:",intervals)

load_data = st.sidebar.checkbox('Carregar Dados')


st.title("Monitor de Ação")
st.subheader("Visualização gráfica")

# candle_graph, line_graph = st.columns(2)
candle_graph = st.empty()
line_graph = st.empty()
if from_date > to_date:
    st.sidebar.error("Data de ínicio maior que a data final")
else:
    df = search_stocks(stock_select, country_select, format_date(from_date), format_date(to_date), interval_select)
    try:
        fig = plot_candlestick(df)
        candle_graph.plotly_chart(fig)
        line_graph.line_chart(df.Close)
        
        if load_data:
            st.subheader('Dados')
            dados = st.dataframe(df)
    except Exception as e:
        st.error(e)





