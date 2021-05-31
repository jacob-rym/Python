import requests
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = 0.0
MY_LONG = 0.0
APP_ID = ""

TWILIO_PHONE_NUM = ""
MY_PHONE_NUM = ""
account_sid = ""
auth_token = ""

req = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": APP_ID,
}

response = requests.get(url=OWM_ENDPOINT, params=req)
response.raise_for_status()
weather_data = response.json()

will_be_raining = False
for hour in weather_data["hourly"][:12]:
    if hour["weather"][0]["id"] < 700:
        will_be_raining = True

if will_be_raining:
    print("It will rain in specified location in the next 12hrs.")
    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(
        to=MY_PHONE_NUM,
        from_=TWILIO_PHONE_NUM,
        body="It will rain in specified location in the next 12hrs ☂️")
    print(message.status)
else:
    print("It will NOT rain in specified location in the next 12hrs.")
