import json as js
import random as rd

class Messages():
	"The class the bot use to know what to say..."

	def __init__(self):
		self.msg_es = js.load(open("assets/text/es/messages.json"))
		self.msg_en = js.load(open("assets/text/en/messages.json"))
		self.r_success_es = open("assets/text/es/random_success.txt").readlines()
		self.r_success_en = open("assets/text/en/random_success.txt").readlines()
		self.r_selection_es = open("assets/text/es/random_selection.txt").readlines()
		self.r_selection_en = open("assets/text/en/random_selection.txt").readlines()
		self.r_conversation_start_es = open("assets/text/es/random_conversation_start.txt").readlines()
		self.r_conversation_start_en = open("assets/text/en/random_conversation_start.txt").readlines()
		self.r_conversation_end_es = open("assets/text/es/random_conversation_end.txt").readlines()
		self.r_conversation_end_en = open("assets/text/en/random_conversation_end.txt").readlines()
		self.r_error_message_es = open("assets/text/es/random_apologies.txt").readlines()
		self.r_error_message_en = open("assets/text/en/random_apologies.txt").readlines()
		self.r_outofcontext_es = open("assets/text/es/random_outofcontext.txt").readlines()
		self.r_outofcontext_en = open("assets/text/en/random_outofcontext.txt").readlines()
		self.r_buttonwanted_es = open("assets/text/es/random_buttonwanted.txt").readlines()
		self.r_buttonwanted_en = open("assets/text/en/random_buttonwanted.txt").readlines()
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
	
	#To get a random selection message...
	def get_selection(self, l):
		if l == 0:
			return rd.choice(self.r_selection_es)
		else:
			return rd.choice(self.r_selection_en)

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
	
	#To get a random out of context button...
	def get_button_wanted(self, l):
		if l == 0:
			return rd.choice(self.r_buttonwanted_es)
		else:
			return rd.choice(self.r_buttonwanted_en)
	
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
			m += "Último precio: <b>" + self.get_price_str(data[8], data[2]) + "</b> " + self.get_variation_arrow(data[3]) + " \n"
			m += "Variación: " + self.get_price_str(data[8], data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volumen: " + self.get_price_str(data[8], data[5]) + "\n"
		else:
			m += "Last price: <b>" + self.get_price_str(data[8], data[2]) + "</b> " + self.get_variation_arrow(data[3]) + "\n"
			m += "Variation: " + self.get_price_str(data[8], data[4]) + " <b>" + self.get_variation_str(data[3]) + "</b>\n"
			m += "Volume: " + self.get_price_str(data[8], data[5]) + "\n"
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
		names = [["BNA", "MEP", "CCL", "Blue", "Mayorista"], ["BNA", "MEP", "CCL", "Cash", "Wholesale"]]
		m += "<b>" + names[l][1] + "</b>: " +  self.get_price_str("ARS", dolar["mep_s"]) + " "  + \
				self.get_variation_str(dolar["mep_v"]) + self.get_variation_arrow(dolar["mep_v"]) + "\n"
		m += "<b>" + names[l][2] + "</b>: " +  self.get_price_str("ARS", dolar["ccl_s"]) + " " + \
				self.get_variation_str(dolar["ccl_v"]) + self.get_variation_arrow(dolar["ccl_v"]) + "\n\n"
		m += "<b>" + names[l][0] + "</b>: " +  self.get_price_str("ARS", dolar["bna_b"]) + " - " + self.get_price_str("ARS", dolar["bna_s"]) + " " + \
				self.get_variation_str(dolar["bna_v"]) + self.get_variation_arrow(dolar["bna_v"]) + "\n"
		m += "<b>" + names[l][3] + "</b>: " +  self.get_price_str("ARS", dolar["blue_b"]) + " - " + self.get_price_str("ARS", dolar["blue_s"]) + " " + \
				self.get_variation_str(dolar["blue_v"]) + self.get_variation_arrow(dolar["blue_v"]) + "\n"
		m += "<b>" + names[l][4] + "</b>: " +  self.get_price_str("ARS", dolar["mayorista_s"]) + " " +\
				self.get_variation_str(dolar["mayorista_v"]) + self.get_variation_arrow(dolar["mayorista_v"]) + "\n"
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
		m += self.get_price_str(row[5], row[2]) + " <b>"
		m += self.get_variation_str(row[3]) + "</b> ("
		m += self.get_price_str(row[5], row[4]) + ") "
		return m

	#To format a company name...
	def get_symbol_name_str(self, symbol, name, cedear_ratio):
		m = "<b>" + name + " (" + symbol + ")</b>"
		if not cedear_ratio == "-":
			m += "\n<i>Cedear (Ratio " + cedear_ratio + ")</i>"
		m += "\n\n"
		return m

	#To format last price...
	def get_price_str(self, currency, number):
		n = ""
		if currency == "ARS":
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
			m += "> Mandame /about para consultar información acerca de tus símbolos preferidos."
			m += "> Mandame /bcba para consultar la <b>Bolsa de Comercio de Buenos Aires</b>. "
			m += "Intento leer los datos desde el sitio de <b>Invertir Online</b>. Podés "
			m += "pensar este comando como una forma rápida de acceder ahí.\n"
			m += "> Mandame /world para consultar otros mercados.\n"
			m += "> Mandame /dolar para consultar sus cotizaciones.\n"
			m += "> Mandame /watchlists para consultar tus listas de seguimiento.\n"
			m += "> Mandame /setwatchlist para configurar una lista de seguimiento.\n"
			m += "> Mandame /erasewatchlist para eliminar una lista de seguimiento.\n"
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
			m += "> Send me /setwatchlist to set up a watchlist.\n"
			m += "> Send me /watchlists to check your watchlist.\n"
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