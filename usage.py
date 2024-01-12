import datetime as dt

class Usage():
	"The class to save usage data..."

	def __init__(self, output_path, errors_path):
		self.output_path = output_path
		self.errors_path = errors_path
		self.reset()

	#Resseting data variables...
	def reset(self):
		self.last_save = dt.datetime.now() #the start up time...
		self.start = 0
		self.about = [0,0] #success, errors...
		self.check = [0,0]
		self.list = [0,0,0] #set, check, errors...
		self.portfolio = [0,0,0,0] #check, buy, sell, errors...
		self.language = [0,0] #spanish, english...
		self.help = 0
		self.info = 0
		self.out_of_context = 0
		self.reports = 0
		self.errors = 0

	#Building usage information message...
	def build_usage_message(self):
		m = "<b>Usage data:</b>" + "\n" + \
			"start: " + str(self.start) + "\n" + \
			"about: " + str(self.about) + "\n" + \
			"check: " + str(self.check) + "\n" + \
			"list: " + str(self.list) + "\n" + \
			"portfolio: " + str(self.portfolio) + "\n" + \
			"language: " + str(self.language) + "\n" + \
			"help: " + str(self.help) + "\n" + \
			"info: " + str(self.info) + "\n" + \
			"out of context: " + str(self.out_of_context) + "\n" + \
			"error reports: " + str(self.reports) + "\n" + \
			"errors: " + str(self.errors) + "\n"
		return m

	#Saving usage to file...
	def save_usage(self):
		file = open(self.output_path, "a")
		t = dt.datetime.now()
		i = t - self.last_save
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		interval = str(i).split(".")[0]
		line = self.build_usage_line(date, interval)
		file.write(line)
		file.close()
		self.reset()

	#Building a data line to save...
	def build_usage_line(self, date, interval):
		line = date + ";"
		line += interval + ";"
		line += str(self.start) + ";"
		line += str(self.about) + ";"
		line += str(self.check) + ";"
		line += str(self.list) + ";"
		line += str(self.portfolio) + ";"
		line += str(self.language) + ";"
		line += str(self.help) + ";"
		line += str(self.info) + ";"
		line += str(self.out_of_context) + ";"
		line += str(self.reports) + ";"
		line += str(self.errors) + "\n"
		return line

	#Registering a new start command...
	def add_start(self):
		self.start += 1
	
	#Registering a new about...
	def add_about(self, key):
		self.about[key] += 1

	#Registering a new bcba...
	def add_check(self, key):
		self.check[key] += 1

	#Registering a new noise...
	def add_list(self, key):
		self.list[key] += 1

	#Registering a new interaction...
	def add_portfolio(self, key):
		self.portfolio[key] += 1

	#Registering a new language...
	def add_language(self, l):
		self.language[l] += 1

	#Registering a new help...
	def add_help(self):
		self.help += 1
	
	#Registering a new info...
	def add_info(self):
		self.info += 1

	#Registering a new wrong_message...
	def add_outofcontext(self):
		self.out_of_context += 1
	
	#Registering a new wrong_message...
	def add_error_report(self):
		self.reports += 1
	
	#Registering a new error...
	def add_error(self):
		self.errors += 1

	#Saving en error report...
	def save_error_report(self, command, description, user):
		file = open(self.errors_path, "a")
		t = dt.datetime.now()
		date = str(t.year) + "-" + str(t.month) + "-" + str(t.day)
		file.write(date)
		file.write(";")
		file.write(command)
		file.write(";")
		file.write(description)
		file.write(";")
		file.write(user + "\n")
		file.close()

	#Printing Usage()...
	def __str__(self):
		return "- MERC's Harvey Bot\n" + \
				"  I am the class in charge of saving some usage data...\n" + \
				"  gitlab.com/rodrigovalla/mercsharveybot\n" + \
				"  rodrigovalla@protonmail.ch"