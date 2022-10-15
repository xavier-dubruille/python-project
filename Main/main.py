from Class.Car import Car
import sqlite3 as sql
import tkinter as tk

def main():

    window = tk.Tk()
    window.title("Bamboo Concess")
    window.geometry("{}x{}+{}+{}".format(500, 500, 50,50))

    frameButtonQuit = tk.Frame(window)
    frameButtonQuit.grid()

    buttonQuit = tk.Button(frameButtonQuit, text = "Quit", command = lambda : window.destroy())
    buttonQuit.pack()

    dbConnection = sql.connect("./Db/bambooConcess.db")
    dbCursor = dbConnection.cursor()

    # dbCursor.execute("select idCar, firstNameCusto from deal natural join Customer where idCusto = 1")
    dbCursor.execute('select idDeal, substr(firstNameCusto, 1, 1) || \'.  \' || lastNameCusto as nameCusto,  idCar, nameBrand, nameMotor, nameType from Deal natural join Car natural join Brand natural join Motor natural join Type natural join customer where firstNameCusto = "Samuel"')
    array = dbCursor.fetchall()
    
    arrayLabelQuery = []
    count = 0
    for e in array:
        arrayLabelQuery.append(tk.Label(window, text = e))
        arrayLabelQuery[count].grid()
        count += 1
    
    dbCursor.close()

    window.mainloop()

if __name__ == "__main__":
    main()




