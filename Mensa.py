# -*- coding: utf-8 -*-

import urllib2
import telegram
from telegram.ext import Updater, CommandHandler
import re

token = '278206043:AAH13RqZiG1AdqcUpTDNbtAB-N_bL9EGeR4'
link = "http://www.werkswelt.de/?id=ingo"

response = urllib2.urlopen(link).read()

foodReg = re.compile(r'Speiseplan.*', re.IGNORECASE)
pattern = re.compile(r'<\/br>(.*?)<\/br>(.*?)<\/br>.*?<\/br>\s+<\/br>', re.IGNORECASE)
priceReg = re.compile(r'[\d,]+', re.IGNORECASE)

food = foodReg.findall(response)[1]
#print response
# print food
food = pattern.findall(food)
result = []
i = 1
for elem in food:
    firstelem = re.sub(r"<sup>.*?<\/sup>", "", elem[0])
    price = priceReg.findall(elem[1])
    result.append("*Essen " + str(i) + " (" + price[0] + "€)*: " + firstelem)
    i = i + 1

result = "\n".join(result)
print result

# here for telegram bot

bot = telegram.Bot(token)
updater = Updater(token)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hallo, hier ist ihr THI-BOT")
def meal(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=result, parse_mode=telegram.ParseMode.MARKDOWN)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('meal', meal))

updater.start_polling()
