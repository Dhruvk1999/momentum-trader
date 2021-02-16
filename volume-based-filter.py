# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:52:02 2021

@author: Dhruv
"""
import pandas as pd
import numpy as np
from nsepy import get_history
from datetime import date

codes=pd.read_csv('midcap.csv')
codes=codes['Symbol'].to_list()
temp=pd.DataFrame()
for stock in codes:
    
    sbin=get_history(stock,start=date(2021,1,9),end=date(2021,2,16))
    
    sbin=sbin.drop([ 'Series', 'High', 'Low', 'Last', 'VWAP', 'Turnover', 'Trades','%Deliverble'],axis=1)
    
    sbin['call'] = np.where((sbin['Close'] >= sbin['Prev Close']) , 1, 0)
    
    avg_vol=sbin['Volume'].rolling(5).mean()
    
    sbin['Vol_rise']=np.where(sbin['Volume']>2*avg_vol,1,0)
    
    sbin['Final Call']=np.where(sbin['call']*sbin['Vol_rise'],'Buy','Sell')
    
    b=sbin[sbin['Final Call']=='Buy']
    
    temp=pd.concat([temp,b])

