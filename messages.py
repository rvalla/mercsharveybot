import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages.json"))
		self.msg_en = js.load(open("assets/text/en/messages.json"))
		self.r_conversation_start_es = open("assets/text/es/random_conversation_start.txt").readlines()
		self.r_conversation_start_en = open("assets/text/en/random_conversation_start.txt").readlines()
		self.r_conversation_end_es = open("assets/text/es/random_conversation_end.txt").readlines()
		self.r_conversation_end_en = open("assets/text/en/random_conversation_end.txt").readlines()
		self.r_error_message_es = open("assets/text/es/random_apologies.txt").readlines()
		self.r_error_message_en = open("assets/text/en/random_apologies.txt").readlines()
		self.r_outofcontext_es = open("assets/text/es/random_outofcontext.txt").readlines()
		self.r_outofcontext_en = open("assets/text/en/random_outofcontext.txt").readlines()

	#To get the desired message from standard messages...
	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]
	
	#To get a random conversation start...
	def get_conversation_start(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_start_es)
		else:
			return rd.choice(self.r_conversation_start_en)
	
	#To get a random conversation end...
	def get_conversation_end(self, l):
		if l == 0:
			return rd.choice(self.r_conversation_end_es)
		else:
			return rd.choice(self.r_conversation_end_en)
	
	#To get a random apology...
	def get_apology(self, l):
		if l == 0:
			return rd.choice(self.r_error_message_es)
		else:
			return rd.choice(self.r_error_message_en)
	
	#To get a random out of context...
	def get_outofcontext(self, l):
		if l == 0:
			return rd.choice(self.r_outofcontext_es)
		else:
			return rd.choice(self.r_outofcontext_en)
	
	#To format a symbol about message (needs data from Market())...
	def build_about_message(self, l, data):
		m = self.get_symbol_name_str(data["symbol"], data["name"], data["cedear_ratio"])
		if l == 0:
			m += data["about_es"]
		else:
			m += data["about_en"]
		m += "\n" + data["url"]
		return m
	
	#To format a symbol last info message (needs data from Market())...
	def build_last_info_message(self, l, exchange, data):
		m = self.get_symbol_name_str(data[0], data[1], data[7])
		if l == 0:
			m += "Último precio: <b>" + self.get_price_str(exchange, data[2]) + "</b>\n"
			m += "Variación: " + self.get_price_str(exchange, data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volumen: " + self.get_price_str(exchange, data[5]) + "\n"
		else:
			m += "Last price: <b>" + self.get_price_str(exchange, data[2]) + "</b>\n"
			m += "Variation: " + self.get_price_str(exchange, data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volume: " + self.get_price_str(exchange, data[5]) + "\n"
		return m
	
	#To format a watchlist...
	def build_last_info_list(self, data):
		m = ""
		for r in data:
			m += self.get_watchlist_row(r)
			m += "\n"
		return m
	
	#To format a watchlist row...
	def get_watchlist_row(self, row):
		m = "<b>" + self.format_listed_symbol(row[1]) + "</b>:  "
		m += self.get_price_str(row[0], row[2]) + " <b>"
		m += self.get_variation_str(row[3]) + "</b> ("
		m += self.get_price_str(row[0], row[4]) + ")"
		return m
	
	#To format symbol on list...
	def format_listed_symbol(self, symbol):
		s = len(symbol)
		m = "-"
		for l in range(6-s):
			m += " "
		m += symbol
		return m

	#To format a company name...
	def get_symbol_name_str(self, symbol, name, cedear_ratio):
		m = "<b>" + name + " (" + symbol + ")</b>"
		if not cedear_ratio == "-":
			m += "\n<i>Cedear (Ratio " + cedear_ratio + ")</i>"
		m += "\n\n"
		return m

	#To format last price...
	def get_price_str(self, exchange, number):
		n = ""
		if exchange == "BCBA":
			n = "AR${:,.2f}".format(number)
		else:
			n = "U$S{:,.2f}".format(number)
		return n
	
	#To format variation percentage...
	def get_variation_str(self, number):
		if number < 0:
			return "{:3.2f}%".format(number)
		else:
			return "+{:3.2f}%".format(number)

	#To build help message...
	def build_help_message(self, l):
		m = ""
		if l == 0:
			m += "Podés pedirme distintas cosas. Acá te dejo los comandos disponibles:\n\n"
			m += "> Mandame /bcba para consultar la <b>Bolsa de Comercio de Buenos Aires</b>. "
			m += "Intento leer los datos desde el sitio de <b>Invertir Online</b>. Podés "
			m += "pensar este comando como una forma rápida de acceder ahí.\n"
			m += "> Mandame /world para consultar otros mercados. "
			m += "> Mandame /cancel para terminar una conversasión.\n"
			m += "> Mandame /error para reportar cualquier error que me encuentres.\n"
			m += "> Mandame /language para cambiar el idioma que uso.\n"
			m += "> Mandame /help para quedarte encerrado en un bucle recursivo."
		else:
			m += "You can ask me for different things. Here is a list with the available commands:\n\n"
			m += "> Send me /bcba to check stocks from the <b>Bolsa de Comercio de Buenos Aires</b>. "
			m += "I try to read the data from <b>Invertir Online</b> platform. You can think about this "
			m += "command as a fast way to check that website.\n"
			m += "> Send me /world to check other exchanges. "
			m += "> Send me /cancel to terminate a conversation session.\n"
			m += "> Send me /error to report whatever error you find on me..\n"
			m += "> Send me /language to change the language I use.\n"
			m += "> Send me /help to be caught by a recursive loop."
		return m
	
	#Printing Messages()...
	def __str__(self):
		return "- MERC's Harvey Bot\n" + \
				"  I am the class in charge of formating and retrieving text messages...\n" + \
				"  gitlab.com/rodrigovalla/mercsharveybot\n" + \
				"  rodrigovalla@protonmail.ch"