# -*- coding: utf-8 -*-

import sys
import requests
import re
import datetime, time
import logging


link = "http://www.werkswelt.de/?id=ingo"

timestamp = 0

mensadata = []

logger = logging.getLogger()

def getMensaData():
    global mensadata, timestamp
    # getting data every blabla minutes

    if (time.time() - timestamp) > (60 * 30):
        session = requests.Session()
        mensadata = []
        now = datetime.datetime.now()

        counter = 0
        noFoodOnWebsite = False

        while True:
            
            # counter >= 1 means iterating with the button through the website
            if counter >= 1:

                headers = {'Content-type': 'application/x-www-form-urlencoded'}
                data = {'mybutton':'vorwärts'}
                newresponse = session.post(link,data=data, headers=headers)

                r = newresponse               
                
                logger.log(logging.INFO,"requests")
         
                response = r.text
                
            else:
                r = session.post(link)
                response = r.text
    
            result = []

            dateReg = re.compile(r'<h4>(.+)</h4>', re.IGNORECASE)
            foodReg = re.compile(r'Essen \d<\/br>(.*?)<\/br>(\d,\d{2})', re.IGNORECASE)
            pattern = re.compile(r'<\/br>(.*?)<\/br>(.*?)<\/br>.*?<\/br>\s+<\/br>', re.IGNORECASE)

            food = foodReg.findall(response)
            
            if counter >= 1:
                logger.log(logging.INFO,"will raus davor" + date)
                try:
                    newdate = dateReg.findall(response)[0]
                except IndexError:
                    logger.log(logging.INFO,"now Date on website is missing")
                    noFoodOnWebsite = True
                    newdate = None

                if date == newdate:
                    logger.log(logging.INFO,"will raus")
                    break

            if noFoodOnWebsite is False:
                date = dateReg.findall(response)[0] 
                    
                result.append(str(date))    
                i = 1
                for elem in food:
                    firstelem = re.sub(r"<sup>.*?<\/sup>", "", elem[0])
                    result.append("*Essen " + str(i) + " (" + elem[1] + "€)*: " + firstelem)
                    i = i + 1

                result = "\n".join(result)
                mensadata.append([now.day,result])

                counter += 1
            noFoodOnWebsite = False
        timestamp = time.time()

    return mensadata            
# end function

