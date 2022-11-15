from Class.DB import DBAccess as DB


class Motor(DB):
    def __init__(self):
        self.id = 0
        self.name = ""

    @staticmethod
    def NameTable():
        # Return the name table
        return "Motor"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "id"
