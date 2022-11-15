import sys

from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
from Class.Customer import Customer

from datetime import datetime
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
        dealList = Deal.GetAll()
        self.rentList = []
        self.soldList = []
        for deal in dealList:
            self.rentList.append(deal) if deal.isRent else self.soldList.append(deal)
        self.customerList = Customer.GetAll()
        self.spaceDisplay = 4
        print("Welcome to Bamboo Concess\n")
        self.MenuChoice()

    def MenuChoice(self):
        menuInput = ""
        while not CheckNumberInput(menuInput, 1, 5):
            menuInput = input("Where do you want to go now ?\n"
                              " 1 : Show your stock.\n"
                              " 2 : Show your transaction history.\n"
                              " 3 : Add a new car to your stock.\n"
                              " 4 : Add a customer\n"
                              " 5 : Exit the program.\n-> ")
        menuInput = int(menuInput)
        if menuInput == 1:
            self.DisplayStock()
        elif menuInput == 2:
            self.DisplayHistory()
        elif menuInput == 3:
            self.AddCar()
        elif menuInput == 4:
            self.AddCustomer()
        else:
            sys.exit()

    def AddCustomer(self):
        newCustomer = Customer()
        newCustomer.firstName = ""
        newCustomer.lastName = ""
        newCustomer.phone = ""
        newCustomer.mail = ""
        newCustomer.address = ""
        while not newCustomer.firstName.isalpha():
            newCustomer.firstName = input("What's the first name ?\n-> ")
        while not newCustomer.lastName.isalpha():
            newCustomer.lastName = input("What's the last name ?\n-> ")
        while not (newCustomer.phone.isdigit() and len(newCustomer.phone) == 10):
            newCustomer.phone = input("What's the phone number (10 numbers)\n-> ")
        newCustomer.phone = int(newCustomer.phone)
        while not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]+\b', newCustomer.mail)):
            newCustomer.mail = input("What's the email address ?\n-> ")
        while not re.fullmatch(r"[a-zA-Z0-9\s._%+-]+, [a-zA-Z0-9\s._%+-]+\b", newCustomer.address):
            newCustomer.address = input("What's the address ?\n-> ")
        print("New customer added\n") if newCustomer.InsertDB() else print("The execution doesn't work\n")
        self.MenuChoice()

    def DisplayStock(self):
        strList = ["Id", "Brand", "Type", "Price (€)"]
        spaceDict = {
            strList[0]: len(strList[0]) + self.spaceDisplay,
            strList[1]: len(max(self.carListStock, key=lambda x: len(x.brand.name)).brand.name) + self.spaceDisplay,
            strList[2]: len(max(self.carListStock, key=lambda x: len(x.type.name)).type.name) + self.spaceDisplay
        }
        for i in range(len(strList) - 1):
            if spaceDict[strList[i]] < len(strList[i]):
                spaceDict[strList[i]] = len(strList[i]) + self.spaceDisplay

        print(f"{strList[0]}" + " " * self.spaceDisplay +
              f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) +
              f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) +
              f"{strList[3]}\n")

        for car in self.carListStock:
            print(f"{str(car.id):{spaceDict[strList[0]]}}"
                  f"{car.brand.name:{spaceDict[strList[1]]}}"
                  f"{car.type.name:{spaceDict[strList[2]]}}"
                  f"{str(car.price)}")

        nextStep = ""
        while not CheckNumberInput(nextStep, 1, 5):
            nextStep = input("\nWhat do you want to do next ?\n"
                             " 1 : Return to the choice menu.\n"
                             " 2 : See a car's details.\n"
                             " 3 : Rent a car.\n"
                             " 4 : Make a deal.\n"
                             " 5 : Remove a car.\n"
                             "-> ")
        nextStep = int(nextStep)
        if nextStep == 1:
            self.MenuChoice()
        elif nextStep == 2:
            goodChoice = False
            while not goodChoice:
                carId = input("Which car do you want to see details from ?\n-> ")
                if carId.isdigit():
                    carId = int(carId)
                    for car in self.carListStock:
                        if carId == car.id:
                            print(f"Brand : {car.brand.name}\n"
                                  f"Type : {car.type.name}\n"
                                  f"Motor : {car.motor.name}\n"
                                  f"Price : {str(car.price)}€\n"
                                  f"Promo : {str(car.promo)}%\n"
                                  f"In stock since : {car.dateStock}\n"
                                  f"Next control : {car.dateTechControl}\n")
                            goodChoice = True
                            choiceRemove = input("Do you want to remove the car from your stock Y/[n]?\n-> ")
                            if choiceRemove.lower() == "y":
                                car.RemoveDb()
                                self.carListStock(False)
                                self.carListStock(True)
                                print("Car removed\n")
                            break
        elif nextStep == 3:
            self.DoTransaction(True)
        elif nextStep == 4:
            self.DoTransaction(False)
        self.MenuChoice()

    def DisplayHistory(self):
        choiceHistory = ""
        while not CheckNumberInput(choiceHistory, 1, 2):
            choiceHistory = input("\n"
                                  " 1 : Rent history display.\n"
                                  " 2 : Transaction history display.\n"
                                  "-> ")
        choiceHistory = int(choiceHistory)
        strList = ["Id", "Date", "Duration", "Brand", "Type", "Price (€)"]
        spaceDict = {}
        if choiceHistory == 1:
            spaceDict[strList[0]] = len(str(
                max(self.rentList, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
            spaceDict[strList[1]] = len(
                max(self.rentList, key=lambda x: len(x.dateStartRent)).dateStartRent) + self.spaceDisplay
            spaceDict[strList[2]] = len(str(
                max(self.rentList, key=lambda x: len(str(x.durationDaysRent))).durationDaysRent)) + self.spaceDisplay
            spaceDict[strList[3]] = len(
                max(self.rentList, key=lambda x: len(x.car.brand.name)).car.brand.name) + self.spaceDisplay
            spaceDict[strList[4]] = len(
                max(self.rentList, key=lambda x: len(x.car.type.name)).car.type.name) + self.spaceDisplay

        for i in range(len(strList) - 1):
            if spaceDict[strList[i]] < len(strList[i]):
                spaceDict[strList[i]] = len(strList[i]) + self.spaceDisplay

        print(f"\n"
              f"{strList[0]}" + " " * (spaceDict[strList[0]] - len(f"{strList[0]}")) +
              f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) +
              f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) +
              f"{strList[3]}" + " " * (spaceDict[strList[3]] - len(f"{strList[3]}")) +
              f"{strList[4]}" + " " * (spaceDict[strList[4]] - len(f"{strList[4]}")) +
              f"{strList[5]}")

        for deal in self.rentList:
            print(f"{str(deal.id):{spaceDict[strList[0]]}}"
                  f"{deal.dateStartRent:{spaceDict[strList[1]]}}"
                  f"{str(deal.durationDaysRent):{spaceDict[strList[2]]}}"
                  f"{deal.car.brand.name:{spaceDict[strList[3]]}}"
                  f"{deal.car.type.name:{spaceDict[strList[4]]}}"
                  f"{str(deal.car.price)}")

        self.MenuChoice()

    def DoTransaction(self, boolRent):
        deal = Deal()
        goodStartDate = None
        goodCustomerId = None
        goodCarId = None
        deal.idCar = None
        deal.idCustomer = None
        deal.durationDays = None
        deal.dateStart = None
        deal.isRent = bool(boolRent)
        spaceDict = {}
        strList = ["Id", "Name", "Phone"]

        while not goodCarId:
            deal.idCar = input("What is the car id ?\n-> ")
            if deal.idCar.isdigit():
                deal.idCar = int(deal.idCar)
                for car in self.carListStock:
                    if car.id == deal.idCar:
                        goodCarId = True
                        break

        spaceDict[strList[0]] = len(str(max(self.customerList, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
        longestCustomer = max(self.customerList, key=lambda x: len(x.lastName))
        spaceDict[strList[1]] = len(
            f"{longestCustomer.firstName[0]}.{longestCustomer.lastName}") + self.spaceDisplay

        for i in range(len(strList) - 1):
            if spaceDict[strList[i]] < len(strList[i]):
                spaceDict[strList[i]] = len(strList[i])

        print(f"List of customers : \n"
              f"{strList[0]}" + " " * (spaceDict[strList[0]] - len(f"{strList[0]}")) +
              f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[0]}")) +
              f"{strList[2]}")

        for customer in self.customerList:
            print(f"{str(customer.id):{spaceDict[strList[0]]}}"
                  f"{f'{customer.firstName[0]}.{customer.lastName}':{spaceDict[strList[1]]}}"
                  f"{customer.phone}")

        while not goodCustomerId:
            deal.idCustomer = input("What is the customer's id ?\n-> ")
            if deal.idCustomer.isdigit():
                deal.idCustomer = int(deal.idCustomer)
                for customer in self.customerList:
                    if customer.id == deal.idCustomer:
                        goodCustomerId = True
                        break
        if deal.isRent:
            while not goodStartDate:
                deal.dateStart = input("When does the rent start ?\n-> ")
                try:
                    deal.dateStart = datetime.strptime(deal.dateStart, '%d/%m/%Y').strftime("%d/%m/%Y")
                    goodStartDate = True
                except ValueError:
                    pass

            while not CheckNumberInput(deal.durationDays, minimum=1):
                deal.durationDays = input("How many days will the rent spend ?\n-> ")
        deal.InsertDB()
        self.MenuChoice()

    def AddCar(self):
        if Car.CarFreePlacesStock() <= 40:
            car = Car()
            nameBrand = None
            nameType = None
            nameMotor = None
            car.price = None
            car.promo = None
            car.dateTechControl = None
            goodDate = None

            while not nameBrand:
                nameBrand = input("What is the name of the brand ?\n-> ")
            while not nameType:
                nameType = input("What is the type ?\n-> ")
            while not nameMotor:
                nameMotor = input("What is the motor's name ?\n-> ")
            while not CheckNumberInput(car.price, minimum=0):
                car.price = input("What is the price ?\n-> ")
            car.price = int(car.price)
            while not CheckNumberInput(car.promo, 0, 100):
                car.promo = input("Any promotion (%) ?\n-> ")
            car.promo = int(car.promo)
            while not goodDate:
                car.dateTechControl = input("What is the date of the tech control ?\n-> ")
                try:
                    car.dateTechControl = datetime.strptime(car.dateTechControl, '%d/%m/%Y').strftime("%d/%m/%Y")
                    goodDate = True
                except ValueError:
                    continue
            car.idBrand = Brand.GetId(nameBrand)
            car.idType = Type.GetId(nameType)
            car.idMotor = Motor.GetId(nameMotor)
            print("Executed\n") if (car.InsertDB()) else print("Not executed\n")
        else:
            print("No free places in stock.\n")
        self.MenuChoice()


ApplicationConsole()
