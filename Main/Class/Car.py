from Class.DB import DBAccess as DB
from Class.Type import Type
from Class.Motor import Motor
from Class.Brand import Brand
import sys
import sqlite3 as sql


class Car(DB):
    def __init__(self):
        self.id = 0
        self.dateStock = ""
        self.dateTechControl = ""
        self.price = 0
        self.promo = 0
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
                    query = "SELECT id, STRFTIME('%d/%m/%Y', dateStock) as dateStockCar, " \
                            "dateTechControl, price || '0' as price, " \
                            "promo FROM Car WHERE id " \
                            "NOT IN (select id FROM Deal WHERE isRent = 0)"

                else:
                    query = "SELECT idCar, STRFTIME('%d/%m/%Y', dateStock) as dateStockCar, " \
                            "dateTechControl, price || '0' as price, promo, " \
                            "SUBSTR(firstName, 1, 1) || '.'  ||  lastName as nameCusto " \
                            "FROM Car NATURAL JOIN Deal NATURAL JOIN Customer " \
                            "WHERE idCar  IN (select idCar FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = Car.LoadResults(cursor, row)
                    car.GetComponents()
                    carList.append(car)
                return carList
            except sql.OperationalError:
                print(f"Error in GetCarList {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)
        return None

    @classmethod
    def CarFreePlacesStock(cls):
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                query = "SELECT count(*) FROM Car " \
                        "WHERE id NOT IN (SELECT id FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                return cursor.fetchone()[0]
            except sql.OperationalError:
                print(f"Error in CarFreePlacesStock {sys.exc_info()}")
                return None
            finally:
                DB.DBClose(cursor)
        return None

    def InsertDB(self):
        cursor, dbConnection = self.DBCursor()
        if cursor is not None:
            try:
                query = f"INSERT INTO Car (dateTechControl, price, idBrand, idType, idMotor, promo) " \
                        f"VALUES ('{self.dateTechControl}', {self.price}, {self.idBrand},{self.idType}, " \
                        f"{self.idMotor}, {self.promo} )"
                cursor.execute(query)
                dbConnection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDBCar {sys.exc_info()}")
            finally:
                self.DBClose(cursor)
        return None

    def RemoveDb(self):
        cursor, dbConnection = self.DBCursor()
        if cursor is not None:
            try:
                query = f"DELETE FROM Car WHERE id = {self.id}"
                cursor.execute(query)
                dbConnection.commit()
                del self
                return True
            except sql.OperationalError:
                print(f"Error in RemoveCarDB {sys.exc_info()}")
            finally:
                DB.DBClose(cursor)
        return None

    @staticmethod
    def GetCar(idCar):
        cursor = Car.DBCursor()[0]
        if cursor is not None:
            try:
                query = f"SELECT id, STRFTIME('%d/%m/%Y', dateStock) as dateStockCar, dateTechControl, " \
                        f"price || '0' as price, promo " \
                        f"FROM Car " \
                        f"WHERE id = {idCar} "
                cursor.execute(query)
                newCar = Car.LoadResults(cursor, cursor.fetchone())
                newCar.GetComponents()
                return newCar
            except sql.OperationalError:
                print(f"Error in GetCar {sys.exc_info()}")
                return None

    def GetComponents(self):
        self.brand = Brand.GetCarComponent(self.id)
        self.motor = Motor.GetCarComponent(self.id)
        self.type = Type.GetCarComponent(self.id)
