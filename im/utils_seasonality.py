from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import kruskal
import pandas as pd


def test_seasonality(sales24: list, sales23: list):
    """
    Args:
        sales24: (list) monthly sales for 2024
        sales23: (list) monthly sales for 2023
    """
    monthly_sales = [sales23[i::11] + sales24[i::11] for i in range(11)]  # Group by month
    stat, p_value = kruskal(*monthly_sales)

    # Decomposition - to plot 
    sales24_series = pd.Series(sales24, index=pd.date_range('2024-01-01', periods=11, freq='ME'))
    sales23_series = pd.Series(sales23, index=pd.date_range('2023-01-01', periods=11, freq='ME'))
    ser = pd.concat([sales24_series, sales23_series])
    decomposition = seasonal_decompose(ser, model='additive', period=11)
    seasonal_decomposition = decomposition.seasonal

    s_dec_chart_data = {
        "labels": seasonal_decomposition.index.strftime('%B').tolist(),
        "data": seasonal_decomposition.tolist()
    }

    return stat, p_value, s_dec_chart_data
