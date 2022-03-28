import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

import Dashboard_Functions as functions


# Add a title and a short description to the app.
st.markdown('''
# Financial Dashboard Application

A web app to interactively visualise price information and technical indicators for an asset. 
Simply specify the asset’s ticker (e.g. TSLA, AAPL, or BTC-USD), the time frame of interest, and whether to see 
a summary of the business/asset or not (optional).

Dataset retrieved from [Yahoo! Finance](https://uk.finance.yahoo.com/). For more information, please visit the [GitHub repository](https://github.com/KOrfanakis/Financial_Dashboard_App).

---
''')

# Add a sidebar for user input.
st.sidebar.header('Query Parameters')

ticker = st.sidebar.text_input('Ticker:')

today = dt.datetime.today()
start_date = st.sidebar.date_input('Start date:',
                                   today - dt.timedelta(days=365*1),  # The default time frame is 1 year.
                                   min_value=today - dt.timedelta(days=365*4),
                                   max_value=today - dt.timedelta(days=31*2))
end_date = st.sidebar.date_input('End date:',
                                 min_value=start_date +
                                 dt.timedelta(days=31*2),
                                 max_value=today)

show_summary = st.sidebar.checkbox('Show summary')

if ticker:
    df = functions.get_price(ticker, start_date, end_date)

    # Write an if/else statement to check whether the ticker exists.
    # If it does not exist, an error message will be displayed to the user.
    if df.shape[0] == 0:
        st.error('Ticker does not exist! Try again.')

    else:
        info_df = functions.get_info_df(ticker)

        st.header(info_df.loc['Name'][0])

        # If a URL for the asset's logo is included, display the logo.
        if len(info_df.loc['Logo URL'][0]) != 0:
            st.image(info_df.loc['Logo URL'][0], width=200)

        if show_summary:
            st.markdown('## Summary')
            st.info(info_df.loc['Summary'][0])

        st.markdown('''
        ## Information

        All prices are in USD ($).''')
        st.dataframe(info_df.drop(['Summary', 'Logo URL']).astype(str))

        closed_dates_list = functions.get_closed_dates(df)

        df = functions.get_MACD(df)
        df = functions.get_RSI(df)

        df = functions.get_trading_strategy(df)

        # Plot the four plots.
        fig = make_subplots(rows=4,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.005,
                            row_width=[0.2, 0.3, 0.3, 0.8])

        fig = functions.plot_candlestick_chart(fig,
                                               df,
                                               row=1,
                                               plot_EMAs=True,
                                               plot_strategy=True)

        fig = functions.plot_MACD(fig, df, row=2)
        fig = functions.plot_RSI(fig, df, row=3)
        fig = functions.plot_volume(fig, df, row=4)

        # Update x-axis.
        fig.update_xaxes(rangebreaks=[dict(values=closed_dates_list)],
                         range=[df['Date'].iloc[0] - dt.timedelta(days=3), df['Date'].iloc[-1] + dt.timedelta(days=3)])

        # Update basic layout properties (width&height, background color, title, etc.).
        fig.update_layout(width=800,
                          height=800,
                          plot_bgcolor='#0E1117',
                          paper_bgcolor='#0E1117',
                          title={
                              'text': '{} - Dashboard'.format(ticker),
                              'y': 0.98
                          },
                          hovermode='x unified',
                          legend=dict(orientation='h',
                                      xanchor='left',
                                      x=0.05,
                                      yanchor='bottom',
                                      y=1.003))

        # Customize axis parameters.
        axis_lw, axis_color = 2, 'white'
        fig.update_layout(xaxis1=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis1=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis2=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis2=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis3=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis3=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        fig.update_layout(xaxis4=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          yaxis4=dict(linewidth=axis_lw,
                                      linecolor=axis_color,
                                      mirror=True,
                                      showgrid=False),
                          font=dict(color=axis_color))

        st.markdown('## Interactive Dashboard')

        st.plotly_chart(fig)

        st.write('**Disclaimer**: The content of this dashboard is for educational purposes only. You should **not** construe any of the provided information as financial advice.')

    st.write('---')
    
st.write('Creator: [Konstantinos Orfanakis](https://github.com/KOrfanakis)')