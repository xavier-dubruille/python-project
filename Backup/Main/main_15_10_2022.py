from Class.Car import Car
import sqlite3 as sql
import tkinter as tk
import tkinter.font as font

def ExecuteQuery(query, frameResults): 
    dbConnection = sql.connect("./Db/bambooConcess.db")
    cursor = dbConnection.cursor()

    cursor.execute(query) 

    arrayLabelQuery = []
    count = 0
    for e in cursor.fetchall():
        arrayLabelQuery.append(tk.Label(frameResults, text = e))
        arrayLabelQuery[count].pack()
        count += 1
    cursor.close()

def ShowStock(frameResults):
    ExecuteQuery("select prixCar as Prix, nameBrand as Brand, nameMotor as Motor, nameType as Type, \
        stockDateCar as DateStock, techControlDateCar as ControlDate, promoCar as Promotion from car \
        NATURAL join Brand NATURAL join Motor NATURAL join Type", frameResults)

def ShowHistory(frameResults):
    ExecuteQuery("select prixCar as Prix, nameBrand as Brand, nameMotor as Motor, nameType as Type, \
        stockDateCar as DateStock, techControlDateCar as ControlDate, promoCar as Promotion from car \
        NATURAL join Brand NATURAL join Motor NATURAL join Type", frameResults)

def MakeReservation():
    pass

def MakeDeal():
    pass

def AddCar():
    pass

def main():

    window = tk.Tk()
    window.title("Bamboo Concess")
    window.attributes('-fullscreen', True)

    window.columnconfigure(0, weight = 2)
    window.columnconfigure(1, weight = 3)
    window.columnconfigure(2, weight = 1)
    window.columnconfigure(3, weight = 1)

    for i in range(6):
        window.rowconfigure(i, weight = 1)
    window.rowconfigure(7, weight = 2)

    frameButtons = tk.Frame(window, highlightthickness=2, highlightbackground = "black")
    frameButtons.grid(column = 0, row = 1, rowspan = 5, sticky = "wesn")
    buttonStock = tk.Button(frameButtons, text = "Display Stock", command = lambda : ShowStock(frameDisplay))
    buttonStock.pack()
    buttonHistory = tk.Button(frameButtons, text = "Display History", command = lambda : ShowHistory(frameDisplay))
    buttonHistory.pack()
    buttonReservation = tk.Button(frameButtons, text = "Make a reservation", command = MakeReservation)
    buttonReservation.pack()
    buttonDeal = tk.Button(frameButtons, text = "Make a deal", command = MakeDeal)
    buttonDeal.pack()
    buttonAddCar = tk.Button(frameButtons, text = "Add a car", command = AddCar)
    buttonAddCar.pack()


    frameTitle = tk.Frame(window, highlightthickness=2, highlightbackground = "yellow")
    frameTitle.grid(column = 1, row = 0, sticky = "wesn")
    labelTitle = tk.Label(frameTitle, text = "Bamboo Concess")
    labelTitle.pack()

    frameSort = tk.Frame(window, highlightthickness = 2, highlightbackground = "blue")
    frameSort.grid(column = 1, row = 1, sticky = "wesn")

    frameDisplay = tk.Frame(window, highlightthickness=2, highlightbackground = "pink")
    frameDisplay.grid(column = 1, row = 2, rowspan=6, sticky="wesn")

    frameOnClick = tk.Frame(window, highlightthickness=2, highlightbackground = "purple")
    frameOnClick.grid(column = 2, row = 1, rowspan = 7, columnspan = 2, sticky ="wesn")

    frameExit = tk.Frame(window)
    frameExit.grid(column = 3, row = 0, sticky = "wesn")    
    buttonExit = tk.Button(frameExit, text = "Exit", command = window.destroy, relief='raised', font=font.Font(family='Helvetica', size=15, weight='bold'))
    buttonExit.pack()

    ExecuteQuery("select prixCar as Prix, nameBrand as Brand, nameMotor as Motor, nameType as Type, \
        stockDateCar as DateStock, techControlDateCar as ControlDate, promoCar as Promotion from car \
        NATURAL join Brand NATURAL join Motor NATURAL join Type", frameDisplay)

    window.mainloop()

main()