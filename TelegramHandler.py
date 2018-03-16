# -*- coding: utf-8 -*-

import logging
import sys
import datetime
import telegram

from telegram.ext import *

from Mensa import getMensaData

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# check if token is given
if len(sys.argv) != 2:

    raise Exception("You need a token as argument")
token = sys.argv[1]

bot = telegram.Bot(token)
updater = Updater(token)
reply_markup = None
def createInlineButtons(txt, clbk):
    global reply_markup
    
    keys = [[]]
    now = datetime.datetime.now()
    keys[0].append(telegram.InlineKeyboardButton(text=txt, callback_data=str(clbk)))
    reply_markup = telegram.InlineKeyboardMarkup(keys)

lastdata = ""

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hallo, hier ist ihr THI-BOT")
def mealtoday(bot, update):
    global lastdata, reply_markup
    createInlineButtons("Vor",1)
    lastdata = getMensaData()[0][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)
    logging.log(logging.INFO,"send meal of today")


def mealtomorrow(bot, update):
    global lastdata

    #createInlineButtons()
    lastdata = getMensaData()[1][1]
    bot.sendMessage(chat_id=update.message.chat_id, text=lastdata, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup)

def button(bot, update):
    global lastdata, reply_markup
    query = update.callback_query
    data = getMensaData()[int(query.data)][1]
    if data is not lastdata:
        if int(query.data) is 1:
            createInlineButtons("Zurück",0)
        else:
            createInlineButtons("Vor",1)

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


updater.start_webhook(listen='127.0.0.1', port=5000, url_path=token)
updater.bot.set_webhook(url='https://julianst.de/' + token)


# end programm with ctrl+c
updater.idle()

