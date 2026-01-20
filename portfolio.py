####   Portfolio Module   #########

from config import INITIAL_BALANCE

class Portfolio:
    ###   Initialize portfolio with starting balance and empty holdings   ###
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.holdings = {}
    
    ###   Attempt to buy stock   ###
    def buy(self, stock, quantity, price):
        cost = quantity * price
        
        if cost > self.balance:
            return False, "Not enough balance to buy"
        
        self.balance -= cost
        self.holdings[stock] = self.holdings.get(stock, 0) + quantity
        
        return True, f"Bought {quantity} shares of {stock}"
    
    ###   Attempt to sell stock   ###
    def sell(self, stock, quantity, price):
        
        if stock not in self.holdings or self.holdings[stock] < quantity:
            return False, "Not enough shares to sell"
        
        revenue = quantity * price
        self.balance += revenue
        self.holdings[stock] -= quantity
        
        if self.holdings[stock] == 0:
            del self.holdings[stock]
        
        return True, f"Sold {quantity} shares of {stock}"
    
    ###   Calculate total portfolio value   ###
    def total_value(self, market_prices):
        value = self.balance
        for stock, qty in self.holdings.items():
            value += qty * market_prices.get(stock, 0)
        return round(value, 2)