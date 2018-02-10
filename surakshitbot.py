from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

ASSIST, LOCATE, ADDRESS, PIC, DESC, PHONE = range(6)

def start(bot, update):
	reply_keyboard = [['Fire', 'Health', 'Police']]

	update.message.reply_text('Hello, and welcome to Surakshit! \n' 'Please select what kind of assistace do you require: ',
		reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	return ASSIST

def assist(bot, update):
	user = update.message.from_user
	logger.info("%Assistance required by %s: %s", user.first_name, update.message.text)
	update.message.reply_text('Understood. \n' 'Please send me your location, \n' 'or send /skip if you do not want to.',
		reply_markup=ReplyKeyboardRemove())

	return LOCATE

def locate(bot, update):
	user = update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
	update.message.reply_text(
		'We have received your coordinates. \n' 'Please tell us the address where you require assistance.')

	return ADDRESS

def skip_locate(bot, update):
	user = update.message.from_user
	logger.info("User %s did not send a location.", user.first_name)
	update.message.reply_text('No worries. \n'
		'Please tell us the address where you require assistance.')

	return ADDRESS

def address(bot, update):
	user = update.message.from_user###
	logger.info("Address of %s: %s", user.first_name, update.message.text)
	update.message.reply_text('Thank you! \n'
		'Assistance is on the way. \n'
		'Please send us a photograph of the condition if possible \n'
		'or send /skip, if not.')

	return PIC

def pic(bot, update):
	user = update.message.from_user
	chat_id = update.message.chat_id
	photo_file = bot.get_file(update.message.photo[-1].file_id)
	photo_file.download(str(chat_id)+'.jpg')
	logger.info("Photo of %s: %s", user.first_name, str(chat_id)+'.jpg')
	update.message.reply_text('Great! \n'
		'Please give us a little description, if possible. \n'
		'If not, send /skip.')

	return DESC

def skip_pic(bot, update):
	user = update.message.from_user
	logger.info("User %s did not send a photo.", user.first_name)
	update.message.reply_text('No worries! \n'
		'Please give us a little description, if possible. \n'
		'If not, send /skip.')

	return DESC

def desc(bot, update):
	user = update.message.from_user
	logger.info("Description of %s: %s", user.first_name, update.message.text)
	update.message.reply_text('Thank you! \n'
		'Please be calm, assistance is on the way. \n'
		'What is your phone number?')

	return PHONE

def skip_desc(bot, update):
	user = update.message.from_user
	logger.info("User %s did not send any description.", user.first_name)
	update.message.reply_text('No worries! \n'
		'Please be calm, assistance is on the way. \n'
		'What is your phone number?')

	return PHONE

def phone(bot, update):
	user = update.message.from_user
	logger.info("Phone number of %s: %s", user.first_name, update.message.text)
	update.message.reply_text('Thank you! \n'
		'Please be calm, assistance is on the way. \n'
		'Details will be sent to you shortly.')

	return ConversationHandler.END

# def details(bot, update):
# 	user = update.message.from_user
# 	logger.info("Details are being sent to %s.", user.first_name)
# 	update.message.reply_text('Please be calm, assistance is on the way. \n'
		

# 		#DETAILS devyanshu dedo					<----------------------------------------------------------

		
# 		)

# 	return ConversationHandler.END


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
	updater = Updater("525927659:AAGE5gJ3A00uLHt7F8iBSK-nrh7Ptrlxdrs")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],

		states={
			# START: [RegexHandler('^(ENTER)$', start)],

			ASSIST: [RegexHandler('^(Fire|Health|Police)$', assist)],

			LOCATE: [MessageHandler(Filters.location, locate),
					CommandHandler('skip', skip_locate)], 

			ADDRESS: [MessageHandler(Filters.text, address)],

			PIC: [MessageHandler(Filters.photo, pic),
					CommandHandler('skip', skip_pic)],

			DESC:  [MessageHandler(Filters.text, desc),
					CommandHandler('skip', skip_desc)],

			PHONE: [MessageHandler(Filters.text, phone)],
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
