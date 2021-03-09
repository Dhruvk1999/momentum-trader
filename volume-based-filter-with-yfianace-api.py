# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:05:54 2021

@author: Dhruv
"""

import pandas as pd
import numpy as np
from datetime import datetime
from yahoo_finance_api import YahooFinance as yf

codes=pd.read_csv('nifty500.csv')
codes=codes['Symbol'].to_list()
temp=pd.DataFrame()

for stock in codes:
    
    sbin=yf((stock+'.NS'),result_range='1mo',interval='1d',dropna='True').result
    sbin['Symbol']=stock
  #  sbin=sbin.drop([ 'Series', 'High', 'Low', 'Last', 'VWAP', 
 #                   'Turnover', 'Trades','%Deliverble'],axis=1)
    
    sbin['call'] = np.where((sbin['Close'] >= sbin['Open']) , 1, 0)
    
    avg_vol=sbin['Volume'].rolling(5).mean()
    
    sbin['Vol_rise']=np.where(sbin['Volume']>2*avg_vol,1,0)
    
    sbin['Final Call']=np.where(sbin['call']*sbin['Vol_rise'],'Buy','Sell')
    
    b=sbin[sbin['Final Call']=='Buy']
    
    
    temp=pd.concat([temp,b])
    
    #op=temp.loc[date(year=2021,month=2,day=16)]
    #temp=temp[(temp['Open']+(0.02*temp['Open']))<temp['Close']] (percentage = 3)
