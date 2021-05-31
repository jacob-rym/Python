import datetime as dt
import pandas
from random import choice
import smtplib

USER_EMAIL = ""
PASS = ""
SMTP = ""

birthdays = pandas.read_csv("birthdays.csv").to_dict(orient="records")

birthday_person = None
day_today = dt.datetime.today().day
month_today = dt.datetime.today().month

for person in birthdays:
    if person["day"] == day_today and person["month"] == month_today:
        birthday_person = person
        break

msg = ""
if birthday_person is not None:
    letters = ("letter_1.txt", "letter_2.txt", "letter_3.txt")
    chosen_letter = choice(letters)
    try:
        with open(file=f"letter_templates/{chosen_letter}") as file:
            letter = file.readlines()
    except FileNotFoundError as e:
        print(f"Letter file not found.\n{e}")
    else:
        msg = "".join(letter)
        msg = msg.replace("[NAME]", birthday_person["name"])
        msg = f"Subject:Happy birthday {birthday_person['name']}!\n\n" + msg

if msg is not "":
    with smtplib.SMTP(SMTP) as connection:
        connection.starttls()
        connection.login(user=USER_EMAIL, password=PASS)
        connection.sendmail(from_addr=USER_EMAIL, to_addrs=birthday_person["email"], msg=msg)
