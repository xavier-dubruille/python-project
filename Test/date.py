from datetime import datetime, timedelta

numbers_of_days_left = (datetime.today()-(datetime.strptime("16/11/22", "%d/%m/%y") + timedelta(days=14))).days
print(numbers_of_days_left)
# if date_end < datetime.strptime(datetime.strftime(datetime.today(), "%d/%m/%y"), "%d/%m/%y"):
#     print("c'est pas fini")
# else:
#     print("c'est fini")




# today: str = "29/11/22"
# another_day: str = "4/12/21"
# date: datetime = datetime.strptime(today, "%d/%m/%y")
# date_2: datetime = datetime.strptime(another_day, "%d/%m/%y")
# date_1 = datetime.strptime(today, "%d/%m/%y")
#
# end_date = date_1 + timedelta(days=10)
#
# print(end_date.strftime("%d/%m/%y"))
# print(date_2 - date)
# print(date)
