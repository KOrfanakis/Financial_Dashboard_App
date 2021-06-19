import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots


def get_price(ticker, start_date, end_date):
    """Return a DataFrame with price information (open, high, low, close, adjusted close, and volume) for the ticker between the specified dates."""
    df = yf.download(ticker, start_date, end_date, progress=False)
    df.reset_index(inplace=True)

    return df


def get_info_df(ticker):
    """Return a DataFrame with various pieces of information (e.g. business summary, volume, market capitalisation, etc.) for the asset."""
    info_dict = yf.Ticker(ticker).info
    columns_dict = {'longName': 'Name',
                    'name': 'Name',
                    'symbol': 'Ticker',
                    'description': 'Summary',
                    'longBusinessSummary': 'Summary',
                    'industry': 'Ιndustry',
                    'previousClose': 'Previous Close',
                    'open': 'Open',
                    'fiftyTwoWeekLow': '52-week Low',
                    'fiftyTwoWeekHigh': '52-week High',
                    'volume': 'Volume (M)',
                    'averageVolume': 'Average Volume (M)',
                    'marketCap': 'Market Cap. (M)',
                    'trailingPE': 'PE Ρatio (TTM)',
                    'trailingEps': 'EPS (TTM)',
                    'logo_url': 'Logo URL'}

    # Some keys are not common for all assets, therefore we need to check for each ticker.
    columns, values = [], []
    for key, value in columns_dict.items():
        try:
            values.append(info_dict[key])
            columns.append(value)
        except:
            pass

    info_df = pd.DataFrame(values, index=columns, columns=['Info'])

    info_df.loc[['Volume (M)', 'Average Volume (M)', 'Market Cap. (M)']] = info_df.loc[[
        'Volume (M)', 'Average Volume (M)', 'Market Cap. (M)']].apply(lambda x: x/1_000_000)  # Normalise to millions.
    info_df.loc['Market Cap. (M)'] = info_df.loc['Market Cap. (M)'].apply(
        lambda x: np.round(x, 1))

    return info_df


def get_closed_dates(df):
    """Return a list containing all dates on which the stock market was closed."""
    # Create a dataframe that contains all dates from the start until today.
    timeline = pd.date_range(start=df['Date'].iloc[0], end=df['Date'].iloc[-1])

    # Create a list of the dates existing in the dataframe.
    df_dates = [day.strftime('%Y-%m-%d') for day in pd.to_datetime(df['Date'])]

    # Finally, determine which dates from the 'timeline' do not exist in our dataframe.
    closed_dates = [
        day for day in timeline.strftime('%Y-%m-%d').tolist()
        if not day in df_dates
    ]

    return closed_dates


def get_MACD(df, column='Adj Close'):
    """Return a DataFrame with the MACD indicator and related information (signal line and histogram)."""
    df['EMA-12'] = df[column].ewm(span=12, adjust=False).mean()
    df['EMA-26'] = df[column].ewm(span=26, adjust=False).mean()

    # MACD Indicator = 12-Period EMA − 26-Period EMA.
    df['MACD'] = df['EMA-12'] - df['EMA-26']

    # Signal line = 9-day EMA of the MACD line.
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Histogram = MACD - Indicator.
    df['Histogram'] = df['MACD'] - df['Signal']

    return df


def get_RSI(df, column='Adj Close', time_window=14):
    """Return a DataFrame with the RSI indicator for the specified time window."""
    diff = df[column].diff(1)

    # This preservers dimensions off diff values.
    up_chg = 0 * diff
    down_chg = 0 * diff

    # Up change is equal to the positive difference, otherwise equal to zero.
    up_chg[diff > 0] = diff[diff > 0]

    # Down change is equal to negative deifference, otherwise equal to zero.
    down_chg[diff < 0] = diff[diff < 0]

    # We set com = time_window-1 so we get decay alpha=1/time_window.
    up_chg_avg = up_chg.ewm(com=time_window - 1,
                            min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1,
                                min_periods=time_window).mean()

    RS = abs(up_chg_avg / down_chg_avg)
    df['RSI'] = 100 - 100 / (1 + RS)

    return df


def get_trading_strategy(df, column='Adj Close'):
    """Return the Buy/Sell signal on the specified (price) column (Default = 'Adj Close')."""
    buy_list, sell_list = [], []
    flag = False

    for i in range(0, len(df)):
        if df['MACD'].iloc[i] > df['Signal'].iloc[i] and flag == False:
            buy_list.append(df[column].iloc[i])
            sell_list.append(np.nan)
            flag = True

        elif df['MACD'].iloc[i] < df['Signal'].iloc[i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(df[column].iloc[i])
            flag = False

        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    # Store the buy and sell signals/lists into the DataFrame.
    df['Buy'] = buy_list
    df['Sell'] = sell_list

    return df


def plot_candlestick_chart(fig, df, row, column=1, plot_EMAs=True, plot_strategy=True):
    """Return a graph object figure containing a Candlestick chart in the specified row."""
    fig.add_trace(go.Candlestick(x=df['Date'],
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlestick Chart'),
                  row=row,
                  col=column)

    # If the boolean argument plot_EMAs is True, then show the line plots for the two exponential moving averages.
    if (plot_EMAs == True):
        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['EMA-12'],
                                 name='12-period EMA',
                                 line=dict(color='dodgerblue', width=2)),
                      row=row,
                      col=column)

        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['EMA-26'],
                                 name='26-period EMA',
                                 line=dict(color='whitesmoke', width=2)),
                      row=row,
                      col=column)

    # Similarly, if the boolean argument plot_strategy is True, then show the Buy/Sell signals.
    if (plot_strategy == True):
        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['Buy'],
                                 name='Buy Signal',
                                 mode='markers',
                                 marker_symbol='triangle-up',
                                 marker=dict(size=9),
                                 line=dict(color='Lime')),
                      row=row,
                      col=column)

        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['Sell'],
                                 name='Sell Signal',
                                 mode='markers',
                                 marker_symbol='triangle-down',
                                 marker=dict(size=9, color='Yellow')),
                      row=row,
                      col=column)

    fig.update_xaxes(rangeslider={'visible': False})
    fig.update_yaxes(title_text='Price ($)', row=row, col=column)

    return fig


def plot_MACD(fig, df, row, column=1):
    """Return a graph object figure containing the MACD indicator, the signal line, and a histogram in the specified row."""
    df['Hist-Color'] = np.where(df['Histogram'] < 0, 'red', 'green')

    fig.add_trace(go.Bar(x=df['Date'],
                         y=df['Histogram'],
                         name='Histogram',
                         marker_color=df['Hist-Color'],
                         showlegend=True),
                  row=row,
                  col=column)

    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df['MACD'],
                             name='MACD',
                             line=dict(color='darkorange', width=2.5)),
                  row=row,
                  col=column)

    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df['Signal'],
                             name='Signal',
                             line=dict(color='cyan', width=2.5)),
                  row=row,
                  col=column)

    fig.update_yaxes(title_text='MACD', row=row, col=column)

    return fig


def plot_RSI(fig, df, row, column=1):
    """Return a graph object figure containing the RSI indicator in the specified row."""
    fig.add_trace(go.Scatter(x=df['Date'].iloc[30:],
                             y=df['RSI'].iloc[30:],
                             name='RSI',
                             line=dict(color='gold', width=2)),
                  row=row,
                  col=column)

    fig.update_yaxes(title_text='RSI', row=row, col=column)

    # Add one red horizontal line at 70% (overvalued) and green line at 30% (undervalued).
    for y_pos, color in zip([70, 30], ['Red', 'Green']):
        fig.add_shape(x0=df['Date'].iloc[1],
                      x1=df['Date'].iloc[-1],
                      y0=y_pos,
                      y1=y_pos,
                      type='line',
                      line=dict(color=color, width=2),
                      row=row,
                      col=column)

    # Add a text box for each line.
    for y_pos, text, color in zip([64, 36], ['Overvalued', 'Undervalued'], ['Red', 'Green']):
        fig.add_annotation(x=df['Date'].iloc[int(df['Date'].shape[0] / 10)],
                           y=y_pos,
                           text=text,
                           font=dict(size=14, color=color),
                           bordercolor=color,
                           borderwidth=1,
                           borderpad=2,
                           bgcolor='lightsteelblue',
                           opacity=0.75,
                           showarrow=False,
                           row=row,
                           col=column)

    # Update the y-axis limits.
    ymin = 25 if df['RSI'].iloc[30:].min() > 25 else df['RSI'].iloc[30:].min() - 5
    ymax = 75 if df['RSI'].iloc[30:].max() < 75 else df['RSI'].iloc[30:].max() + 5
    fig.update_yaxes(range=[ymin, ymax], row=row, col=column)

    return fig


def plot_volume(fig, df, row, column=1):
    """Return a graph object figure containing the volume chart in the specified row."""
    fig.add_trace(go.Bar(x=df['Date'],
                         y=df['Volume'],
                         marker=dict(color='lightskyblue',
                                     line=dict(color='firebrick', width=0.1)),
                         showlegend=False,
                         name='Volume'),
                  row=row,
                  col=column)

    fig.update_xaxes(title_text='Date', row=4, col=1)
    fig.update_yaxes(title_text='Volume ($)', row=row, col=column)

    return fig