import os

import requests

symbol = "TSLA"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": os.environ.get("stock_api_key"),
}

stock_response = requests.get(
    url="https://www.alphavantage.co.query", params=parameters)
stock_response.raise_for_status()

daily_stocks = stock_response.json()

print(daily_stocks)
