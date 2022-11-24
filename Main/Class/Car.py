import sqlite3 as sql
import sys

from Main.Class.Brand import Brand
from Main.Class.DB import DBAccess as Db
from Main.Class.Motor import Motor
from Main.Class.Type import Type


class Car(Db):
    def __init__(self) -> None:
        self.id: int = 0
        self.dateStock: str = ""
        self.dateTechControl: str = ""
        self.price: int = 0
        self.promo: int = 0
        self.idBrand: int = 0
        self.idType: int = 0
        self.idMotor: int = 0
        self.brand: Brand = Brand()
        self.motor: Motor = Motor()
        self.type: Type = Type()

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the car table in the database
        :returns: The name of the car table in the database
        :rtype: str
        """
        return "Car"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the car table in the database
        :returns: The name of the primary key in the car table in the database
        :rtype: str
        """
        return "idCar"

    @staticmethod
    def get_car_list() -> list | None:
        """
        This function get the cars in the database
        :returns: A list of cars from the database
        :rtype: list
        """
        car_list: list = []
        cursor: sql.dbapi2.Cursor = Db.db_cursor()[0]
        if cursor:
            try:
                query: str = "SELECT id, STRFTIME('%d/%m/%Y', dateStock) as dateStock, " \
                        "dateTechControl, price || '0' as price, promo FROM Car WHERE id " \
                        "NOT IN (select idCar FROM Deal WHERE isRent = 0) ORDER BY id"
                cursor.execute(query)
                results_query: list = cursor.fetchall()
                for row in results_query:
                    car = Car.load_results(cursor, row)
                    car.get_components()
                    car_list.append(car)
                return car_list
            except sql.OperationalError:
                print(f"Error in GetCarList {sys.exc_info()}")
            finally:
                Db.db_close(cursor)
        return None

    @staticmethod
    def car_free_places_stock() -> int | None:
        """
        This function check if there is free places in the stock for another car
        :returns: The number of free places in the stock
        :rtype: int
        """
        cursor: sql.dbapi2.Cursor = Db.db_cursor()[0]
        if cursor is not None:
            try:
                query: str = "SELECT count(*) FROM Car WHERE id NOT IN (SELECT id FROM Deal WHERE isRent = 0)"
                cursor.execute(query)
                return cursor.fetchone()[0]
            except sql.OperationalError:
                print(f"Error in CarFreePlacesStock {sys.exc_info()}")
            finally:
                Db.db_close(cursor)
        return None

    def insert_db(self) -> bool:
        """
        This function insert in the database a new car
        :returns: True if the insert was correctly executed
        :rtype: bool
        """
        tuple_db: tuple = self.db_cursor()
        cursor: sql.dbapi2.Cursor = tuple_db[0]
        db_connection: sql.dbapi2.Connection = tuple_db[1]
        if cursor is not None:
            try:
                query: str = f"INSERT INTO Car (dateTechControl, price, idBrand, idType, idMotor, promo) " \
                        f"VALUES ('{self.dateTechControl}', {self.price}, {self.idBrand},{self.idType}, " \
                        f"{self.idMotor}, {self.promo})"
                cursor.execute(query)
                db_connection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDBCar {sys.exc_info()}")
            finally:
                self.db_close(cursor)
        return False

    def remove_db(self) -> bool:
        """
        This function delete the car
        :returns: True if the deleting was correctly executed
        :rtype: bool
        """
        tuple_db: tuple = self.db_cursor()
        cursor: sql.dbapi2.Cursor = tuple_db[0]
        db_connection: sql.dbapi2.Connection = tuple_db[1]
        if cursor is not None:
            try:
                query: str = f"DELETE FROM Car WHERE id = {self.id}"
                cursor.execute(query)
                db_connection.commit()
                del self
                return True
            except sql.OperationalError:
                print(f"Error in RemoveCarDB {sys.exc_info()}")
            finally:
                Db.db_close(cursor)
        return False

    @staticmethod
    def get_car(id_car: int) -> object | None:
        """
        This function get a car in the database chosen by its id
        :param id_car: A integer number
        :type id_car: int
        :returns: An object car with all its components
        :rtype: object
        """
        cursor: sql.dbapi2.Cursor = Car.db_cursor()[0]
        if cursor is not None:
            try:
                query: str = f"SELECT id, STRFTIME('%d/%m/%Y', dateStock) as dateStock, dateTechControl, " \
                        f"price || '0' as price, promo FROM Car WHERE id = {id_car} "
                cursor.execute(query)
                new_car = Car.load_results(cursor, cursor.fetchone())
                new_car.get_components()
                return new_car
            except sql.OperationalError:
                print(f"Error in GetCar {sys.exc_info()}")
            finally:
                Car.db_close(cursor)
        return None

    def get_components(self) -> None:
        """
        This function add to the car its components from the database
        :returns: None
        :rtype: None
        """
        self.brand = Brand.get_car_component(self.id)
        self.motor = Motor.get_car_component(self.id)
        self.type = Type.get_car_component(self.id)
