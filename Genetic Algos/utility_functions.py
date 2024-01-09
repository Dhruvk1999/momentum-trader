import yfinance as yf
import talib
import numpy as np
import random
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)  # Ignore DeprecationWarning
warnings.filterwarnings('ignore', category=FutureWarning) 

# Function to fetch historical stock data using yfinance
def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except: 
        print("error in fetching data")
# Function to calculate MACD using TA-Lib
def calculate_macd(data,fast_period,slow_period):
    try:
        if(fast_period > slow_period):
            temp = fast_period
            fast_period = slow_period
            slow_period = temp
        if(fast_period>1):
            macd, signal, _ = talib.MACD(data['Close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=9)
        else: 
            fast_period = 2 
            macd, signal, _ = talib.MACD(data['Close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=9)
            
        return macd, signal
    except: 
        print(f"error in calculatin macd signal {fast_period,slow_period}")
# Function to calculate Rate of Change (ROC) using TA-Lib
def calculate_roc(data, period):
    try:
        roc = talib.ROC(data['Close'], timeperiod=period)
        return roc
    except:
        print("this period caused the error",period)


# Function to calculate the derivative of RSI
# Function to calculate the derivative of RSI
def calculate_rsi_derivative(data, period):
    try:
        if len(data) >= period:
            rsi = talib.RSI(data['Close'], timeperiod=period)
            rsi_derivative = data.Close.diff()
            return rsi_derivative
        else:
            print("Insufficient data for RSI derivative calculation")
            return None
    except Exception as e:
        print(f"Error calculating RSI derivative: {e}")
        print(period)
        return None
# Function to simulate a trailing stop-loss exit condition


def trailing_stop_loss(data, stop_loss_percentage):
    highest_high = data['High'].rolling(window=20).max()
    stop_loss = highest_high * (1 - stop_loss_percentage)
    return stop_loss