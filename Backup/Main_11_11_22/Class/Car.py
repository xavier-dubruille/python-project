from Class.DB import DBAccess as DB
import sys
import sqlite3 as sql


class Car(DB):
    def __init__(self):
        self.idCar = None
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
    def CarListStock(cls):
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute(
                    "SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, priceCar, "
                    "nameBrand, nameMotor, nameType, promoCar FROM Car NATURAL JOIN Brand NATURAL JOIN Motor NATURAL "
                    "JOIN Type WHERE idCar NOT IN (select idCar FROM deal WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = cls.LoadResults(cursor, row)
                    carList.append(car)
                return carList
            except sql.OperationalError:
                print(f"Error in CarListStock {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)

    @classmethod
    def CarListHistory(cls):
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute("SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, "
                               "priceCar || '0' as priceCar, nameBrand, nameMotor, nameType, promoCar, "
                               "SUBSTR(firstNameCusto, 1, 1) || '.'  ||  lastNameCusto as nameCusto FROM Car NATURAL "
                               "JOIN Brand NATURAL JOIN Motor NATURAL JOIN Type NATURAL JOIN Deal NATURAL JOIN "
                               "Customer WHERE idCar  IN (select idCar FROM deal WHERE isRentDeal = 0)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = cls.LoadResults(cursor, row)
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
                cursor.execute("SELECT count(*) FROM Car NATURAL JOIN Brand NATURAL JOIN Motor NATURAL JOIN Type "
                               "WHERE idCar NOT IN (select idCar FROM deal WHERE isRentDeal = 0)")
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
                cursor.execute(
                    f"INSERT INTO Car (dateTechControlCar, priceCar, idBrand, idType, idMotor, promoCar) "
                    f"VALUES ({self.dateTechControlCar}, {self.priceCar}, {self.idBrand},"
                    f"{self.idType}, {self.idMotor},{self.promoCar})")
                dbConnection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDB {sys.exc_info()}")
                return False
            finally:
                DB.DBClose(cursor)
