from Class.DB import DBAccess as DB


class Customer(DB):
    def __init__(self):
        self.idCusto = None

    @staticmethod
    def NameTable():
        return "Customer"

    @staticmethod
    def IdColumn():
        return "isCusto"
