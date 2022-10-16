from Class.DB import DBAccess as DB
import sys

class Motor(DB):
    def __init__(self): 
        self.idMotor = None
        self.nameMotor = None
    
    @staticmethod
    def NameTable():
        # Return the name table
        return "Motor"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idMotor"