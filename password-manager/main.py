from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os
import json


# noinspection PyBroadException
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
    password_list.extend([choice(letters) for _ in range(randint(8, 10))])
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save():
    web = website_entry.get()
    em_user = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        web: {
            "email": em_user,
            "password": password,
        }
    }

    if not web or not em_user or not password:
        messagebox.showinfo(title="Oops", message="You left some of the fields empty! "
                                                  "Please fill out all of the fields.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            messagebox.showinfo(title=f"Credentials for {website}",
                                message=f"Email: {data[website]['email']}\n"
                                        f"Password: {data[website]['password']}")
    except FileNotFoundError:
        messagebox.showinfo(title=f"Credentials for {website}",
                            message=f"Sorry, no passwords file found.")
    except KeyError:
        messagebox.showinfo(title=f"Credentials for {website}",
                            message=f"Sorry, no passwords found for {website}.")
    finally:
        website_entry.delete(0, END)


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_lab = Label(text="Website:")
website_lab.grid(column=0, row=1)

website_entry = Entry(width=24)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_but = Button(text="Search", width=14, command=find_password)
search_but.grid(column=2, row=1)

email_username_lab = Label(text="Email/Username:")
email_username_lab.grid(column=0, row=2)

email_username_entry = Entry(width=42)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "qbarym@gmail.com")

password_lab = Label(text="Password:")
password_lab.grid(column=0, row=3)

password_entry = Entry(width=24)
password_entry.grid(column=1, row=3)

generate_pass_but = Button(text="Generate Password", width=14, command=generate_password)
generate_pass_but.grid(column=2, row=3)

add_but = Button(text="Add", width=40, command=save)
window.bind('<Return>', save)
add_but.grid(column=1, row=4, columnspan=2)

window.mainloop()
