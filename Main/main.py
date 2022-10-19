from Class.DB import DBAccess as DB
from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
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
        self.labelColumn = 0
        self.carListStock = Car.CarListStock()
        self.carListHistory = Car.CarListHistory()
        self.brandList = Brand.GetAll()
        self.motorList = Motor.GetAll()
        self.typeList = Type.GetAll()
        self.dealList = Deal.GetAll()
        self.CreateBasicWindow()

    # The main display function for the application.
    def CreateBasicWindow(self):

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

        self.buttonStock = tk.Button(self.frameButtons, text = "Display Stock", command = self.DisplayWindowStock)
        self.buttonStock.grid(column = 0, row = 0, sticky = "wesn")
        self.buttonHistory = tk.Button(self.frameButtons, text = "Display History", command = self.DisplayWindowHistory)
        self.buttonHistory.grid(column = 0, row = 1, sticky = "wesn")
        self.buttonReservation = tk.Button(self.frameButtons, text = "Rent a cor", command = self.DisplayWindowRent)
        self.buttonReservation.grid(column = 0, row = 2, sticky = "wesn")
        self.buttonDeal = tk.Button(self.frameButtons, text = "Make a deal", command = self.DisplayWindowDeal)
        self.buttonDeal.grid(column = 0, row = 3, sticky = "wesn")
        self.buttonAddCar = tk.Button(self.frameButtons, text = "Add a car in stock", command = self.DisplayWindowAddCar)
        self.buttonAddCar.grid(column = 0, row = 4, sticky = "wesn")


        frameTitle = tk.Frame(self.window, highlightthickness = 2, highlightbackground = "black")
        frameTitle.grid(column = 1, row = 0, sticky = "wesn")
        frameTitle.rowconfigure(0, weight = 1)
        frameTitle.columnconfigure(0, weight = 1)
        labelTitle = tk.Label(frameTitle, text = self.title)
        labelTitle.grid(column = 0, row = 0, sticky = "wesn")

        frameSort = tk.Frame(self.window, highlightthickness = 1, highlightbackground = "black")
        frameSort.grid(column = 1, row = 1, sticky = "wesn")

        self.frameDisplay = tk.Frame(self.window)
        self.frameDisplay.grid(column = 1, row = 2, rowspan=6, sticky="wesn")
        self.frameDisplay.grid_propagate(False)


        self.frameDetails = tk.Frame(self.window, highlightthickness=2, highlightbackground = "black")
        self.frameDetails.grid(column = 2, row = 1, rowspan = 7, sticky ="wesn")
        self.frameDetails.grid_propagate(False)        
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight = 1)
        self.frameDetails.columnconfigure(0, weight = 1)
        labelTitleDetails = tk.Label(self.frameDetails, text = "DETAILS", anchor = "s", font =  self.police + " underline")
        labelTitleDetails.grid(column = 0, row = 0, sticky = 'wesn')        
        self.labelDetails = tk.Label(self.frameDetails, text = self.printDetails, justify="left", anchor= 'nw')
        self.labelDetails.grid(column = 0, row = 1, sticky = "wesn")


        frameExit = tk.Frame(self.window)
        frameExit.grid(column = 2, row = 0, sticky = "wesn")
        frameExit.rowconfigure(0, weight = 1)
        frameExit.columnconfigure(0, weight = 1)
        buttonExit = tk.Button(frameExit, text = "Exit", command = self.window.destroy, font=font.Font(family='Helvetica', size=15, weight='bold'))
        buttonExit.grid(column = 0, row = 0, sticky = "wesn")

        self.DisplayWindowStock()

        self.window.mainloop()

    # It shows you which car you have in your stock. It is displayed by default.
    def DisplayWindowStock(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonStock["state"] = "disabled"
        
        # self.buttonStock['state'] = 'disabled'
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        for i in range(6):
            self.frameDisplay.rowconfigure(i, weight = i + 1)
        self.frameDisplay.columnconfigure(0, weight = 1)

        spaceBrand = len(max(self.carListStock, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListStock, key=lambda x:len(x.nameType)).nameType) + 4
        spaceIdCar = len("Id") + 4

        titleColumn = "Id" + " " * 4  + "Brand" + " "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Price"
        labelColumn = tk.Label(self.frameDisplay, text = titleColumn, anchor = "w")
        labelColumn.grid(column = 0, row = 0, sticky = "wen")
        
        frameListBoxScroll = tk.Frame(self.frameDisplay)
        frameListBoxScroll.grid(column = 0, row = 1, rowspan = 5, sticky = "wesn")

        scrollbar = Scrollbar(frameListBoxScroll)
        scrollbar.pack(side="right", fill="y")

        listboxStock = tk.Listbox(frameListBoxScroll)
        listboxStock.pack(expand = True, fill = "both")

        for car in self.carListStock:
            listboxStock.insert(END, f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar}")
            listboxStock.bind('<<ListboxSelect>>', self.DisplayDetailsStock)
            

        listboxStock.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxStock.yview)

    # When you click a row to show more information about the car you selected.
    def DisplayDetailsStock(self, event):        
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight = 1)
        self.frameDetails.columnconfigure(0, weight = 1)

        car = self.carListStock[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.nameBrand}\nType : {car.nameType}\nMotor : {car.nameMotor}\nPrice : {car.priceCar}€\nPromo : {car.promoCar}%\nIn stock since : {car.dateStockCar}\nNext control : {car.dateTechControlCar}"
        self.labelDetails.configure(text = self.printDetails)

    # It will show you which car you sell.
    def DisplayWindowHistory(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonHistory["state"] = "disabled"

        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()

        for i in range(6):
            self.frameDisplay.rowconfigure(i, weight = i + 1)
        self.frameDisplay.columnconfigure(0, weight = 1)

        spaceBrand = len(max(self.carListHistory, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListHistory, key=lambda x:len(x.nameType)).nameType) + 4
        spacePrice = len(max(self.carListHistory, key=lambda x:len(x.priceCar)).priceCar) + 4
        spaceIdCar = len("Id") + 4

        titleColumn = "Id" + " "*4 + "Brand" +" "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Price" + " "*(spacePrice-len("Price")) + "Customer"
        labelTitle = tk.Label(self.frameDisplay, text = titleColumn, anchor = "w")
        labelTitle.grid(column = 0, row = 0, sticky = "wen")

        frameListBoxScroll = tk.Frame(self.frameDisplay)
        frameListBoxScroll.grid(column = 0, row = 1, rowspan = 5, sticky = "wesn")

        scrollbar = Scrollbar(frameListBoxScroll)
        scrollbar.pack(side="right", fill="y")

        listboxHistory = tk.Listbox(frameListBoxScroll)
        listboxHistory.pack(expand = True, fill = "both")

        for car in self.carListHistory:
            listboxHistory.insert(END, f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar:{spacePrice}}{car.nameCusto}")
            listboxHistory.bind('<<ListboxSelect>>', self.DisplayDetailsHistory)            

        listboxHistory.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxHistory.yview)

    # When you click a row to show more information about the car you selected.
    def DisplayDetailsHistory(self, event):
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight = 1)
        self.frameDetails.columnconfigure(0, weight = 1)
        
        car = self.carListHistory[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.nameBrand}\nType : {car.nameType}\nMotor : {car.nameMotor}\nPrice : {car.priceCar}€\nPromo : {car.promoCar}%\nIn stock since : {car.dateStockCar}\nNext control {car.dateTechControlCar}\nThe customer is : {car.nameCusto}"
        self.labelDetails.configure(text = self.printDetails)

    # It will help you to change the reservation's statut for a particular car.
    def DisplayWindowRent(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonReservation["state"] = "disabled"
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()
        
    # It will help you to sell a particular car.
    def DisplayWindowDeal(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = "normal"
        self.buttonDeal["state"] = "disabled"
        for widget in self.frameDisplay.winfo_children(): 
            widget.destroy()
        
        
        for i in range(2):
            self.frameDisplay.columnconfigure(i, weight = 1)
        
        for i in range(2):
            self.frameDisplay.rowconfigure(i, weight = 1)

        if Car.CarFreePlacesStock() <= 40:
            vars = {
            "idCar" : tk.StringVar(),
            "idCusto" : tk.StringVar()
            }

            labelCarId = tk.Label(self.frameDisplay, text = "Car id : ")
            labelCarId.grid(column = 0, row = 0, sticky = "wesn")
            dropdownCarId = tk.OptionMenu(self.frameDisplay, vars['idCar'], *map(lambda idCar: idCar.idCar, self.dealList))
            dropdownCarId.grid(column = 1, row = 0, sticky = "wesn")

            labelIdCusto = tk.Label(self.frameDisplay, text = "Customer id : ")
            labelIdCusto.grid(column = 0, row = 1, sticky = "wesn")
            dropdownIdCusto = tk.OptionMenu(self.frameDisplay, vars['idCusto'], *map(lambda idCusto: idCusto.idCusto, self.dealList))
            dropdownIdCusto.grid(column = 1, row = 1, sticky = "wesn")

            buttonMakeDeal = tk.Button(self.frameDisplay, text = "Make the deal", command = lambda : Car.InsertDB(vars))
            buttonMakeDeal.grid(column = 0, row = 6, sticky = "wesn")

        else: 
            labelNoFreePlaces = tk.Label(self.frameDisplay, text = "No free places")
            labelNoFreePlaces.grid(column = 0, row = 0)

    # This menu will help you to add a new car in your stock with a form.
    def DisplayWindowAddCar(self):
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
            # vars = {"nameBrand" : tk.StringVar(), "nameType" : tk.StringVar(), "nameMotor" : tk.StringVar(), "priceCar" : tk.StringVar(),
            # "promoCar" : tk.StringVar(),"dateTechControlCar" : tk.StringVar()}

            car = Car()
            car.nameBrand = tk.StringVar()
            car.nameType = tk.StringVar()
            car.nameMotor = tk.StringVar()
            car.priceCar = tk.StringVar()
            car.promoCar = tk.StringVar()
            car.dateTechControlCar = tk.StringVar()

            labelBrand = tk.Label(self.frameDisplay, text = "Brand : ")
            labelBrand.grid(column = 0, row = 0, sticky = "wesn")
            dropdownBrand = tk.OptionMenu(self.frameDisplay, car.nameBrand, *map(lambda brand: brand.nameBrand, self.brandList))
            dropdownBrand.grid(column = 1, row = 0, sticky = "wesn")

            labelType = tk.Label(self.frameDisplay, text = "Type : ")
            labelType.grid(column = 0, row = 1, sticky = "wesn")
            dropdownType = tk.OptionMenu(self.frameDisplay, car.nameType, *map(lambda type: type.nameType, self.typeList))
            dropdownType.grid(column = 1, row = 1, sticky = "wesn")

            labelMotor = tk.Label(self.frameDisplay, text = "Motor : ")
            labelMotor.grid(column = 0, row = 2, sticky = "wesn")
            dropdownMotor = tk.OptionMenu(self.frameDisplay, car.nameMotor, *map(lambda motor: motor.nameMotor, self.motorList))
            dropdownMotor.grid(column = 1, row = 2, sticky = "wesn")

            labelNextControl = tk.Label(self.frameDisplay, text = "Next tech control :")
            labelNextControl.grid(column = 0, row = 3, sticky = "wesn")
            entryNextControl = tkCal(self.frameDisplay, textvariable = car.dateTechControlCar, locale='fr_BE', date_pattern = "dd/mm/yyyy")
            entryNextControl.grid(column = 1, row = 3, sticky = "wesn")

            labelPrice = tk.Label(self.frameDisplay, text = "Price : ")
            labelPrice.grid(column = 0, row = 4, sticky = "wesn")
            entryPrice = tk.Entry(self.frameDisplay, textvariable = car.priceCar)
            entryPrice.grid(column = 1, row = 4, sticky = "wesn")

            labelPromo = tk.Label(self.frameDisplay, text = "Promo : ")
            labelPromo.grid(column = 0, row = 5, sticky = "wesn")
            entryPromo = tk.Entry(self.frameDisplay, textvariable = car.promoCar)
            entryPromo.grid(column = 1, row = 5, sticky = "wesn")

            buttonAddCar = tk.Button(self.frameDisplay, text = "Add a car in stock", command = lambda :self.VerifyCarInsert(car))
            buttonAddCar.grid(column = 0, row = 6, sticky = "wesn")

        else: 
            labelNoFreePlaces = tk.Label(self.frameDisplay, text = "No free places")
            labelNoFreePlaces.grid(column = 0, row = 0)
    
    def VerifyCarInsert(self, carRawData): 
        car = Car()
        counter = 0
        #Get the id for the motor
        while counter < len(self.motorList) or car.idMotor == None:
            if self.motorList[counter].nameMotor == carRawData.nameMotor.get():
                car.idMotor = self.motorList[counter].idMotor
            counter += 1
        
        counter = 0
        while counter < len(self.brandList) or car.idBrand == None:
            if self.brandList[counter].nameBrand == carRawData.nameBrand.get():
                car.idBrand = self.brandList[counter].idBrand
            counter += 1
        
        counter = 0
        while counter < len(self.typeList) or car.idType == None:
            if self.typeList[counter].nameType == carRawData.nameType.get():
                car.idType = self.typeList[counter].idType
            counter += 1
        
        car.dateTechControlCar = carRawData.dateTechControlCar.get()
        car.priceCar = float(carRawData.priceCar.get())
        car.promoCar = carRawData.promoCar.get()
        car.InsertDB()        
        self.carListStock = Car.CarListStock()
        
# It will launch the application
Application()


