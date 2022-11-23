import sqlite3 as sql
import sys

from Class.DB import DBAccess as DB


class Customer(DB):
    def __init__(self) -> None:
        self.id = self.firstName = self.lastName = self.phone = self.mail = self.address = None

    @staticmethod
    def GetCustomer(idCustomer: bool) -> object:
        """
        This function get a customer from the database chosen by its id
        :param idCustomer: An integer number
        :type idCustomer: int
        :returns: A customer object
        :rtype: object
        """
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
        """
        This function insert a customer in the database
        :returns: True if the insertion was correctly executed
        :rtype: bool
        """
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
        return False

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the customer table in the database
        :returns: The name of the customer table in the database
        :rtype: str
        """
        return "Customer"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the customer table in the database
        :returns: The name of the primary key in the customer table in the database
        :rtype: str
        """
        return "id"
