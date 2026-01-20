####   Data Logger Module   #########

import csv
import os
from datetime import datetime
from config import TRANSACTIONS_FILE, MARKET_PRICES_FILE, DATA_FOLDER

###  Initialize data folder if it doesn't exist  ###
def initialize_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

###   Initialize CSV files with headers   ###
def initialize_csv_files():
    initialize_data_folder()
    
    ### Initialize transactions.csv ###
    if not os.path.isfile(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "action",
                "stock",
                "quantity",
                "price",
                "total_value",
                "balance_after"
            ])

    ### Initialize market_prices.csv ###
    if not os.path.isfile(MARKET_PRICES_FILE):
        with open(MARKET_PRICES_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "symbol", "price"])

###   Log a transaction to CSV   ###
def log_transaction(action, stock, quantity, price, balance):
    with open(TRANSACTIONS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action,
            stock,
            quantity,
            price,
            round(quantity * price, 2),
            round(balance, 2)
        ])

###   Log current market prices to CSV   ###
def log_market_snapshot(market_prices):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(MARKET_PRICES_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for symbol, price in market_prices.items():
            writer.writerow([timestamp, symbol, round(price, 2)])