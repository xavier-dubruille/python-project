from Class.DB import DBAccess as DB


class Brand(DB):
    def __init__(self) -> None:
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the brand table in the database.
        :returns: The name of the brand table in the database.
        :rtype: str
        """
        # Return the name table
        return "Brand"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the brand table in the database.
        :returns: The name of the primary key in the brand table in the database.
        :rtype: str
        """
        return "id"
