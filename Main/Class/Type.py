from Class.DB import DBAccess as DB
import sys

class Type(DB):
    def __init__(self): 
        self.idType = None
        self.nameType = None

    @classmethod
    def GetAllType(clss):
        cursor = DB.DBCursor()
        typeList = []
        if cursor != None: 
            try: 
                cursor.execute("SELECT * FROM Type")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    type = clss.LoadResults(cursor, row)
                    typeList.append(type)
                    return typeList
            except: 
                print("Error in GetAllType")
                print(sys.exc_info()[0])
                return None

            finally: 
                DB.DBClose(cursor)