import stockBeta
from datetime import date, timedelta
from portfolio import holdings, benchmark
import yfinance as yf
# import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# port = zip(holdings["stocks"], holdings["shares"])
today = date.today() - timedelta(days=1)
latest_prices, values, betas, portfolio_weights, beta_weights = ([] for i in range(5))
n = len(holdings["stocks"])

for i in range(n):
    s = holdings["stocks"][i]
    latest_prices.append(yf.Ticker(s).history(period="1d", start=today-timedelta(days=1), end=today)['Close'].values[0])
    values.append(holdings["shares"][i]*latest_prices[i])

portfolio_val = sum(values)
for i in range(n):
    portfolio_weights.append(values[i] / portfolio_val)
    betas.append(stockBeta.beta(holdings["stocks"][i], benchmark))
    beta_weights.append(betas[i]*portfolio_weights[i])

portfolio_beta = sum(beta_weights)
print(portfolio_beta)
