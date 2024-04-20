## stock(ticker_symbol, start_date, end_date, interval)
"""
Downloads stock data from Yahoo Finance, calculates the percentage returns,
and saves the data in a CSV file. The data includes historical stock prices
and their respective returns over a specified time interval.

Parameters:
ticker_symbol: str
    The stock symbol for which data is to be downloaded (e.g., 'AAPL').
start_date: str
    The start date for the data download in DD-MM-YYYY format (e.g., '01-01-2020').
end_date: str
    The end date for the data download in DD-MM-YYYY format (e.g., '31-12-2020').
interval: str
    The interval at which data should be downloaded. Valid intervals include 
    '1d', '5d', '1wk', '1mo', '3mo'.

Returns:
pandas.DataFrame
    A DataFrame containing the downloaded stock data along with calculated 
    percentage returns. The data is also saved as a CSV file in the 'Stocks' folder.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
import os

def stock(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
    def convert_date_format(date_string):
        return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')

    start_date = convert_date_format(start_date)
    end_date = convert_date_format(end_date)

    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
    stock_data['Returns'] = stock_data['Adj Close'].pct_change()

    folder_name = "Stocks"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = f"{folder_name}/{ticker_symbol}_{interval}.csv"
    stock_data.to_csv(file_name)

    return stock_data

## returns(data)
"""
Calculates the percentage change for each numeric column in a DataFrame,
excluding any 'Date' column. It returns a new DataFrame containing these
percentage changes with the same column headers as the input DataFrame.

Parameters:
data: pandas.DataFrame
    The DataFrame for which percentage changes are calculated.

Returns:
pandas.DataFrame
    A DataFrame with percentage changes for each numeric column, maintaining
    the same structure and column headers as the input DataFrame. Non-numeric
    columns, such as 'Date', are excluded from percentage change calculation.
"""

def returns(data):
    new_df = pd.DataFrame(columns=data.columns)
    new_df['Date'] = data['Date']

    for column in data.columns:
        if column != 'Date' and pd.api.types.is_numeric_dtype(data[column]):
            new_df[column] = data[column].pct_change() * 100

    return new_df

## weights(stocks, extra)
"""
Creates a DataFrame of portfolio weights for a set of stocks. It includes
portfolios where each stock is fully weighted and additional portfolios
with randomly assigned weights.

Parameters:
stocks: pandas.DataFrame
    DataFrame containing stock returns, with each column representing a stock.
extra: int
    Number of additional portfolios to create with random weights.

Returns:
pandas.DataFrame
    A DataFrame where each column represents a portfolio, and each row shows
    the weight of a stock in that portfolio. Columns include portfolios with
    full weight in individual stocks and additional portfolios with random weights.
"""

import numpy as np

def weights(stocks, extra):
    num_stocks = len(stocks.columns)
    total_portfolios = num_stocks + extra
    portfolio_names = [f'P{i+1}' for i in range(total_portfolios)]

    weights_df = pd.DataFrame(index=stocks.columns, columns=portfolio_names)
    for i, stock in enumerate(stocks.columns):
        weights_df.iloc[:, i] = 0
        weights_df.at[stock, f'P{i+1}'] = 1

    for i in range(num_stocks, total_portfolios):
        random_weights = np.random.random(num_stocks)
        normalized_weights = random_weights / random_weights.sum()
        weights_df[f'P{i+1}'] = normalized_weights

    return weights_df

## portfolios(weights, returns, period)
"""
Calculates the expected return and volatility for a set of portfolios based
on their weights and stock returns. The function also allows for annualization
of these metrics based on the specified time period.

Parameters:
weights: pandas.DataFrame
    DataFrame containing the weights of each stock in each portfolio.
returns: pandas.DataFrame
    DataFrame containing the returns of each stock.
period: str, optional
    The time period of the returns data ('daily', 'weekly', 'monthly'). Default is 'daily'.

Returns:
pandas.DataFrame
    A DataFrame with portfolio names, expected annualized returns, and annualized volatility.
    Each portfolio's expected return and volatility are calculated based on its constituent
    stock weights and returns.
"""

def portfolios(weights, returns, period='daily'):
    periods_per_year = {'daily': 252, 'weekly': 52, 'monthly': 12}
    portfolio_returns = returns.dot(weights)

    expected_return = portfolio_returns.mean() * periods_per_year[period]
    volatility = portfolio_returns.std() * np.sqrt(periods_per_year[period])

    portfolio_metrics = pd.DataFrame({
        'Portfolio': weights.columns,
        'Expected Returnc (%)': expected_return * 100,
        'Volatility (%)': volatility * 100
    })

    return portfolio_metrics.set_index('Portfolio')

