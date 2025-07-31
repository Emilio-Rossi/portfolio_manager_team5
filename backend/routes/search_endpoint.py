from flask import Blueprint, Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)
search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('', methods=['GET'])
def search_stock():
    query = request.args.get('q', '').upper()

    if not query:
        return jsonify([])

    try:
        ticker = yf.Ticker(query)
        info = ticker.info

        return jsonify({
                "symbol": info.get("symbol", query),
                "name": info.get("shortName", "N/A"),
                "price": round(info.get("regularMarketPrice", 0), 2),
                "change": f"{round(info.get('regularMarketChangePercent', 0), 2)}%"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 400



