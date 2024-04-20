
# Econkit

## Introduction
Econkit is a comprehensive Python library designed for economic and financial data analysis. It offers a wide range of functionalities, from descriptive statistics to advanced portfolio analysis, making it a valuable tool for economists, financial analysts, and researchers.

## Installation
```bash
pip install econkit
```

## Features
Econkit provides the following functionalities:

### Descriptives Function
Perform comprehensive statistical analysis on a DataFrame, computing various descriptive statistics for each numeric column.

### Correlation Function
Compute correlation matrices between numerical columns in a DataFrame. Supports Pearson and Spearman methods and provides significance levels.

### Stock Function
Download and process stock data from Yahoo Finance, including the computation of percentage growth of the Adjusted Close price.

### Table Function
Facilitate the comparison of a specific column across multiple DataFrames by extracting and combining them into a new DataFrame.

### Weights Function
Generate portfolio weights for a collection of stocks, creating multiple portfolios with full weight in one stock and additional portfolios with random weights.

### Portfolios Function
Calculate the expected return and volatility of various portfolios based on their weight allocations and stock returns.

### Frontier Simple Function
Visualize the mean-variance frontier from portfolio data and highlight the portfolio with minimum volatility.

## Usage
Below are basic usage examples for each function in Econkit:

### Descriptives
```python
# result = descriptives(your_dataframe)
# print(result)
```

### Correlation
```python
# correlation(your_dataframe, method="Pearson", p="F")
```

### Stock
```python
# stock_data = stock("ticker_symbol", "start_date", "end_date", "interval")
```

### Table
```python
# combined_df = table("column_name", dataframe1, dataframe2, ...)
# print(combined_df)
```

### Weights
```python
# weights_df = weights(stocks, extra)
```

### Portfolios
```python
# portfolio_metrics = portfolios(weights_df, returns_df, 'daily')
# print(portfolio_metrics)
```

### Frontier Simple
```python
# frontier_simple(your_dataframe)
```

## Contributing
Contributions to the Econkit library are welcome. Please refer to the contributing guidelines for more information.

## License
Econkit is licensed under the MIT License.

## Contact
For inquiries or support, please contact contact@stefanstavrianos.eu.
