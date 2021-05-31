from turtle import Screen, Turtle
from annotation import Annotation
import pandas
import os
import sys


# noinspection PyBroadException
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


screen = Screen()
screen.title("U.S. States Game")

image = resource_path("blank_states_img.gif")

screen.addshape(image)
turtle = Turtle(image)
annotation = Annotation()

states_file = resource_path("50_states.csv")
data = pandas.read_csv(states_file)

states = data["state"].tolist()

while states:
    answer_state = screen.textinput(title=f"{50 - len(states)} / 50 States Correct",
                                    prompt="What's another state's name?")
    answer_state = str(answer_state).title()
    if answer_state == "Exit":
        break

    if answer_state in states:
        state_data = data[data["state"] == answer_state]
        x_text = int(state_data.x)
        y_text = int(state_data.y)
        annotation.create(answer_state, x_text, y_text)
        states.remove(answer_state)

df = pandas.DataFrame(states)
df.to_csv("states_to_learn.csv")
