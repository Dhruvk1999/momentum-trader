# volume spike detector
import pandas as pd
import numpy as np
from datetime import date
from indicators import *
import yfinance as yf
# for loading bar
import ipywidgets as widgets
from IPython.display import display
import sys

#loading the data from the pre-existing csv file
#df=pd.read_csv("data500.csv")
symbols=pd.read_csv("nifty100.csv")
symbols=symbols['Symbol'].values.tolist()

def load_data(symbols=symbols):
    '''
    returns: pd.DataFrame
    takes: list of symbols
    '''
    data = pd.DataFrame()
    print(f"Going to records of {len(symbols)} stocks")

    # Use ipywidgets to show a loading bar in Jupyter
    progress_bar = widgets.FloatProgress(min=0, max=len(symbols), description='Loading data')
    display(progress_bar)

    for i, symbol in enumerate(symbols):
        try:
            temp = yf.download(symbol + ".NS", start="2022-02-25", end=date.today())
            temp["Symbol"] = symbol

            # Calculate rolling average volume
            temp_avg_vol = temp['Volume'].rolling(5).mean()

            data = pd.concat([data, temp])
        except:
            print(f"Error in fetching the data for {symbol}")

        progress_bar.value = i + 1  # Update the loading bar for each stock processed

    return data


def filterVolumeSpike(data,percentage):
    result=pd.DataFrame()
    try:
        data_grouped=data.groupby(by="Symbol")
    except:
        print("Error in grouping")


    for symbol in symbols:
        try:
            temp=data_grouped.get_group(symbol)
    #         [temp.Volume>2*temp_avg_vol]
            temp_avg_vol=temp['Volume'].rolling(5).mean()
            temp=temp[temp.Volume>percentage*temp_avg_vol]
            result=pd.concat([result,temp])
        except:
            print(f"Error in fetching {symbol}")
    return result

def filterVolumeSpikeWithAverage(data,percentage):
    result=pd.DataFrame()
    try:
        data_grouped=data.groupby(by="Symbol")
    except:
        print("Error in grouping")


    for symbol in symbols:
        try:
            temp=data_grouped.get_group(symbol)
    #         [temp.Volume>2*temp_avg_vol]
            temp_avg_vol=temp['Volume'].rolling(5).mean()
            temp['SMA200']=temp['Close'].rolling(200).mean()
            temp = temp[(temp['Volume'] > percentage * temp_avg_vol) & (temp['Close'] < temp['SMA200'])]
            result=pd.concat([result,temp])
        except:
            print(f"Error in fetching {symbol}")
    return result

def filterRSI(data):
    df_grouped=data.groupby("Symbol")
    result=[]

    for i in symbols:
        try:
            temp=df_grouped.get_group(i)
            temp=rsi(temp,4)
            temp=sma(temp,200)
            current_average=list(temp.sma200)[-1]
            current_price=list(temp.Close)[-1]
            current_rsi=list(temp.rsi)[-1]
        except:
            pass
            #print(f"cannot fetch {i}")

        if current_rsi<40 and current_price<current_average:
            result=pd.concat([result,pd.DataFrame(i)])
    return result
        
'''chatGpt refactoring of the above code
import pandas as pd
import yfinance as yf
from datetime import date
import numpy as np

def load_data(symbols):
    
    returns: pd.DataFrame
    takes: list of symbols
    
    data = pd.DataFrame()

    for symbol in symbols:
        try:
            temp = yf.download(symbol + ".NS", start="2022-02-25", end=date.today())
            temp["Symbol"] = symbol
            data = pd.concat([data, temp])
        except Exception as e:
            print(f"Error in fetching the data for {symbol}: {e}")

    return data

def filter_volume_spike(data, symbols, percentage=2):
    result = pd.DataFrame()
    data_grouped = data.groupby(by="Symbol")

    for symbol in symbols:
        try:
            temp = data_grouped.get_group(symbol)
            temp_avg_vol = temp['Volume'].rolling(5).mean()
            temp = temp[temp.Volume > percentage * temp_avg_vol]
            result = pd.concat([result, temp])
        except Exception as e:
            print(f"Error in fetching {symbol}: {e}")

    return result

def filter_rsi(data, symbols):
    result = []

    for symbol in symbols:
        try:
            temp = data[data['Symbol'] == symbol]
            temp = rsi(temp, 4)
            temp = sma(temp, 200)
            current_average = temp.sma200.iloc[-1]
            current_price = temp.Close.iloc[-1]
            current_rsi = temp.rsi.iloc[-1]
        except Exception as e:
            print(f"Cannot fetch {symbol}: {e}")
            continue

        if current_rsi < 40 and current_price < current_average:
            result.append(symbol)

    return result

# Load symbols from nifty100.csv
symbols_df = pd.read_csv("nifty100.csv")
symbols = symbols_df['Symbol'].values.tolist()

# Load data for the symbols
data = load_data(symbols)

# Filter volume spike and RSI
volume_spike_filtered = filter_volume_spike(data, symbols, percentage=2)
rsi_filtered = filter_rsi(data, symbols)
'''

