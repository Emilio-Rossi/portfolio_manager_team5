from flask import Flask, jsonify
from db_utils import get_all_items
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    try:
        items = get_all_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
