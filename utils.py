import os # used to get file name
import re
from sys import _getframe # Used to get function names from within function

FILENAME = os.path.basename(__file__)

AIRLINE_WEBSITES = {
    'AirCanada': 'https://www.aircanada.com/us/en/aco/home.html',
    'AirDo': 'https://www.airdo.jp/en/',
    'AirPremia': 'https://www.airpremia.com/us/en',
    'American': 'https://www.aa.com/homePage.do',
    'ANA': 'https://www.ana.co.jp/en/us/',
    'AsianaAirlines': 'https://flyasiana.com/C/US/EN/index',
    'ChinaAirlines': 'https://www.china-airlines.com/us/en',
    'Delta': 'https://www.delta.com/',
    'EvaAir': 'https://www.evaair.com/en-us/index.html%EF%BB%BF',
    'Hawaiian': 'https://www.hawaiianairlines.com/',
    'Ibex': 'https://www.ibexair.co.jp/en/',
    'JAL': 'https://www.jal.co.jp/jp/en/',
    'JetstarJapan': 'https://www.jetstar.com/jp/en/home?adults=1&children=0&flexible=1&flight-type=2&infants=0&origin=NRT&tab=1',
    'KoreanAir': 'https://www.koreanair.com/',
    'Peach': 'https://www.flypeach.com/en',
    'Scoot': 'https://www.flyscoot.com/en',
    'Singapore': 'https://www.singaporeair.com/en_UK/us/home#/book/bookflight',
    'Skymark': 'https://www.skymark.co.jp/en/',
    'SolaseedAir': 'https://www.solaseedair.jp/en/',
    'Spring': 'https://en.ch.com/',
    'StarflyerDomestic': 'https://www.starflyer.jp/en/',
    'StarflyerInternational': 'https://www.starflyer.jp/int_en/',
    'TigerAir': 'https://www.tigerairtw.com/en',
    'United': 'https://www.united.com/en/us',
    'WestJet': 'https://www.westjet.com/en-us',
    'ZipAir': 'https://www.zipair.net/en'
}

ERROR_CODE = {
    0X0: 'NO_ERROR',
    0X1: 'WEBSITE_ACCESS_FAILURE',
    0X2: 'CALENDAR_FAILURE',
    0X3: 'SOFTWARE_ERROR',
    0x4: 'TIMEOUT'
}

class flightInfo:
    def __init__(self, departureClass, arrivalClass, priceClass, airline, stops, duration, date):
        self.airline = airline
        self.departureClass = departureClass
        self.arrivalClass = arrivalClass
        self.priceClass = priceClass
        self.stops = stops
        self.duration = duration
        self.date = date

class departureInfo:
    def __init__(self, departureTime, departureAirport):
        self.departureTime = departureTime
        self.departureAirport = departureAirport

class arrivalInfo:
    def __init__(self, arrivalTime, arrivalAirport):
        self.arrivalTime = arrivalTime
        self.arrivalAirport = arrivalAirport

class priceInformation:
    def __init__(self, economyPrice, economyRefundablePrice, economyPremiumPrice, businessClassPrice):
        self.economyPrice = economyPrice
        self.economyRefundablePrice = economyRefundablePrice
        self.economyPremiumPrice = economyPremiumPrice
        self.businessClassPrice = businessClassPrice

def getFlightDuration(flightString):
    """Takes a string in the format of 10H, 20M and extracts the hours and minutes.  Returns total number of minutes"""
    timeElementsList = flightString.split()

    hoursList = re.findall('[0-9]+', timeElementsList[0]) # This will return something like ['10']
    minutesList = re.findall('[0-9]+', timeElementsList[1])

    hours = int(hoursList[0])
    minutes = int(minutesList[0])

    hoursInMinutes = hours * 60

    totalMinutes = hoursInMinutes + minutes

    return totalMinutes

def getStops(stopsString):
    """Takes a string for the number of stops and returns an integer"""
    if stopsString == 'NONSTOP':
        stops = 0
    else:
        stops = re.findall('[0-9]+', stopsString)

    return stops