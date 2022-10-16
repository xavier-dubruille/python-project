from Class.DB import DBAccess as DB
import sys

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
    
    @classmethod
    def GetIdWithName(clss, name):
        cursor = clss.DBCursor()
        if cursor != None:
            try:
                cursor.execute("SELECT idBrand FROM Brand WHERE nameBrand = %s" % (name))
                cursor.fetchone()

            except:
                print("Error in GetIdWithNameBrand")
                print(sys.exc_info())
                return None
            finally:
                clss.DBClose(cursor)
