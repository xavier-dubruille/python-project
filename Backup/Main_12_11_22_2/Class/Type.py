from Class.DB import DBAccess as DB
import sqlite3 as sql
import sys


class Type(DB):
    def __init__(self):
        self.idType = None
        self.nameType = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Types"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idType"

    @staticmethod
    def GetId(name):
        cursor, dbConnection = DB.DBCursor()
        try:
            cursor.execute(f"SELECT idType FROM Types WHERE nameType = '{name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(
                    f"INSERT INTO Types (nameType) VALUES ('{name}')")
                dbConnection.commit()
                cursor.execute("SELECT last_insert_rowid()")
                result = cursor.fetchone()[0]
            return result
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
