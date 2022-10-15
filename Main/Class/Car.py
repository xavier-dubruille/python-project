from DB import DBAccess as DB

class Car(DB): 
    def __init__(self): 
        self.idCar = None
        self.stockDateCar = None
        self.techControlDateCar = None
        self.prixCar = None
        self.idBrand = None
        self.idMotor = None
        self.idType = None
        self.promoCar = None


    @staticmethod
    def NameTable():
        # Return the name table
        return "Car"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idCar"