from playsound import playsound
from GoogleNews import GoogleNews
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# coloring the table based on the price going up or down
def highlight_greaterthan(s, threshold, column):
    '''
    call like this
    result.loc['2023-03-15'].reset_index(drop=True).style.apply(highlight_greaterthan, threshold=1, column='upOrDown', axis=1)
    '''
    is_max = pd.Series(data=False, index=s.index)
    is_max[column] = s.loc[column] >= 1
    if(s.loc[column]>=1):
        return ['background-color: green' if is_max.any() else '' for v in is_max]
    else:
        return ['background-color: #ff0047'  for v in is_max]


def AlertRing():
    '''
    Plays the tone until 'i' is pressed twice
    '''
    while(True):
        try:
            playsound('bell.wav')
        except KeyboardInterrupt:
            break

def getIntrinsicValue(symbol):
    
    res=requests.get("https://www.attainix.com/ICTrackerDetail.aspx?stockcode="+symbol+".IN")

    soup=BeautifulSoup(res.text,'html.parser')

    intrinsicValue=soup.find(id='ctl00_PageContent_lbl_IntrinsicStockPrice')
    
    intrinsicValue=str(intrinsicValue.string)
    
    intrinsicValue = float(re.sub(',', '', re.sub('Rs. ', '', intrinsicValue)))
    
    return intrinsicValue
            
def getNews(searchTerm):

    # Creating object
    googlenews = GoogleNews(lang='en', region='US', period='7d')

    # Searching for news articles
    googlenews.search(searchTerm)

    # Getting first page of results
    results = googlenews.results()

    # Printing titles and links of articles
    for result in results:
        print(result['title'])
        print(result['link'])
        print()

    # Getting second page of results
    googlenews.get_page()
    results = googlenews.results()
    
    return googlenews.results()

