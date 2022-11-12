from Class.DB import DBAccess as DB


class Customer(DB):
    def __init__(self):
        self.id = None
        self.firstName = None
        self.lastName = None
        self.phone = None
        self.mail = None
        self.address = None

    @staticmethod
    def NameTable():
        return "Customer"

    @staticmethod
    def IdColumn():
        return "id"
