from Class.DB import DBAccess as DB


class Type(DB):
    def __init__(self):
        self.idType = None
        self.nameType = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Type"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idType"
