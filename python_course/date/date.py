from typing import Literal


Quarter = Literal["first quarter", "second quarter", "third quarter", "fourth quarter"]


def get_quarter(month: int) -> Quarter:
    quarter: Quarter = [
        "first quarter",
        "second quarter",
        "third quarter",
        "fourth quarter",
    ]
    if 1 <= month <= 3:
        return quarter[0]
    elif 3 <= month <= 6:
        return quarter[1]
    elif 6 <= month <= 9:
        return quarter[2]
    elif 9 <= month <= 12:
        return quarter[3]


month_string = input("enter a month: ")
quarter = get_quarter(int(month_string))
print(quarter)
