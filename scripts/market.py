#####   Market Module   #########

import random
from config import INITIAL_STOCKS, PRICE_CHANGE_MIN, PRICE_CHANGE_MAX

class Market:
    ###  Initialize market with initial stock prices  ###
    def __init__(self):
        self.stocks = INITIAL_STOCKS.copy()
    
    ###   Get current price of a stock   ###
    def get_price(self, symbol):
        return self.stocks.get(symbol, 0)
    
    ###   Get all stock prices   ###
    def get_all_prices(self):
        return self.stocks.copy()
    
    ###   Update stock prices with random volatility   ###
    def update_prices(self):
        for symbol in self.stocks:
            change = random.uniform(PRICE_CHANGE_MIN, PRICE_CHANGE_MAX)
            self.stocks[symbol] = round(self.stocks[symbol] * (1 + change), 2)