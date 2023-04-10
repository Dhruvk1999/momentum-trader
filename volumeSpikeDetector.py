# volume spike detector
import pandas as pd
import numpy as np
from datetime import date
from indicators import *
import yfinance as yf
import sys

#loading the data from the pre-existing csv file
#df=pd.read_csv("data500.csv")
symbols=pd.read_csv("nifty100.csv")
symbols=symbols['Symbol'].values.tolist()

def load_data():
    '''
    returns: pd.DataFrame
    takes: null
    symbols: nifty100 Index
    '''
    data=pd.DataFrame()
    # load data
    for symbol in symbols:
        try:
            temp = yf.download(symbol+".NS", start="2023-02-25", end=date.today())
            temp["Symbol"]=symbol
        # assign bool on spike on comparing with past moving average value
            temp_avg_vol=temp['Volume'].rolling(5).mean()
        #data['Vol_rise']=np.where(data['Volume']>2*avg_vol,1,0)
            data=pd.concat([data,temp])    
        except:
            print(f"Error in fetching the data for {symbol}")     
            
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
        
    

