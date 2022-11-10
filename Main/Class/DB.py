import sqlite3
import sqlite3 as sql
import sys


class DBAccess:

    @staticmethod
    def DBCursor():
        try:
            dbConnection = sql.connect("./Db/bambooConcess.db")
            return dbConnection.cursor(), dbConnection
        except sqlite3.OperationalError:
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
                cursor.execute("SELECT * FROM %s WHERE %s = %s" % (cls.NameTable(), cls.IdColumn(), idNumber))
                result = cursor.fetchone()
                return cls.LoadResults(cursor, result)

            except:
                print("Error in LoadWithId")
                print(sys.exc_info())
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
                cursor.execute("SELECT * FROM %s" % (cls.NameTable()))
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    newInstance = cls.LoadResults(cursor, row)
                    instancesList.append(newInstance)
                return instancesList
            except:
                print("Error in GetAll")
                print(sys.exc_info()[0])
                return None

            finally:
                cls.DBClose(cursor)

    @classmethod
    def IsStockedWithId(cls, idNumber):
        cursor = cls.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute("SELECT * FROM %s WHERE %s = %s" % (cls.NameTable(), cls.IdColumn(), idNumber))
                result = cursor.fetchone()
                if result:
                    return True
                return False
            except:
                print("Error in IsStocked")
                print(sys.exc_info())
                return None
            finally:
                cls.DBClose(cursor)
