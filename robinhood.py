#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 22:41:03 2020

@author: petermark
"""

import robin_stocks as rs
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
import numpy as np
import streamlit as st
from datetime import date, timedelta
import yfinance as yf
import pyotp


st.write(""" # Prerit's Robinhood portfolio""")

# Logging in to robinhood
totp  = pyotp.TOTP("My2factorAppHere").now()
rs.login("prerit.saxena17@gmail.com", "prt01081960", mfa_code=totp)

my_stocks = rs.build_holdings()

df = pd.DataFrame(my_stocks)
df = df.T
df['ticker'] = df.index
df = df.reset_index(drop=True)

# rearranging columns
cols = ['ticker', 'name', 'equity', 'percent_change', 'average_buy_price','price','quantity']
df = df[cols].sort_values(by='ticker', ascending=True).reset_index(drop=True)

cols2 = ['equity', 'percent_change', 'average_buy_price','price','quantity']
df[cols2] = df[cols2].apply(pd.to_numeric) 

st.write("Current portfolio")

st.write("""Total portfolio value = $""",df['equity'].sum(),"""Total profit =$""",(round(df['equity'].sum()-(df['average_buy_price']*df['quantity']).sum())))

st.write(df)

option = st.sidebar.selectbox(
    'Select my stock',
     df['ticker'])

tickerSymbol = option

# get data on this ticker

tickerData = yf.Ticker(tickerSymbol)

Today = date.today().isoformat()   
Last_1_week = (date.today()-timedelta(days=7)).isoformat()

option2 = 'Last 5 years'
dates = pd.DataFrame({
  'Date_sel': ['Last 5 years', 'Last 1 year', 'Last 3 months', 'Last 1 month', 'Last 1 week', 'Today' ]
   })

option2 = st.sidebar.selectbox(
    'Select Time Period',
     dates['Date_sel'])

if option2 == 'Today':
    startdate=date.today().isoformat()
elif option2 =='Last 1 week':
    startdate=(date.today()-timedelta(days=7)).isoformat()
elif option2 == 'Last 1 month':
    startdate=(date.today()-timedelta(days=30)).isoformat()
elif option2 == 'Last 3 months':
    startdate=(date.today()-timedelta(days=90)).isoformat()
elif option2 == 'Last 1 year':
    startdate=(date.today()-timedelta(days=365)).isoformat()
elif option2 == 'Last 5 years':
    startdate=(date.today()-timedelta(days=1825)).isoformat()
# get the historical prices for this ticker

tickerDf = tickerData.history(period = '1d', start=startdate, end=date.today())


# Open High low Close Volume Dividends Stock Splits

'Displaying Trend for: ', tickerSymbol

st.line_chart(tickerDf.Close)

'Name: ', df[df['ticker']==option]['name'].values[0]
'Shares: ', round(df[df['ticker']==option]['quantity']).values[0]
'Average Cost per share: $', round(df[df['ticker']==option]['average_buy_price']).values[0]
'Current Equity: $', round(df[df['ticker']==option]['equity']).values[0]
'Total Return: $', (round(df[df['ticker']==option]['equity'].sum()-(df[df['ticker']==option]['average_buy_price']*df[df['ticker']==option]['quantity']).sum()))

# expander = st.beta_expander("Stock Statistics")
# expander.write('Last Close: ',tickerDf.Close[-1])

st.write("""**About the company:** 
         
         """)

st.write(tickerData.info['longBusinessSummary'])

expander = st.beta_expander("Major holders")
expander.write(tickerData.major_holders)

st.sidebar.write(""" \n \n \n Built by **Prerit Saxena** """)




