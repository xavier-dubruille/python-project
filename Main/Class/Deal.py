from Class.DB import DBAccess as DB


class Deal(DB):
    def __init__(self):
        self.idCar = None
        self.idCustomer = None
        self.isRent = None
        self.dateStartRent = None
        self.durationDaysRent = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Deal"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "id"
