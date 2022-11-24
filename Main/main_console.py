import sys

from Main.Class.Car import Car
from Main.Class.Brand import Brand
from Main.Class.Type import Type
from Main.Class.Motor import Motor
from Main.Class.Deal import Deal
from Main.Class.Customer import Customer

from datetime import datetime
import re


def check_number_input(string: str, minimum: int = None, maximum: int = None) -> bool:
    """
    This function check if the string is convertible into integer
    If minimum and/or maximum are given, check also if it's between them
    :param string: A string that will be checked for a number
    :type string: str
    :param minimum: An integer number
    :type minimum: int
    :param maximum: An integer number
    :type maximum: int
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


class ApplicationConsole:
    def __init__(self) -> None:
        self.carListStock: list = Car.get_car_list()
        self.brandList: list = Brand.get_all()
        self.motorList: list = Motor.get_all()
        self.typeList: list = Type.get_all()
        deal_list: list = Deal.get_all()
        self.rentList: list = []
        self.soldList: list = []
        for deal in deal_list:
            if deal.isRent:
                self.rentList.append(deal)
            else:
                self.soldList.append(deal)
        self.customerList: list = Customer.get_all()
        self.spaceDisplay: int = 4
        print("Welcome to Bamboo Concess\n")
        self.menu_choice()

    def menu_choice(self) -> None:
        """
        This function display the basic menu for the user
        :returns: None
        :rtype: None
        """
        menu_input: str = ""
        while not check_number_input(menu_input, 1, 5):
            menu_input: str = input("Where do you want to go now ?\n 1 : Show your stock.\n"
                                    " 2 : Show your transaction history.\n 3 : Add a new car to your stock.\n"
                                    " 4 : Add a customer\n 5 : Exit the program.\n-> ")
        menu_input: int = int(menu_input)
        if menu_input == 1:
            self.display_stock()
        elif menu_input == 2:
            self.display_history()
        elif menu_input == 3:
            self.add_car()
        elif menu_input == 4:
            self.add_customer()
        else:
            sys.exit()

    def add_customer(self) -> None:
        """
        This function asks the user to add a customer to the database with all his characteristics
        :returns: None
        :rtype: None
        """
        new_customer: Customer = Customer()

        while not new_customer.firstName.isalpha():
            new_customer.firstName = input("What's the first name ?\n-> ")
        while not new_customer.lastName.isalpha():
            new_customer.lastName = input("What's the last name ?\n-> ")
        while not (new_customer.phone.isdigit() and len(new_customer.phone) == 10):
            new_customer.phone = input("What's the phone number (10 numbers)\n-> ")
        new_customer.phone = int(new_customer.phone)
        while not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]+\b', new_customer.mail)):
            new_customer.mail = input("What's the email address ?\n-> ")
        while not re.fullmatch(r"[a-zA-Z0-9\s._%+-]+, [a-zA-Z0-9\s._%+-]+\b", new_customer.address):
            new_customer.address = input("What's the address ?\n-> ")
        if new_customer.insert_db():
            print("New customer added\n")
        else:
            print("The execution doesn't work\n")
        self.menu_choice()

    def display_stock(self) -> None:
        """
        This function display the stock from the database
        :returns: None
        :rtype: None
        """
        str_list: list = ["Id", "Brand", "Type", "Price (€)"]
        space_dict: dict = {
            str_list[0]: len(str_list[0]) + self.spaceDisplay,
            str_list[1]: len(max(self.carListStock, key=lambda x: len(x.brand.name)).brand.name) + self.spaceDisplay,
            str_list[2]: len(max(self.carListStock, key=lambda x: len(x.type.name)).type.name) + self.spaceDisplay}

        for i in range(len(str_list) - 1):
            i: int
            if space_dict[str_list[i]] < len(str_list[i]):
                space_dict[str_list[i]]: int = len(str_list[i]) + self.spaceDisplay

        print(f"{str_list[0]}" + " " * self.spaceDisplay +
              f"{str_list[1]}" + " " * (space_dict[str_list[1]] - len(f"{str_list[1]}")) +
              f"{str_list[2]}" + " " * (space_dict[str_list[2]] - len(f"{str_list[2]}")) +
              f"{str_list[3]}")

        for car in self.carListStock:
            car: Car
            print(f"{str(car.id):{space_dict[str_list[0]]}}"
                  f"{car.brand.name:{space_dict[str_list[1]]}}"
                  f"{car.type.name:{space_dict[str_list[2]]}}"
                  f"{str(car.price)}")

        next_step: str = ""
        while not check_number_input(next_step, 1, 5):
            next_step: str = input("\nWhat do you want to do next ?\n"
                                   " 1 : Return to the choice menu.\n"
                                   " 2 : See a car's details.\n"
                                   " 3 : Rent a car.\n"
                                   " 4 : Make a deal.\n"
                                   " 5 : Remove a car.\n"
                                   "-> ")
        next_step: int = int(next_step)
        if next_step == 1:
            self.menu_choice()
        elif next_step == 2:
            good_choice: bool = False
            while not good_choice:
                car_id: str = input("Which car do you want to see details from ?\n-> ")
                if car_id.isdigit():
                    car_id: int = int(car_id)
                    for car in self.carListStock:
                        car: Car
                        if car_id == car.id:
                            print(f"Brand : {car.brand.name}\n"
                                  f"Type : {car.type.name}\n"
                                  f"Motor : {car.motor.name}\n"
                                  f"Price : {str(car.price)}€\n"
                                  f"Promo : {str(car.promo)}%\n"
                                  f"In stock since : {car.dateStock}\n"
                                  f"Next control : {car.dateTechControl}\n")
                            good_choice: bool = True
                            break
        elif next_step == 3:
            self.do_transaction(True)
        elif next_step == 4:
            self.do_transaction(False)
        elif next_step == 5:
            good_car_id: bool = False
            while not good_car_id:
                car_id: str = input("Which car do you want to remove (n for quit this operation)?\n-> ")
                if car_id.lower() == "n":
                    good_car_id: bool = True
                    print("Operation abandoned.\n")
                elif car_id.isdigit():
                    for car in self.carListStock:
                        car: Car
                        if car.id == int(car_id):
                            good_car_id: bool = True
                            car.remove_db()
                            self.carListStock: list = Car.get_car_list()
                            print("Car removed\n")
        self.menu_choice()

    def display_history(self) -> None:
        """
        This function display the history of the user transaction from the database
        :returns: None
        :rtype: None
        """
        choice_history: str = ""
        while not check_number_input(choice_history, 1, 2):
            choice_history: str = input("\n"
                                        " 1 : Rent history display.\n"
                                        " 2 : Transaction history display.\n"
                                        "-> ")
        choice_history: int = int(choice_history)
        str_list: list = ["Id", "Date", "Duration", "Brand", "Type", "Price (€)"]
        space_dict: dict = {}
        list_to_display: list = []
        if choice_history == 1:
            list_to_display: list = self.rentList
        else:
            list_to_display: list = self.soldList

        if not list_to_display:
            print("There isn't a deal in this categories\n")
            self.menu_choice()
            return None

        space_dict[str_list[0]]: int = len(str(
            max(list_to_display, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
        space_dict[str_list[1]]: int = len(
            max(list_to_display, key=lambda x: len(x.dateStartRent)).dateStartRent) + self.spaceDisplay
        space_dict[str_list[2]]: int = len(str(
            max(list_to_display, key=lambda x: len(str(x.durationDaysRent))).durationDaysRent)) + self.spaceDisplay
        space_dict[str_list[3]]: int = len(
            max(list_to_display, key=lambda x: len(x.car.brand.name)).car.brand.name) + self.spaceDisplay
        space_dict[str_list[4]]: int = len(
            max(list_to_display, key=lambda x: len(x.car.type.name)).car.type.name) + self.spaceDisplay

        for i in range(len(str_list) - 1):
            i: int
            if space_dict[str_list[i]] < len(str_list[i]):
                space_dict[str_list[i]]: int = len(str_list[i]) + self.spaceDisplay

        print(f"\n"
              f"{str_list[0]}" + " " * (space_dict[str_list[0]] - len(f"{str_list[0]}")) +
              f"{str_list[1]}" + " " * (space_dict[str_list[1]] - len(f"{str_list[1]}")) +
              f"{str_list[2]}" + " " * (space_dict[str_list[2]] - len(f"{str_list[2]}")) +
              f"{str_list[3]}" + " " * (space_dict[str_list[3]] - len(f"{str_list[3]}")) +
              f"{str_list[4]}" + " " * (space_dict[str_list[4]] - len(f"{str_list[4]}")) +
              f"{str_list[5]}")

        for deal in self.rentList:
            deal: Deal
            print(f"{str(deal.id):{space_dict[str_list[0]]}}"
                  f"{deal.dateStartRent:{space_dict[str_list[1]]}}"
                  f"{str(deal.durationDaysRent):{space_dict[str_list[2]]}}"
                  f"{deal.car.brand.name:{space_dict[str_list[3]]}}"
                  f"{deal.car.type.name:{space_dict[str_list[4]]}}"
                  f"{str(deal.car.price)}")
        print("")
        self.menu_choice()

    def do_transaction(self, bool_rent: bool) -> None:
        """
        This function asks the user to make a deal between one car and one customer
        :returns: None
        :rtype: None
        """
        deal: Deal = Deal()
        good_car_id: bool = False
        good_start_date: bool = False
        good_customer_id: bool = False
        deal.isRent = bool(bool_rent)
        space_dict: dict = {}
        str_list = ["Id", "Name", "Phone"]

        while not good_car_id:
            deal.idCar = input("What is the car id ?\n-> ")
            if deal.idCar.isdigit():
                deal.idCar = int(deal.idCar)
                for car in self.carListStock:
                    if car.id == deal.idCar:
                        good_car_id: bool = True
                        break

        space_dict[str_list[0]]: int = len(
            str(max(self.customerList, key=lambda x: len(str(x.id))).id)) + self.spaceDisplay
        longest_customer: Customer = max(self.customerList, key=lambda x: len(x.lastName))
        space_dict[str_list[1]]: int = len(
            f"{longest_customer.firstName[0]}.{longest_customer.lastName}") + self.spaceDisplay

        for i in range(len(str_list) - 1):
            i: int
            if space_dict[str_list[i]] < len(str_list[i]):
                space_dict[str_list[i]]: int = len(str_list[i])

        print(f"List of customers : \n"
              f"{str_list[0]}" + " " * (space_dict[str_list[0]] - len(f"{str_list[0]}")) +
              f"{str_list[1]}" + " " * (space_dict[str_list[1]] - len(f"{str_list[0]}")) +
              f"{str_list[2]}")

        for customer in self.customerList:
            customer: Customer
            print(f"{str(customer.id):{space_dict[str_list[0]]}}"
                  f"{f'{customer.firstName[0]}.{customer.lastName}':{space_dict[str_list[1]]}}"
                  f"{customer.phone}")

        while not good_customer_id:
            deal.idCustomer = input("What is the customer's id ?\n-> ")
            if deal.idCustomer.isdigit():
                deal.idCustomer = int(deal.idCustomer)
                for customer in self.customerList:
                    if customer.id == deal.idCustomer:
                        good_customer_id: bool = True
                        break
        if deal.isRent:
            while not good_start_date:
                deal.dateStart = input("When does the rent start ?\n-> ")
                try:
                    deal.dateStart = datetime.strptime(deal.dateStart, '%d/%m/%Y').strftime("%d/%m/%Y")
                    good_start_date: bool = True
                except ValueError:
                    continue

            while not check_number_input(deal.durationDays, minimum=1):
                deal.durationDays = input("How many days will the rent spend ?\n-> ")
        deal.insert_db()
        self.menu_choice()

    def add_car(self) -> None:
        """
        This function asks the user to add a car to the database with all the characteristics
        :returns: None
        :rtype: None
        """
        if Car.car_free_places_stock() <= 40:
            car: Car = Car()
            name_brand: str = ""
            name_type: str = ""
            name_motor: str = ""
            good_date: bool = False

            while not name_brand:
                name_brand: str = input("What is the name of the brand ?\n-> ")
            while not name_type:
                name_type: str = input("What is the type ?\n-> ")
            while not name_motor:
                name_motor: str = input("What is the motor's name ?\n-> ")
            while not check_number_input(car.price, minimum=0):
                car.price = input("What is the price ?\n-> ")
            car.price = int(car.price)
            while not check_number_input(car.promo, 0, 100):
                car.promo = input("Any promotion (%) ?\n-> ")
            car.promo = int(car.promo)
            while not good_date:
                car.dateTechControl = input("What is the date of the tech control ?\n-> ")
                try:
                    car.dateTechControl = datetime.strptime(car.dateTechControl, '%d/%m/%Y').strftime("%d/%m/%Y")
                    good_date: bool = True
                except ValueError:
                    continue

            car.idBrand = Brand.get_id(name_brand)
            car.idType = Type.get_id(name_type)
            car.idMotor = Motor.get_id(name_motor)
            if car.insert_db():
                print("Executed\n")
            else:
                print("Not executed\n")
        else:
            print("No free places in stock.\n")
        self.menu_choice()


ApplicationConsole()
