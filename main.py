import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

import requests
import twilio

symbol = "TSLA"
company = "Tesla Inc"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "apikey": os.environ.get("stock_api_key"),
}

stock_response = requests.get(
    url="https://www.alphavantage.co/query", params=parameters)
stock_response.raise_for_status()

daily_stocks = stock_response.json()['Time Series (Daily)']


# use datetime and timedelta to get yesterday and the day before yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
day_before_yesterday = (
    datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

# append last two days in list
last_two_days = [values for key, values in daily_stocks.items() if key ==
                 yesterday or key == day_before_yesterday]


yesterday_closing_stock_price = float(last_two_days[0]['4. close'])

day_before_yesterday_closing_price = float(last_two_days[1]['4. close'])

difference = yesterday_closing_stock_price - day_before_yesterday_closing_price

# increase by 5 % or more / decrease by 5 % or more
if difference >= (5/100 * day_before_yesterday_closing_price) or (day_before_yesterday_closing_price+difference) <= (95/100 * day_before_yesterday_closing_price):

    news_api = requests.get(
        url="https://newsdata.io/api/1/latest?apikey=pub_43d9cf6dbb9545f591061ec4cd8789e8&q=tesla%20inc")
    news_api.raise_for_status()
    # slicing to lastest 3 updates
    last_3_news = news_api.json()['results'][:3]

    # rearranging the news data as dict with title, link and description
    lastest_3 = [{'title': i['title'], 'link': i['link'],
                  'description': i['description']} for i in last_3_news]

    with smtplib.SMTP_SSL("smtp.gmail.com") as mail_connection:
        mail_connection.login(
            user=os.environ.get("email"), password=os.environ.get("password"))
        for news in lastest_3:
            email = EmailMessage()
            email['Subject'] = f"{company} Stock Update"
            email['From'] = os.environ.get("email")
            email['To'] = os.environ.get("receiver")
            email.set_content(
                f"Title: {news['title']}\nLink: {news['link']}\nDescription: {news['description']}")
            mail_connection.send_message(email)
