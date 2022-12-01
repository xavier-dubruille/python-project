from Class.DB import DBAccess as DB
import sys
import sqlite3 as sql


class Motor(DB):
    def __init__(self):
        self.idMotor = None
        self.nameMotor = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Motors"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idMotor"

    @staticmethod
    def GetId(name):
        cursor, dbConnection = DB.DBCursor()
        try:
            cursor.execute(f"SELECT idMotor FROM Motors WHERE nameMotor = '{name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(
                    f"INSERT INTO Motors (nameMotor) VALUES ('{name}')")
                dbConnection.commit()
                cursor.execute("SELECT last_insert_rowid()")
                result = cursor.fetchone()[0]
            return result
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
