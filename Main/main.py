from Class.Car import Car
import sqlite3

def main():

    dbConnection = sqlite3.connect("./Db/bambooConcess.db")
    dbCursor = dbConnection.cursor()

    dbCursor.execute("select idCar, firstNameCusto from deal natural join Customer where idCusto = 1")
    array = dbCursor.fetchall()
    for e in array:
        print(e)
    dbCursor.close()
    
if __name__ == "__main__":
    main()