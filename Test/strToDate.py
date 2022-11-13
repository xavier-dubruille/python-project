from datetime import datetime

date = ""
while True:
    datetime_str = input("date : ")
    try:
        date = datetime.strptime(datetime_str, '%d/%m/%Y').strftime("%d/%m/%Y")
        break
    except ValueError:
        pass

print(date)  # printed in default format
