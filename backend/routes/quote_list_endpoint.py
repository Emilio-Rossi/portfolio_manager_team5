from flask import Blueprint, Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)
quote_list_bp = Blueprint('quote_list', __name__)


@quote_list_bp.route('/quote-list')
def quote_list():
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META']
    results = []

    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            results.append({
                "symbol": info.get("symbol", symbol),
                "name": info.get("shortName", "N/A"),
                "price": round(info.get("regularMarketPrice", 0), 2),
                "change": f"{round(info.get('regularMarketChangePercent', 0), 2)}%"
            })
        except Exception as e:
            print(f"Error loading {symbol}: {e}")

    return jsonify(results)