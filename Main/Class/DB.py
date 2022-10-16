import sqlite3 as sql
import sys

class DBAccess():

    @staticmethod
    def DBCursor():
        try: 
            dbConnection = sql.connect("./Db/bambooConcess.db")
            return dbConnection.cursor()
        except: 
            print("Db Could not be resolved")
            print(sys.exc_info())
            return None

    @staticmethod
    def DBClose(cursor):
        cursor.close()

    @classmethod
    def LoadWithId(clss, id):
        cursor = clss.DBCursor()
        if cursor != None: 
            try: 
                cursor.execute("SELECT * FROM %s WHERE %s = ?" % (clss.NameTable(), clss.IdColumn()), (id, ))
                result = cursor.fetchone()
                return clss.LoadResults(cursor, result)

            except: 
                print("Error in LoadWithId")
                print(sys.exc_info())
                return None
                
            finally:
                clss.DBClose(cursor)
    
    @classmethod
    def LoadResults(clss, cursor, data): 
        newInstance = clss()
        counter = 0
        columnsName = [description[0] for description in cursor.description]
        for columnName in columnsName:
            setattr(newInstance, columnName, data[counter])
            counter += 1
        return newInstance
    
    @classmethod
    def GetAll(clss):
        cursor = clss.DBCursor()
        instancesList = []
        if cursor != None: 
            try: 
                cursor.execute("SELECT * FROM %s" % (clss.NameTable()))
                resultsQuery = cursor.fetchall()
                for row in resultsQuery:
                    newInstance = clss.LoadResults(cursor, row)
                    instancesList.append(newInstance)
                return instancesList
            except: 
                print("Error in GetAll")
                print(sys.exc_info()[0])
                return None

            finally: 
                clss.DBClose(cursor)
    
    @classmethod
    def InsertDB(clss, dictData): 
        cursor = clss.DBCursor()
        if cursor != None:
            try:
                for key in dictData: 
                    print(key)
                # cursor.execute("Insert etc")
            except:
                print("Error in InsertDB")
            finally:
                clss.DBClose(cursor)
