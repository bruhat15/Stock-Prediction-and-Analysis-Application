import streamlit as st
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# List of top 6 stock symbols
top_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA']

@st.cache_data
def fetch_data(symbols):
    prices=[]
    try:
        for symbol in top_symbols:
            url = f"https://www.google.com/finance/quote/{symbol}:NSE"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser') 
            class_name = "YMlKec fxKbKc"  # Update this as needed
        
    # Find the price element
            price_element = soup.find(class_=class_name)
            if price_element:
                price = float(price_element.text.strip()[1:].replace(",", ""))
                prices.append(price)
    except Exception as e:
        print("not done")
    
    return prices,{symbol: yf.Ticker(symbol).history(period='1d', interval='1m') for symbol in symbols}

def display_data(data):
    return pd.concat([df['Close'].rename(symbol) for symbol, df in data.items()], axis=1)

def create_candlestick_chart(symbol, data):
    return go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )]).update_layout(
        title=f'Candlestick chart for {symbol}',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

def apply_custom_css():
    st.markdown("""
        <style>
            /* General Layout */
            .css-1v0mbdj.e16nr0p30 {
                background-color: #2e2e2e; /* Sidebar background color */
            }
            .css-1g5h1lc.e16nr0p30 {
                background-color: #121212; /* Main area background color */
                color: #e0e0e0; /* Text color */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Modern font */
            }
            .css-1a0rprc {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .css-1d391sg, .css-1r44ud2 {
                color: #f5a623; /* Highlight color for text and borders */
            }
            .css-1r44ud2 {
                border-radius: 10px; /* Rounded corners for containers */
                border: 1px solid #333; /* Border for containers */
                padding: 20px; /* Padding for containers */
                box-shadow: 0 10px 20px rgba(0,0,0,0.3); /* Enhanced box shadow */
                margin-bottom: 20px; /* Margin at the bottom of containers */
                background: linear-gradient(145deg, #2d2d2d, #1e1e1e); /* Gradient background */
            }
            .css-18e3g6s {
                border: 1px solid #444; /* Border for input elements */
                border-radius: 8px; /* Rounded corners for input elements */
                padding: 12px; /* Padding for input elements */
                background: #1f1f1f; /* Dark background for inputs */
            }
            .stMarkdown {
                margin: 20px 0; /* Margin for spacing */
                font-size: 1.1em; /* Increase font size for readability */
            }
            .stButton, .stSelectbox, .stRadio, .stTextInput {
                border-radius: 8px; /* Rounded corners for interactive elements */
                padding: 12px; /* Padding for interactive elements */
                border: 1px solid #333; /* Border for interactive elements */
                background-color: #1e1e1e; /* Background color for buttons and selects */
                color: #e0e0e0; /* Text color for buttons and selects */
                transition: background-color 0.3s, box-shadow 0.3s; /* Smooth transition */
            }
            .stButton:hover, .stSelectbox:hover, .stRadio:hover, .stTextInput:hover {
                background-color: #333; /* Darker background on hover */
                box-shadow: 0 5px 10px rgba(0,0,0,0.2); /* Shadow on hover */
            }
            .stPlotlyChart {
                margin: 20px 0; /* Margin for Plotly charts */
                border-radius: 10px; /* Rounded corners for charts */
                box-shadow: 0 10px 20px rgba(0,0,0,0.2); /* Box shadow for charts */
                background: #2c2c2c; /* Background color for charts */
            }
            .stPlotlyChart .plotly-graph-div {
                border-radius: 10px; /* Rounded corners for graph div */
            }
        </style>
    """, unsafe_allow_html=True)
def get_stock_symbol_image(symbol):
    images = {
        'AAPL': 'https://tse1.mm.bing.net/th?id=OIP.AVRK365_ripQHCNly-Ky1AHaHa&pid=Api&P=0&h=180',  # Replace with actual image URL
        'MSFT': 'https://tse1.mm.bing.net/th?id=OIP.w6wIB2kz6BXvOVV_ibR_mwHaG8&pid=Api&P=0&h=180',
        'GOOGL': 'https://tse3.mm.bing.net/th?id=OIP.he3C2c9-ei_V2pAD14yDNgHaE-&pid=Api&P=0&h=180',
        'AMZN': 'https://tse1.mm.bing.net/th?id=OIP.9Wmfe4ghqGMyNFuxE9DbEAHaHa&pid=Api&P=0&h=180',
        'META': 'https://tse2.mm.bing.net/th?id=OIP.pMov_smywtVsK-ITbeSDGwHaHa&pid=Api&P=0&h=180',
        'TSLA': 'https://tse1.mm.bing.net/th?id=OIP.zf8g1tolI3HRPumaeETgcAHaEK&pid=Api&P=0&h=180'
    }
    return images.get(symbol, '')

def display_stock_info(datas,prices):
    for i in range(0, len(top_symbols), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(top_symbols):
                symbol = top_symbols[i + j]
                img_url = get_stock_symbol_image(symbol)
                with cols[j]:
                    st.image(img_url, width=50, caption=symbol)
                    latest_price = datas[symbol]['Close'].iloc[-1] if not datas[symbol]['Close'].empty else 'No data'
                    st.write(f"{symbol}: ${latest_price:.2f}" if isinstance(latest_price, (int, float)) else latest_price)

def dashboard_content(placeholder_1,placeholder_2):
    apply_custom_css()  # Apply custom CSS

    st.title('Stock Dashboard')

    with st.sidebar:
        placeholder_1 = st.selectbox('Select Chart Type for Combined Data', ['Scatter', 'Area', 'Candlestick'])
        placeholder_2 = st.selectbox('Select Stock Symbol for Detailed View', top_symbols + ['None'])
        chart_type=placeholder_1
        selected_symbol=placeholder_2
    prices,datas = fetch_data(top_symbols)
    
    if datas:
        st.subheader("Latest Closing Prices")
        display_stock_info(datas,prices)
        
        total_graph_data = display_data(datas)
        min_close, max_close = total_graph_data.min().min(), total_graph_data.max().max()

        with st.empty():
            if chart_type == 'Scatter':
                st.write(f"{chart_type} depicts the common nearest prices of data.")
                scatter_plot = px.scatter(
                    total_graph_data,
                    title="Combined Stock Prices Scatter Plot",
                    labels={'value': 'Closing Price', 'index': 'Time'},
                    height=600,
                    width=1200
                )
                st.plotly_chart(scatter_plot, use_container_width=True)

            elif chart_type == 'Area':
                st.write(f"{chart_type} depicts the overlying of data.")
                area_plot = px.area(
                    total_graph_data,
                    title="Combined Stock Prices Area Chart",
                    labels={'value': 'Closing Price', 'index': 'Time'},
                    height=600,
                    width=1200
                ).update_yaxes(range=[min_close, max_close]).update_traces(opacity=0.7)
                st.plotly_chart(area_plot, use_container_width=True)

            elif chart_type == 'Candlestick':
                st.write(f"{chart_type} depicts the detailing of data.")
                for symbol in top_symbols:
                    st.plotly_chart(create_candlestick_chart(symbol, datas[symbol]), use_container_width=True)

        if selected_symbol != 'None':
            st.subheader(f'Individual Candlestick Chart for {selected_symbol}')
            st.plotly_chart(create_candlestick_chart(selected_symbol, datas[selected_symbol]), use_container_width=True)
    else:
        st.write("Waiting for market open at 9:30 AM or no data available.")

if __name__ == "__main__":
    dashboard_content()
