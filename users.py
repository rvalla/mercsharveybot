import datetime as dt

class Users():
    "The class to save user's data..."

    def __init__(self, output_path):
        self.output_path = output_path

    #Saving the user's watchlist...
    def save_user_list(self, id, the_list):
        file = open(self.output_path + str(id) + "_watchlist.txt", "w")
        file.write("exchange;symbol;\n")
        for symbol in the_list:
            file.write(symbol[0])
            file.write(";")
            file.write(symbol[1])
            file.write(";\n")
        file.close()

    #To recover the user's watchlist...
    def load_user_list(self, id):
        watchlist = None
        try:
            file = open(self.output_path + str(id) + "_watchlist.txt", "r").readlines()[1:]
            watchlist = []
            for l in file:
                symbol = l.split(";")
                watchlist.append((symbol[0], symbol[1]))
        except:
            pass
        return watchlist

    #Printing Users()...
    def __str__(self):
        return "- MERC's Harvey Bot\n" + \
                "  I am the class in charge of working with user's data...\n" + \
                "  gitlab.com/rodrigovalla/mercsharveybot\n" + \
                "  rodrigovalla@protonmail.ch"