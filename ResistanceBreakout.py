import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from alpha_vantage.timeseries import TimeSeries
import time
import datetime as dt
from yahoofinancials import YahooFinancials
from alpha_vantage.timeseries import TimeSeries

def ATR(dataFrame , n):
    """Function to calculate True Range and Average True Range"""
    dataFrame['H-L'] = abs(dataFrame["High"] - dataFrame["Low"])
    dataFrame['H-PC'] = abs(dataFrame['High'] - dataFrame['Close'].shift(1))
    dataFrame['L-PC'] = abs(dataFrame['Low'] - dataFrame['Close'].shift(1))

    dataFrame['TR'] = dataFrame[['H-L' , 'H-PC' , 'L-PC']].max(axis=1, skipna = False)
    dataFrame['ATR'] = dataFrame['TR'].rolling(n).mean()

    dataFrame2 = dataFrame.drop(['H-L' , 'H-PC' , 'L-PC'], axis = 1)
    return dataFrame2['ATR']


def CAGR(dataFrame):
    """Function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
    dataFrame["cum_return"] = (1 + dataFrame["ret"]).cumprod()
    n = len(dataFrame) / (252*78)
    CAGR = (dataFrame["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR


def volatility(dataFrame):
    """Function to calculate the annualized volatility of a trading strategy"""
    vol = dataFrame["ret"].std() * np.sqrt(252 * 78)
    return vol


def sharpe (dataFrame , riskFreeRate):
    """Function to calculate sharpe ratio"""
    sharpeRatio = (CAGR(dataFrame) - riskFreeRate) / volatility(dataFrame)
    return sharpeRatio


def maxDrawdown(dataFrame):
    """Function to calculate max drawdown"""
    dataFrame["cum_return"] = (1 + dataFrame["ret"]).cumprod()
    dataFrame["cum_roll_max"] = dataFrame["cum_return"].cummax()
    dataFrame["drawdown"] = dataFrame["cum_roll_max"] - dataFrame["cum_return"]
    dataFrame["drawdown_pct"] = dataFrame["drawdown"] / dataFrame["cum_roll_max"]
    maxDrawdown = dataFrame["drawdown_pct"].max()
    return maxDrawdown


tickers = ["MSFT","AAPL","FB","AMZN","INTC","CSCO","VZ","IBM","TSLA","AMD"]
keyPath = "W2MX37GBZUSOEWVF"
ts = TimeSeries(key=keyPath, output_format='pandas')

stockDataIntraday = {}
apiCallCount = 1

start_time = time.time()
for ticker in tickers:
    data = ts.get_intraday(symbol=ticker , interval='15min', outputsize='full')[0]
    apiCallCount += 1
    data.columns = ["Open","High","Low","Close","Volume"]
    data = data.iloc[::-1]
    stockDataIntraday[ticker] = data

    if (apiCallCount == 5):
        apiCallCount = 1
        time.sleep(60 - ((time.time() - start_time) % 60.0))
        print("Waiting")


# Gets all the tickers of the market
tickers = stockDataIntraday.keys()

# Calculate the ATR and rolling max price for each stock and consolidating this info
tickers_signal = {}
tickers_ret = {}

print(stockDataIntraday)
for ticker in tickers:
    print("Calculating the ATR and rolling max price for ", ticker)
    stockDataIntraday[ticker]["ATR"] = ATR(stockDataIntraday[ticker] , 20)
    stockDataIntraday[ticker]["roll_max_cp"] = stockDataIntraday[ticker]["High"].rolling(20).max()
    stockDataIntraday[ticker]["roll_min_cp"] = stockDataIntraday[ticker]["Low"].rolling(20).min()
    stockDataIntraday[ticker]["roll_max_vol"] = stockDataIntraday[ticker]["Volume"].rolling(20).max()
    stockDataIntraday[ticker].dropna(inplace=True)
    tickers_signal[ticker] = ""
    tickers_ret[ticker] = []


# Identifying signals and calculating return (with stoploss factored in)
for ticker in tickers:
    print("calculating returns for ",ticker)
    for i in range(len(stockDataIntraday[ticker])):
        if tickers_signal[ticker] == "":
            tickers_ret[ticker].append(0)
            if (stockDataIntraday[ticker]["High"][i] >= stockDataIntraday[ticker]["roll_max_cp"][i] and
                stockDataIntraday[ticker]["Volume"][i] > 1.5 * stockDataIntraday[ticker]["roll_max_vol"][i-1]):

                tickers_signal[ticker] = "Buy"

            elif (stockDataIntraday[ticker]["Low"][i] <= stockDataIntraday[ticker]["roll_min_cp"][i] and
                  stockDataIntraday[ticker]["Volume"][i] > 1.5 * stockDataIntraday[ticker]["roll_max_vol"][i-1]):

                tickers_signal[ticker] = "Sell"


        elif tickers_signal[ticker] == "Buy":
            if (stockDataIntraday[ticker]["Low"][i] < stockDataIntraday[ticker]["Close"][i-1] - stockDataIntraday[ticker]["ATR"][i-1]):
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i-1] - stockDataIntraday[ticker]["ATR"][i-1])/ stockDataIntraday[ticker]["Close"][i-1] - 1)

            elif stockDataIntraday[ticker]["Low"][i] <= stockDataIntraday[ticker]["roll_min_cp"][i] and stockDataIntraday[ticker]["Volume"][i] > 1.5 * stockDataIntraday[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Sell"
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i] / stockDataIntraday[ticker]["Close"][i - 1]) - 1)
            else:
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i] / stockDataIntraday[ticker]["Close"][i - 1]) - 1)

        elif tickers_signal[ticker] == "Sell":
            if stockDataIntraday[ticker]["High"][i] > stockDataIntraday[ticker]["Close"][i - 1] + stockDataIntraday[ticker]["ATR"][i - 1]:
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i - 1] / (
                            stockDataIntraday[ticker]["Close"][i - 1] + stockDataIntraday[ticker]["ATR"][i - 1])) - 1)
            elif stockDataIntraday[ticker]["High"][i] >= stockDataIntraday[ticker]["roll_max_cp"][i] and \
                    stockDataIntraday[ticker]["Volume"][i] > 1.5 * stockDataIntraday[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Buy"
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i - 1] / stockDataIntraday[ticker]["Close"][i]) - 1)
            else:
                tickers_ret[ticker].append((stockDataIntraday[ticker]["Close"][i - 1] / stockDataIntraday[ticker]["Close"][i]) - 1)


    stockDataIntraday[ticker]["ret"] = np.array(tickers_ret[ticker])


# calculating overall strategy's KPIs
strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = stockDataIntraday[ticker]["ret"]
strategy_df["ret"] = strategy_df.mean(axis=1)

CAGR(strategy_df)
sharpe(strategy_df,0.025)
maxDrawdown(strategy_df)

# vizualization of strategy return
(1+strategy_df["ret"]).cumprod().plot()
plt.show()



