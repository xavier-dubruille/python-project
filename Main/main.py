from Class.Car import Car
import sqlite3

def main():

    dbConnection = sqlite3.connect("./Db/bambooConcess.db")
    dbCursor = dbConnection.cursor()
    dbCursor.execute("SELECT * from Motor")
    array = dbCursor.fetchall()
    for e in array:
        print(e)
    dbCursor.close()
    
if __name__ == "__main__":
    main()