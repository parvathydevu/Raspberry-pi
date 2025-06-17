# main.py
import tkinter as tk
from gui import StockAppGUI
from logic import fetch_stock_price
import threading
import time

class StockApp:
    def __init__(self, root):
        self.gui = StockAppGUI(root, self.start_plotting, self.stop_plotting)
        self.running = False
        self.thread = None

    def fetch_and_plot(self):
        while self.running:
            symbol = self.gui.symbol_var.get()
            timestamp, price = fetch_stock_price(symbol)
            self.gui.update_plot(timestamp, price)
            time.sleep(60)  # Refresh every 60 seconds

    def start_plotting(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.fetch_and_plot, daemon=True)
            self.thread.start()

    def stop_plotting(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()