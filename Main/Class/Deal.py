from Class.DB import DBAccess as DB
import sys

class Deal(DB):
    def __init__(self): 
        self.idCar = None
        self.idCusto = None
    
    @staticmethod
    def NameTable():
        # Return the name table
        return "Deal"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idMotor"