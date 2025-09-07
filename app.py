import requests
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch API key and secret from environment variables
API_KEY = os.getenv("API_KEY")
FINNHUB_SECRET = os.getenv("FINNHUB_SECRET")

# Verify API_KEY and FINNHUB_SECRET are set
if not API_KEY or not FINNHUB_SECRET:
    raise ValueError("API_KEY or FINNHUB_SECRET is not set. Check your .env file.")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all origins on /api routes

@app.route('/', methods=['GET'])
def status():
    """
    Endpoint to check if the API is running.
    """
    return jsonify({"status": "API is running", "message": "Welcome to the Stock Web Crawler API!"})

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """
    Fetch stock data for a given symbol using the Finnhub API.
    """
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": symbol, "token": API_KEY}
    headers = {"X-Finnhub-Secret": FINNHUB_SECRET}

    try:
        # Make the API request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        data = response.json()

        # Validate response structure
        if "c" in data:  # 'c' is the current price key
            return jsonify({
                "symbol": symbol,
                "current_price": data.get("c"),
                "high_price": data.get("h"),
                "low_price": data.get("l"),
                "open_price": data.get("o"),
                "previous_close_price": data.get("pc"),
            })
        else:
            return jsonify({"error": f"Stock data not found for symbol: {symbol}"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error connecting to Finnhub API", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
