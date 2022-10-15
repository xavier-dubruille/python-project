from Class.Car import Car
import sqlite3
import tkinter

def main():

    window = tkinter.Tk()

    frameButtonQuit = tkinter.Frame(window)
    frameButtonQuit.grid()

    buttonQuit = tkinter.Button(frameButtonQuit, text = "Quit", command = lambda : window.destroy())
    buttonQuit.pack()

    dbConnection = sqlite3.connect("./Db/bambooConcess.db")
    dbCursor = dbConnection.cursor()

    dbCursor.execute("select idCar, firstNameCusto from deal natural join Customer where idCusto = 1")
    array = dbCursor.fetchall()
    
    count = 1
    for e in array:
        count +=1
    
    dbCursor.close()

    window.mainloop()

if __name__ == "__main__":
    main()