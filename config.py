#####    Configuration Settings   #########

import os
import sys

#####   Determine base path (works for both .py and .exe)  #########
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    BASE_PATH = os.path.dirname(sys.executable)
else:
    # Running as normal Python script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

####   File paths #########
DATA_FOLDER = os.path.join(BASE_PATH, "data")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.csv")
MARKET_PRICES_FILE = os.path.join(DATA_FOLDER, "market_prices.csv")

####   Initial portfolio settings  #######
INITIAL_BALANCE = 10000.0

#######  Initial stock prices #########
INITIAL_STOCKS = {
    "AAPL": 255.00,
    "GOOGL": 330.00,
    "TSLA": 440.00,
    "AMZN": 130.00,
    "MSFT": 460.00,
    "IBRX": 6.00,
    "PLUG": 3.00,
    "WMT": 120.00,
    "DNN": 4.00,
    "NVDA": 186.00,
    "INTC": 47.00,
    "ONDS": 12.00,
    "BBAI": 6.00
}

#####    Market volatility settings #########
PRICE_CHANGE_MIN = -0.10  # -10%
PRICE_CHANGE_MAX = 0.10   # +10%