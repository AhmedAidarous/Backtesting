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
Resistance breakout is a technical trading term which means that the price of the stock has breached a 
presumed resistance level (determined by the price chart)

When using this strategy, always go for high volume, high activity stock, so you would want to go for pre-market movers, or historically high volume stocks)

For this strategy, I used price breaching 20 period rolling max/min price in conjunction with volume breaching rolling max volume, in definition though, **the breakout rule** 
by definition refers to when the price of an asset moves above a resistance area, or moves below a support area. Breakouts indicate the potential for the price to start trending in the breakout direction.

I will also be using exit/stop loss signals, as it's very important as it caps your losses. The exit signal will be using a 20 period ATR as the rolling stop loss price.

Backtest the strategy by calculating the cumulative return for each stock.



## Renko & OBV
Renko is a good way to look at the stock market, and identify trends that occur. The following is an example of what a Renko graph looks like:
![image](https://user-images.githubusercontent.com/47617364/130065320-df7a4147-a226-4f81-8951-e507dfe8a58c.png)
<br>

This backtesting strategy should be used in stocks that have high volume, and high activity.

### Buy Signal
For this strategy, if the renko bar is >= 2, meaning if the **green bars go up by two steps** and at the same time if the 5 day OBV slope is greater than 30 degrees, **then that's the signal to buy!** Else if the renko bar is less than 2, then **exit.**

### Sell Signal
If the Renko bar is <= -2, and at the same instant, there is a 5 day OBV slope that is less than -30 degrees, then exit. 




## Renko * MACD


