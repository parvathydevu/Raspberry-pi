# gui.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

class StockAppGUI:
    def __init__(self, root, start_callback, stop_callback):
        self.root = root
        self.root.title("Live Stock Plotter")

        # Dropdown
        self.symbol_var = tk.StringVar()
        ttk.Label(root, text="Select Stock:").pack()
        self.symbol_entry = ttk.Combobox(root, textvariable=self.symbol_var)
        self.symbol_entry['values'] = ['TCS.NS', 'INFY.NS', 'RELIANCE.NS']
        self.symbol_entry.pack()

        # Buttons
        self.start_button = ttk.Button(root, text="Start", command=start_callback)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=stop_callback)
        self.stop_button.pack(pady=5)

        # Plot area
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Live Stock Price")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.line, = self.ax.plot([], [], marker='o')

        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        # Data storage
        self.timestamps = []
        self.prices = []

    def update_plot(self, timestamp, price):
        if timestamp and price:
            self.timestamps.append(timestamp)
            self.prices.append(price)

            # Keep only last 20 points
            self.timestamps = self.timestamps[-20:]
            self.prices = self.prices[-20:]

            self.line.set_data(self.timestamps, self.prices)
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
