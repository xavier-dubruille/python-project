from Class.DB import DBAccess as DB
import sys

class Brand(DB):
    def __init__(self): 
        self.idBrand = None
        self.nameBrand = None

    @classmethod
    def GetAllBrand(clss):
        cursor = DB.DBCursor()
        brandList = []
        if cursor != None: 
            try: 
                cursor.execute("SELECT * FROM Brand")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    brand = clss.LoadResults(cursor, row)
                    brandList.append(brand)
                    return brandList
            except: 
                print("Error in GetAllBrand")
                print(sys.exc_info()[0])
                return None

            finally: 
                DB.DBClose(cursor)