import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages.json"))
		self.msg_en = js.load(open("assets/text/en/messages.json"))
		self.r_success_es = open("assets/text/es/random_success.txt").readlines()
		self.r_success_en = open("assets/text/en/random_success.txt").readlines()
		self.r_conversation_start_es = open("assets/text/es/random_conversation_start.txt").readlines()
		self.r_conversation_start_en = open("assets/text/en/random_conversation_start.txt").readlines()
		self.r_conversation_end_es = open("assets/text/es/random_conversation_end.txt").readlines()
		self.r_conversation_end_en = open("assets/text/en/random_conversation_end.txt").readlines()
		self.r_error_message_es = open("assets/text/es/random_apologies.txt").readlines()
		self.r_error_message_en = open("assets/text/en/random_apologies.txt").readlines()
		self.r_outofcontext_es = open("assets/text/es/random_outofcontext.txt").readlines()
		self.r_outofcontext_en = open("assets/text/en/random_outofcontext.txt").readlines()
		self.emojis = self.load_emojis(open("assets/html_emojis.txt").readlines()[1:])
		self.analysis_emoji = ["up_trend", "down_trend", "bar_chart", "crystal_ball", "magnifying_glass", "abacus"]
		self.long_waits_emoji = ["sand_clock", "mate", "cocktail", "tropical", "whisky", "coffee", "soda"]
		self.working_emoji = ["laptop", "keyboard", "phone"]
		self.done_emoji = ["explosion", "rocket", "bomb", "medal"]

	#To get the desired message from standard messages...
	def get_message(self, key, l):
		if l == 1:
			return self.msg_en[key]
		else:
			return self.msg_es[key]
	
	#To get a random success message...
	def get_success(self, l):
		if l == 0:
			return rd.choice(self.r_success_es)
		else:
			return rd.choice(self.r_success_en)

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
	
	#To get a html formated emoji...
	def get_emoji(self, key):
		return self.emojis[key]
	
	#To get a random analysis emoji...
	def get_analysis_emoji(self):
		return self.get_emoji(rd.choice(self.analysis_emoji))
	
	#To get a random working emoji...
	def get_working_emoji(self):
		return self.get_emoji(rd.choice(self.working_emoji))
	
	#To get a random done emoji...
	def get_done_emoji(self):
		return self.get_emoji(rd.choice(self.done_emoji))

	#To get a random long wait emoji...
	def get_long_wait_emoji(self):
		return self.get_emoji(rd.choice(self.long_waits_emoji))
	
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
			m += "Último precio: <b>" + self.get_price_str(exchange, data[2]) + "</b> " + self.get_variation_arrow(data[3]) + " \n"
			m += "Variación: " + self.get_price_str(exchange, data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volumen: " + self.get_price_str(exchange, data[5]) + "\n"
		else:
			m += "Last price: <b>" + self.get_price_str(exchange, data[2]) + "</b>" + self.get_variation_arrow(data[3]) + "\n"
			m += "Variation: " + self.get_price_str(exchange, data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volume: " + self.get_price_str(exchange, data[5]) + "\n"
		return m
	
	#To decide an arrow for the variation...
	def get_variation_arrow(self, number):
		arrow = ""
		if number < -3:
			arrow = self.get_emoji("arrow_downdown")
		elif number < -0.5:
			arrow = self.get_emoji("arrow_down")
		elif number < 0.6:
			arrow = self.get_emoji("arrow_doubt")
		elif number < 3:
			arrow = self.get_emoji("arrow_up")
		else:
			arrow = self.get_emoji("arrow_upup")
		return arrow

	#To format last dolar quotes in Argentina (needs data from Market())...
	def build_dolar_message(self, dolar, l):
		m = ""
		if l == 0:
			m += "<b>Oficial</b>: " +  self.get_price_str("BCBA", dolar["oficial_c"]) + " - <b>" + self.get_price_str("BCBA", dolar["oficial_v"]) + "</b>\n"
			m += "<b>Mayorista</b>: " +  self.get_price_str("BCBA", dolar["mayorista"]) + "\n"
			m += "<b>MEP: " +  self.get_price_str("BCBA", dolar["mep"]) + "</b>\n"
			m += "<b>CCL</b>: " +  self.get_price_str("BCBA", dolar["ccl"])
		else:
			m += "<b>Official</b>: " +  self.get_price_str("BCBA", dolar["oficial_c"]) + " - " + self.get_price_str("BCBA", dolar["oficial_v"]) + "\n"
			m += "<b>MEP</b>: " +  self.get_price_str("BCBA", dolar["mep"]) + "\n"
			m += "<b>CCL: " +  self.get_price_str("BCBA", dolar["ccl"]) + "</b>"
		return m

	#To format a watchlist...
	def build_last_info_list_message(self, data):
		m = ""
		for r in data:
			m += self.get_watchlist_row(r)
			m += "\n"
		return m
	
	#To format a watchlist row...
	def get_watchlist_row(self, row):
		m = "<b>" + row[1] + "</b>:  "
		m += self.get_variation_arrow(row[3]) + " "
		m += self.get_price_str(row[0], row[2]) + " <b>"
		m += self.get_variation_str(row[3]) + "</b> ("
		m += self.get_price_str(row[0], row[4]) + ") "
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
			m += "> Mandame /world para consultar otros mercados.\n"
			m += "> Mandame /setlist para configurar una lista de seguimiento.\n"
			m += "> Mandame /list para consultar tu lista de seguimiento.\n"
			m += "> Mandame /cancel para terminar una conversasión.\n"
			m += "> Mandame /error para reportar cualquier error que me encuentres.\n"
			m += "> Mandame /language para cambiar el idioma que uso.\n"
			m += "> Mandame /info para saber un poco más de mí.\n"
			m += "> Mandame /help para quedarte encerrado en un bucle recursivo."
		else:
			m += "You can ask me for different things. Here is a list with the available commands:\n\n"
			m += "> Send me /bcba to check stocks from the <b>Bolsa de Comercio de Buenos Aires</b>. "
			m += "I try to read the data from <b>Invertir Online</b> platform. You can think about this "
			m += "command as a fast way to check that website.\n"
			m += "> Send me /world to check other exchanges. "
			m += "> Send me /setlist to set up a watchlist.\n"
			m += "> Send me /list to check your watchlist.\n"
			m += "> Send me /cancel to terminate a conversation session.\n"
			m += "> Send me /error to report whatever error you find on me..\n"
			m += "> Send me /language to change the language I use.\n"
			m += "> Send me /info to know a little more about me.\n"
			m += "> Send me /help to be caught by a recursive loop."
		return m
	
	#To build info message...
	def build_info_message(self, l):
		m = ""
		if l == 0:
			m += "Soy un bot desarrollado por @rvalla. Mis comandos se inspiran "
			m += "sobre todo en lo que él necesita para mejorar sus operaciones en el mercado. "
			m += "Podés escribirle para hacerle llegar cualquier duda o comentario.\n\n"
			m += "Mi nombre es un pequeño homenaje a un tal Harvey que en los años sesenta estaba a cargo "
			m += "de calcular las compensaciones en el <b>Chicago Mercantile Exchange</b>, un mercado "
			m += "pionero en derivados financieros. Después llegaron las computadoras..."
		else:
			m += "I am a bot developed by @rvalla. My commands were built thinking in his own needs "
			m += "to improve his investment decisions. "
			m += "Feel free to contact him for any questions or comments.\n\n"
			m += "My name is a small tribute to a certain Harvey who in the 1960s was in charge of "
			m += "calculating offsets on the <b>Chicago Mercantile Exchange</b>, a pioneering financial "
			m += "derivatives market. Then the computers came..."
		return m
	
	def load_emojis(self, data):
		emojis = {}
		for l in data:
			key_and_code = l.split(";")
			emojis[key_and_code[0]] = "&#" + key_and_code[2] + ";"
		return emojis
	
	#Printing Messages()...
	def __str__(self):
		return "- MERC's Harvey Bot\n" + \
				"  I am the class in charge of formating and retrieving text messages...\n" + \
				"  gitlab.com/rodrigovalla/mercsharveybot\n" + \
				"  rodrigovalla@protonmail.ch"