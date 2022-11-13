from Class.DB import DBAccess as DB
from Class.Type import Type
from Class.Motor import Motor
from Class.Brand import Brand
import sys
import sqlite3 as sql


class Car(DB):
    def __init__(self):
        self.idCar = 0
        self.dateStockCar = ""
        self.dateTechControlCar = ""
        self.priceCar = 0
        self.promoCar = 0
        self.idBrand = 0
        self.idType = 0
        self.idMotor = 0
        self.brand = {}
        self.motor = {}
        self.type = {}

    @staticmethod
    def NameTable():
        # Return the name table
        return "Car"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idCar"

    @staticmethod
    def GetCarList(boolStock):
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                if boolStock:
                    query = "SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, " \
                            "dateTechControlCar, priceCar || '0' as priceCar, " \
                            "promoCar FROM Car WHERE idCar " \
                            "NOT IN (select idCar FROM Deal WHERE isRent = 0)"

                else:
                    query = "SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, " \
                            "dateTechControlCar, priceCar || '0' as priceCar, promoCar, " \
                            "SUBSTR(firstName, 1, 1) || '.'  ||  lastName as nameCusto " \
                            "FROM Car NATURAL JOIN Deal NATURAL JOIN Customer " \
                            "WHERE idCar  IN (select idCar FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = Car.LoadResults(cursor, row)
                    car.brand = Brand.GetCarComponent(car.idCar)
                    car.motor = Motor.GetCarComponent(car.idCar)
                    car.type = Type.GetCarComponent(car.idCar)
                    carList.append(car)
                return carList
            except sql.OperationalError:
                print(f"Error in CarListStock {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)

    @classmethod
    def CarFreePlacesStock(cls):
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                query = "SELECT count(*) FROM Car " \
                        "WHERE idCar NOT IN (SELECT idCar FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                return cursor.fetchone()[0]
            except sql.OperationalError:
                print(f"Error in CarFreePlacesStock {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)

    def InsertDB(self):
        cursor, dbConnection = DB.DBCursor()
        if cursor is not None:
            try:
                query = f"INSERT INTO Car (dateTechControlCar, priceCar, idBrand, idType, idMotor, promoCar) " \
                        f"VALUES ('{self.dateTechControlCar}', {self.priceCar}, {self.idBrand},{self.idType}, " \
                        f"{self.idMotor}, {self.promoCar} )"
                cursor.execute(query)
                dbConnection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDB {sys.exc_info()}")
                return False
            finally:
                DB.DBClose(cursor)
