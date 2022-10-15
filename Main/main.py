# from Class.Car import Car
from Class.DB import DBAccess as DB
from Class.Car import Car
from tkinter import *
import tkinter as tk
import tkinter.font as font
import sys

class Application:
    def __init__(self): 
        self.main()

    def ExecuteQuery(self, query, frameResults): 
        cursor = DB.DBCursor()
        if cursor != None:
            try:
                cursor.execute(query) 

                arrayLabelQuery = []
                count = 0
                for e in cursor.fetchall():
                    arrayLabelQuery.append(tk.Label(frameResults, text = e))
                    arrayLabelQuery[count].pack()
                    count += 1
                return 1
            except: 
                print("Error in ExecuteQuery")
                print(sys.exc_info())
                return None
            
            finally:
                DB.DBClose(cursor)

    def ShowStock(self, frameResults):
        carList = Car.CarListStock()
        listboxStock = tk.Listbox(frameResults)
        listboxStock.pack(expand = True, fill = "both")
        for car in carList:
            listboxStock.insert(END, "Prix : {}. Type : {}. Motor : {}. Brand : {}. Promotion : {}. In stock since : {}. Next Control : {}" \
                .format(car.prixCar, car.idType, car.idMotor, car.idBrand, car.promoCar, car.stockDateCar, car.techControlDateCar))
        


        
    def ShowHistory(self, frameResults):
        self.ExecuteQuery("select prixCar as Prix, nameBrand as Brand, nameMotor as Motor, nameType as Type, \
            stockDateCar as DateStock, techControlDateCar as ControlDate, promoCar as Promotion from car \
            NATURAL join Brand NATURAL join Motor NATURAL join Type", frameResults)

    def MakeReservation(self):
        pass

    def MakeDeal(self):
        pass

    def AddCar(self):
        pass

    def main(self):

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
        buttonStock = tk.Button(frameButtons, text = "Display Stock", command = lambda : self.ShowStock(frameDisplay))
        buttonStock.pack()
        buttonHistory = tk.Button(frameButtons, text = "Display History", command = lambda : self.ShowHistory(frameDisplay))
        buttonHistory.pack()
        buttonReservation = tk.Button(frameButtons, text = "Make a reservation", command = self.MakeReservation)
        buttonReservation.pack()
        buttonDeal = tk.Button(frameButtons, text = "Make a deal", command = self.MakeDeal)
        buttonDeal.pack()
        buttonAddCar = tk.Button(frameButtons, text = "Add a car", command = self.AddCar)
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

        self.ShowStock(frameDisplay)

        window.mainloop()

Application()