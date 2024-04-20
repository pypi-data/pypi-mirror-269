import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def frontier_simple(data):
    """
    Plot the mean-variance frontier from a given DataFrame and highlight the portfolio with minimum volatility.

    :param data: DataFrame containing the portfolio data with 'Expected Returnc (%)' and 'Volatility (%)'.
    """

    # Convert columns to numeric, handling non-numeric values
    data['Expected Returnc (%)'] = pd.to_numeric(data['Expected Returnc (%)'], errors='coerce')
    data['Volatility (%)'] = pd.to_numeric(data['Volatility (%)'], errors='coerce')

    # Check if data is valid for plotting
    if data['Expected Returnc (%)'].notna().any() and data['Volatility (%)'].notna().any():
        # Plot portfolios
        plt.scatter(data['Volatility (%)'], data['Expected Returnc (%)'], color='blue')

        # Identify the portfolio with the minimum volatility
        min_vol_index = data['Volatility (%)'].idxmin()
        min_vol_portfolio = data.loc[min_vol_index]
        min_vol_value = min_vol_portfolio['Volatility (%)']
        min_er_value = min_vol_portfolio['Expected Returnc (%)']

        # Highlight the minimum volatility portfolio
        plt.scatter([min_vol_value], [min_er_value], color='red', marker='*', s=150, edgecolors='black')
        plt.annotate(min_vol_index, (min_vol_value, min_er_value), textcoords="offset points", xytext=(0,10), ha='center')

        # Plot settings
        plt.title('Mean - Variance Frontier (No Short Selling)')
        plt.xlabel('Volatility (%)')
        plt.ylabel('Expected Return (%)')
        plt.grid(True)
        plt.show()

        # Print details of the minimum volatility portfolio
        print(f"\nOptimal Portfolio: {min_vol_index}")
        print(f"Expected Return: {min_er_value:.2f}%")
        print(f"Volatility: {min_vol_value:.2f}%\n")
    else:
        print("Data is not suitable for plotting.")


