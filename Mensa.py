# -*- coding: utf-8 -*-

import urllib2, urllib
import telegram
from telegram.ext import Updater, CommandHandler
import re
import time

token = '278206043:AAH13RqZiG1AdqcUpTDNbtAB-N_bL9EGeR4'
link = "http://www.werkswelt.de/?id=ingo"


timestamp = 0

mensadata = []

days = ["today", "tomorrow"]

def getMensaData():
    global mensadata, timestamp
    # getting data every blabla minutes
    if (time.time() - timestamp) > (60 * 30):
        mensadata = []
        # open website
        for day in days:
            if day == "today":
                response = urllib2.urlopen(link).read()      
            else:
                value = ({'mybutton': 'vorwärts'})
                data = urllib.urlencode(value)
                req = urllib2.Request(link, data)
                response = urllib2.urlopen(req).read()
 
            result = []

            dateReg = re.compile(r'<h4>(.+?)</h4>', re.IGNORECASE)
            foodReg = re.compile(r'Speiseplan.*', re.IGNORECASE)
            pattern = re.compile(r'<\/br>(.*?)<\/br>(.*?)<\/br>.*?<\/br>\s+<\/br>', re.IGNORECASE)
            priceReg = re.compile(r'[\d,]+', re.IGNORECASE)

            food = foodReg.findall(response)[1]
            food = pattern.findall(food)
            date = dateReg.findall(response)[0]
            result.append(str(date))

            i = 1
            for elem in food:
                firstelem = re.sub(r"<sup>.*?<\/sup>", "", elem[0])
                price = priceReg.findall(elem[1])
                result.append("*Essen " + str(i) + " (" + price[0] + "€)*: " + firstelem)
                i = i + 1

            result = "\n".join(result)
            mensadata.append([day, result])
            timestamp = time.time()

    return mensadata            
# end function

# here for telegram bot

bot = telegram.Bot(token)
updater = Updater(token)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hallo, hier ist ihr THI-BOT")
def mealtoday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=getMensaData()[0][1], parse_mode=telegram.ParseMode.MARKDOWN)
def mealtomorrow(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=getMensaData()[1][1], parse_mode=telegram.ParseMode.MARKDOWN)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('meal', mealtoday))
dispatcher.add_handler(CommandHandler('mealtoday', mealtoday))
dispatcher.add_handler(CommandHandler('mealtomorrow', mealtomorrow))

updater.start_polling()

# end programm with ctrl+c
updater.idle()
