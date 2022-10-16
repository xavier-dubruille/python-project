from typing import Literal
from Class.DB import DBAccess as DB
from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkcalendar import DateEntry as tkCal
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

        self.frameButtons = tk.Frame(self.window)
        self.frameButtons.grid(column = 0, row = 1, rowspan = 5, sticky = "wesn")
        for i in range(5):
            self.frameButtons.rowconfigure(i, weight = 1)
        self.frameButtons.columnconfigure(0, weight = 1)

        self.buttonStock = tk.Button(self.frameButtons, text = "Display Stock", command = self.ShowStock, relief = "raised")
        self.buttonStock.grid(column = 0, row = 0, sticky = "wesn")
        self.buttonHistory = tk.Button(self.frameButtons, text = "Display History", command = self.ShowHistory, relief = "raised")
        self.buttonHistory.grid(column = 0, row = 1, sticky = "wesn")
        self.buttonReservation = tk.Button(self.frameButtons, text = "Make a reservation", command = self.MakeReservation, relief = "raised")
        self.buttonReservation.grid(column = 0, row = 2, sticky = "wesn")
        self.buttonDeal = tk.Button(self.frameButtons, text = "Make a deal", command = self.MakeDeal, relief = "raised")
        self.buttonDeal.grid(column = 0, row = 3, sticky = "wesn")
        self.buttonAddCar = tk.Button(self.frameButtons, text = "Add a car", command = self.AddCar)
        self.buttonAddCar.grid(column = 0, row = 4, sticky = "wesn")


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
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight = 1)
        self.frameDetails.columnconfigure(0, weight = 1)
        
        labelTitleDetails = tk.Label(self.frameDetails, text = "DETAILS", anchor = "s", font =  self.police + " underline")
        labelTitleDetails.grid(column = 0, row = 0, sticky = 'wesn')
        
        self.labelDetails = tk.Label(self.frameDetails, width = self.frameDetails.winfo_width(), text = self.printDetails, justify="left", anchor= 'nw')
        self.labelDetails.grid(column = 0, row = 1, sticky = "wesn")


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
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonStock["state"] = "disabled"
        
        # self.buttonStock['state'] = 'disabled'
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        scrollbar = Scrollbar(self.frameDisplay)
        scrollbar.pack(side="right", fill="y")

        carListStock = Car.CarListStock()
        spaceBrand = len(max(carListStock, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(carListStock, key=lambda x:len(x.nameType)).nameType) + 4

        titleColumn = "Brand" + " "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Prix"
        labelTitle = tk.Label(self.frameDisplay, state = "normal", text = titleColumn)
        labelTitle.pack(side="top", anchor="nw")

        listboxStock = tk.Listbox(self.frameDisplay, state = "normal")
        listboxStock.pack(expand = True, fill = "both")

        for car in carListStock:
            listboxStock.insert(END, f"{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar}")
            listboxStock.bind('<<ListboxSelect>>', self.ShowDetailsStock)

        listboxStock.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxStock.yview)

    # When you click a row to show more information about the car you selected.
    def ShowDetailsStock(self, event):
        # for widget in self.frameDetails.winfo_children(): 
        #     widget.destroy()
        car = Car.CarListStock()[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.nameBrand}\nType : {car.nameType}\nMotor : {car.nameMotor}\nPrice : {car.priceCar}€\nPromo : {car.promoCar}%\nIn stock since : {car.dateStockCar}\nNext control : {car.dateTechControlCar}"
        self.labelDetails.configure(text = self.printDetails)


    # It will show you which car you sell.
    def ShowHistory(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonHistory["state"] = "disabled"
        
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        scrollbar = Scrollbar(self.frameDisplay)
        scrollbar.pack(side="right", fill="y")

        carListHistory = Car.CarListHistory()
        spaceBrand = len(max(carListHistory, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(carListHistory, key=lambda x:len(x.nameType)).nameType) + 4
        spacePrice = len(max(carListHistory, key=lambda x:len(x.priceCar)).priceCar) + 4

        titleColumn = "Brand" + " "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Prix" + " "*(spacePrice-len("Prix")) + "Customer"
        labelTitle = tk.Label(self.frameDisplay, state = "normal", text = titleColumn)
        labelTitle.pack(side="top", anchor="nw")

        listboxHistory = tk.Listbox(self.frameDisplay, state = "normal")
        listboxHistory.pack(expand = True, fill = "both")

        for car in carListHistory:
            listboxHistory.insert(END, f"{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar:{spacePrice}}{car.nameCusto}")
            listboxHistory.bind('<<ListboxSelect>>', self.ShowDetailsHistory)

        listboxHistory.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxHistory.yview)


    # When you click a row to show more information about the car you selected.
    def ShowDetailsHistory(self, event):
        # for widget in self.frameDetails.winfo_children(): 
        #     widget.destroy()
        car = Car.CarListHistory()[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.nameBrand}\nType : {car.nameType}\nMotor : {car.nameMotor}\nPrice : {car.priceCar}€\nPromo : {car.promoCar}%\nIn stock since : {car.dateStockCar}\nNext control {car.dateTechControlCar}\nThe customer is : {car.nameCusto}"
        self.labelDetails.configure(text = self.printDetails)


    # It will help you to change the reservation's statut for a particular car.
    def MakeReservation(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonReservation["state"] = "disabled"

    # It will help you to sell a particular car.
    def MakeDeal(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonDeal["state"] = "disabled"

    # Tis menu will help you to add a new car in your stock with a form.
    def AddCar(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonAddCar["state"] = "disabled"

        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        for i in range(2):
            self.frameDisplay.columnconfigure(i, weight = 1)
        
        for i in range(7):
            self.frameDisplay.rowconfigure(i, weight = 1)
        
        if Car.CarFreePlacesStock() <= 40:
            vars = {
            "nameBrand" : tk.StringVar(),
            "nameType" : tk.StringVar(),
            "nameMotor" : tk.StringVar(),
            "priceCar" : tk.StringVar(),
            "promoCar" : tk.StringVar(),
            "dateTechControlCar" : tk.StringVar()
            }

            labelBrand = tk.Label(self.frameDisplay, text = "Brand : ")
            labelBrand.grid(column = 0, row = 0, sticky = "wesn")
            dropdownBrand = tk.OptionMenu(self.frameDisplay, vars['nameBrand'], *map(lambda brand: brand.nameBrand, Brand.GetAll()))
            dropdownBrand.grid(column = 1, row = 0, sticky = "wesn")

            labelType = tk.Label(self.frameDisplay, text = "Type : ")
            labelType.grid(column = 0, row = 1, sticky = "wesn")
            dropdownType = tk.OptionMenu(self.frameDisplay, vars['nameType'], *map(lambda type: type.nameType, Type.GetAll()))
            dropdownType.grid(column = 1, row = 1, sticky = "wesn")

            labelMotor = tk.Label(self.frameDisplay, text = "Motor : ")
            labelMotor.grid(column = 0, row = 2, sticky = "wesn")
            dropdownMotor = tk.OptionMenu(self.frameDisplay, vars['nameMotor'], *map(lambda motor: motor.nameMotor, Motor.GetAll()))
            dropdownMotor.grid(column = 1, row = 2, sticky = "wesn")

            labelNextControl = tk.Label(self.frameDisplay, text = "Next tech control :")
            labelNextControl.grid(column = 0, row = 3, sticky = "wesn")
            entryNextControl = tkCal(self.frameDisplay, textvariable = vars['dateTechControlCar'], selectmode = 'day')
            entryNextControl.grid(column = 1, row = 3, sticky = "wesn")

            labelPrice = tk.Label(self.frameDisplay, text = "Price : ")
            labelPrice.grid(column = 0, row = 4, sticky = "wesn")
            entryPrice = tk.Entry(self.frameDisplay, textvariable = vars['priceCar'])
            entryPrice.grid(column = 1, row = 4, sticky = "wesn")

            labelPromo = tk.Label(self.frameDisplay, text = "Promo : ")
            labelPromo.grid(column = 0, row = 5, sticky = "wesn")
            entryPromo = tk.Entry(self.frameDisplay, textvariable = vars['promoCar'])
            entryPromo.grid(column = 1, row = 5, sticky = "wesn")

            buttonAddCar = tk.Button(self.frameDisplay, text = "Add Car", command = lambda x: Car.InsertDB(vars))
            buttonAddCar.grid(column = 0, row = 6, sticky = "wesn")

        else: 
            labelNoFreePlaces = tk.Label(self.frameDisplay, text = "No free places")
            labelNoFreePlaces.grid(column = 0, row = 0)
    
      

# It will launch the application
Application()