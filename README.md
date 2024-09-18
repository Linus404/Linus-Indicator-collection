# Todo
- make readme pretty
- fix MoldyHighlights text and lookback period


# Overview
## TradingView
- Linus-Sammlung:
  - Multiple EMAs
  - VWAP
  - HLC of previous day
  - ATR bands
  - More to come
- MoldyMoves (client request):
  - Highlights consecutive candles and big wicks in those moves
  - Arrows for better visibility
 
## NinjaTrader
- MoldyBars:
  - Custom candle stick bars for inside bars, outside bars, Außenstäbe and default bars
- MoldyBars_clean:
  - removed arrows for cleaner look and better performance
- MoldyHighlights:
  - Marks important levels on the chart such as Overnight High/Low, Prior Settlement, Daily High/Low, etc.
 
## Python
- get_bias:
  - Takes yfinance tickers as input
  - Prints Hurst exponent
  - Prints ADF test
  - Prints short-term direction based on the mean of recent returns
  - Prints volatility level
  - Prints recent returns and recent volatility 

## Further information
This [repo](www.github.com/trading-code/ninjatrader-freeorderflow) has the nt8 Order Flow indicators for free and open source

I will not be working on NinjaTrader indicators anymore.  
As far as I know, it's currently not possible to make a good volume profile in Pinescript. If you know otherwise please let me know!
