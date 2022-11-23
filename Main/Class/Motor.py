from Class.DB import DBAccess as DB


class Motor(DB):
    def __init__(self) -> None:
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable() -> str:
        """
        This function returns the name of the motor table in the database.
        :returns: The name of the motor table in the database.
        :rtype: str
        """
        return "Motor"

    @staticmethod
    def IdColumn() -> str:
        """
        This function returns the primary key name in the motor table in the database.
        :returns: The name of the primary key in the motor table in the database.
        :rtype: str
        """
        return "id"
