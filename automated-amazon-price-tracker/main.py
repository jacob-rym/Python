import requests
from bs4 import BeautifulSoup
import smtplib

TRACKED_PRODUCT_URL = ""
DUMMY_HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

USER_EMAIL = ""
PASS = ""
SMTP = ""
NOTIFY_EMAIL = ""

item_page = requests.get(url=TRACKED_PRODUCT_URL, headers=DUMMY_HEADERS)
item_page.raise_for_status()

soup = BeautifulSoup(item_page.content, "lxml")
price = soup.find("span", {"class": "a-color-price"})

float_price = float(price.text.split()[0].replace(",", "."))
notify_price = 100.0

msg = f"Subject:New price for observed item!\n\nThere is a new price on your observed item - {TRACKED_PRODUCT_URL}"

if float_price < notify_price:
    with smtplib.SMTP(SMTP) as connection:
        connection.starttls()
        connection.login(USER_EMAIL, PASS)
        connection.sendmail(from_addr=USER_EMAIL, to_addrs=NOTIFY_EMAIL, msg=msg)

    print("Email sent!")

else:
    print("Email not sent.")
