from flask import jsonify
import yfinance as yf
def get_latest_stock_price(ticker_symbol):
    if not ticker_symbol:
        raise ValueError("Please provide a stock symbol")

    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period="1d")

    if hist.empty:
        raise ValueError("Invalid symbol or no data found")
    
    return round(float(hist['Close'].iloc[-1]), 2)


