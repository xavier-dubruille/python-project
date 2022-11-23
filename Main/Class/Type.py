from Class.DB import DBAccess as DB


class Type(DB):
    def __init__(self) -> None:
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable() -> str:
        # Return the name table
        return "Type"

    @staticmethod
    def IdColumn() -> str:
        # Return the id column
        return "id"
