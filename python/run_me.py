from os import remove
from datetime import datetime, timedelta
from mail_functions import confirmEmails 
from notification_functions import checkPrice, checkRSI

#mailer options
apikey = #enter your elastic email api key
from_email = #enter the address to send messages from eg. mail.example.org

#timing options
confirmationfreq = 20 #seconds between new user checks/confirmations
pricefreq = 60 #seconds between price change checks in seconds (too low may be blocked by APIs keep >= 10)
rsifreq = 720 #minutes between rsi notifications (every check sends an email. recommend > 60)

#rsi options
data_window_length = 730 #observation window in days (too low may underestimae rsi)
rsi_window_length = 14 #moving average window in days (standard is 14)

#price options
price_window = 60 #number of prices to keep in memory
cooldown = 15 #cooldown period in minutes for price change emails

#delete old price data on startup. protects from incorrect results on startup
#missing file error is expected and compensated for
try:
    remove('btcprices.csv')
except Exception as e:
    print("----------", e, sep=="")

"""
The rest of this file should not be changed. 


"""

#adjust price period label
if pricefreq >=60:
    period_modifier = pricefreq / 60
    period_label = "minutes"
else:
    period_modifier = pricefreq
    period_label = "seconds"

#initialize times
lastconfirmation = datetime.now()
lastrsi = datetime.now()
lastprice = datetime.now()

#send confirmation emails
print("\nChecking for new emails...")
confirmEmails(apikey, from_email)

#send rsi notifications
print("\nSending RSI notifications...")
checkRSI(apikey, from_email, data_window_length, rsi_window_length)

#check for price changes 
print("\nChecking for new price changes...")
checkPrice(apikey, from_email, price_window, period_modifier, period_label, pricefreq, cooldown)
        
#inifite loop to check at specified intervals
while True:
    #send confirmation emails
    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > (lastconfirmation + timedelta(seconds=confirmationfreq)).strftime('%Y-%m-%d %H:%M:%S'):
        lastconfirmation = datetime.now()
        print("\nChecking for new emails...")
        confirmEmails(apikey, from_email)
        
    #send rsi notifications
    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > (lastrsi + timedelta(minutes=rsifreq)).strftime('%Y-%m-%d %H:%M:%S'):
        print("\nSending RSI notifications...")
        lastrsi = datetime.now()
        checkRSI(apikey, from_email, data_window_length, rsi_window_length)
        
    #check for price changes 
    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > (lastprice + timedelta(seconds=pricefreq)).strftime('%Y-%m-%d %H:%M:%S'):
        lastprice = datetime.now()
        print("\nChecking for new price changes...")
        checkPrice(apikey, from_email, price_window, period_modifier, period_label, pricefreq, cooldown)
        
    
        
    
