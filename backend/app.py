from flask import Flask, jsonify,request
from flask_cors import CORS
from db_utils import *
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from routes.portfolio_endpoint import portfolio_bp
from routes.yfinance_endpoint import yfinance_bp
from routes.search_endpoint import search_bp
from routes.quote_list_endpoint import quote_list_bp  # ✅ adjust filename to match your project
from models import *


app = Flask(__name__)

CORS(app)

app.register_blueprint(portfolio_bp)
app.register_blueprint(yfinance_bp)
app.register_blueprint(search_bp)
app.register_blueprint(quote_list_bp)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
