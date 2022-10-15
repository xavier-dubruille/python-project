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
        arrayLabelQuery[count].pack()
        count += 1
    cursor.close()


def main():

    window = tk.Tk()
    window.title("Bamboo Concess")
    window.attributes('-fullscreen', True)

    window.columnconfigure(0, weight = 2)
    window.columnconfigure(1, weight = 3)
    window.columnconfigure(2, weight = 1)
    window.columnconfigure(3, weight = 1)

    for i in range(6):
        window.rowconfigure(i, weight = 1)
    window.rowconfigure(7, weight = 2)

    frameReservation = tk.Frame(window, highlightthickness=2, highlightbackground = "black")
    frameReservation.grid(column = 0, row = 0, rowspan = 3, sticky = "wesn")

    frameStock = tk.Frame(window, highlightthickness=2, highlightbackground = "black")
    frameStock.grid(column = 1, row = 1, rowspan=2, sticky="wesn")

    frameStockAjout = tk.Frame(window, highlightthickness=2, highlightbackground = "black")
    frameStockAjout.grid(column = 2, row = 2, sticky = "wesn")

    frameButtonQuit = tk.Frame(window, highlightthickness=2, highlightbackground = "black")
    frameButtonQuit.grid(column = 3, row = 0, sticky = "wesn")

    buttonQuit = tk.Button(frameButtonQuit, text = "Exit", command = window.destroy)
    buttonQuit.pack()

    ExecuteQuery("select prixCar as Prix, nameBrand as Brand, nameMotor as Motor, nameType as Type, stockDateCar as DateStock, techControlDateCar as ControlDate, promoCar as Promotion from car NATURAL join Brand NATURAL join Motor NATURAL join Type", frameStock)

    window.mainloop()

if __name__ == "__main__":
    main()




