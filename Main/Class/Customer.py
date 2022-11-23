import sqlite3 as sql
import sys

from Class.DB import DBAccess as DB


class Customer(DB):
    def __init__(self) -> None:
        self.id = 0
        self.firstName = ""
        self.lastName = ""
        self.phone = 0
        self.mail = ""
        self.address = ""

    @staticmethod
    def GetCustomer(idCustomer: bool) -> object:
        cursor = Customer.DBCursor()[0]
        if cursor is not None:
            try:
                query = f"SELECT * FROM Customer WHERE id = {idCustomer}"
                cursor.execute(query)
                newCustomer = Customer.LoadResults(cursor, cursor.fetchone())
                return newCustomer
            except sql.OperationalError:
                print(f"Error in GetCustomer : {sys.exc_info()}")
            finally:
                Customer.DBClose(cursor)
        return None

    def InsertDB(self) -> bool:
        cursor, dbConnection = self.DBCursor()
        if cursor is not None:
            try:
                query = f"INSERT INTO Customer (firstName, lastName, phone, mail, address) " \
                        f"VALUES ('{self.firstName}', '{self.lastName}', {self.phone}, '{self.mail}', '{self.address}')"
                cursor.execute(query)
                dbConnection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDB Customer {sys.exc_info()}")
            finally:
                self.DBClose(cursor)
        return None

    @staticmethod
    def NameTable() -> str:
        return "Customer"

    @staticmethod
    def IdColumn() -> str:
        return "id"
