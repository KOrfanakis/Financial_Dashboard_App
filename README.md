# Financial Dashboard App

## Objective

This repository demonstrates how to create a financial dashboard with Python’s Streamlit and deploy it to the Heroku cloud platform. 

## The Dashboard

The dashboard application calculates and (interactively) displayes stock price information and indicators. Specifically, it plots:

- A candlestick chart for the stock's price, along with the 12- and 26-period exponential moving average,
- The MACD indicator, along with its signal line,
- The Relative Strength Index (RSI) indicator, and finally,
- The trading volume.

It also includes a trading strategy based on the MACD indicator and its signal line.

## Disclaimer:exclamation:

Any information provided in this project is for educational purposes only. It is **not** intended as financial or investment advice and should not be construed or relied on as such.

## Tools





## Brief Introduction to Technical Indicators



## The Strategy

In our case, we will construct our trading strategy based on the MACD indicator and its signal line. Specifically, we will create a 'Buy Signal’ when the MACD crosses above its signal line and a ‘Sell Signal’ when the MACD crosses below the signal line. The two types of signals will be overlayed on the candlestick chart as triangles (specifically, green up-pointing triangles for ‘Buy’ and yellow down-pointing triangles for ‘Sell’).

## The Dataset

For retrieving the dataset, we will use [yfinance](https://pypi.org/project/yfinance/), which offers a reliable, threaded, and Pythonic way to download historical market data from [Yahoo! finance](https://finance.yahoo.com/). We just need to specify the stock's ticker and the time frame of interest. The extracted dataset contains daily data for the opening, lowest, highest, closing, and [adjusted closing](https://www.investopedia.com/terms/a/adjusted_closing_price.asp) price of the stock, along with its trading volume.
