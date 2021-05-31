from tkinter import *
from tkinter import messagebox
from pandas import *
from random import choice
import os

BACKGROUND_COLOR = "#B1DDC6"
FLASHCARD_COLOR = "white"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

current_card = {}
to_learn = []


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # noinspection PyBroadException
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def run():
    global to_learn

    try:
        data = pandas.read_csv(resource_path("data/words_to_learn.csv"))
    except FileNotFoundError:
        try:
            data = read_csv(resource_path("data/french_words.csv"))
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="Data file not found.")
        else:
            to_learn = data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")

    next_card()


def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def save_words_to_learn():
    global to_learn, current_card

    try:
        to_learn.remove(current_card)
    except ValueError as ex:
        messagebox.showinfo(title="Error", message=f"Cannot remove card from deck.\n{str(ex)}")
    else:
        pandas.DataFrame(to_learn).to_csv(resource_path("data/words_to_learn.csv"), mode="w", header=True, index=False)

    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file=resource_path("images/wrong.png"))
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

check_image = PhotoImage(file=resource_path("images/right.png"))
known_button = Button(image=check_image, highlightthickness=0, command=save_words_to_learn)
known_button.grid(column=1, row=1)

run()

window.mainloop()
