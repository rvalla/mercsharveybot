from telegram.ext import (
			Application, InlineQueryHandler, CommandHandler,
			CallbackQueryHandler, ContextTypes, ConversationHandler,
			MessageHandler, filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import traceback, logging
import json as js
from usage import Usage
from messages import Messages
from markets import Markets
from users import Users
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

#Filterint warnings about conversation handlers configuration...
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

print("Starting MERC's Harvey Bot...", end="\n")
config = js.load(open("config.json")) #The configuration file (token included)
us = Usage("usage.csv", "errors.csv") #The class to work with usage data...
msg = Messages() #The class to build content of text messages...
mk = Markets() #The class to access local and web data about the market...
users = Users("data/users/")
ABOUT, CHECKING, SETLIST_NAME, SETLIST_BCBA, SETLIST_WORLD, ERASE_LIST, ERASE_LIST_CONFIRM, \
	ERROR_1, ERROR_2 = range(9) #The general conversation states...

#Welcome message for people who start the bot...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " started the bot...")
	us.add_start()
	await context.bot.send_message(chat_id=id, text=msg.get_message("start", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_emoji("money_bag"), parse_mode=ParseMode.HTML)

#Starting an about company session...
async def trigger_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " starts about conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("start_about", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_analysis_emoji(), parse_mode=ParseMode.HTML)
	return ABOUT

#Looking for the last price for the sent symbol...
async def get_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	symbol = update.message.text.upper()
	data = None
	try:
		data = mk.get_symbol("BCBA", symbol)
	except:
		pass #Symbol is not in mk.bcba dictionary...
	if data == None:
		try:
			data = mk.get_symbol("WORLD", symbol)
		except:
			pass #Symbol is not in mk.world dictionary...
	if data != None and data["ready"] == True:
		message = msg.build_about_message(get_language(context), data)
		us.add_about(0)
	else:
		if data == None:
			message = msg.get_message("error_about", get_language(context))
		else:
			message = msg.get_message("refuse_about", get_language(context))
		us.add_about(1)
	await context.bot.send_message(chat_id=id, text=message, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
	return ABOUT

#Starting a checking prices session...
async def trigger_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	exchange = update.message.text.upper().split(" ")[0].split("@")[0][1:]
	logging.info(str(hide_id(id)) + " starts checking conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("start_check", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("info_check", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_analysis_emoji(), parse_mode=ParseMode.HTML)
	context.chat_data["actual_exchange"] = exchange
	return CHECKING

#Looking for the last price for the sent symbol...
async def get_last_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	exchange = context.chat_data["actual_exchange"]
	symbol = update.message.text.upper()
	try:
		data = mk.get_last_info(exchange, symbol)
		message = msg.build_last_info_message(get_language(context), exchange, data)
		await context.bot.send_message(chat_id=id, text=message, parse_mode=ParseMode.HTML)
		us.add_check(0)
	except:
		us.add_check(1)
		await context.bot.send_message(chat_id=id, text=msg.get_message("error_check", get_language(context)), parse_mode=ParseMode.HTML)
	return CHECKING

#Starting a watchlist setup session...
async def trigger_setlist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " wants to set up a watchlist...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("set_list_1", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("set_list_2", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_working_emoji(), parse_mode=ParseMode.HTML)
	if not "watchlists" in context.chat_data:
		context.chat_data["watchlists"] = []
	return SETLIST_NAME

#Deciding the list name...
async def name_for_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	list_name = update.message.text.replace(" ", "_").lower()
	context.chat_data["active_key"] = "wl_" + list_name
	if list_name in context.chat_data["watchlists"]:
		await context.bot.send_message(chat_id=id, text=msg.get_message("overwrite_set_list", get_language(context)), parse_mode=ParseMode.HTML)
	else:
		context.chat_data["watchlists"].append(list_name)
	context.chat_data[context.chat_data["active_key"]] = []
	await context.bot.send_message(chat_id=id, text=msg.get_message("set_list_3", get_language(context)), parse_mode=ParseMode.HTML)
	return SETLIST_BCBA

#Adding BCBA symbols to watchlist...
async def add_bcba_symbol_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	symbol = update.message.text.upper()
	if not symbol == "OK":
		is_in, currency = mk.check_symbol_and_currency("BCBA", symbol)
		if is_in:
			context.chat_data[context.chat_data["active_key"]].append(["BCBA", symbol, currency])
			await context.bot.send_message(chat_id=id, text=msg.get_selection(get_language(context)), parse_mode=ParseMode.HTML)
		else:
			await context.bot.send_message(chat_id=id, text=msg.get_message("error_set_list", get_language(context)), parse_mode=ParseMode.HTML)
		return SETLIST_BCBA
	else:
		await context.bot.send_message(chat_id=id, text=msg.get_message("set_list_4", get_language(context)), parse_mode=ParseMode.HTML)
		return SETLIST_WORLD

#Adding World symbols to watchlist...
async def add_world_symbol_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	symbol = update.message.text.upper()
	if not symbol == "OK":
		is_in, currency = mk.check_symbol_and_currency("WORLD", symbol)
		if is_in:
			context.chat_data[context.chat_data["active_key"]].append(["WORLD", symbol, currency])
			await context.bot.send_message(chat_id=id, text=msg.get_selection(get_language(context)), parse_mode=ParseMode.HTML)
		else:
			await context.bot.send_message(chat_id=id, text=msg.get_message("error_set_list", get_language(context)), parse_mode=ParseMode.HTML)
		return SETLIST_WORLD
	else:
		users.save_user_data(id, context.chat_data)
		await context.bot.send_message(chat_id=id, text=msg.get_message("set_list_5", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=id, text=msg.get_done_emoji(), parse_mode=ParseMode.HTML)
		us.add_list(0)
		return ConversationHandler.END

#Asking the user which watchlist to erase...
async def trigger_eraselist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	if not "watchlists" in context.chat_data:
		users.load_user_data(id, context.chat_data)
	if not context.chat_data == None:
		keyboard = user_lists_keyboard(context.chat_data["watchlists"])
		reply = InlineKeyboardMarkup(keyboard)
		await context.bot.send_message(chat_id=id, text=msg.get_message("erase_list_1", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)
		us.add_list(2)
		return ERASE_LIST
	else:
		await context.bot.send_message(chat_id=id, text=msg.get_message("error_list", get_language(context)), parse_mode=ParseMode.HTML)
		us.add_list(3)
		return ConversationHandler.END

#Deleting a watchtlist if the user confirm...
async def confirm_eraselist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	the_list = update.message.text.lower()
	if context.chat_data["erase_list"] == the_list:
		erase_list(the_list, context.chat_data)
		users.save_user_data(id, context.chat_data)
		await context.bot.send_message(chat_id=id, text=msg.get_message("erase_list_3", get_language(context)), parse_mode=ParseMode.HTML)
		return ConversationHandler.END
	else:
		await context.bot.send_message(chat_id=id, text=msg.get_message("error_erase_list", get_language(context)), parse_mode=ParseMode.HTML)
		us.add_list(3)
		return ConversationHandler.END

#Removing watchlist from context.chat_data...
def erase_list(list_name: str, chat_data: dict) -> None:
	for wl in range(len(chat_data["watchlists"])):
		if chat_data["watchlists"][wl] == list_name:
			del chat_data["watchlists"][wl]
			break
	del chat_data["wl_" + list_name]

#Looking for last data for us dolar quotes in Argentina...
async def get_last_dolar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	try:
		await context.bot.send_message(chat_id=id, text=msg.get_message("start_dolar", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=id, text=msg.get_analysis_emoji(), parse_mode=ParseMode.HTML)
		mk.update_dolar_ar()
		message = msg.build_dolar_message(mk.dolar_ar, get_language(context))
		await context.bot.send_message(chat_id=id, text=message, parse_mode=ParseMode.HTML)
		us.add_dolar(0)
	except:
		await context.bot.send_message(chat_id=id, text=msg.get_message("error_dolar", get_language(context)), parse_mode=ParseMode.HTML)
		us.add_dolar(1)

#Sending an updated watchlist to the user...
async def user_watchlists(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	if not "watchlists" in context.chat_data:
		users.load_user_data(id, context.chat_data)
	if "watchlists" in context.chat_data:
		if len(context.chat_data["watchlists"]) > 0:
			keyboard = user_lists_keyboard(context.chat_data["watchlists"])
			reply = InlineKeyboardMarkup(keyboard)
			await context.bot.send_message(chat_id=id, text=msg.get_message("start_list", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)
		else:
			await context.bot.send_message(chat_id=id, text=msg.get_message("error_list", get_language(context)), parse_mode=ParseMode.HTML)
			us.add_list(3)
	else:
		await context.bot.send_message(chat_id=id, text=msg.get_message("error_list", get_language(context)), parse_mode=ParseMode.HTML)
		us.add_list(3)

def user_lists_keyboard(list_names: list) -> list:
	keyboard = []
	for l in range(len(list_names)):
		if l%2 == 0:
			keyboard.append([InlineKeyboardButton(text=list_names[l].capitalize(), callback_data="wl_" + list_names[l])])
		else:
			keyboard[l//2].append(InlineKeyboardButton(text=list_names[l].capitalize(), callback_data="wl_" + list_names[l]))
	return keyboard

#Starting an error report session...
async def trigger_error_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " wants to report an error...")
	await context.bot.send_message(chat_id=id, text=msg.get_apology(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_1", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_emoji("ear"), parse_mode=ParseMode.HTML)
	return ERROR_1

#Saving error related command...
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = update.message.text
	context.chat_data["error_command"] = m
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_2", get_language(context)), parse_mode=ParseMode.HTML)
	return ERROR_2

#Saving error description...
async def report_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = context.chat_data["error_command"]
	m2 = update.message.text
	context.chat_data["error_description"] = m2
	us.add_error_report()
	us.save_error_report(m, m2, str(hide_id(id)))
	admin_msg = "Error reported:\n-command: " + m + "\n-description: " + m2
	await context.bot.send_message(chat_id=config["admin_id"], text=admin_msg, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_3", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_emoji("envelope"), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Ending any convertation...
async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " endss a conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_conversation_end(get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("end_conversation", get_language(context)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_done_emoji(), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Sending a help message...
async def print_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " asked for help...")
	us.add_help()
	m = msg.build_help_message(get_language(context))
	await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_emoji("magnifying_glass"), parse_mode=ParseMode.HTML)

#Sending an info message...
async def print_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " asked for info...")
	us.add_info()
	m = msg.build_info_message(get_language(context))
	await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_emoji("keyboard"), parse_mode=ParseMode.HTML)

#Checking which language to use with the actual user...
def get_language(context: ContextTypes.DEFAULT_TYPE) -> None:
	if "language" in context.chat_data:
		return context.chat_data["language"]
	else:
		return 0

#A commando to allow a user decide which language to use...
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	await context.bot.send_message(chat_id=id, text=msg.get_message("language_1", get_language(context)), reply_markup=reply, parse_mode=ParseMode.HTML)

#Setting language configuration for actual user...
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
	id = update.effective_chat.id
	if query == "l_1":
		logging.info("English is the language selected by " + str(hide_id(id)))
		context.chat_data["language"] = 1
		us.add_language(1)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language_2", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=id, text=msg.get_emoji("cocktail"), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(hide_id(id)))
		context.chat_data["language"] = 0
		us.add_language(0)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language_3", get_language(context)), parse_mode=ParseMode.HTML)
		await context.bot.send_message(chat_id=id, text=msg.get_emoji("mate"), parse_mode=ParseMode.HTML)

#Handling conversation clicks on InlineKeyboardButtons...
async def conversation_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	query = update.callback_query
	await query.answer()
	if query.data.startswith("wl"):
		context.chat_data["erase_list"] = query.data.split("_")[1]
		await context.bot.send_message(chat_id=id, text=msg.get_message("erase_list_2", get_language(context)), parse_mode=ParseMode.HTML)
		return ERASE_LIST_CONFIRM
	else:
		logging.info("Strange query from button recieved!")
		return ConversationHandler.END

#Handling default clicks on InlineKeyboardButtons...
async def default_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	query = update.callback_query
	await query.answer()
	if query.data.startswith("l"):
		await set_language(update, context, query.data)
	if query.data.startswith("wl"):
		if len(context.chat_data[query.data]) > 0:
			await context.bot.send_message(chat_id=id, text=msg.get_message("building_list", get_language(context)), parse_mode=ParseMode.HTML)
			await context.bot.send_message(chat_id=id, text=msg.get_long_wait_emoji(), parse_mode=ParseMode.HTML)
			data = mk.get_last_info_list(context.chat_data[query.data])
			message = msg.build_last_info_list_message(data)
			await context.bot.send_message(chat_id=id, text=message, parse_mode=ParseMode.HTML)
			us.add_list(1)
		else:
			await context.bot.send_message(chat_id=id, text=msg.get_message("error_list_2", get_language(context)), parse_mode=ParseMode.HTML)
			await context.bot.send_message(chat_id=id, text=msg.get_apology(get_language(context)), parse_mode=ParseMode.HTML)
			await context.bot.send_message(chat_id=id, text=msg.get_emoji("microscope"), parse_mode=ParseMode.HTML)
			us.add_list(3)
	else:
		logging.info("Strange query from button recieved!")

#Sending usage data...
async def bot_usage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		m = us.build_usage_message()
		await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to check bot usage data...")
		await context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(context)), parse_mode=ParseMode.HTML)

#Saving usage data...
async def save_usage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = update.message.text.split(" ")
	if len(m) > 1 and m[1] == config["password"]:
		us.save_usage()
		await context.bot.send_message(chat_id=id, text="¡Datos guardados!", parse_mode=ParseMode.HTML)
	else:
		logging.info(hide_id(id) + " wanted to save bot usage data...")
		await context.bot.send_message(chat_id=id, text=msg.get_message("intruder", get_language(context)), parse_mode=ParseMode.HTML)

#Testing things...
async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	message = update.message.text
	await context.bot.send_message(chat_id=id, text=message, parse_mode=ParseMode.HTML)

#Notifying the user about out of context conversation...
async def out_of_context(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	us.add_outofcontext()
	logging.info(str(hide_id(id)) + " sent out of context message...")
	await context.bot.send_message(chat_id=id, text=msg.get_outofcontext(get_language(context)), parse_mode=ParseMode.HTML)

#Notifying the user about out of context conversation when expecting a button click...
async def button_wanted(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	us.add_outofcontext()
	logging.info(str(hide_id(id)) + " sent out of context message in a conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_button_wanted(get_language(context)), parse_mode=ParseMode.HTML)

#Sending error notification to administrator...
async def error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(hide_id(id))
	logging.info(m)
	await context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

#Building the general conversation handler...
def build_general_conversation_handler():
	print("Building music conversation handler...", end="\n")
	handler = ConversationHandler(
		entry_points=[CommandHandler("about", trigger_about), CommandHandler("bcba", trigger_check),
					CommandHandler("world", trigger_check), CommandHandler("setwatchlist", trigger_setlist),
					CommandHandler("erasewatchlist", trigger_eraselist), CommandHandler("error", trigger_error_submit)],
		states={
			ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_about)],
			CHECKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_last_info)],
			SETLIST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_for_list)],
			SETLIST_BCBA: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_bcba_symbol_to_list)],
			SETLIST_WORLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_world_symbol_to_list)],
			ERASE_LIST: [CallbackQueryHandler(conversation_button_click),
						MessageHandler(filters.TEXT & ~filters.COMMAND, button_wanted)],
			ERASE_LIST_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_eraselist)],
			ERROR_1: [MessageHandler(filters.TEXT, report_command)],
			ERROR_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_error)],
		},
		fallbacks=[MessageHandler(filters.COMMAND, end_conversation)],
		per_chat=True, per_user=False, per_message=False)
	return handler

#Here the magic happens...
def main() -> None:
	if config["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif config["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	print("Ready to build the bot...", end="\n")
	app = Application.builder().token(config["token"]).build()
	#app.add_error_handler(error_notification)
	app.add_handler(build_general_conversation_handler(), group=1)
	app.add_handler(CallbackQueryHandler(default_button_click), group=1)
	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, out_of_context), group=1)
	app.add_handler(CommandHandler("start", start), group=2)
	app.add_handler(CommandHandler("dolar", get_last_dolar), group=2)
	app.add_handler(CommandHandler("watchlists", user_watchlists), group=2)
	app.add_handler(CommandHandler("language", select_language), group=2)
	app.add_handler(CommandHandler("help", print_help), group=2)
	app.add_handler(CommandHandler("info", print_info), group=2)
	app.add_handler(CommandHandler("botusage", bot_usage), group=2)
	app.add_handler(CommandHandler("saveusage", save_usage), group=2)
	app.add_handler(CommandHandler("debug", debug), group=2)
	if config["webhook"]:
		print("Ready to set webhook...", end="\n")
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"])
		app.run_webhook(listen="0.0.0.0", port=config["webhook_port"], secret_token=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		print("Ready to start polling...", end="\n")
		app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
	main()