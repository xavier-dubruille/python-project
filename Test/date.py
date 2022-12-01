from datetime import datetime, timedelta

# numbers_of_days_left = (datetime.today() - (datetime.strptime("16/11/22", "%d/%m/%y") + timedelta(days=14))).days
# print(numbers_of_days_left)

print((datetime.today() - datetime.strptime("2021-11-30", "%Y-%m-%d")).days >= 365)
