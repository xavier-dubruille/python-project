from Main.Class.database import DBAccess as Db


class Brand(Db):
    def __init__(self) -> None:
        """
        It creates a new object Brand
        """
        self.id: int = 0
        self.name: str = ""

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the brand table in the database
        :returns: The name of the brand table in the database
        """
        return "brand"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the brand table in the database
        :returns: The name of the primary key in the brand table in the database
        """
        return "id"
