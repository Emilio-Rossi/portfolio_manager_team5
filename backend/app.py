from flask import Flask, jsonify,request
from db_utils import *
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

from models import *
app = Flask(__name__)

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    try:
        items = get_all_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/portfolio', methods=['POST'])
def insert_portfolio():
    try:
        data = request.get_json()
        item = PortfolioItem(**data)  # Validate
        new_id = insert_portfolio_item(item)
        return jsonify({
            "message": "Portfolio item added successfully",
            "id": new_id,
            "data": item.dict()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True, port=5000)
