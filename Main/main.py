import tkinter.font as font
from tkinter import *
from tkcalendar import DateEntry as tkCal
import math
import re
from Main.Class.Brand import Brand
from Main.Class.Customer import Customer
from Main.Class.Deal import Deal
from Main.Class.Motor import Motor
from Main.Class.Type import Type
from Main.Class.Car import Car


def check_number_input(string: str, minimum: int = None, maximum: int = None) -> bool:
    """
    This function check if the string is convertible into integer
    If minimum and/or maximum are given, check also if it's between them
    :param string: A string that will be checked for a number
    :type string: str
    :param minimum: An integer number
    :type string: int
    :param maximum: An integer number
    :type string: int
    :returns: True if the string is convertible to digit and respect the minimum and the maximum
    :rtype: bool
    """
    if not string.isdigit():
        return False
    if maximum is not None and minimum is not None:
        if maximum >= int(string) >= minimum:
            return True
        return False
    elif maximum is not None:
        if maximum >= int(string):
            return True
        return False
    elif minimum is not None:
        if int(string) >= minimum:
            return True
        return False
    return True


class Application:
    # TODO : change to snake case the db
    def __init__(self) -> None:
        self.window: Tk | None = None
        self.buttonAddCar: Button | None = None
        self.buttonDeal: Button | None = None
        self.buttonReservation: Button | None = None
        self.buttonHistory: Button | None = None
        self.buttonStock: Button | None = None
        self.buttonAddCustomer: Button | None = None
        self.frameButtons: Frame | None = None
        self.frameDetails: Frame | None = None
        self.frameDisplay: Frame | None = None
        self.frameSort: Frame | None = None
        self.labelColumn: Label | None = None
        self.labelDetails: Label | None = None
        self.spaceDisplay: int = 4
        self.rowNumberRent: int = 5
        self.rowNumberSelling: int = 3
        self.rowNumberAddCar: int = 7
        self.rowNumberAddCustomer: int = 6
        self.lcmRowNumberDisplay: int = math.lcm(self.rowNumberRent, self.rowNumberSelling, self.rowNumberAddCar,
                                                 self.rowNumberAddCustomer)
        self.printDetails: str = ""
        self.police: str = "courier 15"
        self.title: str = "Bamboo Concess"
        self.rentList: list = []
        self.carListFree: list = []
        self.carListStock: list = []
        self.dealList: list = []
        self.set_or_reset_car_lists()
        self.brandList: list = Brand.get_all()
        self.motorList: list = Motor.get_all()
        self.typeList: list = Type.get_all()
        self.customerList: list = Customer.get_all()
        self.create_basic_window()

    # The main display function for the application.
    def create_basic_window(self) -> None:
        self.window: Tk = Tk()

        self.window.title(self.title)
        self.window.attributes('-fullscreen', True)
        self.window.option_add("*Font", self.police)
        self.window.config(bg="white")

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=1)

        for i in range(6):
            self.window.rowconfigure(i, weight=1)
        self.window.rowconfigure(7, weight=2)

        self.frameButtons: Frame = Frame(self.window)
        self.frameButtons.grid(column=0, row=1, rowspan=5, sticky=NSEW)
        for i in range(6):
            self.frameButtons.rowconfigure(i, weight=1)
        self.frameButtons.columnconfigure(0, weight=1)

        self.buttonStock: Button = Button(self.frameButtons, text="Display Stock",
                                          command=self.display_window_stock)
        self.buttonStock.grid(column=0, row=0, sticky=NSEW)
        self.buttonHistory: Button = Button(self.frameButtons, text="Display History",
                                            command=self.display_window_history)
        self.buttonHistory.grid(column=0, row=1, sticky=NSEW)
        self.buttonReservation: Button = Button(self.frameButtons, text="Rent a car",
                                                command=self.display_window_rent)
        self.buttonReservation.grid(column=0, row=2, sticky=NSEW)
        self.buttonDeal: Button = Button(self.frameButtons, text="Make a deal",
                                         command=self.display_window_selling)
        self.buttonDeal.grid(column=0, row=3, sticky=NSEW)
        self.buttonAddCar: Button = Button(self.frameButtons, text="Add a car in stock",
                                           command=self.display_window_add_car)
        self.buttonAddCar.grid(column=0, row=4, sticky=NSEW)
        self.buttonAddCustomer: Button = Button(self.frameButtons, text="Add a customer",
                                                command=self.display_window_add_customer)
        self.buttonAddCustomer.grid(column=0, row=5, sticky=NSEW)

        frame_title: Frame = Frame(self.window, highlightthickness=2, highlightbackground="black")
        frame_title.grid(column=1, row=0, sticky=NSEW)
        frame_title.rowconfigure(0, weight=1)
        frame_title.columnconfigure(0, weight=1)
        label_title: Label = Label(frame_title, text=self.title)
        label_title.grid(column=0, row=0, sticky=NSEW)

        self.frameSort: Frame = Frame(self.window, highlightthickness=1, highlightbackground="black")
        self.frameSort.grid(column=1, row=1, sticky=NSEW)
        self.frameSort.pack_propagate(False)
        self.frameSort.grid_propagate(False)

        self.frameDisplay: Frame = Frame(self.window)
        self.frameDisplay.grid(column=1, row=2, rowspan=6, sticky=NSEW)
        for i in range(self.lcmRowNumberDisplay):
            self.frameDisplay.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.frameDisplay.grid_columnconfigure(i, weight=1)
        self.frameDisplay.pack_propagate(False)
        self.frameDisplay.grid_propagate(False)

        self.frameDetails: Frame = Frame(self.window, highlightthickness=2, highlightbackground="black")
        self.frameDetails.grid(column=2, row=1, rowspan=7, sticky=NSEW)
        self.frameDetails.grid_propagate(False)
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight=1)
        self.frameDetails.columnconfigure(0, weight=1)
        label_title_details: Label = Label(self.frameDetails, text="DETAILS", anchor="s",
                                           font=self.police + " underline")
        label_title_details.grid(column=0, row=0, sticky='wesn')
        self.labelDetails: Label = Label(self.frameDetails, text=self.printDetails, justify="left", anchor='nw')
        self.labelDetails.grid(column=0, row=1, sticky=NSEW)

        frame_exit: Frame = Frame(self.window)
        frame_exit.grid(column=2, row=0, sticky=NSEW)
        frame_exit.rowconfigure(0, weight=1)
        frame_exit.columnconfigure(0, weight=1)
        button_exit: Button = Button(frame_exit, text="Exit", command=self.window.destroy,
                                     font=font.Font(family='Helvetica', size=15, weight='bold'))
        button_exit.grid(column=0, row=0, sticky=NSEW)

        self.display_window_stock()
        self.window.mainloop()

    # It shows you which car you have in your stock. It is displayed by default.
    def display_window_stock(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonStock["state"] = DISABLED

        self.reset_display_and_sort_frames()

        str_list: list = ["Id", "Brand", "Type", "Price (€)", "Rented"]
        space_dict: dict = {
            str_list[0]: len(str(max(self.carListStock, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay,
            str_list[1]: len(max(self.carListStock, key=lambda x: len(x.brand.name)).brand.name) + self.spaceDisplay,
            str_list[2]: len(max(self.carListStock, key=lambda x: len(x.type.name)).type.name) + self.spaceDisplay,
            str_list[3]: len(max(self.carListStock, key=lambda x: len(x.price)).price) + self.spaceDisplay
        }

        title_column: str = f"{str_list[0]}" + " " * (space_dict[str_list[0]] - len(f"{str_list[0]}")) + \
                            f"{str_list[1]}" + " " * (space_dict[str_list[1]] - len(f"{str_list[1]}")) + \
                            f"{str_list[2]}" + " " * (space_dict[str_list[2]] - len(f"{str_list[2]}")) + \
                            f"{str_list[3]}" + " " * (space_dict[str_list[2]] - len(f"{str_list[2]}")) + \
                            f"{str_list[4]}"

        label_title_column: Label = Label(self.frameDisplay, text=title_column)
        label_title_column.pack(anchor=NW)

        frame_list_box_scroll: Frame = Frame(self.frameDisplay)
        frame_list_box_scroll.pack(expand=True, fill=BOTH, anchor=W)

        scrollbar: Scrollbar = Scrollbar(frame_list_box_scroll)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox_stock: Listbox = Listbox(frame_list_box_scroll)
        listbox_stock.pack(expand=True, fill=BOTH, anchor=W)

        for car in self.carListStock:
            rented: str = ""
            for deal in self.rentList:
                if deal.idCar == car.id:
                    rented: str = "Rented"
                    break
            listbox_stock.insert(END,
                                 f"{str(car.id):{space_dict[str_list[0]]}}"
                                 f"{car.brand.name:{space_dict[str_list[1]]}}"
                                 f"{car.type.name:{space_dict[str_list[2]]}}"
                                 f"{car.price:{space_dict[str_list[3]]}}"
                                 f"{rented}")
            listbox_stock.bind('<<ListboxSelect>>', self.display_details_stock)

        listbox_stock.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listbox_stock.yview)

    # When you click a row to show more information about the car you selected.
    def display_details_stock(self, event: Event) -> None:
        car: Car = self.carListStock[event.widget.curselection()[0]]
        self.printDetails: str = f"Brand : {car.brand.name}\nType : {car.type.name}\nMotor : {car.motor.name}\n" \
                                 f"Price : {car.price}€\nPromo : {car.promo}%\nIn stock since : {car.dateStock}\n" \
                                 f"Next control : {car.dateTechControl}"
        self.labelDetails.configure(text=self.printDetails)

    # It will show you which car you sell.
    def display_window_history(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonHistory["state"] = DISABLED

        self.reset_display_and_sort_frames()

        if not self.dealList:
            listbox_history: Listbox = Listbox(self.frameDisplay)
            listbox_history.pack(expand=True, fill=BOTH)
            listbox_history.insert(END, "There is no cars in this category")

        else:
            str_list: list = ["Id", "Brand", "Type", "Price (€)", "Customer"]
            space_dict: dict = {
                str_list[0]: len(str(
                    max(self.dealList, key=lambda x: len(str(x.car.id))).car.id)) + self.spaceDisplay,
                str_list[1]: len(
                    max(self.dealList, key=lambda x: len(x.car.brand.name)).car.brand.name) + self.spaceDisplay,
                str_list[2]: len(
                    max(self.dealList, key=lambda x: len(x.car.type.name)).car.type.name) + self.spaceDisplay,
                str_list[3]: len(
                    max(self.dealList, key=lambda x: len(x.car.price)).car.price) + self.spaceDisplay
            }

            title_column: str = f"{str_list[0]}" + " " * (space_dict[str_list[0]] - len(f"{str_list[0]}")) + \
                                f"{str_list[1]}" + " " * (space_dict[str_list[1]] - len(f"{str_list[1]}")) + \
                                f"{str_list[2]}" + " " * (space_dict[str_list[2]] - len(f"{str_list[2]}")) + \
                                f"{str_list[3]}" + " " * (space_dict[str_list[3]] - len(f"{str_list[3]}")) + \
                                f"{str_list[4]}"

            label_title: Label = Label(self.frameDisplay, text=title_column, anchor="w")
            label_title.pack(anchor=W)

            frame_list_box_scroll: Frame = Frame(self.frameDisplay)
            frame_list_box_scroll.pack(expand=True, fill=BOTH)

            scrollbar: Scrollbar = Scrollbar(frame_list_box_scroll)
            scrollbar.pack(side=RIGHT, fill=Y)

            listbox_history: Listbox = Listbox(frame_list_box_scroll)
            listbox_history.pack(expand=True, fill=BOTH)

            for deal in self.dealList:
                listbox_history.insert(END,
                                       f"{str(deal.car.id):{space_dict[str_list[0]]}}"
                                       f"{deal.car.brand.name:{space_dict[str_list[1]]}}"
                                       f"{deal.car.type.name:{space_dict[str_list[2]]}}"
                                       f"{deal.car.price:{space_dict[str_list[3]]}}"
                                       f"{deal.customer.firstName[0]}.{deal.customer.lastName}")
                listbox_history.bind('<<ListboxSelect>>', self.display_details_history)

            listbox_history.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=listbox_history.yview)

    # When you click a row to show more information about the car you selected.
    def display_details_history(self, event: Event) -> None:
        for i in range(2):
            self.frameDetails.rowconfigure(i, weight=1)
        self.frameDetails.columnconfigure(0, weight=1)

        deal: Deal = self.dealList[event.widget.curselection()[0]]
        self.printDetails: str = f"Brand : {deal.car.brand.name}\nType : {deal.car.type.name}\n" \
                                 f"Motor : {deal.car.motor.name}\nPrice : {deal.car.price}€\n" \
                                 f"Promo : {deal.car.promo}%\nIn stock since : {deal.car.dateStock}\n" \
                                 f"Next control {deal.car.dateTechControl}\n" \
                                 f"The customer is : {deal.customer.firstName} {deal.customer.lastName}"
        self.labelDetails.configure(text=self.printDetails)

    # It will help you to change the reservation's status for a particular car.
    # 5
    def display_window_rent(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonReservation["state"] = DISABLED
        self.reset_display_and_sort_frames()
        rowspan: int = int(self.lcmRowNumberDisplay / self.rowNumberRent)
        if not self.carListFree:
            label_no_free_places: Label = Label(self.frameDisplay, text="No car left for renting.")
            label_no_free_places.pack()

        else:
            raw_deal: Deal = Deal()
            raw_deal.idCar = StringVar()
            raw_deal.idCustomer = StringVar()
            raw_deal.dateStartRent = StringVar()
            raw_deal.durationDaysRent = StringVar()
            raw_deal.isRent = 1

            label_id_car: Label = Label(self.frameDisplay, text="Car id : ")
            label_id_car.grid(column=0, row=0, rowspan=rowspan, sticky=NSEW)
            dropdown_car_id: OptionMenu = OptionMenu(self.frameDisplay, raw_deal.idCar,
                                                     *map(lambda x: f"{x.id} price : {x.price} promo : {x.promo}",
                                                          self.carListFree))
            dropdown_car_id.grid(column=1, row=0, rowspan=rowspan, sticky=NSEW)

            label_id_customer: Label = Label(self.frameDisplay, text="Customer id : ")
            label_id_customer.grid(column=0, row=rowspan, rowspan=rowspan, sticky=NSEW)
            dropdown_id_customer: OptionMenu = OptionMenu(self.frameDisplay, raw_deal.idCustomer,
                                                          *map(lambda x: f"{x.id} {x.firstName[0]}.{x.lastName}",
                                                               self.customerList))
            dropdown_id_customer.grid(column=1, row=rowspan, rowspan=rowspan, sticky=NSEW)

            label_date_start_rent: Label = Label(self.frameDisplay, text="Date of the rent : ")
            label_date_start_rent.grid(column=0, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)
            entry_date_start_rent: tkCal = tkCal(self.frameDisplay, textvariable=raw_deal.dateStartRent, locale='fr_BE',
                                                 date_pattern="dd/mm/yyyy")
            entry_date_start_rent.grid(column=1, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)

            label_duration_days_rent: Label = Label(self.frameDisplay, text="Duration days of the rent : ")
            label_duration_days_rent.grid(column=0, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)
            entry_duration_days_rent: Entry = Entry(self.frameDisplay, textvariable=raw_deal.durationDaysRent)
            entry_duration_days_rent.grid(column=1, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)

            button_rent_a_car: Button = Button(self.frameDisplay, text="Make the rent",
                                               command=lambda: self.verify_deal(raw_deal))
            button_rent_a_car.grid(column=1, row=rowspan * 4, rowspan=rowspan, sticky=NSEW)

    # It will help you to sell a particular car.
    # 3
    def display_window_selling(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonDeal["state"] = DISABLED
        self.reset_display_and_sort_frames()
        rowspan: int = int(self.lcmRowNumberDisplay / self.rowNumberSelling)

        if self.carListFree:
            raw_deal: Deal = Deal()
            raw_deal.idCar = StringVar()
            raw_deal.idCustomer = StringVar()
            raw_deal.isRent = 0

            label_car_id: Label = Label(self.frameDisplay, text="Car id : ")
            label_car_id.grid(column=0, row=0, rowspan=rowspan, sticky=NSEW)
            dropdown_car_id: OptionMenu = OptionMenu(self.frameDisplay, raw_deal.idCar,
                                                     *map(lambda x: f"{x.id} price : {x.price} promo : {x.promo}",
                                                          self.carListFree))
            dropdown_car_id.grid(column=1, row=0, rowspan=rowspan, sticky=NSEW)

            label_id_customer: Label = Label(self.frameDisplay, text="Customer id : ")
            label_id_customer.grid(column=0, row=rowspan, rowspan=rowspan, sticky=NSEW)
            dropdown_id_customer: OptionMenu = OptionMenu(self.frameDisplay, raw_deal.idCustomer,
                                                          *map(lambda x: f"{x.id} {x.firstName[0]}.{x.lastName}",
                                                               self.customerList))
            dropdown_id_customer.grid(column=1, row=rowspan, rowspan=rowspan, sticky=NSEW)

            button_make_deal: Button = Button(self.frameDisplay, text="Make the deal",
                                              command=lambda: self.verify_deal(raw_deal))
            button_make_deal.grid(column=1, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)

        else:
            label_no_free_places: Label = Label(self.frameDisplay, text="No car left for selling.")
            label_no_free_places.pack()

    # This menu will help you to add a new car in your stock with a form.
    # 7
    def display_window_add_car(self) -> None:
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonAddCar["state"] = DISABLED
        self.reset_display_and_sort_frames()
        rowspan: int = int(self.lcmRowNumberDisplay / self.rowNumberAddCar)

        if Car.car_free_places_stock() <= 40:
            raw_car: dict = {
                "nameBrand": StringVar(),
                "nameType": StringVar(),
                "nameMotor": StringVar(),
                "price": StringVar(),
                "promo": StringVar(),
                "dateTechControl": StringVar()
            }

            label_brand: Label = Label(self.frameDisplay, text="Brand : ")
            label_brand.grid(column=0, row=0, rowspan=rowspan, sticky=NSEW)
            entry_brand: Entry = Entry(self.frameDisplay, textvariable=raw_car["nameBrand"])
            entry_brand.grid(column=1, row=0, rowspan=rowspan, sticky=NSEW)

            label_type: Label = Label(self.frameDisplay, text="Type : ")
            label_type.grid(column=0, row=rowspan, rowspan=rowspan, sticky=NSEW)
            entry_type: Entry = Entry(self.frameDisplay, textvariable=raw_car["nameType"])
            entry_type.grid(column=1, row=rowspan, rowspan=rowspan, sticky=NSEW)

            label_motor: Label = Label(self.frameDisplay, text="Motor : ")
            label_motor.grid(column=0, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)
            entry_type: Entry = Entry(self.frameDisplay, textvariable=raw_car["nameMotor"])
            entry_type.grid(column=1, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)

            label_next_control: Label = Label(self.frameDisplay, text="Next tech control :")
            label_next_control.grid(column=0, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)
            entry_next_control: tkCal = tkCal(self.frameDisplay, textvariable=raw_car["dateTechControl"],
                                              locale='fr_BE',
                                              date_pattern="dd/mm/yyyy")
            entry_next_control.grid(column=1, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)

            label_price: Label = Label(self.frameDisplay, text="Price : ")
            label_price.grid(column=0, row=rowspan * 4, rowspan=rowspan, sticky=NSEW)
            entry_price: Entry = Entry(self.frameDisplay, textvariable=raw_car["price"])
            entry_price.grid(column=1, row=rowspan * 4, rowspan=rowspan, sticky=NSEW)

            label_promo: Label = Label(self.frameDisplay, text="Promo : ")
            label_promo.grid(column=0, row=rowspan * 5, rowspan=rowspan, sticky=NSEW)
            entry_promo: Entry = Entry(self.frameDisplay, textvariable=raw_car["promo"])
            entry_promo.grid(column=1, row=rowspan * 5, rowspan=rowspan, sticky=NSEW)

            button_add_car: Button = Button(self.frameDisplay, text="Add a car in stock",
                                            command=lambda: self.verify_car_insert(raw_car))
            button_add_car.grid(column=1, row=rowspan * 6, rowspan=rowspan, sticky=NSEW)
        else:
            label_no_free_places: Label = Label(self.frameDisplay, text="No free places")
            label_no_free_places.pack()

    # 6
    def display_window_add_customer(self):
        for widget in self.frameButtons.winfo_children():
            if widget.widgetName == "button":
                widget["state"] = NORMAL
        self.buttonAddCustomer["state"] = DISABLED
        self.reset_display_and_sort_frames()
        rowspan: int = int(self.lcmRowNumberDisplay / self.rowNumberAddCustomer)

        raw_customer: dict = {
            "firstName": StringVar(),
            "lastName": StringVar(),
            "phone": StringVar(),
            "mail": StringVar(),
            "address": StringVar()
        }
        label_first_name: Label = Label(self.frameDisplay, text="Firstname : ")
        label_first_name.grid(column=0, row=0, rowspan=rowspan, sticky=NSEW)
        entry_first_name: Entry = Entry(self.frameDisplay, textvariable=raw_customer["firstName"])
        entry_first_name.grid(column=1, row=0, rowspan=rowspan, sticky=NSEW)

        label_last_name: Label = Label(self.frameDisplay, text="Lastname : ")
        label_last_name.grid(column=0, row=rowspan, rowspan=rowspan, sticky=NSEW)
        entry_last_name: Entry = Entry(self.frameDisplay, textvariable=raw_customer["lastName"])
        entry_last_name.grid(column=1, row=rowspan, rowspan=rowspan, sticky=NSEW)

        label_phone: Label = Label(self.frameDisplay, text="Phone : ")
        label_phone.grid(column=0, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)
        entry_phone: Entry = Entry(self.frameDisplay, textvariable=raw_customer["phone"])
        entry_phone.grid(column=1, row=rowspan * 2, rowspan=rowspan, sticky=NSEW)

        label_mail: Label = Label(self.frameDisplay, text="Email Address :")
        label_mail.grid(column=0, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)
        entry_mail: Entry = Entry(self.frameDisplay, textvariable=raw_customer["mail"])
        entry_mail.grid(column=1, row=rowspan * 3, rowspan=rowspan, sticky=NSEW)

        label_address: Label = Label(self.frameDisplay, text="Address : ")
        label_address.grid(column=0, row=rowspan * 4, rowspan=rowspan, sticky=NSEW)
        entry_address: Entry = Entry(self.frameDisplay, textvariable=raw_customer["address"])
        entry_address.grid(column=1, row=rowspan * 4, rowspan=rowspan, sticky=NSEW)

        button_add_customer: Button = Button(self.frameDisplay, text="Add a car in stock",
                                             command=lambda: self.verify_customer_insert(raw_customer))
        button_add_customer.grid(column=1, row=rowspan * 5, rowspan=rowspan, sticky=NSEW)

    def verify_customer_insert(self, customer_string_var: dict) -> None:
        text_info: str = ""
        new_customer: Customer = Customer()
        new_customer.firstName = customer_string_var["firstName"].get()
        if not new_customer.firstName or bool(re.search(r'\d', new_customer.firstName)):
            text_info += "- There is no firstname.\n"
        new_customer.lastName = customer_string_var["lastName"].get()
        if not new_customer.lastName or bool(re.search(r'\d', new_customer.lastName)):
            text_info += "- There is no lastname.\n"
        new_customer.phone = customer_string_var["phone"].get()
        if not (new_customer.phone.isdigit() and len(new_customer.phone) == 10):
            text_info += "- There is no phone number.\n"
        new_customer.mail = customer_string_var["mail"].get()
        if not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]+\b', new_customer.mail)):
            text_info += "- There is no email address.\n"
        new_customer.address = customer_string_var["address"].get()
        if not re.fullmatch(r"[a-zA-Z0-9\s._%+-]+, [a-zA-Z0-9\s._%+-]+\b", new_customer.address):
            text_info += "- It's not a good address.\n"
        if not text_info:
            new_customer.insert_db()
            self.customerList: list = Customer.get_all()
            self.display_window_stock()
        for widget in self.frameSort.winfo_children():
            widget.destroy()
        label_error: Label = Label(self.frameSort, text=text_info)
        label_error.pack()

    def verify_car_insert(self, car_string_var: dict) -> None:
        """

        :type car_string_var: object
        :rtype: object
        """
        text_info: str = ""
        car: Car = Car()
        car.idBrand = Brand.get_id(car_string_var["nameBrand"].get())
        if not car.idBrand:
            text_info += "- There is no brand name.\n"
        car.idType = Type.get_id(car_string_var["nameType"].get())
        if not car.idType:
            text_info += "- There is no type name.\n"
        car.idMotor = Motor.get_id(car_string_var["nameMotor"].get())
        if not car.idMotor:
            text_info += "- There is no motor name.\n"
        car.dateTechControl = car_string_var["dateTechControl"].get()
        if not car.dateTechControl:
            text_info += "- There is no date for the tech control.\n"
        car.price = car_string_var["price"].get()
        if not car.price or not check_number_input(str(car.price), 1):
            text_info += "- It's not a good price.\n"
        car.promo = car_string_var["promo"].get()
        if not car.promo or not check_number_input(str(car.promo), 0, 100):
            text_info += "- It's not a good promotion.\n"
        if not text_info:
            car.insert_db()
            self.set_or_reset_car_lists()
            self.display_window_stock()
        for widget in self.frameSort.winfo_children():
            widget.destroy()
        label_error: Label = Label(self.frameSort, text=text_info)
        label_error.pack()

    def verify_deal(self, deal: Deal) -> None:
        text_info: str = ""
        new_deal: Deal = Deal()
        raw_id_car = deal.idCar.get()
        if raw_id_car:
            new_deal.idCar = raw_id_car.split()[0]
        if not new_deal.idCar:
            text_info += "- There is no car id chosen.\n"
        raw_id_customer = deal.idCustomer.get()
        if raw_id_customer:
            new_deal.idCustomer = raw_id_customer.split()[0]
        if not new_deal.idCustomer:
            text_info += "- There is no customer id chosen.\n"
        new_deal.isRent = deal.isRent
        if new_deal.isRent:
            new_deal.dateStartRent = deal.dateStartRent.get()
            if not new_deal.dateStartRent:
                text_info += "- There is no date for the rent.\n"
            new_deal.durationDaysRent = deal.durationDaysRent.get()
            if not new_deal.durationDaysRent:
                text_info += "- There is no duration for the rent.\n"
        if not text_info:
            new_deal.insert_db()
            self.set_or_reset_car_lists()
            text_info: str = "Deal saved"
            if new_deal.isRent:
                self.display_window_rent()
            else:
                self.display_window_selling()
        for widget in self.frameSort.winfo_children():
            widget.destroy()
        label_error: Label = Label(self.frameSort, text=text_info)
        label_error.pack()

    def set_or_reset_car_lists(self):
        self.carListStock: list = Car.get_car_list()
        self.dealList: list = Deal.get_all()
        self.rentList: list = []
        self.carListFree: list = []
        for deal in self.dealList:
            if deal.isRent:
                self.rentList.append(deal)

        for car in self.carListStock:
            counter: int = 0
            found: bool = False
            while counter < len(self.rentList) and not found:
                if car.id == self.rentList[counter].idCar:
                    found: bool = True
                counter += 1
            if not found:
                self.carListFree.append(car)

    def reset_display_and_sort_frames(self):
        for widget in self.frameDisplay.winfo_children():
            widget.destroy()
        for widget in self.frameSort.winfo_children():
            widget.destroy()


# It will launch the application
Application()
