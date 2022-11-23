from Class.DB import DBAccess as DB
from Class.Car import Car
from Class.Customer import Customer
import sqlite3 as sql
import sys


class Deal(DB):
    def __init__(self) -> None:
        self.idCar = self.idCustomer = self.isRent = self.dateStartRent = None
        self.durationDaysRent = self.car = self.customer = None

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the deal table in the database
        :returns: The name of the deal table in the database
        :rtype: str
        """
        return "Deal"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the deal table in the database
        :returns: The name of the primary key in the deal table in the database
        :rtype: str
        """
        return "id"

    def InsertDB(self) -> bool:
        """
        This function insert in the database a new deal
        :returns: True if the insert was correctly executed
        :rtype: bool
        """
        cursor, dbConnection = DB.DBCursor()
        if cursor is not None:
            try:
                query = f"INSERT INTO Deal (isRent, dateStartRent, durationDaysRent, idCar, idCustomer) " \
                        f"VALUES ({self.isRent}, '{self.dateStartRent}', {self.durationDaysRent},{self.idCar}, " \
                        f"{self.idCustomer})"
                cursor.execute(query)
                dbConnection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDBDeal {sys.exc_info()}")
            finally:
                DB.DBClose(cursor)
        return False

    @staticmethod
    def GetAll() -> list:
        """
        This function get all the cars from the database
        :returns: A list of all the cars
        :rtype: list
        """
        cursor = Deal.DBCursor()[0]
        dealList = []
        if cursor is not None:
            try:
                cursor.execute(f"SELECT * FROM {Deal.NameTable()}")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    newDeal = Deal.LoadResults(cursor, row)
                    newDeal.car = Car.GetCar(newDeal.idCar)
                    newDeal.customer = Customer.GetCustomer(newDeal.idCustomer)
                    dealList.append(newDeal)
                return dealList
            except sql.OperationalError:
                print(f"Error in GetAllDeal {sys.exc_info()}")
            finally:
                Deal.DBClose(cursor)
        return []
