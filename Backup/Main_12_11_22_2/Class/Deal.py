from Class.DB import DBAccess as DB


class Deal(DB):
    def __init__(self):
        self.idCar = None
        self.idCustomer = None

    @staticmethod
    def NameTable():
        # Return the name table
        return "Deals"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idMotor"

