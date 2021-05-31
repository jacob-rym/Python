import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API_KEY = ""
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_API_KEY = ""
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_PHONE_NUM = ""
MY_PHONE_NUM = ""
account_sid = ""
auth_token = ""

alpha_req = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY,
}

alpha_rsp = requests.get(url=ALPHA_ENDPOINT, params=alpha_req)
alpha_rsp.raise_for_status()
tesla_stocks = alpha_rsp.json()
two_previous_days = list(tesla_stocks["Time Series (Daily)"].keys())[:2]
two_previous_days.reverse()

closing_price = []
for day in two_previous_days:
    closing_price.append(float(tesla_stocks["Time Series (Daily)"][day]["4. close"]))

delta = closing_price[1] / closing_price[0]

is_delta_5 = False
delta_title = ""

if delta >= 1.05:
    delta_title = f"TSLA: 🔺{round(abs((delta-1)*100), 2)}%\n"
    is_delta_5 = True
elif delta <= 0.95:
    delta_title = f"TSLA: 🔻{round(abs((delta-1)*100), 2)}%\n"
    is_delta_5 = True


if is_delta_5:
    news_req = {
        "q": COMPANY_NAME,
        "pageSize": 3,
        "apiKey": NEWS_API_KEY,
    }

    news_rsp = requests.get(url=NEWS_ENDPOINT, params=news_req)
    news_rsp.raise_for_status()

    tesla_articles = news_rsp.json()

    notification = delta_title

    for article in tesla_articles["articles"]:
        notification += f"""Headline: {article['title']}\nBrief: {article['description']}\n\n"""

    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(
        to=MY_PHONE_NUM,
        from_=TWILIO_PHONE_NUM,
        body=notification)
    print(message.status)
