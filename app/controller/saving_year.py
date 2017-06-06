import datetime


def saving_year(data):
    data = data.split(" ")
    year = generate_year()
    for y in year:
        for d in data:
            if str(y) == d:
                return [y,"saved_amount","outstanding_loans"]


def generate_year():
    now = datetime.datetime.now()
    current_year = now.year
    years = []
    for i in range(2014, current_year):
        years.append(i)
    return years


def creation_year():
    now = datetime.datetime.now()
    current_year = now.year
    years = []
    for i in range(2010, current_year + 1):
        years.append(i)
    return years



