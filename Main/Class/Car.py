from Class.DB import DBAccess as DB
from Class.Type import Type
from Class.Motor import Motor
from Class.Brand import Brand
import sys
import sqlite3 as sql


class Car(DB):
    def __init__(self) -> None:
        self.id = self.dateStock = self.dateTechControl = self.price = self.promo = self.idBrand = None
        self.idType = self.idMotor = self.brand = self.motor = self.type = None

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the car table in the database
        :returns: The name of the car table in the database
        :rtype: str
        """
        return "Car"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the car table in the database
        :returns: The name of the primary key in the car table in the database
        :rtype: str
        """
        return "idCar"

    @staticmethod
    def GetCarList(boolStock: bool) -> list:
        """
        This function get the cars in the database
        :param boolStock: A boolean number
        :type boolStock: bool
        :returns: A list of cars from the database
        :rtype: list
        """
        carList = []
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                if boolStock:
                    query = "SELECT id, STRFTIME('%d/%m/%Y', dateStock) as dateStock, " \
                            "dateTechControl, price || '0' as price, " \
                            "promo FROM Car WHERE id " \
                            "NOT IN (select id FROM Deal WHERE isRent = 0)"

                else:
                    query = "SELECT idCar, STRFTIME('%d/%m/%Y', dateStock) as dateStock, " \
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
            finally:
                DB.DBClose(cursor)
        return []

    @staticmethod
    def CarFreePlacesStock() -> int:
        """
        This function check if there is free places in the stock for another car
        :returns: The number of free places in the stock
        :rtype: int
        """
        cursor = DB.DBCursor()[0]
        if cursor is not None:
            try:
                query = "SELECT count(*) FROM Car " \
                        "WHERE id NOT IN (SELECT id FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                return cursor.fetchone()[0]
            except sql.OperationalError:
                print(f"Error in CarFreePlacesStock {sys.exc_info()}")
            finally:
                DB.DBClose(cursor)
        return 0

    def InsertDB(self) -> bool:
        """
        This function insert in the database a new car
        :returns: True if the insert was correctly executed
        :rtype: bool
        """
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
        return False

    def RemoveDb(self) -> bool:
        """
        This function delete the car
        :returns: True if the deleting was correctly executed
        :rtype: bool
        """
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
        return False

    @staticmethod
    def GetCar(idCar: int) -> object:
        """
        This function get a car in the database chosen by its id
        :param idCar: A integer number
        :type idCar: int
        :returns: An object car with all its components
        :rtype: object
        """
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
            finally:
                Car.DBClose(cursor)
        return None

    def GetComponents(self) -> None:
        """
        This function add to the car its components from the database
        :returns: None
        :rtype: None
        """
        self.brand = Brand.GetCarComponent(self.id)
        self.motor = Motor.GetCarComponent(self.id)
        self.type = Type.GetCarComponent(self.id)
