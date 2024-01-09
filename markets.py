import time
import requests
import random
from bs4 import BeautifulSoup

class Markets():
    "The class to access local and web data about the market..."

    def __init__(self):
        self.iol = "https://iol.invertironline.com/titulo/cotizacion/"
        self.bcba, self.world = self.load_tickers(open("data/tickers.csv").readlines()[1:])

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
        ticker["ready"] = data[7] in ("True\n")
        return ticker

    #Returning symbol data...
    def get_symbol(self, exchange, symbol):
        try:
            if exchange == "BCBA":
                return self.bcba[symbol]
            else:
                return self.world[symbol]
        except:
            return None
    
    #Looking for the last price of a symbol at iol website...
    def get_last_info(self, exchange, symbol):
        self.pause(2, 5) #To avoid requesting the website a lot...
        table = self.get_symbol_table(exchange, symbol)
        last_p, variation_p, variation_q = self.get_symbol_price_and_variation(exchange, table)
        volume_m, volume_n = self.get_symbol_volumes(exchange, table)
        if exchange == "BCBA":
            name = self.bcba[symbol]["name"]
            cedear_ratio = self.bcba[symbol]["cedear_ratio"]
        else:
            name = self.world[symbol]["name"]
            cedear_ratio = "-"
        return [symbol, name, last_p, variation_p, variation_q, volume_m, volume_n, cedear_ratio]
    
    #Looking for the last prices of a watch list...
    def get_last_info_list(self, exchanges_and_symbols):
        data = []
        for s in exchanges_and_symbols:
            self.pause(0.5, 3)
            table = self.get_symbol_table(s[0], s[1])
            last_p, variation_p, variation_q = self.get_symbol_price_and_variation(s[0], table)
            data.append([s[0], s[1], last_p, variation_p, variation_q])
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
    def get_symbol_price_and_variation(self, exchange, table):
        aux = table.find_all("span")
        last_p = float(aux[3].text.replace(".", "").replace(",", "."))
        variation_p = float(aux[9].text.replace(",", "."))
        variation_q = float(aux[7].text.replace(".", "").replace(",", "."))
        return last_p, variation_p, variation_q
    
    #Extracting volumes from table...
    def get_symbol_volumes(self, exchange, table):
        aux = table.find_all("li")
        volume_m = 0
        volume_n = 0
        try:
            volume_n = int(aux[1].text.replace("Q: ", ""))
            if exchange == "BCBA":
                volume_m = float(aux[0].text.replace("$ ", "").replace(".", "").replace(",", ".")) 
            else:
                volume_m = float(aux[0].text.replace("US$ ", "").replace(".", "").replace(",", "."))
        except:
            pass
        return volume_m, volume_n
    
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