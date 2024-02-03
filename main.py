#!/usr/bin/python3

import requests
import random
import re
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

def start(update, context) -> None:
	"""Displays a greeting and keyboard"""
	chat = update.effective_chat
	user = update.message.from_user
	context.bot.send_message(chat_id=chat.id,
							 text='Hello, ' + user.first_name + '!')
	keyboard = [
		[InlineKeyboardButton('I want a picture!', callback_data='1')],
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('How can I help?',
								reply_markup=reply_markup)
	logging.info(
		'Bot started by user {} {} (@{})'.format(
			user.first_name,
			user.last_name,
			user.username
		)
	)

def help(update, context) -> None:
	"""Displays help"""
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id,
							 text='/start - start\n/help - help')

def button(update, context) -> None:
	"""Processes clicks on the buttons"""
	query = update.callback_query
	query.answer()
	choice = query.data
	if choice == '1':
		query.edit_message_text(text='Write whatever comes to mind (but not too much!)')

def create(update, context) -> None:
	"""Create image"""
	chat = update.effective_chat
	
	user_message = update.message.text
	
	r = requests.post(
		"https://api.deepai.org/api/text2img",
		data={
		    'text': user_message,
		},
		# Put your api-key here
		headers={'api-key': ''}
	)

	context.bot.send_message(chat_id=chat.id,
							 text=r.json())
	keyboard = [
		[InlineKeyboardButton('I want a picture!', callback_data='1')],
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=chat.id,
							 text='What else?',
							 reply_markup=reply_markup)

def main() -> None:
	"""Starts a bot"""
	# Message to the terminal
	print('The bot is launched. Click Ctrl+C to stop')
	# Set logging
	format = '%(asctime)s %(levelname)s: %(message)s'
	logging.basicConfig(filename='applog.log', level=logging.INFO, format=format)
	# Token from BotFather
	token = ''
	# Create Updater
	updater = Updater(token)
	# Get Dispather for creating handlers
	dispatcher = updater.dispatcher
	# The handler of the command /start
	dispatcher.add_handler(CommandHandler('start', start))
	# The handler of the command /help
	dispatcher.add_handler(CommandHandler('help', help))
	# The handler of the command /create
	dispatcher.add_handler(CommandHandler('create', create))
	# The handler of the buttons
	dispatcher.add_handler(CallbackQueryHandler(button))
	# The handler of the new messages
	dispatcher.add_handler(MessageHandler(Filters.text, create))
	# Launch of listening messages
	updater.start_polling()
	# The handler of Ctrl+C
	updater.idle()

if __name__ == '__main__':
	main()
