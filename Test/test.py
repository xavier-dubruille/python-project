import re


def checkNumberInput(string, minimum, maximum):
    if re.search('[^0-9]', str(string)) and string != "" and maximum <= int(string) <= minimum:
        return False
    return True


inp = " "
while not checkNumberInput(inp, 0, 5):
    inp = input("input : ")
