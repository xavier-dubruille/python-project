from Class.DB import DBAccess as DB
from Class.Car import Car
from tkinter import *
import tkinter as tk
import tkinter.font as font
import sys

class Application:
    def __init__(self): 
        self.police = "courier 15"
        self.title = "Bamboo Concess"
        self.printDetails = ""
        self.DisplayBasicWindow()

    # The main display function for the application.
    def DisplayBasicWindow(self):

        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.attributes('-fullscreen', True)
        self.window.option_add("*Font", self.police)
        self.window.config(bg="white")

        self.window.columnconfigure(0, weight = 1)
        self.window.columnconfigure(1, weight = 2)
        self.window.columnconfigure(2, weight = 1)

        for i in range(6):
            self.window.rowconfigure(i, weight = 1)
        self.window.rowconfigure(7, weight = 2)

        frameButtons = tk.Frame(self.window)
        frameButtons.grid(column = 0, row = 1, rowspan = 5, sticky = "wesn")
        for i in range(5):
            frameButtons.rowconfigure(i, weight = 1)
        frameButtons.columnconfigure(0, weight = 1)

        buttonStock = tk.Button(frameButtons, text = "Display Stock", command = self.ShowStock, state = "disabled", relief = "raised")
        buttonStock.grid(column = 0, row = 0, sticky = "wesn")
        buttonHistory = tk.Button(frameButtons, text = "Display History", command = self.ShowHistory, relief = "raised")
        buttonHistory.grid(column = 0, row = 1, sticky = "wesn")
        buttonReservation = tk.Button(frameButtons, text = "Make a reservation", command = self.MakeReservation, relief = "raised")
        buttonReservation.grid(column = 0, row = 2, sticky = "wesn")
        buttonDeal = tk.Button(frameButtons, text = "Make a deal", command = self.MakeDeal, relief = "raised")
        buttonDeal.grid(column = 0, row = 3, sticky = "wesn")
        buttonAddCar = tk.Button(frameButtons, text = "Add a car", command = self.AddCar)
        buttonAddCar.grid(column = 0, row = 4, sticky = "wesn")


        frameTitle = tk.Frame(self.window, highlightthickness = 2, highlightbackground = "black")
        frameTitle.grid(column = 1, row = 0, sticky = "wesn")
        labelTitle = tk.Label(frameTitle, text = self.title)
        labelTitle.pack(expand = True, fill = "y")

        frameSort = tk.Frame(self.window, highlightthickness = 1, highlightbackground = "black")
        frameSort.grid(column = 1, row = 1, sticky = "wesn")

        self.frameDisplay = tk.Frame(self.window)
        self.frameDisplay.grid(column = 1, row = 2, rowspan=6, sticky="wesn")

        self.frameDetails = tk.Frame(self.window, highlightthickness=2, highlightbackground = "black")
        self.frameDetails.grid(column = 2, row = 1, rowspan = 7, sticky ="wesn")
        self.frameDetails.rowconfigure(0, weight = 1)
        self.frameDetails.columnconfigure(0, weight = 1)
        self.labelDetails = tk.Label(self.frameDetails, text = self.printDetails, justify="left", highlightthickness = 2, highlightbackground = "black", anchor= 'w')
        self.labelDetails.grid(column = 0, row = 0, sticky = "wesn")


        frameExit = tk.Frame(self.window)
        frameExit.grid(column = 2, row = 0, sticky = "wesn")
        frameExit.rowconfigure(0, weight = 1)
        frameExit.columnconfigure(0, weight = 1)
        buttonExit = tk.Button(frameExit, text = "Exit", command = self.window.destroy, relief='raised', font=font.Font(family='Helvetica', size=15, weight='bold'))
        buttonExit.grid(column = 0, row = 0, sticky = "wesn")

        self.ShowStock()

        self.window.mainloop()

    # It show you which car you have in your stock. It is display by default.
    def ShowStock(self):
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        scrollbar = Scrollbar(self.frameDisplay)
        scrollbar.pack(side="right", fill="y")
        carList = Car.CarListStock()
        spaceBrand = len(max(carList, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(carList, key=lambda x:len(x.nameType)).nameType) + 4

        titleColumn = "Brand" + " "*spaceBrand + "Type" + " "*spaceType +  "Prix"
        labelTitle = tk.Label(self.frameDisplay, state = "normal", text = titleColumn, anchor="n")
        labelTitle.pack(side="top")

        listboxStock = tk.Listbox(self.frameDisplay, state = "normal")
        listboxStock.pack(expand = True, fill = "both")



        for car in carList:
            listboxStock.insert(END, f"{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar}")
            listboxStock.bind('<<ListboxSelect>>', self.ShowDetails)

        listboxStock.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxStock.yview)

    # When you click a row to show more information about the car you selected.
    def ShowDetails(self, event):
        # for widget in self.frameDetails.winfo_children(): 
        #     widget.destroy()
        car = Car.CarListStock()[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.nameBrand}\nType : {car.nameType}\nMotor : {car.nameMotor}\nPrice : {car.priceCar}€\nPromo : {car.promoCar}%\nIn stock since : {car.dateStockCar}\nNext control : {car.dateTechControlCar}"
        self.labelDetails.configure = self.printDetails


    # It will show you which car you sell.
    def ShowHistory(self):
        self.ShowStock()

    # It will help you to change the reservation's statut for a particular car.
    def MakeReservation(self):
        pass

    # It will help you to sell a particular car.
    def MakeDeal(self):
        pass

    # Tis menu will help you to add a new car in your stock with a form.
    def AddCar(self):
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

# It will launch the application
Application()