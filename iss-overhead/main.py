import requests
from datetime import datetime
from time import sleep
import smtplib

MY_LAT = 0.0
MY_LONG = 0.0
USER_EMAIL = ""
PASS = ""


def is_iss_visible():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])

    if ((MY_LAT - 5) < iss_latitude < (MY_LAT + 5)) and ((MY_LONG - 5) < iss_longitude < (MY_LONG + 5)):
        return True
    else:
        return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 2
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 2

    time_now = datetime.now().hour

    if sunrise >= time_now or time_now >= sunset:
        return True
    else:
        return False


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=USER_EMAIL, password=PASS)
        connection.sendmail(
            from_addr=USER_EMAIL,
            to_addrs=USER_EMAIL,
            msg=f"Subject:ISS is visible\n\nLook up!"
        )


while True:
    print(f"Is it dark? {is_dark()}")
    print(f"ISS visible? {is_iss_visible()}")

    if is_dark() and is_iss_visible():
        print("ISS is currently visible from your location.")
        send_email()
        break
    else:
        print("ISS is currently NOT visible from your location.")
        sleep(60)
