import re


def checkNumberInput(string, minimum, maximum):
    if not string.isdigit():
        return False
    if maximum > int(string) > minimum:
        return True
    return False


inp = " "
while not checkNumberInput(inp, 0, 5):
    inp = input("input : ")
