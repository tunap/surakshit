#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
from firebase import firebase
firebase = firebase.FirebaseApplication('https://surakshit-11.firebaseio.com')
data_d={}
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DEPART, PHONE, LOCATION = range(3)

def start(bot, update):
    reply_keyboard = [['Fire','Health','Police']]
    update.message.reply_text(
        'Hello, and welcome to Suraksha!'
	'What is your department?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return DEPART


def depart(bot, update):
    user = update.message.from_user
    data_d['dept']= update.message.text
    data_d['name']=user.first_name
    logger.info("Department of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me your phone number.',
                              reply_markup=ReplyKeyboardRemove())
    return PHONE


def phone(bot, update):
    user = update.message.from_user
    data_d['mobile']=update.message.text
    logger.info("Phone number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thanks! Now, send me your location please,')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    data_d['loc']=str(user_location.latitude)+','+str(user_location.longitude)
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Thanks, you have been succesfully registered!')
    print(data_d)
    result  = firebase.post('/provider',data_d)
    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("504173349:AAGOsv_bfarAFAwEMBbebvp5TgSP7jGnOmc")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            DEPART: [RegexHandler('^(Fire|Health|Police)$', depart)],

            PHONE: [MessageHandler(Filters.text, phone)],                   

            LOCATION: [MessageHandler(Filters.location, location)]        
            
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
   
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
