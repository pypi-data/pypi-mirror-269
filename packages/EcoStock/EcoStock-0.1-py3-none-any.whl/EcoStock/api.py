from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, Response, FileResponse
from pydantic import BaseModel, Field, validator
from typing import List, Dict
from datetime import datetime
from EcoStock.functions import (
    get_stock_data,
    plot_candlestick,
    avg_stock_data,
    get_world_bank_data,
    calculate_correlation,
    plot_correlation,
    generate_text,
)
from plotly.offline import plot
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import traceback
import uvicorn
import io
import base64
from io import BytesIO
import plotly.io as pio
import sys
import kaleido

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

@app.get("/stock_data/{ticker}/{start_date}/{end_date}")
async def get_stock_data_api(ticker: str, start_date: str, end_date: str):
    try:
        return get_stock_data(ticker, start_date, end_date).to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/plot_candlestick/{ticker}/{start_date}/{end_date}", response_class=HTMLResponse)
async def plot_candlestick_api(ticker: str, start_date: str, end_date: str):
    try:
        stock_data = get_stock_data(ticker, start_date, end_date)
        fig = plot_candlestick(stock_data, ticker)

        # Convert fig to an HTML string
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        traceback_str = ''.join(traceback.format_exception(*sys.exc_info()))
        print(traceback_str)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/avg_stock_data/{ticker}/{start_year}/{end_year}")
async def avg_stock_data_api(ticker: str, start_year: str, end_year: str):
    """
    Fetch stock data from Yahoo Finance and resample to annual frequency.

    Parameters:
    ticker (str): Ticker symbol of the stock.
    start_year (str): Start year in 'YYYY' format.
    end_year (str): End year in 'YYYY' format.

    Returns:
    pandas.DataFrame: DataFrame containing the annual average stock data.
    """
    try:
        return avg_stock_data(ticker, start_year, end_year).to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/world_bank_data/{indicator}/{country}/{start_date}/{end_date}")
async def get_world_bank_data_api(indicator: str, country: str, start_date: str, end_date: str):
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
    try:
        return get_world_bank_data(indicator, country, start_date, end_date).to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/calculate_correlations/{ticker}/{start_date}/{end_date}/{indicator}/{country}")
async def calculate_correlations_api(ticker: str, start_date: str, end_date: str, indicator: str, country: str):
    try:
        stock_data = avg_stock_data(ticker, start_date, end_date)
        econ_data = get_world_bank_data(indicator, country, start_date, end_date)
        return calculate_correlation(stock_data, econ_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/plot_correlations/{ticker}/{start_date}/{end_date}/{indicator}/{country}/{stock_label}/{econ_label}", response_class=HTMLResponse)
async def plot_correlations_api(ticker: str, start_date: str, end_date: str, indicator: str, country: str, stock_label: str, econ_label: str):
    try:
        stock_data = avg_stock_data(ticker, start_date, end_date)
        econ_data = get_world_bank_data(indicator, country, start_date, end_date)
        fig = plot_correlation(stock_data, econ_data, stock_label, econ_label)
        plot_html = fig.to_html(full_html=False)
        return plot_html
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/generate_text/{prompt}")
async def generate_text_api(prompt: str):
    """
    Generate text using OpenAI GPT-3.

    Parameters:
    prompt (str): The prompt for text generation.

    Returns:
    str: Generated text.
    """
    try:
        return generate_text(prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument("-p", "--port", type=int, default=8000, help="The port to bind.")
    parser.add_argument("-r", "--reload", action="store_true", help="Enable hot reloading.")
    args = parser.parse_args()

    uvicorn.run("api:app", host="127.0.0.1", port=args.port, reload=args.reload)
