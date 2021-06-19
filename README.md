# Financial Dashboard Application

This repository demonstrates how to create a financial dashboard with Python’s [Streamlit](https://streamlit.io/) and deploy it to the [Heroku](https://www.heroku.com/) cloud platform. 

- Access the application: [<img src='https://upload.wikimedia.org/wikipedia/commons/e/ec/Heroku_logo.svg' width="100" align="center">](https://financial-dashboard-ko.herokuapp.com/)
- See the application in action: [<img src='https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg' width="40" align="center">](https://www.youtube.com/)
- View the app as a notebook: [<img src='https://cdn.freelogovectors.net/wp-content/uploads/2018/06/kaggle-logo.png' width="70" align="center">](https://www.kaggle.com/korfanakis/stock-technical-indicators-for-tesla-macd-rsi)

<br>

## The Dashboard

The dashboard application calculates and (interactively) displays stock price information and indicators. Specifically, it plots:

- A candlestick chart for the stock's price, along with the 12- and 26-period exponential moving average,
- The MACD indicator, along with its signal line,
- The Relative Strength Index (RSI) indicator, and finally,
- The trading volume.

It also includes a trading strategy based on the MACD indicator and its signal line.

<br>

:exclamation::exclamation::exclamation:**Disclaimer**:exclamation::exclamation::exclamation:: Any information provided in this project is for educational purposes only. It is **not** intended as financial or investment advice and should not be construed or relied on as such.

## Dataset

For retrieving the dataset, we will use [yfinance](https://pypi.org/project/yfinance/), which offers a reliable, threaded, and Pythonic way to download historical market data from [Yahoo! finance](https://finance.yahoo.com/). We just need to specify the stock's ticker and the time frame of interest. The extracted dataset contains daily data for the opening, lowest, highest, closing, and [adjusted closing](https://www.investopedia.com/terms/a/adjusted_closing_price.asp) price of the stock, along with its trading volume.

## Files

- **Dashboard_App.py** - The Python script containing the code for the application.
- **Dashboard_Functions.py** – A separate script with all custom functions required for the application.
- **requirements.txt** – A text file that contains all libraries that need to be installed for the app to work.
- **setup.sh** – A shell file that creates a streamlit folder.
- **Procfile** – A simple text file used to first execute the setup.sh and then call streamlit run to run the application.

You can read more 

## Brief Introduction to Technical Indicators

Simply put, technical indicators are visual tools used by investors/traders to help them make investment choices. Technical indicators use historical data to interpret and forecast the future price action of a financial asset [1]. Together, these indicators form the basis of technical analysis [2].

Examples of common technical indicators include the [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp), [Money Flow Index](https://www.investopedia.com/terms/m/mfi.asp), Stochastics, [MACD](https://www.investopedia.com/terms/m/macd.asp), and [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp).

In this notebook, we will only use two indicators:

1) **Moving average convergence divergence** (**MACD**) [3]: The MACD is calculated by subtracting the 26-period [exponential moving average](https://www.investopedia.com/terms/e/ema.asp) (EMA) from the 12-period EMA. <br>The result of that calculation is the **MACD line**. A nine-day EMA of the MACD (called the "**signal line**") is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals. Traders may buy the asset when the MACD crosses above its signal line and sell the asset when the MACD crosses below the signal line.

2) **Relative Strength Index** (**RSI**) [4]: measures the magnitude of recent price changes to evaluate **overbought** or **oversold** conditions in the price of an asset. The RSI is displayed as an oscillator (a line graph that moves between two extreme values) and can have a value from 0 to 100. <br>Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security is becoming overbought or overvalued and may be primed for a trend reversal or corrective pullback in price. An RSI reading of 30 or below indicates an oversold or undervalued condition.

<br>

MACD measures the relationship between two EMAs, while the RSI measures price change in relation to recent price highs and lows. These two indicators are often used together to provide analysts with a more complete technical picture of a market.

Both indicators measure [momentum](https://www.investopedia.com/investing/momentum-and-relative-strength-index/) in a market. However, because they measure different factors, they sometimes give contrary indications [3].

## Trading Strategy

In our case, we will construct our trading strategy based on the MACD indicator and its signal line. Specifically, we will create a 'Buy Signal’ when the MACD crosses above its signal line and a ‘Sell Signal’ when the MACD crosses below the signal line. The two types of signals will be overlayed on the candlestick chart as triangles (specifically, green up-pointing triangles for ‘Buy’ and yellow down-pointing triangles for ‘Sell’).

## Resources

[1]

[2]
