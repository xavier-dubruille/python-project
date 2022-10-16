from Class.DB import DBAccess as DB
import sys

class Brand(DB):
    def __init__(self): 
        self.idMotor = None
        self.nameMotor = None

    @classmethod
    def GetAllMotor(clss):
        cursor = DB.DBCursor()
        motorList = []
        if cursor != None: 
            try: 
                cursor.execute("SELECT * FROM Motor")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    motor = clss.LoadResults(cursor, row)
                    motorList.append(motor)
                    return motorList
            except: 
                print("Error in GetAllBrand")
                print(sys.exc_info()[0])
                return None

            finally: 
                DB.DBClose(cursor)