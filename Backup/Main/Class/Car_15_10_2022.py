class Car():
    def __init__(self, arg_brand = "No brand at the moment"):
        self._brand = arg_brand
        self._typeOfCar = ""
        self._typeOfMotor = ""
        self._timeInStock = 0
        self._nextInspection = 0
        self._priceEuro = 0
        self._rented = False

    def __str__(self):
        return "Product(name={})".format(self._brand)
  
    @property
    def brand(self):
        return self._brand

    @property
    def price_euro(self):
        return self._priceEuro

    @price_euro.setter
    def price_euro(self, arg_priceEuro):
        self._priceEuro = arg_priceEuro
