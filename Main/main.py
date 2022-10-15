from Class.Car import Car
import sqlite3 as sql
import tkinter as tk

def ExecuteQuery(query, frameResults): 
    dbConnection = sql.connect("./Db/bambooConcess.db")
    cursor = dbConnection.cursor()

    cursor.execute(query) 

    arrayLabelQuery = []
    count = 0
    for e in cursor.fetchall():
        arrayLabelQuery.append(tk.Label(frameResults, text = e))
        arrayLabelQuery[count].grid()
        count += 1
    cursor.close()


def main():

    window = tk.Tk()
    window.title("Bamboo Concess")
    window.geometry("{}x{}+{}+{}".format(500, 500, 50,50))

    frameButtonQuit = tk.Frame(window)
    frameButtonQuit.grid()

    buttonQuit = tk.Button(frameButtonQuit, text = "Quit", command = window.destroy)
    buttonQuit.pack()


    # dbCursor.execute("select idCar, firstNameCusto from deal natural join Customer where idCusto = 1")
    buttonQuery = tk.Button(window, text = "query", command = lambda : ExecuteQuery('select idDeal, substr(firstNameCusto, 1, 1) || \'.  \' || lastNameCusto as nameCusto,  idCar, nameBrand, nameMotor, nameType from Deal natural join Car natural join Brand natural join Motor natural join Type natural join customer where firstNameCusto = "Samuel"', window))
    buttonQuery.grid()

    window.mainloop()

if __name__ == "__main__":
    main()




