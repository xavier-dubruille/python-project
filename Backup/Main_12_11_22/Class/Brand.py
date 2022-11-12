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
        return "Brand"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idBrand"

    @staticmethod
    def GetIdFromName(name):
        cursor, dbConnection = DB.DBCursor()
        try:
            cursor.execute(f"SELECT {Brand.IdColumn()} FROM {Brand.NameTable()} WHERE nameBrand = '{name}'")
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO Brand (nameBrand) VALUES ('{name}')")
                dbConnection.commit()
                cursor.execute("SELECT last_insert_rowid()")
                return cursor.fetchone()
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
