from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
from Class.Customer import Customer

import re


def checkNumberInput(string, minimum, maximum):
    if not string.isdigit():
        return False
    if maximum >= int(string) >= minimum:
        return True
    return False


class ApplicationConsole:
    def __init__(self):
        self.carListStock = Car.CarListStock()
        self.carListHistory = Car.CarListHistory()
        self.brandList = Brand.GetAll()
        self.motorList = Motor.GetAll()
        self.typeList = Type.GetAll()
        self.dealList = Deal.GetAll()
        self.customerList = Customer.GetAll()
        self.showMainMenu()

    def showMainMenu(self):
        print("Welcome to Bamboo Concess")
        ApplicationConsole.menuChoice(self)

    def menuChoice(self):
        menuInput = ""
        while not checkNumberInput(menuInput, 1, 5):
            menuInput = input(
                "\nWhere do you want to go now ?\n 1 : Show your stock."
                "\n 2 : Show your transaction history.\n 3 : Rent a "
                "car.\n 4 : Make a deal.\n 5 : Add a new car to your stock.\n -> ")
        menuInput = int(menuInput)
        if menuInput == 1:
            ApplicationConsole.displayStock(self)
        elif menuInput == 2:
            ApplicationConsole.displayHistory(self)
        elif menuInput == 3:
            ApplicationConsole.rentACar()
        elif menuInput == 4:
            ApplicationConsole.makeADeal()
        elif menuInput == 5:
            ApplicationConsole.addACar()

    def displayStock(self):
        spaceBrand = len(max(self.carListStock, key=lambda x: len(x.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListStock, key=lambda x: len(x.nameType)).nameType) + 4
        spaceIdCar = len("Id") + 4
        print("\nId" + " " * 4 + "Brand" + " " * (spaceBrand - len("Brand")) + "Type" + " " * (
                spaceType - len("Type")) + "Price")
        for car in self.carListStock:
            print(f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar}")

        nextStep = ""
        while not checkNumberInput(nextStep, 1, 2):
            nextStep = input("\nWhat do you want to do next ?\n 1 : Return to the choice menu."
                             "\n 2 : See a car's details.\n -> ")
        nextStep = int(nextStep)
        if nextStep == 1:
            ApplicationConsole.menuChoice(self)
        elif nextStep == 2:
            goodChoice = False
            while not goodChoice:
                carId = input("\nWhich car do you want to see details from ?\n-> ")
                if carId.isdigit():
                    carId = int(carId)
                    for car in self.carListStock:
                        if carId == car.idCar:
                            print(f"\nBrand : {car.nameBrand}\nType : {car.nameType}"
                                  f"\nMotor : {car.nameMotor}\nPrice : {str(car.priceCar)}€"
                                  f"\nPromo : {str(car.promoCar)}%\nIn stock since : {str(car.dateStockCar)}"
                                  f"\nNext control : {str(car.dateTechControlCar)}")
                            goodChoice = True
                            break
            ApplicationConsole.menuChoice(self)

    def displayHistory(self):
        spaceBrand = len(max(self.carListHistory, key=lambda x: len(x.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListHistory, key=lambda x: len(x.nameType)).nameType) + 4
        spacePrice = len(max(self.carListHistory, key=lambda x: len(x.priceCar)).priceCar) + 4
        spaceIdCar = len("Id") + 4

        print("\nId" + " " * 4 + "Brand" + " " * (spaceBrand - len("Brand")) + "Type" + " " * (
                spaceType - len("Type")) + "Price (€)" + " " * (spacePrice - len("Price")) + "Customer")

        for car in self.carListHistory:
            print(
                f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}"
                f"{car.nameType:{spaceType}}{car.priceCar:{spacePrice}}{car.nameCusto}")
        ApplicationConsole.menuChoice(self)

    @staticmethod
    def rentACar():
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            deal.idCar = input("What is the car's id ?")
            deal.idCustomer = input("What is the customer's id ?")
            deal.isRentDeal = 1
            deal.dateStartRentDeal = input("When does the rent start ?")
            deal.durationDaysRentDeal = input("How many days will the rent spend ?")
        else:
            print("No Free places.")

    @staticmethod
    def makeADeal():
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            deal.idCar = input("What is the car's id ?")
            deal.idCustomer = input("What is the customer's id ? ")

    @staticmethod
    def addACar():
        if Car.CarFreePlacesStock() <= 40:
            car = Car()
            nameBrand = input("What is the name of the brand ?\n-> ")
            car.idBrand = Brand.GetIdFromName(nameBrand)
            car.nameType = input("What is the type ?\n-> ")
            car.nameMotor = input("What is the motor's name ?\n-> ")
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
            print("Executed") if (car.InsertDB()) else print("Not executed")
        else:
            print("No free places in stock.")

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
