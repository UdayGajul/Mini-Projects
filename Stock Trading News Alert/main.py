# Stock trading news alert project

import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Here AV or av means Alpha Vantage
# And NA or na means News API

load_dotenv()

# Stock constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
AV_API_KEY = os.getenv("AV_API_KEY")
AV_ENDPOINT = "https://www.alphavantage.co/query"

# News constants
NA_API_KEY = os.getenv("NA_API_KEY")
NA_ENDPOINT = "https://newsapi.org/v2/everything"

# Twilio constants
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# TODO 1 Get the stock percentage
av_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": AV_API_KEY,
}


stock_api = requests.get(url=AV_ENDPOINT, params=av_parameters)

stock_api.raise_for_status()

stock_data = stock_api.json()

today = datetime.now().date()

yesterday = str(today - timedelta(days=1))

day_before_yesterday = str(today - timedelta(days=2))

# print(yesterday, type(yesterday), day_before_yesterday, type(day_before_yesterday))


yesterday_price = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_price = float(
    stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"]
)

# print(yesterday_price, type(yesterday_price), day_before_yesterday_price, type(day_before_yesterday_price))

price_difference = yesterday_price - day_before_yesterday_price

up_down = None
if price_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage = round((price_difference / yesterday_price) * 100)

# print(percentage)

if abs(percentage) > 5:
    # print('Get news')

    # TODO 2 get news
    na_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NA_API_KEY,
    }

    news_api = requests.get(url=NA_ENDPOINT, params=na_parameters)

    news_api.raise_for_status()

    news_data = news_api.json()["articles"][:3]

    # print(news_data)

    # with open('stock-news.json', 'w') as j:
    #     json.dump(news_data, j, indent=4)

    formatted_articles = [
        f"{STOCK}: {up_down}{percentage}%\nHeadlines: {article['title']}\nBrief: {article['description']}"
        for article in news_data
    ]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=os.getenv("FROM"),
            to=os.getenv("TO"),
            content_sid=os.getenv("CONTENT_SID"),
        )

    print(message.sid, message.status)

else:
    print('no news')

# USE - PythonAnywhere to run daily
