import time
import requests
import random
from bs4 import BeautifulSoup

class Markets():
    "The class to access local and web data about the market..."

    def __init__(self):
        self.iol = "https://iol.invertironline.com/titulo/cotizacion/"
        self.cro = "https://www.cronista.com/MercadosOnline/dolar.html"
        self.dolar_ar = {} #here the class stores dolar quotes in Argentina
        self.bcba, self.world = self.load_tickers(open("data/tickers.csv").readlines()[1:])

    #Looking for dolar quotes in Argentina...
    def update_dolar_ar(self):
        self.pause(3,5)
        page = requests.get(self.cro).text
        page_soup = BeautifulSoup(page, "html.parser")
        variation = page_soup.find_all("td", class_="percentage")
        buy = page_soup.find_all("div", class_="buy-value")
        sell = page_soup.find_all("div", class_="sell-value")   
        self.dolar_ar["bna_b"] = self.get_dolar_price(buy[0].text)
        self.dolar_ar["bna_s"] = self.get_dolar_price(sell[0].text)
        self.dolar_ar["bna_v"] = self.get_dolar_variation(variation[0].text)
        self.dolar_ar["blue_b"] = self.get_dolar_price(buy[1].text)
        self.dolar_ar["blue_s"] = self.get_dolar_price(sell[1].text)
        self.dolar_ar["blue_v"] = self.get_dolar_variation(variation[1].text)
        self.dolar_ar["mep_b"] = self.get_dolar_price(buy[2].text)
        self.dolar_ar["mep_s"] = self.get_dolar_price(sell[2].text)
        self.dolar_ar["mep_v"] = self.get_dolar_variation(variation[2].text)
        self.dolar_ar["ccl_b"] = self.get_dolar_price(buy[4].text)
        self.dolar_ar["ccl_s"] = self.get_dolar_price(sell[4].text)
        self.dolar_ar["ccl_v"] = self.get_dolar_variation(variation[4].text)
        self.dolar_ar["mayorista_b"] = self.get_dolar_price(buy[3].text)
        self.dolar_ar["mayorista_s"] = self.get_dolar_price(sell[3].text)
        self.dolar_ar["mayorista_v"] = self.get_dolar_variation(variation[3].text)

    #Extracting prices from text...
    def get_dolar_price(self, data):
        number_str = data.replace("$", "").replace(".", "").replace(",", ".")
        return float(number_str)
    
    #Extracting variations from text...
    def get_dolar_variation(self, data):
        number_str = data.replace(",", ".").replace("%", "")
        return float(number_str)

    #Loading info to database...
    def load_tickers(self, data):
        bcba = {}
        world = {}
        for l in data:
            fields = l.split(";")
            if fields[2]== "BCBA":
                bcba[fields[0]] = self.load_ticker(fields)
            else:
                world[fields[0]] = self.load_ticker(fields)
        return bcba, world

    #Creating a dictionary for each symbol...
    def load_ticker(self, data):
        ticker = {}
        ticker["symbol"] = data[0]
        ticker["exchange"] = data[2]
        ticker["name"] = data[1]
        ticker["about_en"] = data[3]
        ticker["about_es"] = data[4]
        ticker["url"] = data[5]
        ticker["cedear_ratio"] = data[6]
        ticker["currency"] = data[7]
        ticker["ready"] = data[8] in ("True\n")
        return ticker

    #Returning symbol data...
    def get_symbol(self, exchange, symbol):
        if self.is_symbol_in_database(exchange, symbol):
            if exchange == "BCBA":
                return self.bcba[symbol]
            else:
                return self.world[symbol]
        else:
            return None
    
    #Checking if a symbol is in the database...
    def is_symbol_in_database(self, exchange, symbol):
        is_in = False
        if exchange == "BCBA":
            is_in = symbol in self.bcba
        elif exchange == "WORLD":
            is_in = symbol in self.world
        return is_in
    
    #Returning if symbols is in the database and its currency...
    def check_symbol_and_currency(self, exchange, symbol):
        is_in = self.is_symbol_in_database(exchange, symbol)
        if is_in:
            currency = self.get_symbol_currency(exchange, symbol)
        else:
            currency = ""
        return is_in, currency

    #Looking for the last price of a symbol at iol website...
    def get_last_info(self, exchange, symbol):
        self.pause(2, 5) #To avoid requesting the website a lot...
        name, cedear_ratio, currency = self.get_symbol_name_ratio_and_currency(exchange, symbol)
        table = self.get_symbol_table(exchange, symbol)
        last_p, variation_p, variation_q = self.get_symbol_price_and_variation(table)
        volume_m, volume_n = self.get_symbol_volumes(currency, table)
        return [symbol, name, last_p, variation_p, variation_q, volume_m, volume_n, cedear_ratio, currency]
    
    #Looking for the last prices of a watch list...
    def get_last_info_list(self, exchanges_and_symbols):
        data = []
        for s in exchanges_and_symbols:
            self.pause(1, 3)
            try:
                table = self.get_symbol_table(s[0], s[1])
                currency = s[2]
                last_p, variation_p, variation_q = self.get_symbol_price_and_variation(table)
                data.append([s[0], s[1], last_p, variation_p, variation_q, currency])
            except:
                pass
        return data

    #Building the correct url for symbol...
    def get_symbol_iol_url(self, exchange, symbol):
        if not exchange == "BCBA":
            exchange = self.world[symbol]["exchange"]
        url = self.iol + exchange + "/" + symbol
        return url
    
    #Looking for data table in url...
    def get_symbol_table(self, exchange, symbol):
        page = requests.get(self.get_symbol_iol_url(exchange, symbol)).text
        page_soup = BeautifulSoup(page, "html.parser")
        table = page_soup.find("table", class_="table table-striped table-condensed")
        return table
    
    #Extracting price and variations from table...
    def get_symbol_price_and_variation(self, table):
        aux = table.find_all("span")
        last_p = float(aux[3].text.replace(".", "").replace(",", "."))
        variation_p = float(aux[9].text.replace(",", "."))
        variation_q = float(aux[7].text.replace(".", "").replace(",", "."))
        return last_p, variation_p, variation_q
    
    #Extracting volumes from table...
    def get_symbol_volumes(self, currency, table):
        aux = table.find_all("li")
        volume_m = 0
        volume_n = 0
        try:
            volume_n = int(aux[1].text.replace("Q: ", ""))
            if currency == "ARS":
                volume_m = float(aux[0].text.replace("$ ", "").replace(".", "").replace(",", ".")) 
            else:
                volume_m = float(aux[0].text.replace("US$ ", "").replace(".", "").replace(",", "."))
        except:
            pass
        return volume_m, volume_n
    
    #Looking for symbol name, ratio and currency in database...
    def get_symbol_name_ratio_and_currency(self, exchange, symbol):
        if exchange == "BCBA":
            name = self.bcba[symbol]["name"]
            cedear_ratio = self.bcba[symbol]["cedear_ratio"]
            currency  = self.bcba[symbol]["currency"]
        else:
            name = self.world[symbol]["name"]
            cedear_ratio = self.world[symbol]["cedear_ratio"]
            currency  = self.world[symbol]["currency"]
        return name, cedear_ratio, currency
    
    #Looking for symbol currency in database...
    def get_symbol_currency(self, exchange, symbol):
        if exchange == "BCBA":
            currency  = self.bcba[symbol]["currency"]
        else:
            currency  = self.world[symbol]["currency"]
        return currency
    
    #Deciding a random pause...
    def pause(self, minimum, maximum):
        t = random.uniform(minimum, maximum)
        time.sleep(t)
    
    #Printing Markets()...
    def __str__(self):
        return "- MERC's Harvey Bot\n" + \
                "  I am the class in charge of access local and web data about the market...\n" + \
                "  gitlab.com/rodrigovalla/mercsharveybot\n" + \
                "  rodrigovalla@protonmail.ch"