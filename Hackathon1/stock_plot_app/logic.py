import yfinance as yf
from datetime import datetime
import requests

# Disable SSL verification (INSECURE)
session = requests.Session()
session.verify = False
yf.shared._requests = session  # patch yfinance

def fetch_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d", interval="1m").tail(1)['Close'].values[0]
        timestamp = datetime.now().strftime("%H:%M:%S")
        return timestamp, price
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None
