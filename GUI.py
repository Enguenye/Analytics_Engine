from tkinter import *
from tkinter import ttk
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

def clicked6():
    a.map2()

def clicked7():
    a.KilometersTraveled()

def clicked8():
    a.KilometersTraveledbyUser()

def clicked9():
    a.QuarantineUV()

def clicked10():
    a.QuarantineAQ()

def clicked11():
    a.HeatMapUV()

def clicked12():
    a.HeatMapAQ()

def clicked13():
    a.HeatMap()

def clicked14():
    a.UserActivityPerHour()

def clicked15():
    a.UserActivityPerDayWeek()

def clicked16():
    a.growthofUV()

def clicked17():
    a.growthofAQ()

def clicked18():
    a.AqPerZone()

def clicked19():
    a.UvPerZone()

def clicked20():
    a.UserAvtivityPerZone()

a=Analytics()

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('650x1000')

tab_control = ttk.Notebook(window)
tab_control.pack(padx=10, pady=10)
tab1 = ttk.Frame(tab_control)
tab1.pack(side=RIGHT, fill=BOTH)
tab_control.add(tab1, text='AQ/UV Information')
tab2 = ttk.Frame(tab_control)
tab2.pack(side = RIGHT, fill = BOTH)
tab_control.add(tab2, text='Geographical location')

tab3 = ttk.Frame(tab_control)
tab3.pack(side = RIGHT, fill = BOTH)
tab_control.add(tab3, text='Users information')

tab4 = ttk.Frame(tab_control)
tab4.pack(side = RIGHT, fill = BOTH)
tab_control.add(tab4, text='Other questions of interest')

tab5 = ttk.Frame(tab_control)
tab5.pack(side = RIGHT, fill = BOTH)
tab_control.add(tab5, text='Zones information')


btn = Button(tab1, text="Distribution of UV radiation per day of the week",command=clicked1,
          height = 7,
          width = 80)

btn.pack(pady = 20, padx = 20)

btn2 = Button(tab1, text="Distribution of air pollution per day of the week",command=clicked2,
          height = 7,
          width = 80)
btn2.pack(pady = 20, padx = 20)

btn3 = Button(tab2, text="Map(How are the uv quality measures around Bogota)",command=clicked3,
          height = 7,
          width = 80)
btn3.pack(pady = 20, padx = 20)

btn4 = Button(tab1, text="Methane concentration on the air per hour of the day",command=clicked4,
          height = 7,
          width = 80)

btn4.pack(pady = 20, padx = 20)

btn5 = Button(tab1, text="UV radiation around bogota per hour of the day",command=clicked5,
          height = 7,
          width = 80)

btn5.pack(pady = 20, padx = 20)

btn6 = Button(tab2, text="Map(How are the air pollution measures around Bogota)",command=clicked6,
          height = 7,
          width = 80)

btn6.pack(pady = 20, padx = 20)

btn7 = Button(tab3, text="Total of kilometers traveled per month",command=clicked7,
          height = 7,
          width = 80)

btn7.pack(pady = 20, padx = 20)

btn8 = Button(tab3, text="Kilometers traveled by user",command=clicked8,
          height = 7,
          width = 80)

btn8.pack(pady = 20, padx = 20)

btn9 = Button(tab4, text="Effects of the quarantine on uv radiation quality",command=clicked9,
          height = 7,
          width = 80)

btn9.pack(pady = 20, padx = 20)

btn10 = Button(tab4, text="Effects of quarantine on the air quality of the city",command=clicked10,
          height = 7,
          width = 80)

btn10.pack(pady = 20, padx = 20)

btn11= Button(tab2, text="Heat map of UV radiation",command=clicked11,
          height = 7,
          width = 80)

btn11.pack(pady = 20, padx = 20)

btn12= Button(tab2, text="Heat map of air quality",command=clicked12,
          height = 7,
          width = 80)

btn12.pack(pady = 20, padx = 20)

btn13 = Button(tab3, text="Heat map of user engagement",command=clicked13,
          height = 7,
          width = 80)

btn13.pack(pady = 20, padx = 20)

btn14 = Button(tab3, text="Hours of the day with the most user engagement",command=clicked14,
          height = 7,
          width = 80)

btn14.pack(pady = 20, padx = 20)

btn15 = Button(tab3, text="Days of the week with the most user engagement",command=clicked15,
          height = 7,
          width = 80)

btn15.pack(pady = 20, padx = 20)

btn16 = Button(tab1, text="Change of UV radiation during the year",command=clicked16,
          height = 7,
          width = 80)

btn16.pack(pady = 20, padx = 20)

btn17 = Button(tab1, text="Change of air quality during the year",command=clicked17,
          height = 7,
          width = 80)

btn17.pack(pady = 20, padx = 20)

btn18 = Button(tab5, text="Air quality per zone on Bogota",command=clicked18,
          height = 7,
          width = 80)

btn18.pack(pady = 20, padx = 20)

btn19 = Button(tab5, text="UV radiation per zone on Bogota",command=clicked19,
          height = 7,
          width = 80)

btn19.pack(pady = 20, padx = 20)

btn20 = Button(tab5, text="User actitivy per zone",command=clicked20,
          height = 7,
          width = 80)

btn20.pack(pady = 20, padx = 20)



window.mainloop()