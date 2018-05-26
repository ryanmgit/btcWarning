import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from talib import RSI
from mail_functions import priceMailer, rsiMailer
from deribit_api import RestClient


def checkRSI(apikey, from_email, data_window_length, rsi_window_length):#window length for data and window length for moving average are passed through
    try:
        #create start and end dates
        start = (datetime.now() - timedelta(days=data_window_length)).strftime('%Y-%m-%d')
        end = datetime.now().strftime('%Y-%m-%d')
        

        #get closing price data
        symbol = 'BITSTAMP/USD'
        btc = web.DataReader(symbol, 'quandl', start, end)['Last']
        
        #make into numpy array
        close = btc.values
        
        #use TA-lib to calculate rsi
        array = RSI(close, timeperiod=rsi_window_length)
        
        #graph last 2 years
        #plt.figure()
        #plt.plot(array)
        #plt.show()

        #get last month
        #lastmonth = array[-31:]

        #graph last month 
        #plt.figure()
        #plt.plot(lastmonth)
        #plt.show()
        
        #get todays rsi
        rsitoday = round( array[-1], 2)
        
        
        #interpret rsi meaning
        if rsitoday >= 70:
            rsimeaning = "is overbought"
        elif 70 > rsitoday > 50:
            rsimeaning = "is trending towards being overbought"
        elif rsitoday == 50:
            rsimeaning = "shows no trend"
        elif 50 < rsitoday < 30:
            rsimeaning = "is trending towards being overbought"
        elif rsitoday <= 30:
            rsimeaning = "is oversold"
        
        print("----------The RSI is ", rsitoday, " which indicates that bitcoin ", sep="")
        print("---------------", rsimeaning, sep="")
        
        #send rsi notification emails
        rsiMailer(apikey, from_email, rsitoday, rsimeaning)
        
    except Exception as e:
        print(e)
        

def checkPrice(apikey, from_email, price_window, period_modifier, period_label, pricefreq, cooldown): 
    try:
        #read csv file with recent prices
        pricedf = pd.read_csv('btcprices.csv', index_col=0)
       
        #get current price from api
        client = RestClient()
        index = client.index()
        price = index['btc']       

        #add new price to dataframe
        newprice = {'price' : price}
        newpricedf = pd.DataFrame(newprice, index=[datetime.utcnow()])
        pricedf = pricedf.append(newpricedf)
        

        #keep only last 60 prices
        if len(pricedf) > price_window:
            pricedf.drop(pricedf.index[0], inplace=True)
        length = len(pricedf)
        
        #write out to csv
        pricedf.to_csv('btcprices.csv')
        
        #initialize variables
        maxchng = 0
        periods = 0
        direction = ""
        
        #collect at least 3 datapoints before calculating 
        if len(pricedf) < 4:
            print("----------More data needed for accurate results")
        else:
            #calculate max price change
            for i in range(-2, -length, -1):
                chng = (pricedf["price"].iloc[-1] - pricedf["price"].iloc[i]) / pricedf["price"].iloc[i]
                if abs(chng) > abs(maxchng):
                    maxchng = chng
                    periods = -i -1
            
            #make percentage
            maxchng = maxchng * 100
            
            #assign direction of price change
            if maxchng > 0:
                direction = "up"
            elif maxchng < 0:
                direction = "down"
            
            #round percentage
            maxchng = round( abs(maxchng), 2)
            
            #modify label when appropriate
            if periods == 1 and period_label == "minutes":
                period_label = period_label[:-1]
            if period_label == "seconds" and periods * period_modifier > 119:
                period_label = "minutes"
                period_modifier = pricefreq/60
                
            #print results    
            print("----------The price has gone ", direction, " ", maxchng, "% in the past ", '%.0f' % (periods * period_modifier), " ", period_label, ".", sep="")
        
            #check and send mail if price changes sufficiently
            if maxchng > 30:
                priceMailer(apikey, from_email, 30, periods, maxchng, direction, period_modifier, period_label, cooldown)
            elif maxchng > 25:
                priceMailer(apikey, from_email, 25, periods, maxchng, direction, period_modifier, period_label, cooldown)
            elif maxchng > 20:
                priceMailer(apikey, from_email, 20, periods, maxchng, direction, period_modifier, period_label, cooldown)
            elif maxchng > 15:
                priceMailer(apikey, from_email, 15, periods, maxchng, direction, period_modifier, period_label, cooldown)
            elif maxchng > 10:
                priceMailer(apikey, from_email, 10, periods, maxchng, direction, period_modifier, period_label, cooldown)
            elif maxchng > 5:
                priceMailer(apikey, from_email, 5, periods, maxchng, direction, period_modifier, period_label, cooldown)
                
    except (IOError, OSError):
        print("----------Error: btcprices.csv could not be found or is corrupted.")
        print("----------Creating new file....")
        
        #get current price from api
        client = RestClient()
        index = client.index()
        price = index['btc']   
        
        #create new dataframe and csv
        newdf = {'price' : price}
        pricedf = pd.DataFrame(newdf, index=[datetime.utcnow()])
        pricedf.to_csv('btcprices.csv')
        print("----------New file created.")
    
    except Exception as e:
        print(e)
        