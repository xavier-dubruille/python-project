import sqlite3 as sql
import sys


class DBAccess:
    @staticmethod
    def DBCursor():
        try:
            dbConnection = sql.connect("../Db/bambooConcess.db")
            return dbConnection.cursor(), dbConnection
        except sql.OperationalError:
            print(f"Db was not resolved {sys.exc_info()}")
            return None

    @staticmethod
    def DBClose(cursor):
        cursor.close()

    @classmethod
    def LoadWithId(cls, idNumber):
        cursor = cls.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute(f"SELECT * FROM {cls.NameTable()} WHERE {cls.IdColumn()} = {idNumber}")
                result = cursor.fetchone()
                return cls.LoadResults(cursor, result)

            except sql.OperationalError:
                print(f"Error in LoadWithId {sys.exc_info()}")
                return None

            finally:
                cls.DBClose(cursor)

    @classmethod
    def LoadResults(cls, cursor, data):
        newInstance = cls()
        counter = 0
        for columnName in cursor.description:
            setattr(newInstance, columnName[0], data[counter])
            counter += 1
        return newInstance

    @classmethod
    def GetAll(cls):
        cursor = cls.DBCursor()[0]
        instancesList = []
        if cursor is not None:
            try:
                cursor.execute(f"SELECT * FROM {cls.NameTable()}")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    newInstance = cls.LoadResults(cursor, row)
                    instancesList.append(newInstance)
                return instancesList
            except sql.OperationalError:
                print(f"Error in GetAll {sys.exc_info()}")
                return None

            finally:
                cls.DBClose(cursor)

    @classmethod
    def IsStockedWithId(cls, idNumber):
        cursor = cls.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute(f"SELECT * FROM {cls.NameTable()} WHERE {cls.IdColumn()} = {idNumber}")
                result = cursor.fetchone()
                if result:
                    return True
                return False
            except sql.OperationalError:
                print(f"Error in IsStocked {sys.exc_info()}")
                return None
            finally:
                cls.DBClose(cursor)

    @classmethod
    def Get(cls, idCar):
        cursor, dbConnection = cls.DBCursor()
        try:
            cursor.execute(f"SELECT * FROM {cls.NameTable()} LEFT JOIN Cars WHERE idCar = {idCar}")
            return cls.LoadResults(cursor, cursor.fetchone())
        except sql.OperationalError:
            print(f"Error in Get {sys.exc_info()}")
            return None
        finally:
            cls.DBClose(cursor)
