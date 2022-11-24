from Main.Class.DB import DBAccess as Db


class Type(Db):
    def __init__(self) -> None:
        self.id: int = 0
        self.name: str = ""

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the type table in the database
        :returns: The name of the type table in the database
        :rtype: str
        """
        return "Type"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the type table in the database
        :returns: The name of the primary key in the type table in the database
        :rtype: str
        """
        return "id"
