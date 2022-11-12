from Class.DB import DBAccess as DB
import sqlite3 as sql
import sys


class Brand(DB):
    def __init__(self):
        self.idBrand = None
        self.nameBrand = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Brands"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idBrand"

    @staticmethod
    def GetId(name):
        cursor, dbConnection = DB.DBCursor()
        try:
            cursor.execute(f"SELECT idBrand FROM Brands WHERE nameBrand = '{name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(
                    f"INSERT INTO Brands (nameBrand) VALUES ('{name}')")
                dbConnection.commit()
                cursor.execute("SELECT last_insert_rowid()")
                result = cursor.fetchone()[0]
            return result
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
