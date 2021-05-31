from turtle import Turtle

FONT = ("Arial", 9, "normal")
ALIGN = "center"


class Annotation(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()

    def create(self, text, x, y):
        self.goto(x, y)
        self.write(text, align=ALIGN, font=FONT)
