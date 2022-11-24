import tkinter.font as font
from tkinter import *

from tkcalendar import DateEntry as tkCal

from Main.Class.Brand import Brand
from Main.Class.Customer import Customer
from Main.Class.Deal import Deal
from Main.Class.Motor import Motor
from Main.Class.Type import Type
from Main.Class.Car import Car


def CheckNumberInput(string: str, minimum: int = None, maximum: int = None) -> bool:
    """
    This function check if the string is convertible into integer
    If minimum and/or maximum are given, check also if it's between them
    :param string: A string that will be checked for a number
    :type string: str
    :param minimum: An integer number
    :type string: int
    :param maximum: An integer number
    :type string: int
    :returns: True if the string is convertible to digit and respect the minimum and the maximum
    :rtype: bool
    """
    if not string.isdigit():
        return False
    if maximum is not None and minimum is not None:
        if maximum >= int(string) >= minimum:
            return True
        return False
    elif maximum is not None:
        if maximum >= int(string):
            return True
        return False
    elif minimum is not None:
        if int(string) >= minimum:
            return True
        return False
    return True


class Application:
    def __init__(self) -> None:
        self.buttonAddCar = None
        self.labelDetails = None
        self.frameDetails = None
        self.frameDisplay = None
        self.buttonDeal = None
        self.buttonReservation = None
        self.buttonHistory = None
        self.buttonStock = None
        self.buttonAddCustomer = None
        self.window = None
        self.frameButtons = None
        self.printDetails = None
        self.labelColumn = None
        self.frameSort = None
        self.spaceDisplay = 4
        self.rentList = []
        self.soldList = []
        self.carListFree = []
        self.carListStock = []
        self.dealList = []
        self.police = "courier 15"
        self.title = "Bamboo Concess"
        self.SetOrResetCarLists()
        self.brandList = Brand.GetAll()
        self.motorList = Motor.GetAll()
        self.typeList = Type.GetAll()
        self.customerList = Customer.GetAll()
        self.CreateBasicWindow()

    # The main display function for the application.
    def CreateBasicWindow(self) -> None:

        self.window = Tk()
        self.window.title(self.title)
        self.window.attributes('-fullscreen', True)
        self.window.option_add("*Font", self.police)
        self.window.config(bg="white")

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=1)

        for i in range(6):
            self.window.rowconfigure(i, weight=1)
        self.window.rowconfigure(7, weight=2)

        self.frameButtons = Frame(self.window)
        self.frameButtons.grid(column=0, row=1, rowspan=5, sticky=NSEW)
        for i in range(6):
            self.frameButtons.rowconfigure(i, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        self.buttonStock = Button(self.frameButtons, text="Display Stock", command=self.DisplayWindowStock)
        self.buttonStock.grid(column=0, row=0, sticky=NSEW)
        self.buttonHistory = Button(self.frameButtons, text="Display History", command=self.DisplayWindowHistory)
        self.buttonHistory.grid(column=0, row=1, sticky=NSEW)
        self.buttonReservation = Button(self.frameButtons, text="Rent a car", command=self.DisplayWindowRent)
        self.buttonReservation.grid(column=0, row=2, sticky=NSEW)
        self.buttonDeal = Button(self.frameButtons, text="Make a deal", command=self.DisplayWindowSelling)
        self.buttonDeal.grid(column=0, row=3, sticky=NSEW)
        self.buttonAddCar = Button(self.frameButtons, text="Add a car in stock", command=self.DisplayWindowAddCar)
        self.buttonAddCar.grid(column=0, row=4, sticky=NSEW)
        self.buttonAddCustomer = Button(self.frameButtons, text="Add a customer", command=self.DisplayWindowAddCustomer)
        self.buttonAddCustomer.grid(column=0, row=5, sticky=NSEW)

        frameTitle = Frame(self.window, highlightthickness=2, highlightbackground="black")
        frameTitle.grid(column=1, row=0, sticky=NSEW)
        frameTitle.rowconfigure(0, weight=1)
        frameTitle.columnconfigure(0, weight=1)
        labelTitle = Label(frameTitle, text=self.title)
        labelTitle.grid(column=0, row=0, sticky=NSEW)

        self.frameSort = Frame(self.window, highlightthickness=1, highlightbackground="black")
        self.frameSort.grid(column=1, row=1, sticky=NSEW)
        self.frameSort.pack_propagate(False)
        self.frameSort.grid_propagate(False)

        self.frameDisplay = Frame(self.window)
        self.frameDisplay.grid(column=1, row=2, rowspan=6, sticky=NSEW)
        for i in range(105):
            self.frameDisplay.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.frameDisplay.grid_columnconfigure(i, weight=1)
        self.frameDisplay.pack_propagate(False)
        self.frameDisplay.grid_propagate(False)

        self.frameDetails = Frame(self.window, highlightthickness=2, highlightbackground="black")
        self.frameDetails.grid(column=2, row=1, rowspan=7, sticky=NSEW)
        self.frameDetails.grid_propagate(False)
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight=1)
        self.frameDetails.columnconfigure(0, weight=1)
        labelTitleDetails = Label(self.frameDetails, text="DETAILS", anchor="s", font=self.police + " underline")
        labelTitleDetails.grid(column=0, row=0, sticky='wesn')
        self.labelDetails = Label(self.frameDetails, text=self.printDetails, justify="left", anchor='nw')
        self.labelDetails.grid(column=0, row=1, sticky=NSEW)

        frameExit = Frame(self.window)
        frameExit.grid(column=2, row=0, sticky=NSEW)
        frameExit.rowconfigure(0, weight=1)
        frameExit.columnconfigure(0, weight=1)
        buttonExit = Button(frameExit, text="Exit", command=self.window.destroy,
                            font=font.Font(family='Helvetica', size=15, weight='bold'))
        buttonExit.grid(column=0, row=0, sticky=NSEW)

        self.DisplayWindowStock()

        self.window.mainloop()

    # It shows you which car you have in your stock. It is displayed by default.
    def DisplayWindowStock(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonStock["state"] = DISABLED

        self.ResetDisplayAndSortFrames()

        strList = ["Id", "Brand", "Type", "Price (€)", "Rented"]
        spaceDict = {
            strList[0]: len(str(max(self.carListStock, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay,
            strList[1]: len(max(self.carListStock, key=lambda x: len(x.brand.name)).brand.name) + self.spaceDisplay,
            strList[2]: len(max(self.carListStock, key=lambda x: len(x.type.name)).type.name) + self.spaceDisplay,
            strList[3]: len(max(self.carListStock, key=lambda x: len(x.price)).price) + self.spaceDisplay
        }

        titleColumn = f"{strList[0]}" + " " * (spaceDict[strList[0]] - len(f"{strList[0]}")) + \
                      f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) + \
                      f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) + \
                      f"{strList[3]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) + \
                      f"{strList[4]}"

        labelTitleColumn = Label(self.frameDisplay, text=titleColumn)
        labelTitleColumn.pack(anchor=NW)

        frameListBoxScroll = Frame(self.frameDisplay)
        frameListBoxScroll.pack(expand=True, fill=BOTH, anchor=W)

        scrollbar = Scrollbar(frameListBoxScroll)
        scrollbar.pack(side=RIGHT, fill=Y)

        listboxStock = Listbox(frameListBoxScroll)
        listboxStock.pack(expand=True, fill=BOTH, anchor=W)

        for car in self.carListStock:
            rented = ""
            for deal in self.rentList:
                if deal.idCar == car.id:
                    rented = "Rented"
                    break
            listboxStock.insert(END,
                                f"{str(car.id):{spaceDict[strList[0]]}}"
                                f"{car.brand.name:{spaceDict[strList[1]]}}"
                                f"{car.type.name:{spaceDict[strList[2]]}}"
                                f"{car.price:{spaceDict[strList[3]]}}"
                                f"{rented}")
            listboxStock.bind('<<ListboxSelect>>', self.DisplayDetailsStock)

        listboxStock.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listboxStock.yview)

    # When you click a row to show more information about the car you selected.
    def DisplayDetailsStock(self, event: Event) -> None:
        car = self.carListStock[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {car.brand.name}\nType : {car.type.name}\nMotor : {car.motor.name}\n" \
                            f"Price : {car.price}€\n" \
                            f"Promo : {car.promo}%\nIn stock since : {car.dateStock}\n" \
                            f"Next control : {car.dateTechControl}"
        self.labelDetails.configure(text=self.printDetails)

    # It will show you which car you sell.
    def DisplayWindowHistory(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonHistory["state"] = DISABLED

        self.ResetDisplayAndSortFrames()

        if not self.dealList:
            listboxHistory = Listbox(self.frameDisplay)
            listboxHistory.pack(expand=True, fill=BOTH)
            listboxHistory.insert(END, "There is no cars in this category")

        else:
            strList = ["Id", "Brand", "Type", "Price (€)", "Customer"]
            spaceDict = {
                strList[0]: len(str(
                    max(self.dealList, key=lambda x: len(str(x.car.id))).car.id)) + self.spaceDisplay,
                strList[1]: len(
                    max(self.dealList, key=lambda x: len(x.car.brand.name)).car.brand.name) + self.spaceDisplay,
                strList[2]: len(
                    max(self.dealList, key=lambda x: len(x.car.type.name)).car.type.name) + self.spaceDisplay,
                strList[3]: len(
                    max(self.dealList, key=lambda x: len(x.car.price)).car.price) + self.spaceDisplay
            }

            titleColumn = f"{strList[0]}" + " " * (spaceDict[strList[0]] - len(f"{strList[0]}")) + \
                          f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) + \
                          f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) + \
                          f"{strList[3]}" + " " * (spaceDict[strList[3]] - len(f"{strList[3]}")) + \
                          f"{strList[4]}"

            labelTitle = Label(self.frameDisplay, text=titleColumn, anchor="w")
            labelTitle.pack(anchor=W)

            frameListBoxScroll = Frame(self.frameDisplay)
            frameListBoxScroll.pack(expand=True, fill=BOTH)

            listboxHistory = Listbox(frameListBoxScroll)
            listboxHistory.pack(expand=True, fill=BOTH)

            scrollbar = Scrollbar(frameListBoxScroll)
            scrollbar.pack(side=RIGHT, fill=Y)

            for deal in self.dealList:
                listboxHistory.insert(END,
                                      f"{str(deal.car.id):{spaceDict[strList[0]]}}"
                                      f"{deal.car.brand.name:{spaceDict[strList[1]]}}"
                                      f"{deal.car.type.name:{spaceDict[strList[2]]}}"
                                      f"{deal.car.price:{spaceDict[strList[3]]}}"
                                      f"{deal.customer.firstName[0]}.{deal.customer.lastName}")
                listboxHistory.bind('<<ListboxSelect>>', self.DisplayDetailsHistory)

            listboxHistory.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=listboxHistory.yview)

    # When you click a row to show more information about the car you selected.
    def DisplayDetailsHistory(self, event: Event) -> None:
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight=1)
        self.frameDetails.columnconfigure(0, weight=1)

        deal = self.dealList[event.widget.curselection()[0]]
        self.printDetails = f"Brand : {deal.car.brand.name}\n" \
                            f"Type : {deal.car.type.name}\n" \
                            f"Motor : {deal.car.motor.name}\n" \
                            f"Price : {deal.car.price}€\n" \
                            f"Promo : {deal.car.promo}%\n" \
                            f"In stock since : {deal.car.dateStock}\n" \
                            f"Next control {deal.car.dateTechControl}\n" \
                            f"The customer is : {deal.customer.firstName} {deal.customer.lastName}"
        self.labelDetails.configure(text=self.printDetails)

    # It will help you to change the reservation's status for a particular car.
    """5"""

    def DisplayWindowRent(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonReservation["state"] = DISABLED

        self.ResetDisplayAndSortFrames()

        if not self.carListFree:
            labelNoFreePlaces = Label(self.frameDisplay, text="No car left for renting.")
            labelNoFreePlaces.pack()

        else:
            rawDeal = Deal()
            rawDeal.idCar = StringVar()
            rawDeal.idCustomer = StringVar()
            rawDeal.dateStartRent = StringVar()
            rawDeal.durationDaysRent = StringVar()
            rawDeal.isRent = 1

            labelCarId = Label(self.frameDisplay, text="Car id : ")
            labelCarId.grid(column=0, row=0, rowspan=21, sticky=NSEW)
            dropdownCarId = OptionMenu(self.frameDisplay, rawDeal.idCar,
                                       *map(lambda x: f"{x.id} price : {x.price} promo : {x.promo}", self.carListFree))
            dropdownCarId.grid(column=1, row=0, rowspan=21, sticky=NSEW)

            labelIdCustomer = Label(self.frameDisplay, text="Customer id : ")
            labelIdCustomer.grid(column=0, row=21, sticky=NSEW)
            dropdownIdCustomer = OptionMenu(self.frameDisplay, rawDeal.idCustomer,
                                            *map(lambda x: f"{x.id} {x.firstName[0]}.{x.lastName}", self.customerList))
            dropdownIdCustomer.grid(column=1, row=21, rowspan=21, sticky=NSEW)

            labelDateStartRent = Label(self.frameDisplay, text="Date of the rent : ")
            labelDateStartRent.grid(column=0, row=42, rowspan=21, sticky=NSEW)
            entryDateStartRent = tkCal(self.frameDisplay, textvariable=rawDeal.dateStartRent, locale='fr_BE',
                                       date_pattern="dd/mm/yyyy")
            entryDateStartRent.grid(column=1, row=42, rowspan=21, sticky=NSEW)

            labelDurationDaysRent = Label(self.frameDisplay, text="Duration days of the rent : ")
            labelDurationDaysRent.grid(column=0, row=63, rowspan=21, sticky=NSEW)
            entryDurationDaysRent = Entry(self.frameDisplay, textvariable=rawDeal.durationDaysRent)
            entryDurationDaysRent.grid(column=1, row=63, rowspan=21, sticky=NSEW)

            buttonRentACar = Button(self.frameDisplay, text="Make the rent", command=lambda: self.VerifyDeal(rawDeal))
            buttonRentACar.grid(column=1, row=84, rowspan=21, sticky=NSEW)

    # It will help you to sell a particular car.
    """3"""

    def DisplayWindowSelling(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonDeal["state"] = DISABLED

        self.ResetDisplayAndSortFrames()
        if self.carListFree:

            rawDeal = Deal()
            rawDeal.idCar = StringVar()
            rawDeal.idCustomer = StringVar()
            rawDeal.isRent = 0

            labelCarId = Label(self.frameDisplay, text="Car id : ")
            labelCarId.grid(column=0, row=0, rowspan=35, sticky=NSEW)
            dropdownCarId = OptionMenu(self.frameDisplay, rawDeal.idCar,
                                       *map(lambda x: f"{x.id} price : {x.price} promo : {x.promo}", self.carListFree))
            dropdownCarId.grid(column=1, row=0, rowspan=35, sticky=NSEW)

            labelIdCustomer = Label(self.frameDisplay, text="Customer id : ")
            labelIdCustomer.grid(column=0, row=35, rowspan=35, sticky=NSEW)
            dropdownIdCustomer = OptionMenu(self.frameDisplay, rawDeal.idCustomer,
                                            *map(lambda x: f"{x.id} {x.firstName[0]}.{x.lastName}", self.customerList))
            dropdownIdCustomer.grid(column=1, row=35, rowspan=35, sticky=NSEW)

            buttonMakeDeal = Button(self.frameDisplay, text="Make the deal", command=lambda: self.VerifyDeal(rawDeal))
            buttonMakeDeal.grid(column=1, row=70, rowspan=35, sticky=NSEW)

        else:
            labelNoFreePlaces = Label(self.frameDisplay, text="No car left for selling.")
            labelNoFreePlaces.pack()

    # This menu will help you to add a new car in your stock with a form.
    """7"""

    def DisplayWindowAddCar(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonAddCar["state"] = DISABLED

        self.ResetDisplayAndSortFrames()

        if Car.CarFreePlacesStock() <= 40:
            rawCar = {
                "nameBrand": StringVar(),
                "nameType": StringVar(),
                "nameMotor": StringVar(),
                "price": StringVar(),
                "promo": StringVar(),
                "dateTechControl": StringVar()
            }

            labelBrand = Label(self.frameDisplay, text="Brand : ")
            labelBrand.grid(column=0, row=0, rowspan=15, sticky=NSEW)
            entryBrand = Entry(self.frameDisplay, textvariable=rawCar["nameBrand"])
            entryBrand.grid(column=1, row=0, rowspan=15, sticky=NSEW)

            labelType = Label(self.frameDisplay, text="Type : ")
            labelType.grid(column=0, row=15, rowspan=15, sticky=NSEW)
            entryType = Entry(self.frameDisplay, textvariable=rawCar["nameType"])
            entryType.grid(column=1, row=15, rowspan=15, sticky=NSEW)

            labelMotor = Label(self.frameDisplay, text="Motor : ")
            labelMotor.grid(column=0, row=30, rowspan=15, sticky=NSEW)
            entryType = Entry(self.frameDisplay, textvariable=rawCar["nameMotor"])
            entryType.grid(column=1, row=30, rowspan=15, sticky=NSEW)

            labelNextControl = Label(self.frameDisplay, text="Next tech control :")
            labelNextControl.grid(column=0, row=45, rowspan=15, sticky=NSEW)
            entryNextControl = tkCal(self.frameDisplay, textvariable=rawCar["dateTechControl"], locale='fr_BE',
                                     date_pattern="dd/mm/yyyy")
            entryNextControl.grid(column=1, row=45, rowspan=15, sticky=NSEW)

            labelPrice = Label(self.frameDisplay, text="Price : ")
            labelPrice.grid(column=0, row=60, rowspan=15, sticky=NSEW)
            entryPrice = Entry(self.frameDisplay, textvariable=rawCar["price"])
            entryPrice.grid(column=1, row=60, rowspan=15, sticky=NSEW)

            labelPromo = Label(self.frameDisplay, text="Promo : ")
            labelPromo.grid(column=0, row=75, rowspan=15, sticky=NSEW)
            entryPromo = Entry(self.frameDisplay, textvariable=rawCar["promo"])
            entryPromo.grid(column=1, row=75, rowspan=15, sticky=NSEW)

            buttonAddCar = Button(self.frameDisplay, text="Add a car in stock",
                                  command=lambda: self.VerifyCarInsert(rawCar))
            buttonAddCar.grid(column=1, row=90, rowspan=15, sticky=NSEW)
        else:
            labelNoFreePlaces = Label(self.frameDisplay, text="No free places")
            labelNoFreePlaces.pack()

    def DisplayWindowAddCustomer(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonAddCustomer["state"] = DISABLED

        self.ResetDisplayAndSortFrames()

        rawCustomer = {
            "firstName": StringVar(),
            "lastName": StringVar(),
            "phone": StringVar(),
            "mail": StringVar(),
            "address": StringVar()
        }
        labelFirstName = Label(self.frameDisplay, text="Firstname : ")
        labelFirstName.grid(column=0, row=0, rowspan=21, sticky=NSEW)
        entryFirstName = Entry(self.frameDisplay, textvariable=rawCustomer["firstName"])
        entryFirstName.grid(column=1, row=0, rowspan=21, sticky=NSEW)

        labelLastName = Label(self.frameDisplay, text="Lastname : ")
        labelLastName.grid(column=0, row=21, rowspan=21, sticky=NSEW)
        entryLastName = Entry(self.frameDisplay, textvariable=rawCustomer["lastName"])
        entryLastName.grid(column=1, row=21, rowspan=21, sticky=NSEW)

        labelPhone = Label(self.frameDisplay, text="Phone : ")
        labelPhone.grid(column=0, row=42, rowspan=21, sticky=NSEW)
        entryPhone = Entry(self.frameDisplay, textvariable=rawCustomer["phone"])
        entryPhone.grid(column=1, row=42, rowspan=21, sticky=NSEW)

        labelMail = Label(self.frameDisplay, text="Email Address :")
        labelMail.grid(column=0, row=63, rowspan=21, sticky=NSEW)
        entryMail = Entry(self.frameDisplay, textvariable=rawCustomer["mail"])
        entryMail.grid(column=1, row=63, rowspan=21, sticky=NSEW)

        labelAddress = Label(self.frameDisplay, text="Address : ")
        labelAddress.grid(column=0, row=84, rowspan=21, sticky=NSEW)
        entryAddress = Entry(self.frameDisplay, textvariable=rawCustomer["address"])
        entryAddress.grid(column=1, row=84, rowspan=21, sticky=NSEW)

        buttonAddCustomer = Button(self.frameDisplay, text="Add a car in stock",
                                   command=lambda: self.VerifyCustomerInsert(rawCustomer))
        buttonAddCustomer.grid(column=1, row=90, rowspan=15, sticky=NSEW)

    def VerifyCustomerInsert(self, customerStringVar: dict) -> None:
        pass

    def VerifyCarInsert(self, carStringVar: dict) -> None:
        """

        :type carStringVar: object
        :rtype: object
        """
        textInfo: str = ""
        car: Car = Car()
        car.idBrand = Brand.GetId(carStringVar["nameBrand"].get())
        if not car.idBrand:
            textInfo += "- There is no brand name.\n"
        car.idType = Type.GetId(carStringVar["nameType"].get())
        if not car.idType:
            textInfo += "- There is no type name.\n"
        car.idMotor = Motor.GetId(carStringVar["nameMotor"].get())
        if not car.idMotor:
            textInfo += "- There is no motor name.\n"
        car.dateTechControl = carStringVar["dateTechControl"].get()
        if not car.dateTechControl:
            textInfo += "- There is no date for the tech control.\n"
        car.price = carStringVar["price"].get()
        if not car.price or not CheckNumberInput(car.price, 1):
            textInfo += "- It's not a good price.\n"
        car.promo = carStringVar["promo"].get()
        if not car.promo or not CheckNumberInput(car.promo, 0, 100):
            textInfo += "- It's not a good promotion.\n"
        if not textInfo:
            car.InsertDB()
            self.SetOrResetCarLists()
            textInfo = "Car saved"
        for widget in self.frameSort.winfo_children():
            widget.destroy()
        labelError = Label(self.frameSort, text=textInfo)
        labelError.pack()

    def VerifyDeal(self, deal: Deal) -> None:
        textInfo = ""
        newDeal = Deal()
        newDeal.dateStartRent = None
        newDeal.durationDaysRent = None
        newDeal.idCustomer = None
        newDeal.idCar = None
        rawIdCar = deal.idCar.get()
        if rawIdCar:
            newDeal.idCar = rawIdCar.split()[0]
        if not newDeal.idCar:
            textInfo += "- There is no car id chosen.\n"
        rawIdCustomer = deal.idCustomer.get()
        if rawIdCustomer:
            newDeal.idCustomer = rawIdCustomer.split()[0]
        if not newDeal.idCustomer:
            textInfo += "- There is no customer id chosen.\n"
        newDeal.isRent = deal.isRent
        if newDeal.isRent:
            newDeal.dateStartRent = deal.dateStartRent.get()
            if not newDeal.dateStartRent:
                textInfo += "- There is no date for the rent.\n"
            newDeal.durationDaysRent = deal.durationDaysRent.get()
            if not newDeal.durationDaysRent:
                textInfo += "- There is no duration for the rent.\n"
        if not textInfo:
            newDeal.InsertDB()
            self.SetOrResetCarLists()
            textInfo = "Deal saved"
            if newDeal.isRent:
                self.DisplayWindowRent()
            else:
                self.DisplayWindowSelling()
        for widget in self.frameSort.winfo_children():
            widget.destroy()
        labelError = Label(self.frameSort, text=textInfo)
        labelError.pack()

    def SetOrResetCarLists(self):
        self.carListStock = Car.GetCarList()
        self.dealList = Deal.GetAll()
        self.rentList = []
        self.soldList = []
        self.carListFree = []
        for deal in self.dealList:
            if deal.isRent:
                self.rentList.append(deal)
            else:
                self.soldList.append(deal)

        for car in self.carListStock:
            counter = 0
            found = False
            while counter < len(self.rentList) and not found:
                if car.id == self.rentList[counter].idCar:
                    found = True
                counter += 1
            if not found:
                self.carListFree.append(car)

    def ResetDisplayAndSortFrames(self):
        for widget in self.frameDisplay.winfo_children():
            widget.destroy()
        for widget in self.frameSort.winfo_children():
            widget.destroy()


# It will launch the application
Application()
