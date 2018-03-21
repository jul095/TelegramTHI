# -*- coding: utf-8 -*-

import logging
import sys
import datetime
import telegram
import argparse

from telegram.ext import *

from Mensa import getMensaData

reload(sys)  
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()


# check if token is given
parser = argparse.ArgumentParser(description='Python Telegram Mensa Bot')
parser.add_argument('-t','--token', help='token for the telegram bot',required=True)
parser.add_argument('-d','--debug', help='debug flag, change webhook mode to polling, enable info logging', required=False)
args = parser.parse_args()

token = args.token

if args.debug is not None:
    logger.setLevel(logging.INFO)

bot = telegram.Bot(token)
updater = Updater(token)
reply_markup = None

keys = [[]]
def createInlineButtons(txt, clbk):
    global reply_markup, keys
    
    now = datetime.datetime.now()
    keys[0].append(telegram.InlineKeyboardButton(text=txt, callback_data=str(clbk)))
    reply_markup = telegram.InlineKeyboardMarkup(keys)

lastdata = ""

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hallo, hier ist ihr THI-BOT")
def mealtoday(bot, update):
    global lastdata, reply_markup
    createInlineButtons("Vor",1)
    createInlineButtons("Zurück",0)
    lastdata = getMensaData()[0][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    logging.log(logging.INFO,"send meal of today")


def mealtomorrow(bot, update):
    global lastdata

    #createInlineButtons()
    lastdata = getMensaData()[1][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

currentPos = 1
def button(bot, update):
    global lastdata, reply_markup, currentPos
    query = update.callback_query
    
    
    length = len(getMensaData())
    
    data = getMensaData()[currentPos][1]

    if data is not lastdata:

        if currentPos is length-1:
            createInlineButtons("Zurück",0)
            currentPos -= 1
        else:
            createInlineButtons("Vor",1)
            currentPos += 1

        bot.editMessageText(chat_id=query.message.chat_id, text=data, message_id=query.message.message_id, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
        lastdata = data
        
        
    else:
        pass
    bot.answerCallbackQuery(callback_query_id=query.id)


dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('meal', mealtoday))
dispatcher.add_handler(CommandHandler('mealtoday', mealtoday))
dispatcher.add_handler(CommandHandler('mealtomorrow', mealtomorrow))
dispatcher.add_handler(CallbackQueryHandler(button))


if args.debug is None:
    updater.start_webhook(listen='127.0.0.1', port=5000, url_path=token)
    updater.bot.set_webhook(url='https://julianst.de/' + token)
else:
    updater.start_polling()

# end programm with ctrl+c
updater.idle()

