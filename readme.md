# Backtesting Investment Algorithm Strategies
It's very important that before you deploy your algorithmic strategies, that you first test them on the real world. Now back testing in a nutshell is nothing but testing your strategy by applying the rules and trading strategies on historical market data to see how it would faire up in the real world stock market.

Now when assessing the performance of your strategy, you must factor in two things:
<br>
• **Slippage** 
<br>
• **Brokerage Commission Costs**
<br><br>
Now Backtesting is very critical in assessing the merit of a trading strategy / system. Therefore don't deploy a strategy in the live stock market until it's backtested.

However a criticism to backtesting is the fact that it tests it's performance on historical data, therefore it has little predictive power.

There are 4 strategies which are used to backtest your investment strategies, these are as follows.

## Monthly Portfolio Rebalancing 
To use htis strategy, first pick any universe of stocks (Large cap, mid cap, small cap, industry specific, factor specific, etc). Stick to this group of stock as the source for your portfolio for the entire duration of backtesting. 

Now build a portfolio with m number of stocks, based on their monthly returns, and pick the top m number of stocks based on monthly returns. So now you would want to pick the top **n** number of stocks based on monthly returns.

Rebalance the portfolio every month by removing the worse **x** stocks and replacing them with the top **x** stocks from the universe of stocks. 
 



## Resistance Breakout


## Renko & OBV

## Renko * MACD


