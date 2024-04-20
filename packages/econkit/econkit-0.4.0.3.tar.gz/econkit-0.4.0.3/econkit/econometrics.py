## descriptives(data)
"""
Computes descriptive statistics for each numeric column in a DataFrame.

Parameters:
data: pandas.DataFrame
    The DataFrame from which the statistics will be calculated.

Returns:
pandas.DataFrame
    A DataFrame where each row represents a specific statistic (Mean, Median,
    Min, Max, Standard Deviation, Quartile Deviation, Kurtosis Fisher, Kurtosis
    Pearson, Skewness, Coefficient of Quartile Deviation) and each column
    corresponds to a numeric column from the input DataFrame.
"""

import pandas as pd
import numpy as np
from scipy.stats import kurtosis

def descriptives(data):
    all_descriptives = []  
    statistics_labels = ["Mean", "Median", "Min", "Max", "St. Deviation", "Quartile Deviation", "Kurtosis Fisher", "Kurtosis Pearson", "Skewness", "Co-efficient of Q.D"]
    first_column = True  

    for name in data.columns:
        if pd.api.types.is_numeric_dtype(data[name]):
            column_data = data[name].dropna()

            statistics_values = [
                round(column_data.mean(), 2), 
                round(column_data.median(), 2),
                round(column_data.min(), 2), 
                round(column_data.max(), 2), 
                round(column_data.std(), 2), 
                round((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2, 2),
                round(kurtosis(column_data, fisher=True, nan_policy='omit'), 4),
                round(kurtosis(column_data, fisher=False, nan_policy='omit'), 4),
                round(column_data.skew(), 4),
                round((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 / column_data.median(), 4) if column_data.median() != 0 else 0
            ]

            if first_column:
                descriptive_df = pd.DataFrame({'STATISTICS': statistics_labels, name: statistics_values})
                first_column = False
            else:
                descriptive_df = pd.DataFrame({name: statistics_values})

            all_descriptives.append(descriptive_df)

    result_df = pd.concat(all_descriptives, axis=1)
    return result_df

## correlation(df, method="Pearson", p="F")
"""
Calculates and prints the correlation matrix and p-values for numeric columns 
in the provided DataFrame. Supports Pearson and Spearman correlation methods.

Parameters:
df: pandas.DataFrame
    The DataFrame for which correlations are calculated.
method: str, optional
    The method of correlation ('Pearson' or 'Spearman'). Default is 'Pearson'.
p: str, optional
    If 'T', p-value matrix is also printed; if 'F', only correlation matrix 
    is printed. Default is 'F'.

Returns:
None
    This function prints the correlation matrix and optionally the p-value
    matrix directly to the console.
"""

import numpy as np
import pandas as pd
import scipy.stats

def correlation(df, method="Pearson", p=False):
    def format_p_value(p_value):
        formatted = f"{p_value:0.3f}"
        if formatted.startswith("0."):
            return formatted[1:]
        return formatted

    numeric_df = df.select_dtypes(include=[np.number])
    if method == "Pearson":
        print("\n" + "=" * 21 + f"\n {method} Correlation\n" + "=" * 21)
    elif method == "Spearman":
        print("\n" + "=" * 27 + f"\n {method} Rank Correlation\n" + "=" * 27)
    elif method == "Kendall":
        print("\n" + "=" * 26 + f"\n {method} Rank Correlation\n" + "=" * 26)

    corr_matrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)
    pmatrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)

    keys = numeric_df.columns.tolist()

    for i, key1 in enumerate(keys):
        for j, key2 in enumerate(keys):
            if i > j:
                continue

            data1 = numeric_df[key1].dropna()
            data2 = numeric_df[key2].dropna()

            common_index = data1.index.intersection(data2.index)
            data1 = data1.loc[common_index]
            data2 = data2.loc[common_index]

            if len(common_index) < 2:
                corr_matrix.at[key1, key2] = 'nan'
                corr_matrix.at[key2, key1] = 'nan'
                continue

            if method == 'Spearman':
                correlation, p_value = scipy.stats.spearmanr(data1, data2)
            elif method == 'Pearson':
                correlation, p_value = scipy.stats.pearsonr(data1, data2)
            elif method == 'Kendall':
                correlation, p_value = scipy.stats.kendalltau(data1, data2)

            pmatrix.at[key1, key2] = format_p_value(p_value)
            pmatrix.at[key2, key1] = format_p_value(p_value)

            stars = "     "
            if p_value < 0.001:
                stars = " *** "
            elif p_value < 0.01:
                stars = " **  "
            elif p_value < 0.05:
                stars = " *   "
            elif p_value < 0.1:
                stars = " .   "

            correlation_str = f"{format_p_value(correlation)}{stars}"
            corr_matrix.at[key1, key2] = correlation_str
            corr_matrix.at[key2, key1] = correlation_str

    corr_matrix_str = corr_matrix.to_string(sparsify=True, justify='center')
    explanation = "\n\n--\nSignif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'"

    print("\n\n>> Correlation Matrix <<\n")
    print(corr_matrix_str + explanation)

    if p:
        print("\n\n>> P-Value Matrix <<\n")
        print(pmatrix.to_string())
        print("\n")
    else:
        print("\n")


## table(column_name, *dataframes)
"""
Creates a DataFrame by combining a specified column from multiple DataFrames.

Parameters:
column_name: str
    The name of the column to be extracted from each DataFrame.
dataframes: variable number of pandas.DataFrame
    DataFrames from which the specified column will be extracted.

Returns:
pandas.DataFrame
    A new DataFrame with the specified column from each of the provided 
    DataFrames.
"""

import inspect

def table(column_name, *dataframes):
    if not dataframes:
        raise ValueError("No dataframes provided")

    frame = inspect.currentframe()
    try:
        df_names = []
        for df in dataframes:
            for var_name, var_val in frame.f_back.f_locals.items():
                if var_val is df:
                    df_names.append(var_name)
                    break
            else:
                df_names.append("UnnamedDataFrame")
    finally:
        del frame

    combined_df = pd.DataFrame()

    for df, name in zip(dataframes, df_names):
        if column_name in df.columns:
            combined_df[name] = df[column_name]
        else:
            combined_df[name] = pd.NA

    return round(combined_df,2)

