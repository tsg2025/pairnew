import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# Function to calculate z-score
def calculate_zscore(series, lookback):
    mean = series.rolling(window=lookback).mean()
    std = series.rolling(window=lookback).std()
    zscore = (series - mean) / std
    return zscore

# Streamlit app
st.title("Pair Trading Backtesting")

# Input boxes
st.sidebar.header("Input Parameters")
symbol1 = st.sidebar.text_input("Enter Stock Symbol 1", "AAPL")
symbol2 = st.sidebar.text_input("Enter Stock Symbol 2", "MSFT")
lookback = st.sidebar.number_input("Lookback Period for Z-Score", min_value=1, value=30)
from_date = st.sidebar.date_input("From Date", datetime(2020, 1, 1))  # User selects start date
to_date = st.sidebar.date_input("To Date", datetime(2023, 1, 1))  # User selects end date

# Go button
if st.sidebar.button("Go"):
    if not symbol1.strip() or not symbol2.strip():
        st.error("Please provide valid stock tickers.")
    elif from_date > to_date:
        st.error("Start date must be before end date.")
    else:
        try:
            with st.spinner('Fetching data...'):
                # Fetch data for symbol1
                stock1 = yf.Ticker(symbol1)
                info1 = stock1.info
                data1 = stock1.history(start=from_date, end=to_date, interval="1d")
                
                # Fetch data for symbol2
                stock2 = yf.Ticker(symbol2)
                info2 = stock2.info
                data2 = stock2.history(start=from_date, end=to_date, interval="1d")
                
                # Check if data is empty
                if data1.empty or data2.empty:
                    st.error(f"Failed to fetch data for {symbol1} or {symbol2}. Please check the ticker symbols and try again.")
                else:
                    # Calculate ratio and z-score
                    data1['Close'] = data1['Close']
                    data2['Close'] = data2['Close']
                    ratio = data1['Close'] / data2['Close']
                    zscore = calculate_zscore(ratio, lookback)
                    
                    # Display results
                    st.subheader("Backtest Results")
                    st.write(f"#### {symbol1} - {info1.get('longName', 'N/A')}")
                    st.write(f"#### {symbol2} - {info2.get('longName', 'N/A')}")
                    
                    st.write("### Z-Score Series")
                    st.line_chart(zscore)
                    
                    st.write("### Stock Prices")
                    st.write(f"#### {symbol1} Close Prices")
                    st.line_chart(data1['Close'])
                    st.write(f"#### {symbol2} Close Prices")
                    st.line_chart(data2['Close'])
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
