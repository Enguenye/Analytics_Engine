from tkinter import *
from Main import Analytics


def clicked1():
    a.averageUVPerDay()

def clicked2():
    a.averageAQPerDay()

def clicked3():
    a.map()

def clicked4():
    a.Methane_concentration_per_hour()

def clicked5():
    a.Radiation()

a=Analytics()

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('100x500')

btn = Button(window, text="Average UV radiation per day of the week",command=clicked1,
          height = 7,
          width = 80)

btn.grid(column=3, row=1)

btn2 = Button(window, text="Average air pollution per day of the week",command=clicked2,
          height = 7,
          width = 80)

btn2.grid(column=3, row=2)
btn3 = Button(window, text="Map(How are the air pollution and uv quality measures around Bogota)",command=clicked3,
          height = 7,
          width = 80)

btn3.grid(column=3, row=3)
btn4 = Button(window, text="Methane concentration on the air per hour of the day",command=clicked4,
          height = 7,
          width = 80)

btn4.grid(column=3, row=4)
btn5 = Button(window, text="UV radiation around bogota per hour of the day",command=clicked5,
          height = 7,
          width = 80)

btn5.grid(column=3, row=5)


window.mainloop()