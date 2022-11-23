from Class.DB import DBAccess as DB


class Type(DB):
    def __init__(self) -> None:
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the type table in the database
        :returns: The name of the type table in the database
        :rtype: str
        """
        return "Type"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the type table in the database
        :returns: The name of the primary key in the type table in the database
        :rtype: str
        """
        return "id"
