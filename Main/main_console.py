from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
from Class.Customer import Customer

import re


def CheckNumberInput(string, minimum=None, maximum=None):
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


class ApplicationConsole:
    def __init__(self):
        self.carListStock = Car.GetCarList(True)
        self.carListHistory = Car.GetCarList(False)
        self.brandList = Brand.GetAll()
        self.motorList = Motor.GetAll()
        self.typeList = Type.GetAll()
        self.dealList = Deal.GetAll()
        self.customerList = Customer.GetAll()
        self.ShowMainMenu()

    def ShowMainMenu(self):
        print("Welcome to Bamboo Concess")
        self.MenuChoice()

    def MenuChoice(self):
        menuInput = ""
        while not CheckNumberInput(menuInput, 1, 5):
            menuInput = input(
                "\nWhere do you want to go now ?\n 1 : Show your stock."
                "\n 2 : Show your transaction history.\n 3 : Make a deal.\n 4 : Add a new car to your stock.\n -> ")
        menuInput = int(menuInput)
        if menuInput == 1:
            self.DisplayStock()
        elif menuInput == 2:
            self.DisplayHistory()
        elif menuInput == 3:
            self.MakeADeal()
        elif menuInput == 4:
            self.AddACar()

    def displayStock(self):
        spaceBrand = len(max(self.carListStock, key=lambda car: len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListStock, key=lambda x: len(x.nameType)).nameType) + 4
        spaceIdCar = len("Id") + 4
        print("\nId" + " " * 4 + "Brand" + " " * (spaceBrand - len("Brand")) + "Type" + " " * (
                spaceType - len("Type")) + "Price (€)")
        for car in self.carListStock:
            print(
                f"{str(car.idCar):{spaceIdCar}}{car.brand.name:{spaceBrand}}{car.type.name:{spaceType}}{car.priceCar}")

        nextStep = ""
        while not CheckNumberInput(nextStep, 1, 3):
            nextStep = input("\nWhat do you want to do next ?\n 1 : Return to the choice menu."
                             "\n 2 : See a car's details.\n 3 : Rent a car.\n-> ")
        nextStep = int(nextStep)
        if nextStep == 1:
            self.MenuChoice()
        elif nextStep == 2:
            goodChoice = False
            while not goodChoice:
                carId = input("\nWhich car do you want to see details from ?\n-> ")
                if carId.isdigit():
                    carId = int(carId)
                    for car in self.carListStock:
                        if carId == car.idCar:
                            print(f"\nBrand : {car.brand.name}\nType : {car.type.name}"
                                  f"\nMotor : {car.motor.name}\nPrice : {str(car.priceCar)}€"
                                  f"\nPromo : {str(car.promoCar)}%\nIn stock since : {str(car.dateStockCar)}"
                                  f"\nNext control : {str(car.dateTechControlCar)}")
                            goodChoice = True
                            break
        elif nextStep == 3:
            self.RentACar()
        self.MenuChoice()

    def DisplayHistory(self):
        spaceBrand = len(max(self.carListHistory, key=lambda x: len(x.brand.name)).brand.name) + 4
        spaceType = len(max(self.carListHistory, key=lambda x: len(x.type.name)).type.name) + 4
        spacePrice = len(str(max(self.carListHistory, key=lambda x: len(str(x.priceCar))).priceCar)) + 4
        spaceId = len("Id") + 4

        print("\nId" + " " * (spaceId - len("Id")) + "Brand" + " " * (spaceBrand - len("Brand")) + "Type" + " " * (
                spaceType - len("Type")) + "Price (€)" + " " * (spacePrice - len("Price (€)")) + "Customer")

        for car in self.carListHistory:
            print(
                f"{str(car.idCar):{spaceId}}{car.brand.name:{spaceBrand}}"
                f"{car.type.name:{spaceType}}{car.priceCar:{spacePrice}}{car.nameCusto}")
        self.MenuChoice()

    def RentACar(self):
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            goodChoice = False
            idCar = None
            while not goodChoice:
                idCar = input("What is the car's id ?\n-> ")
                if idCar.isdigit():
                    idCar = int(idCar)
                    for car in self.carListStock:
                        if car.idCar == idCar:
                            goodChoice = True
                            break
            deal.idCar = idCar
            spaceId = len(str(max(self.customerList, key=lambda x: len(str(x.id))).id)) + 4
            longestCustomer = max(self.customerList, key=lambda x: len(x.lastName))
            spaceName = len(f"{longestCustomer.firstName[0]}.{longestCustomer.lastName}") + 4
            print("List of customers : ")
            print("Id" + " " * (spaceId - len("Id")) + "Name" + " " * (spaceName - len("Name")) + "Phone")
            for customer in self.customerList:
                print(
                    f"{str(customer.id):{spaceId}}{f'{customer.firstName[0]}.{customer.lastName}':{spaceName}}"
                    f"{customer.phone}")
            goodChoice = False
            idCustomer = None
            while not goodChoice:
                idCustomer = input("What is the customer's id ?\n-> ")
                if idCustomer.isdigit():
                    idCustomer = int(idCustomer)
                    for customer in self.customerList:
                        if customer.id == idCustomer:
                            goodChoice = True
                            break
            deal.idCustomer = idCustomer
            deal.isRent = True
            goodChoice = False
            dateStart = None
            while not goodChoice:
                dateStart = input("When does the rent start ?\n-> ")
                if re.search('[0-9/]', dateStart):
                    goodChoice = True
            deal.dateStartRent = dateStart
            durationDays = ""
            while not CheckNumberInput(durationDays, minimum=1):
                durationDays = input("How many days will the rent spend ?\n-> ")
            deal.durationDaysRent = int(durationDays)
        else:
            print("\nNo Free places.")
        self.MenuChoice()

    def MakeADeal(self):
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            deal.idCar = input("What is the car's id ?")
            deal.idCustomer = input("What is the customer's id ? ")
        self.MenuChoice()

    def AddACar(self):
        if Car.CarFreePlacesStock() <= 40:
            car = Car()
            nameBrand = ""
            while not nameBrand:
                nameBrand = input("What is the name of the brand ?\n-> ")
            nameType = ""
            while not nameType:
                nameType = input("What is the type ?\n-> ")
            nameMotor = ""
            while not nameMotor:
                nameMotor = input("What is the motor's name ?\n-> ")
            car.priceCar = ""
            while not car.priceCar.isdigit():
                car.priceCar = input("What is the price ?\n-> ")
            car.priceCar = int(car.priceCar)
            car.promoCar = ""
            while not car.promoCar.isdigit():
                car.promoCar = input("Any promotion ?(put the number)\n-> ")
            car.promoCar = int(car.promoCar)
            car.dateTechControlCar = ""
            goodDate = False
            while not goodDate:
                car.dateTechControlCar = input("\nWhat is the date of the tech control ?\n-> ")
                if re.search("[0-9/]", car.dateTechControlCar):
                    goodDate = True
            car.brand.id = Brand.GetId(nameBrand)
            car.type.id = Type.GetId(nameType)
            car.motor.id = Motor.GetId(nameMotor)
            print("Executed") if (car.InsertDB()) else print("Not executed")
        else:
            print("No free places in stock.")
        self.MenuChoice()

    # def VerifyCarInsert(self, carRawData):
    #     car = Car()
    #     counter = 0
    #     #Get the id for the motor
    #     while counter < len(self.motorList) or car.idMotor == None:
    #         if self.motorList[counter].nameMotor == carRawData.nameMotor.get():
    #             car.idMotor = self.motorList[counter].idMotor
    #         counter += 1

    #     counter = 0
    #     while counter < len(self.brandList) or car.idBrand == None:
    #         if self.brandList[counter].nameBrand == carRawData.nameBrand.get():
    #             car.idBrand = self.brandList[counter].idBrand
    #         counter += 1

    #     counter = 0
    #     while counter < len(self.typeList) or car.idType == None:
    #         if self.typeList[counter].nameType == carRawData.nameType.get():
    #             car.idType = self.typeList[counter].idType
    #         counter += 1

    #     car.dateTechControlCar = carRawData.dateTechControlCar.get()
    #     car.priceCar = float(carRawData.priceCar.get())
    #     car.promoCar = carRawData.promoCar.get()
    #     car.InsertDB()
    #     self.carListStock = Car.CarListStock()


ApplicationConsole()
