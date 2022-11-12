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
    def GetIdFromName(name):
        cursor, dbConnection = DB.DBCursor()
        try:
            cursor.execute(f"SELECT {Motor.IdColumn()} FROM {Motor.NameTable()} WHERE nameMotor = '{name}'")
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO {Motor.NameTable()} (nameMotor) VALUES ('{name}')")
                dbConnection.commit()
                cursor.execute("SELECT last_insert_rowid()")
                return cursor.fetchone()
        except sql.OperationalError:
            print(f"Error in GetIdFromName {sys.exc_info()}")
            return None
        finally:
            DB.DBClose(cursor)
