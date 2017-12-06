from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
	InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging
import chemistry
from chemistry import Chemistry
def token():
	directory = "C:\\Users\\Roberto\\Desktop\TOKEN.txt"
	with open(directory) as text_object:
		token = text_object.read().strip()
	return token


start_message = "Welcome to Roberto's bot, write '/help' to get the list of commands."
TOKEN = token()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=start_message)

def balance(bot, update, args):
	equation = "".join(args)
	user = Chemistry(equation)
	if user.check_equation():
		# if the equation is written right
		balanced = user.balance()
		if balanced == False:
			# if something went wrong during the balance
			bot.send_message(chat_id=update.message.chat_id, text="Something"
							 " went wrong during the balance of the equation."
							 )
			equation_example(bot, update)
		else:
			# went all right
			bot.send_message(chat_id=update.message.chat_id, text=balanced)
	else:
		# if the equation isn't written right
		bot.send_message(chat_id=update.message.chat_id, text="Something went "
						 "wrong during the balance of the equation."
						 )
		equation_example(bot, update)

def checkbalance(bot, update, args):
	equation = "".join(args)
	user = Chemistry(equation)
	if user.check_equation():
		# if equation is written right
		balanced = user.printifBalanced()
		if balanced == False:
			# if something went wrong during the balance
			bot.send_message(chat_id=update.message.chat_id,
							 text=chemistry.balance_error
							 )
			equation_example(bot, update)
		else:
			# if it went all right
			bot.send_message(chat_id=update.message.chat_id, text=balanced)
	else:
		# if equation wasn't written right
		bot.send_message(chat_id=update.message.chat_id,
						 text=chemistry.balance_error
						 )
		equation_example(bot, update)

def equation_example(bot, update):
	# quick shortcut
	bot.send_message(chat_id=update.message.chat_id,
					 text=chemistry.equation_example)

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry I don't know "
					 "that command"
					 )

def getElements(bot, update, args):
	equation = "".join(args)
	user = Chemistry(equation)
	if user.check_equation():
		# if equation is written right
		elements = user.returnElements()
		if elements == False:
			# if something went wrong during the balance
			bot.send_message(chat_id=update.message.chat_id,
							 text=chemistry.balance_error
							 )
			equation_example(bot, update)
		else:
			# if it went all right
			bot.send_message(chat_id=update.message.chat_id, text=elements)
	else:
		# if equation wasn't written right
		bot.send_message(chat_id=update.message.chat_id,
						 text=chemistry.balance_error
						 )
		equation_example(bot, update)

def help(bot, update):
	help_str = ""
	with open("help.txt", "r") as file:
		for line in file:
			help_str += line
	bot.send_message(chat_id=update.message.chat_id, text=help_str)

start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
balance_handler = CommandHandler("balance", balance, pass_args=True)
ifbalance_handler = CommandHandler("checkbalance", checkbalance, pass_args=True)
getElements_handler = CommandHandler("getElements", getElements, pass_args=True)
unknow_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(help_handler)
dispatcher.add_handler(getElements_handler)
dispatcher.add_handler(balance_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(ifbalance_handler)
dispatcher.add_handler(unknow_handler)
print("Listening...")
updater.start_polling()