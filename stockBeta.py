import pandas as pd
import numpy as np
import yfinance as yf

#Params:
#Stock: A stock ticker, e.g. "MSFT"
#Market: A index or ETF to use as  benchmark, e.g. "SPY"
def beta(stock, market):
    s = getHistory(stock)
    m = getHistory(market)
    begin = max(s.loc[0, 'Date'], m.loc[0, 'Date'])
    stock_df = getDailyChange(s, begin)
    market_df = getDailyChange(m, begin)
    dstock = stock_df['Change'].values
    dmarket = market_df['Change'].values
    return np.cov(dstock, dmarket)[0][1]/np.var(dmarket)

def getHistory(ticker):
    ticker = yf.Ticker(ticker)
    ticker_data = ticker.history(period="max")
    ticker_data.reset_index(level=0, inplace=True)
    t = ticker_data.loc[:, ['Date', 'Close']]
    return t

def getDailyChange(a, start):
    a = a[a['Date'] >= start]
    a['Change'] = a['Close'].pct_change()
    a.reset_index(drop=True, inplace=True)
    a.drop([0], inplace=True)
    return a
