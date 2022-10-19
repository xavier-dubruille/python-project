from Class.DB import DBAccess as DB
import sys

class Customer(DB):
    def __init__(self):
        self.idCusto = None
    
    def NameTable():
        return "Customer"

    def IdColumn():
        return "isCusto"