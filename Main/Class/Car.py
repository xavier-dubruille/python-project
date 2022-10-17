from Class.DB import DBAccess as DB
import sys

class Car(DB): 
    def __init__(self): 
        self.idCard = None
        self.dateStockCar = None
        self.dateTechControlCar = None
        self.priceCar = None
        self.nameBrand = None
        self.nameType = None
        self.nameMotor = None
        self.promoCar = None
        self.idBrand = None
        self.idType = None
        self.idMotor = None


    @staticmethod
    def NameTable():
        # Return the name table
        return "Car"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idCar"
    
    @classmethod
    def CarListStock(clss): 
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor != None:
            try:
                cursor.execute("SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, priceCar, nameBrand, nameMotor, \
                nameType, promoCar \
                FROM Car \
                NATURAL JOIN Brand \
                NATURAL JOIN Motor\
                NATURAL JOIN Type\
                WHERE idCar NOT IN (select idCar FROM deal WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = clss.LoadResults(cursor, row)
                    carList.append(car)
                return carList
            except:
                print("Error in CarListStock")
                print(sys.exc_info())
                return None 
            finally: 
                DB.DBClose(cursor)

    @classmethod
    def CarListHistory(clss):
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor != None:
            try:
                cursor.execute("SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, priceCar || '0' as priceCar, \
                nameBrand, nameMotor, nameType, promoCar, SUBSTR(firstNameCusto, 1, 1) || '.'  ||  lastNameCusto as nameCusto \
                FROM Car \
                NATURAL JOIN Brand \
                NATURAL JOIN Motor \
                NATURAL JOIN Type \
                NATURAL JOIN Deal \
                NATURAL JOIN Customer \
                WHERE idCar  IN (select idCar FROM deal WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = clss.LoadResults(cursor, row)
                    carList.append(car)
                return carList

            except:
                print("Error in CarListHistory")
                print(sys.exc_info())
                return None
            finally:
                DB.DBClose(cursor)
    
    @classmethod
    def CarFreePlacesStock(clss): 
        cursor = DB.DBCursor()[0]
        if cursor != None: 
            try: 
                cursor.execute("SELECT count(*) \
                FROM Car \
                NATURAL JOIN Brand \
                NATURAL JOIN Motor \
                NATURAL JOIN Type \
                WHERE idCar NOT IN (select idCar FROM deal WHERE isRentDeal = 0)")
                return cursor.fetchone()[0]
            except:
                print("Error in CarFreePlacesStock")
                print(sys.exc_info())
                return None 
            finally: 
                DB.DBClose(cursor)

    def InsertDB(self): 
        cursor, dbConnection = DB.DBCursor()
        if cursor != None:
            try:
                for motor in self.motorList:
                    if motor.nameMotor == self.nameMotor.get():
                        self.idMotor = motor.idMotor 
                        break
                        
                for type in self.typeList:
                    if type.nameType == self.nameType.get():
                        self.idType = type.idType
                        break
                
                for brand in self.brandList:
                    if brand.nameBrand == self.nameBrand.get():
                        self.idBrand = brand.idBrand
                        break
                
                cursor.execute("INSERT INTO Car (dateTechControlCar, priceCar, idBrand, idType, idMotor, promoCar) VALUES (?, ?, ?, ?, ?, ?)"\
                    , (self.dateTechControlCar.get(), self.priceCar.get(), self.idBrand, self.idType, self.idMotor, self.promoCar.get(), ))
                dbConnection.commit()
            except:
                print("Error in InsertDB")
                print(sys.exc_info())
            finally:
                DB.DBClose(cursor)