from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
from Class.Customer import Customer

import re
from datetime import datetime


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
        self.ShowMainMenu()

    def ShowMainMenu(self):
        print("Welcome to Bamboo Concess")
        self.MenuChoice()

    def MenuChoice(self):
        menuInput = ""
        while not CheckNumberInput(menuInput, 1, 4):
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
        self.MenuChoice()

    def DisplayStock(self):
        strList = ["Id", "Brand", "Type", "Price (€)"]
        spaceDict = {
            strList[0]: len(strList[0]) + self.spaceDisplay,
            strList[1]: len(max(self.carListStock, key=lambda x: len(x.brand.name)).brand.name) + self.spaceDisplay,
            strList[2]: len(max(self.carListStock, key=lambda x: len(x.type.name)).type.name) + self.spaceDisplay
        }
        for i in range(len(strList)-1):
            if spaceDict[strList[i]] < len(strList[i]):
                spaceDict[strList[i]] = len(strList[i]) + self.spaceDisplay

        print(f"\n{strList[0]}" + " " * self.spaceDisplay +
              f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) +
              f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) +
              f"{strList[3]}")
        for car in self.carListStock:
            print(
                f"{str(car.id):{spaceDict[strList[0]]}}"
                f"{car.brand.name:{spaceDict[strList[1]]}}"
                f"{car.type.name:{spaceDict[strList[2]]}}"
                f"{str(car.price)}")

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
                        if carId == car.id:
                            print(f"\nBrand : {car.brand.name}\nType : {car.type.name}"
                                  f"\nMotor : {car.motor.name}\nPrice : {str(car.price)}€"
                                  f"\nPromo : {str(car.promo)}%\nIn stock since : {str(car.dateStock)}"
                                  f"\nNext control : {str(car.dateTechControl)}")
                            goodChoice = True
                            break
        elif nextStep == 3:
            self.RentACar()
        self.MenuChoice()

    def DisplayHistory(self):
        choiceHistory = ""
        while not CheckNumberInput(choiceHistory, 1, 2):
            choiceHistory = input(" 1 : Rent history display.\n 2 : Transaction history display.\n-> ")
        choiceHistory = int(choiceHistory)
        strList = ["Id", "Date", "Duration", "Brand", "Type", "Price (€)"]
        spaceDict = {}
        if choiceHistory == 1:
            spaceDict[strList[0]] = len(str(
                max(self.rentList, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
            spaceDict[strList[1]] = len(
                max(self.rentList, key=lambda x: len(x.dateStartRent)).dateStartRent) + self.spaceDisplay
            spaceDict[strList[2]] = len(
                str(
                    max(self.rentList, key=lambda x:
                        len(str(x.durationDaysRent))).durationDaysRent)) + self.spaceDisplay
            spaceDict[strList[3]] = len(
                max(self.rentList, key=lambda x: len(x.car.brand.name)).car.brand.name) + self.spaceDisplay
            spaceDict[strList[4]] = len(
                max(self.rentList, key=lambda x: len(x.car.type.name)).car.type.name) + self.spaceDisplay

        for i in range(len(strList)-1):
            if spaceDict[strList[i]] < len(strList[i]):
                spaceDict[strList[i]] = len(strList[i]) + self.spaceDisplay

        print(f"\n{strList[0]}" + " " * (spaceDict[strList[0]] - len(f"{strList[0]}")) +
              f"{strList[1]}" + " " * (spaceDict[strList[1]] - len(f"{strList[1]}")) +
              f"{strList[2]}" + " " * (spaceDict[strList[2]] - len(f"{strList[2]}")) +
              f"{strList[3]}" + " " * (spaceDict[strList[3]] - len(f"{strList[3]}")) +
              f"{strList[4]}" + " " * (spaceDict[strList[4]] - len(f"{strList[4]}")) +
              f"{strList[5]}")

        for deal in self.rentList:
            print(
                f"{str(deal.id):{spaceDict[strList[0]]}}"
                f"{deal.dateStartRent:{spaceDict[strList[1]]}}"
                f"{str(deal.durationDaysRent):{spaceDict[strList[2]]}}"
                f"{deal.car.brand.name:{spaceDict[strList[3]]}}"
                f"{deal.car.type.name:{spaceDict[strList[4]]}}"
                f"{str(deal.car.price)}")

        # spaceBrand = len(max(self.carListHistory, key=lambda x: len(x.brand.name)).brand.name) + 4
        # spaceType = len(max(self.carListHistory, key=lambda x: len(x.type.name)).type.name) + 4
        # spacePrice = len(str(max(self.carListHistory, key=lambda x: len(str(x.price))).price)) + 4
        # spaceId = len("Id") + 4
        #
        # print("\nId" + " " * (spaceId - len("Id")) + "Brand" + " " * (spaceBrand - len("Brand")) + "Type" + " " * (
        #         spaceType - len("Type")) + "Price (€)" + " " * (spacePrice - len("Price (€)")) + "Customer")
        #
        # for car in self.carListHistory:
        #     print(
        #         f"{str(car.id):{spaceId}}{car.brand.name:{spaceBrand}}"
        #         f"{car.type.name:{spaceType}}{car.price:{spacePrice}}{car.nameCusto}")
        self.MenuChoice()

    def RentACar(self):
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            goodChoice = False
            idCar = None
            while not goodChoice:
                idCar = input("What is the car id ?\n-> ")
                if idCar.isdigit():
                    idCar = int(idCar)
                    for car in self.carListStock:
                        if car.id == idCar:
                            goodChoice = True
                            break
            deal.idCar = idCar
            idStr = "Id"
            nameStr = "Name"
            phoneStr = "Phone"
            spaceId = len(str(max(self.customerList, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
            if spaceId < len(idStr):
                spaceId = len(idStr)
            longestCustomer = max(self.customerList, key=lambda x: len(x.lastName))
            spaceName = len(f"{longestCustomer.firstName[0]}.{longestCustomer.lastName}") + self.spaceDisplay
            if spaceName < len(nameStr):
                spaceName = len(nameStr)
            print("List of customers : ")
            print(f"{idStr}" + " " * (spaceId - len(f"{idStr}")) +
                  f"{nameStr}" + " " * (spaceName - len(f"{nameStr}"))
                  + f"{phoneStr}")
            for customer in self.customerList:
                print(
                    f"{str(customer.id):{spaceId}}"
                    f"{f'{customer.firstName[0]}.{customer.lastName}':{spaceName}}"
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
            dateStart = 1
            while not goodChoice:
                dateStrStart = input("When does the rent start ?\n-> ")
                try:
                    dateStart = datetime.strptime(dateStrStart, '%d/%m/%Y').strftime("%d/%m/%Y")
                    goodChoice = True
                except ValueError:
                    pass
            deal.dateStartRent = dateStart
            durationDays = ""
            while not CheckNumberInput(durationDays, minimum=1):
                durationDays = input("How many days will the rent spend ?\n-> ")
            deal.durationDaysRent = int(durationDays)
            deal.InsertDB()
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
            car.price = ""
            while not car.price.isdigit():
                car.price = input("What is the price ?\n-> ")
            car.price = int(car.price)
            car.promo = ""
            while not car.promo.isdigit():
                car.promo = input("Any promotion ?(put the number)\n-> ")
            car.promo = int(car.promo)
            car.dateTechControl = ""
            goodDate = False
            while not goodDate:
                car.dateTechControl = input("\nWhat is the date of the tech control ?\n-> ")
                if re.search("[0-9/]", car.dateTechControl):
                    goodDate = True
            car.idBrand = Brand.GetId(nameBrand)
            car.idType = Type.GetId(nameType)
            car.idMotor = Motor.GetId(nameMotor)
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
