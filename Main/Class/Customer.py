import sqlite3 as sql
import sys

from Class.DB import DBAccess as DB


class Customer(DB):
    def __init__(self):
        self.id = 0
        self.firstName = ""
        self.lastName = ""
        self.phone = 0
        self.mail = ""
        self.address = ""

    @staticmethod
    def GetCustomer(idCustomer):
        cursor = Customer.DBCursor()[0]
        if cursor is not None:
            try:
                query = f"SELECT * FROM Customer WHERE id = {idCustomer}"
                cursor.execute(query)
                newCustomer = Customer.LoadResults(cursor, cursor.fetchone())
                return newCustomer
            except sql.OperationalError:
                print(f"Error in GetCustomer : {sys.exc_info()}")
                return None
            finally:
                Customer.DBClose(cursor)
        return None

    def InsertDB(self):
        cursor, dbConnection = self.DBCursor()
        if cursor is not None:
            try:
                query = f"INSERT INTO Customer (firstName, lastName, phone, mail, address) " \
                        f"VALUES ({self.firstName}, {self.lastName}, {self.phone}, {self.mail}, {self.address})"
                cursor.execute(query)
                dbConnection.commit()
            except sql.OperationalError:
                print(f"Error in InsertDB Customer {sys.exc_info()}")
            finally:
                self.DBClose(cursor)
        return None

    @staticmethod
    def NameTable():
        return "Customer"

    @staticmethod
    def IdColumn():
        return "id"
