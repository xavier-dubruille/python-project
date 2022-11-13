from Class.DB import DBAccess as DB
import sqlite3 as sql
import sys


class Deal(DB):
    def __init__(self):
        self.idCar = None
        self.idCustomer = None
        self.isRent = None
        self.dateStartRent = None
        self.durationDaysRent = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Deal"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "id"

    def InsertDB(self):
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
                print(f"Error in InsertDB {sys.exc_info()}")
                return False
            finally:
                DB.DBClose(cursor)
