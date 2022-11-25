from Main.Class.DB import DBAccess as Db
from Main.Class.Car import Car
from Main.Class.Customer import Customer
import sqlite3 as sql
import sys


class Deal(Db):
    def __init__(self) -> None:
        self.id: int = 0
        self.id_car: any = None
        self.id_customer: any = None
        self.is_rent: bool = False
        self.date_start_rent: any = None
        self.duration_days_rent: any = None
        self.car: Car = Car()
        self.customer: Customer = Customer()

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the deal table in the database
        :returns: The name of the deal table in the database
        :rtype: str
        """
        return "deal"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the deal table in the database
        :returns: The name of the primary key in the deal table in the database
        :rtype: str
        """
        return "id"

    def insert_db(self) -> bool:
        """
        This function insert in the database a new deal
        :returns: True if the insert was correctly executed
        :rtype: bool
        """
        tuple_db: tuple = self.db_cursor()
        cursor: sql.dbapi2.Cursor = tuple_db[0]
        db_connection: sql.dbapi2.Connection = tuple_db[1]
        if cursor is not None:
            try:
                query: str = ""
                if self.is_rent:
                    query: str = f"INSERT INTO deal " \
                                 f"(is_rent, date_start_rent, duration_days_rent, id_car, id_customer) " \
                        f"VALUES ({self.is_rent}, {self.date_start_rent}, {self.duration_days_rent}, {self.id_car}, " \
                        f"{self.id_customer})"
                else:
                    query: str = f"INSERT INTO deal (is_rent, id_car, id_customer) " \
                        f"VALUES ({self.is_rent}, {self.id_car}, {self.id_customer})"
                cursor.execute(query)
                db_connection.commit()
                return True
            except sql.OperationalError:
                print(f"Error in InsertDBDeal {sys.exc_info()}")
            finally:
                self.db_close(cursor)
        return False

    @staticmethod
    def get_all() -> list | None:
        """
        This function get all the cars from the database
        :returns: A list of all the cars
        :rtype: list
        """
        cursor: sql.dbapi2.Cursor = Deal.db_cursor()[0]
        deal_list: list = []
        if cursor is not None:
            try:
                cursor.execute("SELECT * FROM deal ORDER BY id_car")
                results_query: list = cursor.fetchall()
                for row in results_query:
                    new_deal: Deal = Deal.load_results(cursor, row)
                    new_deal.car = Car.get_car(new_deal.id_car)
                    new_deal.customer = Customer.get_customer(new_deal.id_customer)
                    deal_list.append(new_deal)
                return deal_list
            except sql.OperationalError:
                print(f"Error in GetAllDeal {sys.exc_info()}")
            finally:
                Deal.db_close(cursor)
        return None
