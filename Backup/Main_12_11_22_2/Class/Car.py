from Class.DB import DBAccess as DB
from Class.Brand import Brand
import sys
import sqlite3 as sql


class Car(DB):
    def __init__(self):
        self.idCar = None
        self.dateStockCar = None
        self.dateTechControlCar = None
        self.priceCar = None
        self.nameType = None
        self.nameMotor = None
        self.promoCar = None
        self.idType = None
        self.idMotor = None
        self.brand = None
        self.motor = None
        self.type = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Cars"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idCar"

    @staticmethod
    def CarListStock():
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute(
                    "SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, priceCar, "
                    "promoCar FROM Cars WHERE idCar "
                    "NOT IN (select idCar FROM Deals WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = Car.LoadResults(cursor, row)
                    car.brand = Brand.Get(car.idCar)
                    carList.append(car)
                return carList
            except sql.OperationalError:
                print(f"Error in CarListStock {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)

    @staticmethod
    def CarListHistory():
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute("SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, "
                               "priceCar || '0' as priceCar, nameMotor, nameMotor, nameType, promoCar, "
                               "SUBSTR(firstNameCusto, 1, 1) || '.'  ||  lastNameCusto as nameCusto FROM Cars NATURAL "
                               "JOIN Brands NATURAL JOIN Motors NATURAL JOIN Types NATURAL JOIN Deals NATURAL JOIN "
                               "Customers WHERE idCar  IN (select idCar FROM Deals WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = Car.LoadResults(cursor, row)
                    carList.append(car)
                return carList

            except sql.OperationalError:
                print(f"Error in CarListHistory {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)

    @classmethod
    def CarFreePlacesStock(cls):
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute("SELECT count(*) FROM Cars NATURAL JOIN Brands NATURAL JOIN Motors NATURAL JOIN Types "
                               "WHERE idCar NOT IN (select idCar FROM Deals WHERE isRentDeal = 0)")
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
                query = f"INSERT INTO Cars (dateTechControlCar, priceCar, idBrand, idType, idMotor, promoCar) " \
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
