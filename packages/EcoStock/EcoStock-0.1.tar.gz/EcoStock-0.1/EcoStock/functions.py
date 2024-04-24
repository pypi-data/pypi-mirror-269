# Nel file functions.py, includeremo tutte le funzioni per ottenere i dati finanziari e economici ecc...
# ESEMPIO:
# EcoStock/functions.py

import pandas as pd
import numpy as np
import requests
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import openai
from openai import OpenAI
import os
import base64
import io

# Define the get_stock_data function
def get_stock_data(ticker, start_date, end_date):
    """
    Fetch stock data from Yahoo Finance.

    Parameters:
    ticker (str): Ticker symbol of the stock.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    pandas.DataFrame: DataFrame containing the stock data.
    """
    return yf.download(ticker, start=start_date, end=end_date)

# Plotting the stock data
def plot_candlestick(stock_data, ticker):
    """
    Plot the stock data as a candlestick chart.

    Parameters:
    stock_data (pandas.DataFrame): DataFrame containing the stock data.
    ticker (str): Ticker symbol of the stock.
    """
    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data['Open'],
                                         high=stock_data['High'],
                                         low=stock_data['Low'],
                                         close=stock_data['Close'])])

    # Add volume bars
    fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], marker=dict(color=np.where(stock_data['Close'] >= stock_data['Open'], 'green', 'red')), yaxis='y2'))

    # Add range slider
    fig.update_layout(
        title=f'{ticker} Stock Price',
        yaxis_title='Stock Price (USD)',
        shapes = [dict(x0='2022-01-01', x1='2022-12-31', y0=0, y1=1, xref='x', yref='paper', line_width=2)],
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis2=dict(domain=[0, 0.2], anchor='x', title='Volume')
    )

    return fig

# Annual average stock data
def avg_stock_data(ticker, start_year, end_year):
    """
    Fetch stock data from Yahoo Finance and resample to annual frequency.

    Parameters:
    ticker (str): Ticker symbol of the stock.
    start_year (str): Start year in 'YYYY' format.
    end_year (str): End year in 'YYYY' format.

    Returns:
    pandas.DataFrame: DataFrame containing the annual average stock data.
    """
    # Format the years as 'YYYY-MM-DD'
    start_date = f'{start_year}-01-01'
    end_date = f'{end_year}-12-31'

    # Fetch the daily stock data
    df = yf.download(ticker, start=start_date, end=end_date)

    # Resample to annual frequency, calculating the mean of each year
    df = df.resample('A').mean()

    # Modify the index to only include the year
    df.index = df.index.year

    return df

# World Bank data
def get_world_bank_data(indicator, country, start_date, end_date):
    """
    Fetch economic data from the World Bank.

    Parameters:
    indicator (str): The indicator of interest.
    country (str): The country of interest.
    start_date (str): The start date for the data.
    end_date (str): The end date for the data.

    Returns:
    pandas.DataFrame: DataFrame containing the economic data.
    """
    # Define the API URL
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_date}:{end_date}&format=json"

    # Send the HTTP request and get the response
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()

        # Check if the data has at least two elements
        if len(data) < 2:
            print("Error: No data available for the given parameters")
            return pd.DataFrame()

        # Convert the data to a DataFrame and set the date as the index
        df = pd.DataFrame(data[1])
        df['date'] = pd.to_datetime(df['date']).dt.year
        df.set_index('date', inplace=True)

        # Extract the name of the indicator and the country
        df['indicator'] = df['indicator'].apply(lambda x: x['value'])
        df['country'] = df['country'].apply(lambda x: x['value'])

        return df
    else:
        print(f"Error: HTTP request failed with status code {response.status_code}")
        return pd.DataFrame()

# Calculate correlation
def calculate_correlation(stock_data, econ_data):
    """
    Calculate the correlation coefficient between stock and economic data.

    Parameters:
    stock_data (pandas.DataFrame): DataFrame containing the stock data.
    econ_data (pandas.DataFrame): DataFrame containing the economic data.

    Returns:
    float: Correlation coefficient.
    """
    # Check if 'Close' column exists in stock_data
    if 'Close' not in stock_data.columns:
        print("Error: 'Close' column not found in stock_data")
        return None

    # Merge the data
    merged_data = pd.merge(stock_data, econ_data, how='inner', left_index=True, right_index=True)

    # Check if merged_data is empty
    if merged_data.empty:
        print("Error: No matching data found for stock_data and econ_data")
        return None

    return merged_data['Close'].corr(merged_data['value'])

# Plotting correlation
def plot_correlation(stock_data, econ_data, stock_label, econ_label):
    """
    Plot the correlation between stock and economic data over time.

    Parameters:
    stock_data (pandas.DataFrame): DataFrame containing the stock data.
    econ_data (pandas.DataFrame): DataFrame containing the economic data.
    stock_label (str): Label for the stock data.
    econ_label (str): Label for the economic data.
    """
    # Check if 'Close' column exists in stock_data
    if 'Close' not in stock_data.columns:
        print("Error: 'Close' column not found in stock_data")
        return None

    # Merge the data
    merged_data = pd.merge(stock_data, econ_data, how='inner', left_index=True, right_index=True)

    # Check if merged_data is empty
    if merged_data.empty:
        print("Error: No matching data found for stock_data and econ_data")
        return None

    # Calculate the correlation
    correlation = merged_data['Close'].corr(merged_data['value'])

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))  # Increase the size of the plot

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(stock_label, color=color)
    ax1.plot(stock_data.index, stock_data['Close'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel(econ_label, color=color)
    ax2.plot(econ_data.index, econ_data['value'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Format the y-tick labels to include a dollar sign and display in terms of billions or trillions
    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '${:.1f}{}'.format(num, ['', 'K', 'M', 'B', 'T'][magnitude])

    formatter = mticker.FuncFormatter(lambda x, pos: human_format(x))
    ax2.yaxis.set_major_formatter(formatter)

    plt.title(f'Correlation between {stock_label} and {econ_label}: {correlation:.2f}')
    plt.grid(True)
    fig.tight_layout()
    
    return  plt.show()

# Generate text using OpenAI GPT-3
def generate_text(prompt):
    os.environ['OPENAI_API_KEY'] = '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'
    openai.api_key = os.getenv('OPENAI_API_KEY')
    client_openai = OpenAI()
    response = client_openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()
