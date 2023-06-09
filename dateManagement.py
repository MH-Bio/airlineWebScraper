import calendar
import numpy as np
from datetime import datetime
import os
import utils
from sys import _getframe # Used to get function names from within function

FILENAME = os.path.basename(__file__)

calendar.setfirstweekday(6) # sets first day of week to Sunday

class departureDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

class returnDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

class currentTime:
    def __init__(self, currentSecond, currentMinute, currentHour, currentDay, currentMonth, currentYear):
        self.currentSecond = datetime.now().second
        self.currentMinute = datetime.now().minute
        self.currentHour = datetime.now().hour
        self.currentDay = datetime.now().day
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year

def getCurrentSecond():
    """Returns current seconds as an int"""
    return datetime.now().second

def getCurrentMinute():
    """Returns current minute as an int"""
    return datetime.now().minute

def getCurrentHour():
    """Returns current hour as an int in the 24 hour format"""
    return datetime.now().hour

def getCurrentDay():
    """Returns the current day as an int"""
    return datetime.now().day

def getCurrentMonth():
    """Returns the current month as an int"""
    return datetime.now().month

def getCurrentYear():
    """Returns the current day as an int"""
    return datetime.now().year

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

def get_week_of_month(year, month, day):
    """Takes a date as an input and returns the week of the month that day is on (1-6)"""
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x == day)[0][0] + 1

    return week_of_month

def get_day_of_week(year, month, day):
    """Takes a date as an input and returns the day of the week as a number (1-7)"""
    x = np.array(calendar.monthcalendar(year, month))
    day_of_week = np.where(x == day)[1][0] + 1

    return day_of_week

def convert_to_next_day(year, month, day):
    """Takes an input date and returns a year, month, day.
    This will take into account month rollovers (e.g. July 31st + 1 day is August 1st)"""
    adjustedYear = -1
    adjustedMonth = -1
    adjustedDay = -1

    leapYear = False
    if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
        leapYear = True

    # 30 days september, apr, june, nov
    # 31 days in jan, mar, may, july, aug, oct, dec

    if month == 12 and day == 31:
        adjustedYear = year + 1
        adjustedMonth = 1
        adjustedDay = 1
    elif month == 2: # February handling
        if leapYear == True:
            if day == 29:
                adjustedYear = year
                adjustedMonth = 3
                adjustedDay = 1
            else:
                adjustedYear = year
                adjustedMonth = month
                adjustedDay = day + 1
        else:
            if day == 28:
                adjustedYear = year
                adjustedMonth = 3
                adjustedDay = 1
            else:
                adjustedYear = year
                adjustedMonth = month
                adjustedDay = day + 1
    elif month in [4, 6, 9, 11]: # april, june, sep, nov
        if day == 30:
            adjustedYear = year
            adjustedMonth = month + 1
            adjustedDay = 1
        else:
            adjustedYear = year
            adjustedMonth = month
            adjustedDay = day + 1
    else: # all other months have 31 days
        if day == 31:
            adjustedYear = year
            adjustedMonth = month + 1
            adjustedDay = 1
        else:
            adjustedYear = year
            adjustedMonth = month
            adjustedDay = day + 1

    return adjustedYear, adjustedMonth, adjustedDay