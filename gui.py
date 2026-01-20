##############     Main GUI interface   ##############

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from market import Market
from portfolio import Portfolio
from data_logger import initialize_csv_files, log_transaction, log_market_snapshot

############   Stock Market Simulator GUI ############
class StockSimulatorGUI:
    def __init__(self):
        initialize_csv_files()
        # Initialize market and portfolio
        self.market = Market()
        self.portfolio = Portfolio()
        self.portfolio_history = []
        self.previous_prices = self.market.get_all_prices().copy()
        
        self.setup_window()
        self.setup_panels()
        self.setup_widgets()
        
        self.refresh()
    
#######   Create main window  #######
    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("Stock Market Simulator")
        self.root.geometry("1050x600")
        self.root.configure(bg="#7373f2")
   
##########   Setup panels   ##########
    def setup_panels(self):
        # Left panel - Portfolio
        self.left = tk.Frame(self.root, bg="#adf4d4", width=300, padx=10, pady=10, relief="ridge", bd=2)
        self.left.pack(side="left", fill="y", padx=10, pady=10)
        
        # Center panel - Trading controls
        self.center = tk.Frame(self.root, bg="#ecd99c", padx=10, pady=10, relief="ridge", bd=2)
        self.center.pack(side="left", expand=True, padx=10, pady=10)
        
        # Right panel - Market
        self.right = tk.Frame(self.root, bg="#ef848d", width=300, padx=10, pady=10, relief="ridge", bd=2)
        self.right.pack(side="right", fill="y", padx=10, pady=10)
   
###########    Setup widgets in panels   ###########
    def setup_widgets(self):
        # LEFT PANEL - Portfolio
        tk.Label(self.left, text="My Portfolio", font=("Arial", 14, "bold"), bg="#d1e7dd").pack(pady=5)
        
        self.balance_label = tk.Label(self.left, text="", font=("Arial", 12), bg="#d1e7dd")
        self.balance_label.pack(pady=5)
        
        self.portfolio_box = tk.Text(self.left, height=15, width=30, bg="#e9f7ef")
        self.portfolio_box.pack(pady=5)
        
        # CENTER PANEL - Trading controls
        tk.Label(self.center, text="Trading Panel", font=("Arial", 14, "bold"), bg="#fff3cd").pack(pady=5)
        
        tk.Label(self.center, text="Select Stock:", bg="#fff3cd").pack()
        self.selected_stock = tk.StringVar(value="AAPL")
        stock_menu = ttk.Combobox(self.center, textvariable=self.selected_stock,values=list(self.market.get_all_prices().keys()))
        stock_menu.pack(pady=5)
        
        tk.Label(self.center, text="Quantity:", bg="#fff3cd").pack()
        self.qty_entry = tk.Entry(self.center)
        self.qty_entry.pack(pady=5)
        
        tk.Button(self.center, text="BUY", width=15, command=self.buy, bg="#198754", fg="white").pack(pady=5)
        tk.Button(self.center, text="SELL", width=15, command=self.sell, bg="#dc3545", fg="white").pack(pady=5)
        
        ###########   Chart ############
        self.fig = Figure(figsize=(5, 3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.center)
        self.canvas.get_tk_widget().pack(pady=20)
        
        # RIGHT PANEL - Live Market
        tk.Label(self.right, text="Live Market", font=("Arial", 14, "bold"), bg="#f8d7da").pack(pady=5)
        self.market_box = tk.Text(self.right, height=20, width=30, bg="#f8d7da")
        self.market_box.pack(pady=5)

#########   Refresh display  ###########
    def refresh(self):
        stocks = self.market.get_all_prices()
        
        # Update balance display
        self.balance_label.config(text=f"Balance: ${self.portfolio.balance:.2f}")
        
        # Update portfolio holdings
        self.portfolio_box.delete("1.0", tk.END)
        if not self.portfolio.holdings:
            self.portfolio_box.insert(tk.END, "No stocks owned\n")
        else:
            for stock, qty in self.portfolio.holdings.items():
                self.portfolio_box.insert(tk.END, f"{stock}: {qty} shares\n")
        
        # Update live market with color coding
        self.market_box.config(state="normal")
        self.market_box.delete("1.0", tk.END)
        
        for symbol, price in stocks.items():
            prev = self.previous_prices.get(symbol, price)
            
            if price > prev:
                color = "green"
                arrow = "↑"
            elif price < prev:
                color = "red"
                arrow = "↓"
            else:
                color = "black"
                arrow = "→"
            
            self.market_box.insert(tk.END, f"{symbol}: ${price:.2f} {arrow}\n", symbol)
            self.market_box.tag_config(symbol, foreground=color)
        
        self.previous_prices = stocks.copy()
        self.market_box.config(state="disabled")
        
        # Update portfolio value chart
        self.portfolio_history.append(self.portfolio.total_value(stocks))
        self.ax.clear()
        self.ax.plot(self.portfolio_history, marker="o")
        self.ax.set_title("Portfolio Value Over Time")
        self.ax.set_ylabel("Value ($)")
        self.canvas.draw()

#########   Buy/Sell Handlers   ###########    
    def buy(self):
        try:
            stock = self.selected_stock.get()
            qty = int(self.qty_entry.get())
            price = self.market.get_price(stock)
            
            success, message = self.portfolio.buy(stock, qty, price)
            
            if success:
                # Log transaction
                log_transaction("BUY", stock, qty, price, self.portfolio.balance)
                
                # Update market and log prices
                self.market.update_prices()
                log_market_snapshot(self.market.get_all_prices())
                
                self.refresh()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        
        except ValueError:
            messagebox.showerror("Error", "Enter a valid quantity")
    
    def sell(self):
        """Handle sell button click"""
        try:
            stock = self.selected_stock.get()
            qty = int(self.qty_entry.get())
            price = self.market.get_price(stock)
            
            success, message = self.portfolio.sell(stock, qty, price)
            
            if success:
                # Log transaction
                log_transaction("SELL", stock, qty, price, self.portfolio.balance)
                
                # Update market and log prices
                self.market.update_prices()
                log_market_snapshot(self.market.get_all_prices())
                
                self.refresh()
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        
        except ValueError:
            messagebox.showerror("Error", "Enter a valid quantity")

#########   Run the GUI main loop   ###########    
    def run(self):
        self.root.mainloop()