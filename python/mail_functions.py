from ElasticEmailClient import ApiClient, Email
import mysql.connector
import csv
from datetime import datetime, timedelta

def priceMailer(apikey, from_email, notification, periods, maxchng, direction, period_modifier, period_label, cooldown):
    notification = str(notification)
    periods = str(periods)
    maxchng = str(maxchng)
    
    try:
        #open connection to sql server
        cnx = mysql.connector.connect(user='python', password='nDM3KQyRmpmFNgAAvvve7488474yggvg', host='127.0.0.1', database='email_list', port='8889')
        cursor = cnx.cursor()
        
        #find emails at specified notification level
        search = "SELECT `email` FROM `email_list` WHERE `" + direction + notification + "` = '1' AND `lastemail` < '" + (datetime.now() - timedelta(minutes=cooldown)).strftime('%Y-%m-%d %H:%M:%S') + "';"
        cursor.execute(search)
        emails = cursor.fetchall()
    
        #if there are new emails update sql and send emails
        if emails != []:
        
            #reset cooldown period
            update = "UPDATE `email_list`.`email_list` SET `lastemail` = CURRENT_TIMESTAMP, `lastemail%` = '" + notification + "', `lastmodified` = CURRENT_TIMESTAMP WHERE `" + direction + notification + "` = '1' AND `lastemail` < '" + (datetime.now() - timedelta(minutes=cooldown)).strftime('%Y-%m-%d %H:%M:%S') + "';"
            cursor.execute(update)
            cnx.commit()
            cursor.close()
            cnx.close()
    
            #create csv with email adresses
            with open( direction + notification + 'emails.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(['"ToEmail"'])
                wr.writerows(emails)

            #send emails using api
            ApiClient.apiKey = apikey
            subject = 'BTC Warning: the price is' + direction + ' ' + notification + '.'
            fromEmail = from_email
            fromName = 'BTC Warning'
            bodyText = ''
            bodyHtml = '<div style="background-color:#f4d167;"><!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"><v:fill type="tile" src="btcwarning.halfmoonsoftware.com/images/formbackground.png" color="#7bceeb"/></v:background><![endif]--><table height="100%" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td valign="top" align="left" background="btcwarning.halfmoonsoftware.com/images/formbackground.png"><div style="position: relative; background-color: rgba(179, 182, 188, 0.9); width: 56%; padding: 6%; border-radius: 50px; display: inline-block; font-size: 2vw; margin: 5% 16% 5% 16%;"><div style="text-align: center;font-size: 3vw;">The price of bitcoin has gone ' + direction + ' ' + maxchng + '% in the past ' + '%.0f' % (periods * period_modifier) + ' ' + period_label + '! We\'ll keep an eye on it and let you know if it reaches any of your other notification levels.</div></div><div style="background-color: rgba(179, 182, 188, 0.9); padding: 1%; border-radius: 20px; position: fixed; width:30%; bottom: 0; margin: 0% 35% 0% 35%; text-align:center; display: inline-block"><div>&nbsp;<a href="btcwarning.halfmoonsoftware.com/unsubscribe.html">Unsubscribe from BTC Warnings</a>&nbsp;</div><div>&nbsp;<a href="{unsubscribe}">Block messages from this mailer</a></div></div></td></tr></table></div>'
            files = { direction + notification + 'emails.csv'}
            filenameWithRecipients = direction + notification + 'emails.csv' 
            
            emailResponse = Email.Send(subject, fromEmail, fromName, bodyText = bodyText, bodyHtml = bodyHtml, attachmentFiles = files, mergeSourceFilename = filenameWithRecipients)
            
            #print results
            print("----------", notification, "% ", direction, " notification sent.", sep="")            

            try:
                print('----------MsgID to store locally: ')
                print('---------------', emailResponse['messageid'], " (available only for single recipient messages)", sep="")#Available only if sent to a single recipient
                print('----------TransactionID to store locally: ')
                print('---------------', emailResponse['transactionid'], sep="")
            except TypeError:
                    print('----------Server returned an error: ', emailResponse)
        else:
            cursor.close()
            cnx.close()
            print("-----------No Users at ", direction, " ", notification, "% outside of cooldown.", sep="", end="\n\n")
    except Exception as e:
        print(e)
    
def rsiMailer(apikey, from_email, rsitoday, rsimeaning):
    rsitoday = str(rsitoday)
    
    try:
        #open connection to sql server
        cnx = mysql.connector.connect(user='python', password='nDM3KQyRmpmFNgAAvvve7488474yggvg', host='127.0.0.1', database='email_list', port='8889')
        cursor = cnx.cursor()
        
        #find needing rsi notification
        search = "SELECT `email` FROM `email_list` WHERE `rsi` = '1';"
        cursor.execute(search)
        emails = cursor.fetchall()
    
        #if there are new emails update sql and send emails
        if emails != []:
    
            #create csv with email adresses
            with open( 'rsiemails.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(['"ToEmail"'])
                wr.writerows(emails)

            #send emails using api
            ApiClient.apiKey = apikey
            subject = 'BTC Warning RSI Notification'
            fromEmail = from_email
            fromName = 'BTC Warning'
            bodyText = ''
            bodyHtml = '<div style="background-color:#f4d167;"><!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"><v:fill type="tile" src="btcwarning.halfmoonsoftware.com/images/formbackground.png" color="#7bceeb"/></v:background><![endif]--><table height="100%" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td valign="top" align="left" background="btcwarning.halfmoonsoftware.com/images/formbackground.png"><div style="position: relative; background-color: rgba(179, 182, 188, 0.9); width: 56%; padding: 6%; border-radius: 50px; display: inline-block; font-size: 2vw; margin: 5% 16% 5% 16%;"><div style="text-align: center;font-size: 3vw;">Bitcoin\'s rsi is ' + rsitoday + '. This indicates that bitcoin ' + rsimeaning + '!</div></div><div style="background-color: rgba(179, 182, 188, 0.9); padding: 1%; border-radius: 20px; position: fixed; width:30%; bottom: 0; margin: 0% 35% 0% 35%; text-align:center; display: inline-block"><div>&nbsp;<a href="btcwarning.halfmoonsoftware.com/unsubscribe.html">Unsubscribe from BTC Warnings</a>&nbsp;</div><div>&nbsp;<a href="{unsubscribe}">Block messages from this mailer</a></div></div></td></tr></table></div>'
            files = {'rsiemails.csv'}
            filenameWithRecipients = 'rsiemails.csv' 
            
            emailResponse = Email.Send(subject, fromEmail, fromName, bodyText = bodyText, bodyHtml = bodyHtml, attachmentFiles = files, mergeSourceFilename = filenameWithRecipients)
            
            #print results
            print("----------RSI Notification Sent.")
            
            try:
                print('----------MsgID to store locally: ')
                print('---------------', emailResponse['messageid'], " (available only for single recipient messages)", sep="")#Available only if sent to a single recipient
                print('----------TransactionID to store locally: ')
                print('---------------', emailResponse['transactionid'], sep="")
            except TypeError:
                    print('----------Email server returned an error: ', emailResponse)
        else:
            cursor.close()
            cnx.close()
            print("----------No RSI users")
    except Exception as e:
        print(e)      
    
def confirmEmails(apikey, from_email):
    try:
        #open connection to sql server
        cnx = mysql.connector.connect(user='python', password='nDM3KQyRmpmFNgAAvvve7488474yggvg', host='127.0.0.1', database='email_list', port='8889')
        cursor = cnx.cursor()
        
        #find new emails to confirm
        search = "SELECT `email` FROM `email_list` WHERE `confirmationsent` = 0;"
        cursor.execute(search)
        emails = cursor.fetchall()
    
    
        #if there are new emails update sql and send emails
        if emails != []:
        
            #mark validation as sent in sql
            update = "UPDATE `email_list`.`email_list` SET `confirmationsent` = 1, `lastmodified` = CURRENT_TIMESTAMP WHERE `email_list`.`confirmationsent` = 0;"
            cursor.execute(update)
            cnx.commit()
            cursor.close()
            cnx.close()
    
            #create csv with email adresses
            with open('confirmationemails.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(['"ToEmail"'])
                wr.writerows(emails)

            #send emails using api
            ApiClient.apiKey = apikey
            subject = 'BTC Warning Email Confirmation'
            fromEmail = from_email
            fromName = 'BTC Warning'
            bodyText = ''
            bodyHtml = '<div style="background-color:#f4d167;"><!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"><v:fill type="tile" src="btcwarning.halfmoonsoftware.com/images/formbackground.png" color="#7bceeb"/></v:background><![endif]--><table height="100%" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td valign="top" align="left" background="btcwarning.halfmoonsoftware.com/images/formbackground.png"><div style="position: relative; background-color: rgba(179, 182, 188, 0.9); width: 56%; padding: 6%; border-radius: 50px; display: inline-block; font-size: 2vw; margin: 5% 16% 5% 16%;"><div style="text-align: center;font-size: 3vw;">Thanks for signing up!</div></div><div style="background-color: rgba(179, 182, 188, 0.9); padding: 1%; border-radius: 20px; position: fixed; width:30%; bottom: 0; margin: 0% 35% 0% 35%; text-align:center; display: inline-block"><div>&nbsp;<a href="btcwarning.halfmoonsoftware.com/unsubscribe.html">Unsubscribe from BTC Warnings</a>&nbsp;</div><div>&nbsp;<a href="{unsubscribe}">:&#40;</a></div></div></td></tr></table></div>'
            files = { 'confirmationemails.csv' }
            filenameWithRecipients = 'confirmationemails.csv' 
            
            emailResponse = Email.Send(subject, fromEmail, fromName, bodyText = bodyText, bodyHtml = bodyHtml, attachmentFiles = files, mergeSourceFilename = filenameWithRecipients)
            
            #print completion
            print("----------Confirmation emails sent.")

            try:
                print('----------MsgID to store locally: ')
                print('---------------', emailResponse['messageid'], " (available only for single recipient messages)", sep="")#Available only if sent to a single recipient
                print('----------TransactionID to store locally: ')
                print('---------------', emailResponse['transactionid'], sep="")
            except TypeError:
                    print('----------Email server returned an error: ', emailResponse)
        else:
            cursor.close()
            cnx.close()
            print("----------No new users.")
    except Exception as e:
        print(e)
    