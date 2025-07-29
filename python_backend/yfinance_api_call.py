from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def get_stock_data():
    # Get ticker symbol from query parameter
    ticker_symbol = request.args.get('symbol')

    if not ticker_symbol:
        return jsonify({"error": "Please provide a stock symbol"}), 400

    # Fetch data using yfinance
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period="1d")

    if hist.empty:
        return jsonify({"error": "Invalid symbol or no data found"}), 404

    # Prepare response
    latest_price = hist['Close'].iloc[-1]
    return jsonify({
        "symbol": ticker_symbol,
        "latest_price": latest_price
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
