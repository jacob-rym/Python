from tkinter import *
from math import floor
import os


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# noinspection PyBroadException
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def reset_countdown():
    global reps
    reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_lab.config(text="Timer")
    checkmarks_lab.config(text="")


def start_countdown():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_lab.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_lab.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer_lab.config(text="Work", fg=GREEN)


def count_down(count):
    global reps
    mins = count // 60
    secs = count % 60

    canvas.itemconfig(timer_text, text=f"{mins:02d}:{secs:02d}")
    if count >= 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_countdown()
        marks = ""
        work_sessions = floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmarks_lab.config(text=marks)


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = resource_path("tomato.png")
tomato_img = PhotoImage(file=img)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_lab = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
timer_lab.grid(column=1, row=0)

start_but = Button(text="Start", highlightthickness=0, command=start_countdown)
start_but.grid(column=0, row=2)

reset_but = Button(text="Reset", highlightthickness=0, command=reset_countdown)
reset_but.grid(column=2, row=2)

checkmarks_lab = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
checkmarks_lab.grid(column=1, row=3)

window.mainloop()
