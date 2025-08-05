# routes/portfolio_endpoint.py
from decimal import Decimal
from flask import Blueprint, jsonify, request
from models import PortfolioItem
from db_utils import get_net_quantity, view_portfolios, insert_portfolio_item,view_purchases,get_current_balance, get_all_balance
from function import get_latest_stock_price

portfolio_bp = Blueprint('portfolio', __name__)

# GET /portfolio
@portfolio_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    try:
        items = view_portfolios()
        for item in items:        
            price=get_latest_stock_price(item['ticker'])
            dPrice=Decimal(str(price))
            val=dPrice*item['total_quantity']
            item['current_value'] = round(float(val), 2)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
#GET /purchases/all
@portfolio_bp.route('/purchases/all', methods=['GET'])
def get_purchases():
    try:
        items = view_purchases()
        for item in items:
            print(item)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@portfolio_bp.route('/balance', methods=['GET'])
def get_balance():
    try:
        balance = get_current_balance()  # returns float
        return jsonify({"current_balance": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /portfolio
@portfolio_bp.route('/portfolio', methods=['POST'])
def insert_portfolio():
    try:
        data = request.get_json()
        # Get latest stock price
        price = get_latest_stock_price(data['ticker'])
        if price is None:
            return jsonify({"error": "Invalid ticker or stock price unavailable"}), 400

        # Calculate balance
        current_balance = get_current_balance()
        cost = price * data['quantity']
        
        if current_balance < cost:
            return jsonify({"error": "Not enough balance to purchase this stock"}), 400
        
        # Update data with computed fields
        data['purchase_price'] = price
        data['balance'] = current_balance - cost

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
@portfolio_bp.route('/sell/portfolio', methods=['POST'])
def sell_portfolio():
    try:
        data = request.get_json()
        price=get_latest_stock_price(data['ticker'])

        data['purchase_price']=price
        data['balance']=get_current_balance()+price*data['quantity']

        sell_item = PortfolioItem(**data)  # Validate input

        # Check holdings
        net_quantity = get_net_quantity(sell_item.ticker)
        if net_quantity <= 0:
            return jsonify({"error": f"No holdings found for {sell_item.ticker}"}), 400
        if sell_item.quantity > net_quantity:
            return jsonify({"error": f"Cannot sell {sell_item.quantity}, only {net_quantity} available"}), 400


        # Prepare DB insert
        insert_data = {
            "ticker": sell_item.ticker,
            "quantity": -sell_item.quantity,  # negative for sell
            "asset_type": "equity",  # or dynamic lookup
            "purchase_price": sell_item.purchase_price,
            "purchase_date": sell_item.purchase_date,
            "balance":sell_item.balance

        }
        # Insert into DB
        new_id = insert_portfolio_item(PortfolioItem(**insert_data))

        return jsonify({
            "message": "Portfolio item added successfully",
            "id": new_id,
            "data": sell_item.dict() # ✅ Convert Pydantic object to dict
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400