# -*- coding: utf-8 -*-

import sys
import urllib2, urllib
import re
import datetime, time

link = "http://www.werkswelt.de/?id=ingo"

timestamp = 0

mensadata = []


def getMensaData():
    global mensadata, timestamp
    # getting data every blabla minutes

    if (time.time() - timestamp) > (60 * 30):
    
        mensadata = []
        now = datetime.datetime.now()

        counter = 0

        while counter < 2:

            if counter == 1:
                value = ({'mybutton': 'vorwärts'})
                data = urllib.urlencode(value)
                req = urllib2.Request(link, data)
                response = urllib2.urlopen(req).read()
            else:
                response = urllib2.urlopen(link).read() 
    
             
            result = []

            dateReg = re.compile(r'<h4>(.+)</h4>', re.IGNORECASE)
            foodReg = re.compile(r'Essen \d<\/br>(.*?)<\/br>(\d,\d{2})', re.IGNORECASE)
            pattern = re.compile(r'<\/br>(.*?)<\/br>(.*?)<\/br>.*?<\/br>\s+<\/br>', re.IGNORECASE)

            food = foodReg.findall(response)
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

        timestamp = time.time()

    return mensadata            
# end function

# here for telegram bot


