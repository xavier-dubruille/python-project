import sqlite3 as sql
import sys


class DBAccess:
    @staticmethod
    def DBCursor() -> tuple:
        try:
            dbConnection = sql.connect("../Db/bambooConcess.db")
            return dbConnection.cursor(), dbConnection
        except sql.OperationalError:
            print(f"Error in DBCursor {sys.exc_info()}")
            return None

    @staticmethod
    def DBClose(cursor: object) -> None:
        cursor.close()

    @classmethod
    def LoadWithId(cls, idNumber: int) -> object:
        cursor = cls.DBCursor()[0]
        if cursor is not None:
            try:
                cursor.execute(f"SELECT * FROM {cls.NameTable()} WHERE {cls.IdColumn()} = {idNumber}")
                result = cursor.fetchone()
                return cls.LoadResults(cursor, result)
            except sql.OperationalError:
                print(f"Error in LoadWithId {sys.exc_info()}")
            finally:
                cls.DBClose(cursor)
        return None

    @classmethod
    def LoadResults(cls, cursor: object, data: list) -> object:
        newInstance = cls()
        counter = 0
        for columnName in cursor.description:
            setattr(newInstance, columnName[0], data[counter])
            counter += 1
        return newInstance

    @classmethod
    def GetAll(cls) -> list:
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
                print(f"Error in GetAllDB {sys.exc_info()}")
            finally:
                cls.DBClose(cursor)
        return None

    @classmethod
    def GetId(cls, name: str) -> int:
        cursor, dbConnection = cls.DBCursor()
        if cursor is not None:
            try:
                query = f"SELECT {cls.IdColumn()} FROM {cls.NameTable()} WHERE name = '{name}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if not result:
                    query = f"INSERT INTO {cls.NameTable()} (name) VALUES ('{name}')"
                    cursor.execute(query)
                    dbConnection.commit()
                    cursor.execute("SELECT last_insert_rowid()")
                    result = cursor.fetchone()[0]
                return result
            except sql.OperationalError:
                print(f"Error in GetId {sys.exc_info()}")
            finally:
                cls.DBClose(cursor)
        return None

    @classmethod
    def GetCarComponent(cls, idCar: int) -> object:
        cursor, dbConnection = cls.DBCursor()
        if cursor is not None:
            try:
                query = f"SELECT {cls.NameTable()}.id, {cls.NameTable()}.name FROM {cls.NameTable()} JOIN Car " \
                        f"ON {cls.NameTable()}.{cls.IdColumn()} = Car.id{cls.NameTable()} WHERE Car.id = {idCar}"
                cursor.execute(query)
                return cls.LoadResults(cursor, cursor.fetchone())
            except sql.OperationalError:
                print(f"Error in GetCarComponent {sys.exc_info()}")
            finally:
                cls.DBClose(cursor)
        return None
