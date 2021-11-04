import datetime

def toDateYMD(fecha, separator): #yyyy/mm/dd
    arrDate = fecha.split(separator)
    day = int(arrDate[2])
    month = int(arrDate[1])
    year = int(arrDate[0])
    print(day, month, year)
    date = datetime.date(year, month, day)
    return date

def toDateDMY(fecha, separator): #dd/mm/yyyy
    arrDate = fecha.split(separator)
    day = int(arrDate[0])
    month = int(arrDate[1])
    year = int(arrDate[2])
    print(day, month, year)
    date = datetime.date(year, month, day)
    return date