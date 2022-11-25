from Main.Class.DB import DBAccess as Db


class Motor(Db):
    def __init__(self) -> None:
        self.id: int = 0
        self.name: str = ""

    @staticmethod
    def name_table() -> str:
        """
        This function returns the name of the motor table in the database
        :returns: The name of the motor table in the database
        :rtype: str
        """
        return "motor"

    @staticmethod
    def id_column() -> str:
        """
        This function returns the primary key name in the motor table in the database
        :returns: The name of the primary key in the motor table in the database
        :rtype: str
        """
        return "id"
