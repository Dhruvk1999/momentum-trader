import yfinance as yf
import pandas as pd
import numpy as np

# data collection

def get_individual_data(symbol,start,end):
    return yf.download(symbol,start,end)

def get_sectoral_data(sector_name, start, end):
    # Read symbols from the CSV file
    symbols = list(pd.read_csv(sector_name + ".csv")["Symbol"])
    
    data = pd.DataFrame()
    
    for symbol in symbols:
        # Download historical stock data using yfinance
        stock_data = yf.download(symbol+".NS", start=start, end=end)
        
        # Add a column to the data indicating the symbol
        stock_data['Symbol'] = symbol
        
        # Append the stock data to the main data DataFrame
        data = data.append(stock_data)
    
    return data

def get_cluster_based_group_data(symbols,start,end):
    ## implement a clustering algorithm to cluster the stocks into some logical groups
    pass
    


    
    