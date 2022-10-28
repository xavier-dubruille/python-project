from Class.DB import DBAccess as DB
from Class.Car import Car
from Class.Brand import Brand
from Class.Type import Type
from Class.Motor import Motor
from Class.Deal import Deal
from Class.Customer import Customer

class Application():
    def __init__(self):
        self.carListStock = Car.CarListStock()
        self.carListHistory = Car.CarListHistory()
        self.brandList = Brand.GetAll()
        self.motorList = Motor.GetAll()
        self.typeList = Type.GetAll()
        self.dealList = Deal.GetAll()
        self.custoList = Customer.GetAll()
        self.showMainMenu()

    def showMainMenu(self):
        wichMenu = input("Welcome to bambooConcess \nWhere do you want to go ?\n 1 : Show your stock.\n 2 : Show your transaction history.\n 3 : Rent a car.\n 4 : Make a deal.\n 5 : Add a new car to your stock.\n ->")
        if wichMenu == 1:
            Application.displayStock()
        elif wichMenu == 2:
            Application.displayHistory()
        elif wichMenu == 3:
            Application.rentACar()
        elif wichMenu == 4:
            Application.makeADeal()
        
    def displayStock(self):
        spaceBrand = len(max(self.carListStock, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListStock, key=lambda x:len(x.nameType)).nameType) + 4
        spaceIdCar = len("Id") + 4

        print("Id" + " " * 4  + "Brand" + " "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Price")
        for car in self.carListStock:
            print(f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar}") 

    def displayHistory(self):
        spaceBrand = len(max(self.carListHistory, key=lambda car:len(car.nameBrand)).nameBrand) + 4
        spaceType = len(max(self.carListHistory, key=lambda x:len(x.nameType)).nameType) + 4
        spacePrice = len(max(self.carListHistory, key=lambda x:len(x.priceCar)).priceCar) + 4
        spaceIdCar = len("Id") + 4

        print("Id" + " "*4 + "Brand" +" "*(spaceBrand-len("Brand")) + "Type" + " "*(spaceType-len("Type")) +  "Price" + " "*(spacePrice-len("Price")) + "Customer")

        for car in self.carListHistory:
            f"{str(car.idCar):{spaceIdCar}}{car.nameBrand:{spaceBrand}}{car.nameType:{spaceType}}{car.priceCar:{spacePrice}}{car.nameCusto}"

    def rentACar(self):
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()     
            deal.idCar = input("What is the car's id ?")
            deal.idCusto = input("What is the customer's id")
            deal.isRentDeal = 1
            deal.dateStartRentDeal = input("When does the rent start ?")
            deal.durationDaysRentDeal = input("How many days will the rent spend ?")
        else:
            print("No Free places.")

    def makeADeal(self):
        if Car.CarFreePlacesStock() <= 40:
            deal = Deal()
            deal.idCar = input("What is the car's id ?")
            deal.idCusto = input("What is the customer's id ? ")



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

Application() 
