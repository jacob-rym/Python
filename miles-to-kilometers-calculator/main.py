from tkinter import *


def miles_to_kms():
    miles = float(entry.get())
    kms = round(miles * 1.609344, 2)
    amount_label.config(text=str(kms))


window = Tk()
window.title("Miles to Kilometers Calculator")
window.geometry("300x100")
window.config(padx=30, pady=15)

entry = Entry()
entry.grid(column=1, row=0)

miles_label = Label(text="Miles")
miles_label.grid(column=2, row=0)

is_equal_label = Label(text="is equal to")
is_equal_label.grid(column=0, row=1)

amount_label = Label(text="0")
amount_label.grid(column=1, row=1)

km_label = Label(text="Km")
km_label.grid(column=2, row=1)

calc_button = Button(text="Calculate", command=miles_to_kms)
calc_button.grid(column=1, row=2)

window.mainloop()
