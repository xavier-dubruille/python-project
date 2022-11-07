from Class.DB import DBAccess as DB


class Brand(DB):
    def __init__(self): 
        self.idBrand = None
        self.nameBrand = None
    
    @staticmethod
    def NameTable():
        # Return the name table
        return "Brand"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idDeal"
    
   
