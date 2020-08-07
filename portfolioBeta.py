import stockBeta
from datetime import date, timedelta
from portfolio import holdings, benchmark
import yfinance as yf
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
print("Portfolio Beta:", round(portfolio_beta,2))

col_names = ["Stock", "Shares", today.strftime("%m/%d/%Y") + " Price", "Beta", "Portfolio Weight", "Beta Weight"]
df = pd.DataFrame(columns = col_names)
df["Stock"] = holdings["stocks"]
df["Shares"] = holdings["shares"]
df[today.strftime("%m/%d/%Y") + " Price"] = latest_prices
df["Beta"] = betas
df["Portfolio Weight"] = portfolio_weights
df["Beta Weight"] = beta_weights
print(df)
