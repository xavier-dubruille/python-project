from Class.DB import DBAccess as DB


class Motor(DB):
    def __init__(self) -> None:
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable() -> str:
        # Return the name table
        return "Motor"

    @staticmethod
    def IdColumn() -> str:
        # Return the id column
        return "id"
