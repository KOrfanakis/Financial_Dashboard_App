<p align="center">
  <img src="Images/Repo_title.svg" width="700" title="hover text">
</p>
<p align="center">
  This repository demonstrates how to create a financial dashboard with Python’s <a href="https://streamlit.io/">Streamlit</a> and deploy it to the <a href="https://www.heroku.com/">Heroku</a> cloud platform. 
  <br>
</p>

--- 

- Access the application: [<img src='https://upload.wikimedia.org/wikipedia/commons/e/ec/Heroku_logo.svg' width="100" align="center">](https://financial-dashboard-ko.herokuapp.com/)
- See the application in action: [<img src='https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg' width="40" align="center">](https://youtu.be/kG7MtRgYHgU)
- View the app as a notebook: [<img src='https://upload.wikimedia.org/wikipedia/commons/7/7c/Kaggle_logo.png' width="70" align="center">](https://www.kaggle.com/korfanakis/stock-technical-indicators-for-tesla-macd-rsi)

<br>

**Table of Contents**

<!--ts-->
1. [The Dashboard](#the-dashboard)
2. [Dataset](#dataset)
3. [Files](#files)
4. [Brief Introduction to Technical Indicators](#brief-introduction-to-technical-indicators)
5. [Trading Strategy](#trading-strategy)
6. [References](#references)
7. [Feedback](#feedback)
<!--te-->

<br>

## The Dashboard

The dashboard application calculates and (interactively) displays stock price information and indicators. Specifically, it plots:

- A candlestick chart for the stock's price, along with the 12- and 26-period exponential moving average,
- The MACD indicator, along with its signal line,
- The Relative Strength Index (RSI) indicator, and finally,
- The trading volume.

It also includes a trading strategy based on the MACD indicator and its signal line. This project is **not** a tutorial on finance terms and concepts; however, I have included a section titled ‘[Brief Introduction to Technical Indicators](brief-introduction-to-technical-indicators)’ that introduces some of these topics.

<br>

:exclamation::exclamation::exclamation:**Disclaimer**:exclamation::exclamation::exclamation:: Any information provided in this project is for educational purposes only. It is **not** intended as financial or investment advice and should not be construed or relied on as such.

<br>

## Dataset

For retrieving the dataset, we will use [yfinance](https://pypi.org/project/yfinance/), which offers a reliable, threaded, and Pythonic way to download historical market data from [Yahoo! finance](https://finance.yahoo.com/). We just need to specify the stock's ticker and the time frame of interest. The extracted dataset contains daily data for the opening, lowest, highest, closing, and [adjusted closing](https://www.investopedia.com/terms/a/adjusted_closing_price.asp) price of the stock, along with its trading volume.

<br>

## Files

The source code for implementing the Streamlit application is organised into two Python Scripts: 
-	**Dashboard_App.py**: the main script. 
-	**Dashboard_Functions.py**: a separate script with all custom functions required for the application.

Just by having these two files, we can run a Streamlit app locally in a browser [[1](references)]. For deployment to Heroku, three extra files are needed:
- **requirements.txt** – A text file that contains all libraries that need to be installed for the app to work.
- **setup.sh** – A shell file that creates a streamlit folder.
- **Procfile** – A simple text file used to first execute the setup.sh and then call streamlit run to run the application.

You can read more about these files in Refs [[1-3](references)].

<br>

## Brief Introduction to Technical Indicators

Simply put, technical indicators are visual tools used by investors/traders to help them make investment choices. Technical indicators use historical data to interpret and forecast the future price action of a financial asset [[4](references)]. Together, these indicators form the basis of technical analysis [[5](references)].

Examples of common technical indicators include the [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp), [Money Flow Index](https://www.investopedia.com/terms/m/mfi.asp), Stochastics, [MACD](https://www.investopedia.com/terms/m/macd.asp), and [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp).

In this notebook, we will only use two indicators:

1) **Moving average convergence divergence** (**MACD**) [[6](references)]: The MACD is calculated by subtracting the 26-period [exponential moving average](https://www.investopedia.com/terms/e/ema.asp) (EMA) from the 12-period EMA. <br>The result of that calculation is the **MACD line**. A nine-day EMA of the MACD (called the "**signal line**") is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals. Traders may buy the asset when the MACD crosses above its signal line and sell the asset when the MACD crosses below the signal line.

2) **Relative Strength Index** (**RSI**) [[7](references)]: measures the magnitude of recent price changes to evaluate **overbought** or **oversold** conditions in the price of an asset. The RSI is displayed as an oscillator (a line graph that moves between two extreme values) and can have a value from 0 to 100. <br>Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security is becoming overbought or overvalued and may be primed for a trend reversal or corrective pullback in price. An RSI reading of 30 or below indicates an oversold or undervalued condition.

<br>

MACD measures the relationship between two EMAs, while the RSI measures price change in relation to recent price highs and lows. These two indicators are often used together to provide analysts with a more complete technical picture of a market.

Both indicators measure [momentum](https://www.investopedia.com/investing/momentum-and-relative-strength-index/) in a market. However, because they measure different factors, they sometimes give contrary indications [[6](references)].

<br>

## Trading Strategy

In our case, we will construct our trading strategy based on the MACD indicator and its signal line. Specifically, we will create a 'Buy Signal’ when the MACD crosses above its signal line and a ‘Sell Signal’ when the MACD crosses below the signal line. The two types of signals will be overlayed on the candlestick chart as triangles (specifically, green up-pointing triangles for ‘Buy’ and yellow down-pointing triangles for ‘Sell’).

<br>

## References

- For creating and deploying the application:
 
  [1] [Get Started](https://docs.streamlit.io/en/stable/getting_started.html) with Streamlit and [Gallery of Examples](https://streamlit.io/gallery?type=apps&category=finance-business) from the official website (Retrieved on Jun 16, 2021).

  [2] [Deploying your Streamlit dashboard with Heroku](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku) by Gilbert Tanner on his personal [website](https://gilberttanner.com/) (Retrieved on Jun 18, 2021).

  [3] [Build 12 Data Science Apps with Python and Streamlit - Full Course](https://www.youtube.com/watch?v=JwSS70SZdyM) by the [DataProfessor](https://www.youtube.com/c/DataProfessor/videos) on [freeCodeCamp.org’s YouTube Channel](https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ) (Retrieved on Jun 17, 2021).

<br>

- For finance terms, concepts, and Python implementation:

  [4] [Technical Indicator](https://www.investopedia.com/terms/t/technicalindicator.asp#:~:text=Technical%20indicators%20are%20heuristic%20or,to%20predict%20future%20price%20movements.) by James Chen on [Investopedia](https://www.investopedia.com/) (Retrieved on Jun 11, 2021).

  [5] [Technical Analyst](https://www.investopedia.com/terms/t/technical-analyst.asp) by Adam Hayes
on [Investopedia](https://www.investopedia.com/) (Retrieved on Jun 11, 2021).

  [6] [Moving Average Convergence Divergence (MACD)](https://www.investopedia.com/terms/m/macd.asp) by Jason Fernando on [Investopedia](https://www.investopedia.com/) (Retrieved on Jun 11, 2021).

  [7] [Relative Strength Index (RSI)](https://www.investopedia.com/terms/r/rsi.asp) by Jason Fernando on [Investopedia](https://www.investopedia.com/) (Retrieved on Jun 11, 2021). 

  [8] [Compute RSI for stocks with python (Relative Strength Index)](https://tcoil.info/compute-rsi-for-stocks-with-python-relative-strength-index/) by Michal Vasulka on [tcoil.info](https://tcoil.info/) (Retrieved on Jun 10, 2021).

<br>

# Feedback

If you have any feedback or ideas to improve this project, feel free to contact me via:

<a href="https://twitter.com/korfanakis">
  <img align="left" alt="Twitter" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" />
</a>

<a href="https://uk.linkedin.com/in/korfanakis">
  <img align="left" alt="LinkedIn" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />
</a>
