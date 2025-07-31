from flask import Flask, jsonify,request
from db_utils import *
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from routes.portfolio_endpoint import portfolio_bp
from routes.yfinance_endpoint import yfinance_bp
from routes.search_endpoint import search_bp
from models import *
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(portfolio_bp)
app.register_blueprint(yfinance_bp)
app.register_blueprint(search_bp)
CORS(app)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
