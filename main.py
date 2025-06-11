import os
from datetime import datetime, timedelta

import requests

symbol = "TSLA"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": os.environ.get("stock_api_key"),
}

stock_response = requests.get(
    url="https://www.alphavantage.co/query", params=parameters)
stock_response.raise_for_status()

daily_stocks = stock_response.json()['Time Series (Daily)']

print(daily_stocks)

# use datetime and timedelta to get yesterday and the day before yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (
    datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
