# routes/portfolio_endpoint.py
from flask import Blueprint, jsonify, request
from models import PortfolioItem
from db_utils import view_portfolios, insert_portfolio_item,view_purchases

portfolio_bp = Blueprint('portfolio', __name__)

# GET /portfolio
@portfolio_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    try:
        items = view_portfolios()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#GET /purchases/all
@portfolio_bp.route('/purchases/all', methods=['GET'])
def get_purchases():
    try:
        items = view_purchases()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST /portfolio
@portfolio_bp.route('/portfolio', methods=['POST'])
def insert_portfolio():
    try:
        data = request.get_json()
        item = PortfolioItem(**data)  # Validate with Pydantic
        new_id = insert_portfolio_item(item)
        return jsonify({
            "message": "Portfolio item added successfully",
            "id": new_id,
            "data": item.dict()  # ✅ Convert Pydantic object to dict
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
#POST /sell portfolio
