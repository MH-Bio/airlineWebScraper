class departureDate:
    def __init__(self, year, month, day):
        self.year = -1
        self.month = -1
        self.day = -1

class returnDate:
    def __init__(self, year, month, day):
        self.year = -1
        self.month = -1
        self.day = -1

def getMonthStrShort(monthNum):
    """Returns the three letter code used by United Airlines to input dates"""
    monthStr = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    return monthStr.get(monthNum)

def getMonthStrLong(monthNum):
    """Returns the full month string"""
    monthStr = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    return monthStr.get(monthNum)

def getDayStr(dayNum):
    """Converts single digit days to two digit days (e.g. 2 becomes 02)"""
    returnStr = 'ERROR'
    if dayNum < 10:
        returnStr = '0%d' % dayNum
    else:
        returnStr = str(dayNum)

    return returnStr

def setDepartureDate(self, year, month, day):
    """Sets the deparutre date global variable"""
    departure = departureDate(year, month, day)

def setReturnDate(self, year, month, day):
    """Sets the deparutre date global variable"""
    returnDate = returnDate(year, month, day)