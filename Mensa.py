# -*- coding: utf-8 -*-

import urllib2, urllib
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import re
import time, datetime
import logging
from collections import deque

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# changing token for testing
token = '278206043:AAH13RqZiG1AdqcUpTDNbtAB-N_bL9EGeR4' # this is the right token
# token = '188956812:AAGfjGfm5kTKT9iktSsvim6Ue200dROFT2w' # juliantestbot token
link = "http://www.werkswelt.de/?id=ingo"

timestamp = 0

mensadata = []

days = deque(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

def getMensaData():
    global mensadata, timestamp
    # getting data every blabla minutes
    if (time.time() - timestamp) > (60 * 30):
        mensadata = []
        now = datetime.datetime.now()
        # open website
        for j in range(0,2):
            if days[j] == now.strftime('%A'):
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
            mensadata.append([days[j], result])
            timestamp = time.time()

    return mensadata            
# end function

# here for telegram bot

bot = telegram.Bot(token)
updater = Updater(token)
reply_markup = None
def createInlineButtons():
    global reply_markup

    keys = [[]]
    now = datetime.datetime.now()
    n = list(days).index(now.strftime('%A')) 
    # shifting the hole thing
    days.rotate(len(days) - n)

    for i in range(0, 2):
        if i is 0:
            keys[0].append(telegram.InlineKeyboardButton(text=days[i], callback_data=str(i)))
        else:
            keys[0].append(telegram.InlineKeyboardButton(text=days[i], callback_data=str(i)))
    reply_markup = telegram.InlineKeyboardMarkup(keys)

lastdata = ""
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hallo, hier ist ihr THI-BOT")
def mealtoday(bot, update):
    global lastdata
    createInlineButtons()
    lastdata = getMensaData()[0][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
def mealtomorrow(bot, update):
    global lastdata
    createInlineButtons()
    lastdata = getMensaData()[1][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

def button(bot, update):
    global lastdata
    query = update.callback_query
    data = getMensaData()[int(query.data)][1]
    if data is not lastdata:
        bot.editMessageText(chat_id=query.message.chat_id, text=data, message_id=query.message.message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
        lastdata = data
    else:
        pass
   

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('meal', mealtoday))
dispatcher.add_handler(CommandHandler('mealtoday', mealtoday))
dispatcher.add_handler(CommandHandler('mealtomorrow', mealtomorrow))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

# end programm with ctrl+c
updater.idle()
