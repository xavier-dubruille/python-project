from Main.Class.DB import DBAccess as Db


class Brand(Db):
    def __init__(self) -> None:
        self.id: int = 0
        self.name: str = ""

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the brand table in the database
        :returns: The name of the brand table in the database
        :rtype: str
        """
        return "brand"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the brand table in the database
        :returns: The name of the primary key in the brand table in the database
        :rtype: str
        """
        return "id"
