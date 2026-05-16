import time
import requests
import random
import datetime as dt
import mercscharts as mplt
from bs4 import BeautifulSoup

class Markets():
    "The class to access local and web data about the market..."

    def __init__(self):
        self.iol = "https://iol.invertironline.com/titulo/cotizacion/"
        self.arg_api = "https://api.argentinadatos.com/v1/"
        self.hoy = "https://dolarhoy.com/"
        self.dolar_ar = {} #here the class stores dolar quotes in Argentina
        self.dolar_min_interval = dt.timedelta(minutes=10)
        self.dolar_y_min_interval = dt.timedelta(hours=17)
        self.dolar_update = dt.datetime(year=2021, month=1, day=1)
        self.dolar_update_y = dt.datetime(year=2020, month=1, day=1)
        self.bcba, self.world = self.load_tickers(open("data/tickers.csv").readlines()[1:])

     #Looking for dolar quotes in Argentina...
    def update_dolar_ar(self):
        today = dt.datetime.today()
        if today - self.dolar_update_y > self.dolar_y_min_interval:
            self.update_yesterday_dolar_ar(today)
        if today - self.dolar_update > self.dolar_min_interval:    
            page = requests.get(self.hoy).text
            page_soup = BeautifulSoup(page, "html.parser")
            buy = page_soup.find_all("div", class_="compra")
            sell = page_soup.find_all("div", class_="venta")
            self.save_dolar_data("oficial", buy[2], sell[2])
            self.save_dolar_data("blue", buy[1], sell[1])
            self.save_dolar_data("mep", buy[3], sell[3])
            self.save_dolar_data("ccl", buy[4], sell[4])
            self.save_dolar_data("cripto", buy[5], sell[5])
            self.dolar_update = today

    #Extracting dolar values from website...
    def save_dolar_data(self, dict_key, div_buy, div_sell):
        b = self.get_dolar_price(div_buy.find("div", class_="val").text)
        s = self.get_dolar_price(div_sell.find("div", class_="val").text)
        v = (s / self.dolar_ar[dict_key + "_y"] - 1) * 100
        self.dolar_ar[dict_key + "_b"] = b
        self.dolar_ar[dict_key + "_s"] = s
        self.dolar_ar[dict_key + "_v"] = v

    #Looking for dolar quotes in Argentina...
    def update_yesterday_dolar_ar(self, today):
        yesterday = today - dt.timedelta(days=1)
        if not self.dolar_update_y.day == yesterday.day:
            if self.dolar_update - self.dolar_update_y > self.dolar_y_min_interval:
                try:
                    self.load_yesterday_dolar_data("oficial", "oficial", yesterday)
                    self.load_yesterday_dolar_data("blue", "blue", yesterday)
                    self.load_yesterday_dolar_data("bolsa", "mep", yesterday)
                    self.load_yesterday_dolar_data("contadoconliqui", "ccl", yesterday)
                    self.load_yesterday_dolar_data("cripto", "cripto", yesterday)
                    self.dolar_update_y = yesterday
                except:
                    pass

    #Loading data in dolar_ar...
    def load_yesterday_dolar_data(self, api_key, dict_key, yesterday):
        api_url = self.arg_api + "cotizaciones/dolares/" + api_key + "/"
        dolar_yesterday = requests.get(api_url + self.date_to_url_string(yesterday)).json()
        self.dolar_ar[dict_key + "_y"] = dolar_yesterday["venta"]

    #Formating date for api url...
    def date_to_url_string(self, date):
        m = str(date.year) + "/"
        m += "{:02d}".format(date.month) + "/"
        m += "{:02d}".format(date.day)
        return m

    #Returning dolar data...
    def dolar_ar_data(self):
        self.update_dolar_ar()
        return self.dolar_ar

    #Extracting prices from text...
    def get_dolar_price(self, data):
        number_str = data.replace("$", "").replace(",",".")
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
    
    #Calculating a custom MEP...
    def get_mep(self, symbol):
        mep = None
        if self.is_symbol_in_database("BCBA", symbol) and self.is_symbol_in_database("BCBA", symbol + "D"):
            data = self.get_last_info_list([["BCBA", symbol, "ARS"],["BCBA", symbol + "D", "US"]])
            if len(data) == 2:
                mep = data[0][2] / data[1][2]
        return mep 

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
    
    #Helping with cash or not cash decisions...
    def cash_or_not(self, c_price, f_price, periods, anual_inflation, anual_i_rate):
        inflation = self.monthly_variation(anual_inflation)
        i_rate = self.monthly_variation(anual_i_rate)
        cash_n, cash_a = self.payment_history(f_price, periods, c_price, 0, inflation, i_rate)
        cash_n_up, cash_a_up = self.payment_history(f_price, periods, c_price, 0, self.add_error(True, inflation), self.add_error(True, i_rate))
        cash_n_down, cash_a_down = self.payment_history(f_price, periods, c_price, 0, self.add_error(False, inflation), self.add_error(False, i_rate))
        financed_n, financed_a = self.payment_history(f_price, periods, f_price / periods, f_price / periods, inflation, i_rate)
        financed_n_up, financed_a_up = self.payment_history(f_price, periods, f_price / periods, f_price / periods, self.add_error(True, inflation), self.add_error(True, i_rate))
        financed_n_down, financed_a_down = self.payment_history(f_price, periods, f_price / periods, f_price / periods, self.add_error(False, inflation), self.add_error(False, i_rate))
        chart = mplt.lines_chart(6,4,120,[financed_a, cash_a],[financed_a_down, financed_a_up, cash_a_down, cash_a_up])
        in_cash, difference = self.decide_cash_or_not(cash_a[periods-1], financed_a[periods-1])
        return in_cash, difference, cash_a[periods-1], financed_a[periods-1], chart

    #Calculating expense progression (inflation and interest_rate m/m)...
    def payment_history(self, capital, periods, initial_payment, installment, inflation, interest_rate):
        investment = capital - initial_payment
        investment_actual = investment
        nominal = -capital + investment
        actual = nominal
        n_list = [nominal]
        a_list = [actual]
        for p in range(periods - 1):
            investment = investment * interest_rate - installment
            investment_actual = investment_actual * interest_rate / inflation - installment / pow(inflation, p+1)
            nominal = -capital + investment
            actual = -capital + investment_actual
            n_list.append(nominal)
            a_list.append(actual)
        return n_list, a_list
    
    #Deciding if cash is more convenient...
    def decide_cash_or_not(self, in_cash, financed):
        ratio = financed / in_cash
        decision = 2
        if ratio < 0.97:
            decision = 1
        elif ratio > 1.03:
            decision = 0
        return decision, ratio-1

    #Calculating a monthly variation rate from anual one...
    def monthly_variation(self, anual_rate):
        return pow(anual_rate, 1/12)
    
    #Adding error to rates...
    def add_error(self, up, rate):
        variation = rate - 1
        new_rate = 1
        if up:
            new_rate += variation * 1.25
        else:
            new_rate += variation * 0.75
        return new_rate

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
