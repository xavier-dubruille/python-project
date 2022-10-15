from Class.DB import DBAccess as DB
import sys

class Car(DB): 
    def __init__(self): 
        self.idCar = None
        self.dateStockCar = None
        self.dateTechControlCar = None
        self.prixCar = None
        self.nameBrand = None
        self.nameMotor = None
        self.nameType = None
        self.promoCar = None


    @staticmethod
    def NameTable():
        # Return the name table
        return "Car"

    @staticmethod
    def IdColumn():
        # Return the id column
        return "idCar"
    
    @classmethod
    def CarListStock(clss): 
        carList = []
        cursor = DB.DBCursor()
        if cursor != None:
            try:
                cursor.execute("SELECT idCar, STRFTIME('%d/%m/%Y', dateStockCar) as dateStockCar, dateTechControlCar, prixCar, nameBrand, nameMotor, \
                nameType, promoCar \
                FROM Car \
                NATURAL JOIN Brand \
                NATURAL JOIN Motor\
                NATURAL JOIN Type\
                where idCar NOT in (select idCar from deal)")
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    car = clss.LoadResults(cursor, row)
                    carList.append(car)
                return carList
            except:
                print("Error in CarListStock")
                print(sys.exc_info())
                return None 
            finally: 
                DB.DBClose(cursor)
