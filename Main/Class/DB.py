import sqlite3 as sql
import sys


class DBAccess:
    @staticmethod
    def DBCursor() -> tuple:
        """
        This function get the connection and the cursor of the database
        :returns: The connection and the cursor of the database
        :rtype: tuple
        """
        try:
            dbConnection = sql.connect("../Db/bambooConcess.db")
            return dbConnection.cursor(), dbConnection
        except sql.OperationalError:
            print(f"Error in DBCursor {sys.exc_info()}")
            return ()

    @staticmethod
    def DBClose(cursor: sql.dbapi2.Connection) -> None:
        """
        This function close a connection of the database chosen by its cursor
        :param cursor: A SQLITE3 object
        :type cursor: sqlite3.dbapi2.Connection
        :returns: None
        :rtype: None
        """
        cursor.close()

    @classmethod
    def LoadWithId(cls, idNumber: int) -> object:
        """
        This function collect date of the class chosen by cls from the idNumber in the database
        :param idNumber: An integer number
        :type idNumber: int
        :returns: A cls object
        :rtype: object
        """
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
    def LoadResults(cls, cursor: sql.dbapi2.Connection, data: list) -> object:
        """
        This function create a new object with the data
        :param cursor: A SQLITE3 object
        :type cursor: sqlite3.dbapi2.Connection
        :param data: A list with all the data to create a new object
        :type data: list
        :returns: A new cls object
        :rtype: object
        """
        newInstance = cls()
        counter = 0
        for columnName in cursor.description:
            setattr(newInstance, columnName[0], data[counter])
            counter += 1
        return newInstance

    @classmethod
    def GetAll(cls) -> list:
        """
        This function get all the data from the database chosen by cls.
        :returns: A list of all the cls object from the database.
        :rtype: list
        """
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
        return []

    @classmethod
    def GetId(cls, name: str) -> int:
        """
        This function get the id from the row that the name matches
        :param name: A string of the name of a row in the database
        :type name: str
        :returns: The id of the row checked with the name
        :rtype: int
        """
        cursor, dbConnection = cls.DBCursor()
        if cursor and name:
            try:
                query = f"SELECT {cls.IdColumn()} FROM {cls.NameTable()} WHERE name = '{name}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if not result:
                    query = f"INSERT INTO {cls.NameTable()} (name) VALUES ('{name}')"
                    cursor.execute(query)
                    dbConnection.commit()
                    cursor.execute("SELECT last_insert_rowid()")
                    result = cursor.fetchone()
                return result[0]
            except sql.OperationalError:
                print(f"Error in GetId {sys.exc_info()}")
            finally:
                cls.DBClose(cursor)
        return 0

    @classmethod
    def GetCarComponent(cls, idCar: int) -> object:
        """
        This function get a component of a car chosen by its id
        :param idCar: An integer number matches a car
        :type idCar: int
        :returns: A new cls object
        :rtype: object
        """
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
