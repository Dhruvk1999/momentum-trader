# data preparation
# setting the target variable

import yfinance as yf
import pandas as pd
import numpy as np
from talib import abstract

def add_bollinger_band_features(data):
    # Calculate Bollinger Bands
    upper_band, middle_band, lower_band = abstract.BBANDS(data['Close'])

    # Calculate deviation from the middle band
    data['BB_Deviation'] = (data['Close'] - middle_band) / middle_band

    # Create binary indicator for inside/outside bands
    data['Inside_BB'] = np.where((data['Close'] >= lower_band) & (data['Close'] <= upper_band), 1, 0)

    # Calculate distance from the nearest band
    data['Distance_from_Lower'] = (data['Close'] - lower_band) / middle_band
    data['Distance_from_Upper'] = (data['Close'] - upper_band) / middle_band

    return data


def add_alpha_factors(data):
    # Calculate Moving Averages
    data['SMA_10'] = abstract.SMA(data.Close, timeperiod=10)
    data['SMA_50'] = abstract.SMA(data.Close, timeperiod=50)

    # Calculate RSI
    data['RSI'] = abstract.RSI(data.Close)

    # Calculate MACD
    data['MACD'], _, _ = abstract.MACD(data.Close)

    # Calculate Bollinger Bands
    upper_band, middle_band, lower_band = abstract.BBANDS(data.Close)
    data['Upper_Band'] = upper_band
    data['Middle_Band'] = middle_band
    data['Lower_Band'] = lower_band

    # Calculate ATR
    data['ATR'] = abstract.ATR(data.High,data.Low,data.Close)

    # Calculate OBV
    data['OBV'] = abstract.OBV(data.Close,data.Volume)

    # Calculate VWAP
    #data['VWAP'] = abstract.VWAP(data)

    # Calculate custom indicator (e.g., SMA cross)
    data['SMA_Cross'] = np.where(data['SMA_10'] > data['SMA_50'], 1, 0)

    # ... Add more alpha factors here ...
    data = add_bollinger_band_features(data)

    return data


# setting the target variables

def forward_returns(no_of_days, data):
    data['Forward_Returns'] = data['Close'].shift(no_of_days) / data['Close'] - 1
    return data

def binary_target_with_percentage(no_of_days, data, percentage_threshold):
    data = forward_returns(no_of_days, data)  # Calculate forward returns

    # Create binary target variable: 1 for returns exceeding percentage threshold, 0 otherwise
    data['Binary_Target_Percentage'] = data['Forward_Returns'].apply(lambda x: 1 if x > percentage_threshold else 0)
    return data

# Example function to create volatility-based target variable
def volatility_based_target(no_of_days, data):
    data = forward_returns(no_of_days, data)  # Calculate forward returns

    # Calculate standard deviation of returns for the specified number of days
    data['Volatility'] = data['Close'].pct_change().rolling(window=no_of_days).std()

    # Create binary target variable: 1 for returns exceeding volatility threshold, 0 otherwise
    volatility_threshold = 2.0  # Example threshold for high volatility
    data['Volatility_Based_Target'] = data['Forward_Returns'].apply(lambda x: 1 if abs(x) > volatility_threshold * data['Volatility'].iloc[-1] else 0)
    return data