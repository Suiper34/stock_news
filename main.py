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

# print(daily_stocks)

# use datetime and timedelta to get yesterday and the day before yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (
    datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

# append last two days in list
last_two_days = [values for key, values in daily_stocks.items() if key ==
                 yesterday or key == day_before_yesterday]
print(last_two_days)

yesterday_closing_stock_price = last_two_days[0]['close']


day_before_yesterday_closing_price = last_two_days[1]['close']

difference = yesterday_closing_stock_price - day_before_yesterday_closing_price

# increase by 5 % or more / decrease by 5 % or more
if difference >= (5/100 * day_before_yesterday_closing_price) or (day_before_yesterday_closing_price+difference) <= (95/100 * day_before_yesterday_closing_price):
    print("get new update")
