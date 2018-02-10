from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, ASSIST, LOCATE, ADDRESS, PIC, DESC, PHONE, DETAILS = range(8)

def intro(bot, update):
	reply_markup=ReplyKeyboardRemove()

	update.message.reply_text('Hello, and welcome to Surakshit!')

	return START

def start(bot, update):
	reply_keyboard = [['YES', 'NO']]

	update.message.reply_text('Hello, and welcome to Surakshit!',
		'Do you require any assistance?')
	reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

	return ASSIST

def assist(bot, update):
	reply_keyboard = [['Fire Fighters', 'Health Related', 'Police']]

	user = update.message.from_user
	logger.info("%s requires assistance!", user.first_name, update.message.text)
	update.message.reply_text('Please select what kind of assistace do you require: ')
	reply_markup=ReplyKeyboardRemove(reply_keyboard, one_time_keyboard=True)
	update.message.reply_text(
		'Understood.'
    	'Please send me your location, '
    	'or send /skip if you do not want to.')

	return LOCATE

def not_assist(bot, update):
	user = update.message.from_user
	logger.info("User %s does not require assistance.", user.first_name)
	update.message.reply_text(
		'Send /start if you want to re-initiate the chat!'
		'Stay safe, Stay Happy.')
	reply_markup=ReplyKeyboardRemove()

	return ConversationHandler.END

def locate(bot, update):
	user = update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text('We have received your coordinates.'
    	'Please tell us the address where you require assistance.')

    return ADDRESS

def skip_locate(bot, update):
	user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('No worries. '
    	'Please tell us the address where you require assistance.')

    return ADDRESS

def address(bot, update):
	user = update.message.from_user
    logger.info("Address of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you!'
    	'Assistance is on the way.'
    	'Please send us a photograph of the condition if possible'
    	'or send /skip, if not.'
    	)

    return PIC

def pic(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('%z.jpg' %z message.chat.id)
    logger.info("Photo of %s: %s", user.first_name, '%z.jpg' %z message.chat.id)
    update.message.reply_text('Great! '
    	'Please give us a little description, if possible.'
        'If not, send /skip.')

    return DESC

def skip_pic(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('No worries! '
    	'Please give us a little description, if possible.'
        'If not, send /skip.')

    return DESC

def desc(bot, update):
    user = update.message.from_user
    logger.info("Description of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you!'
    	'Please be calm, assistance is on the way.'
    	'What is your phone number?')

    return PHONE

def skip_desc(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send any description.", user.first_name)
    update.message.reply_text('No worries! '
    	'Please be calm, assistance is on the way.'
        'What is your phone number?')

    return PHONE

def phone(bot, update):
	user = update.message.from_user
    logger.info("Phone number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you!'
    	'Please be calm, assistance is on the way.'
    	'Details will be sent to you shortly.')

    return DETAILS

def details(bot, update):
	user = update.message.from_user
	logger.info("Details are being sent to %s.", user.first_name)
	update.message.reply_text('Please be calm, assistance is on the way.'
    	

    	#DETAILS 					<----------------------------------------------------------

    	
    	)

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',)
    reply_markup=ReplyKeyboardRemove()

    return ConversationHandler.END
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("525927659:AAGE5gJ3A00uLHt7F8iBSK-nrh7Ptrlxdrs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher



    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('intro', intro)],

        states={
            START: [RegexHandler('YES', assist),
            		RegexHandler('NO', not_assist)],

            ASSIST: [MessageHandler(Filters.locate, locate),
                    CommandHandler('skip', skip_locate)], 

            LOCATE: [MessageHandler(Filters.address, address)],

            ADDRESS: [MessageHandler(Filters.pic, pic),
            		CommandHandler('skip', skip_pic)],

            PIC:  [MessageHandler(Filters.desc, desc),
            		CommandHandler('skip', skip_desc)],

            DESC: [MessageHandler(Filters.phone, phone)],

            DETAILS: [MessageHandler(Filters.text, details)]
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
