import os # used to get file name
import json
import re
from sys import _getframe # Used to get function names from within function

# Return codes
NO_ERROR = 0x0
WEBSITE_ACCESS_FAILURE = 0x1
CALENDAR_FAILURE = 0x2
SOFTWARE_ERROR = 0x3
TIMEOUT = 0x4
PRICE_UNAVILABLE = 'Not available'

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

def destinationListGenerator(airlineName):
    """Returns a list of routesthat will be used when entering a route on an airline's website.
       Keep in mind that this is only one half of the tirp, and is the higher ranking item in the JSON file.
       For international flights this will be the arrival airport.
       For domestic flights, this will be the departure airport."""
    with open('airlineRoutes.json') as f:
        airlineData = json.load(f)

    destinationList = []
    airlineRoute = airlineData[airlineName]['Routes']
    for destination in airlineRoute:
        destinationList.append(destination)

    return destinationList

def getLongAirportCityName(airportCode):
    """Takes a three letter airport code and returns the city name of the airport.
    For example PDX will return Portland.  This function obtains information from the airportInfo.json file"""
    with open('airportInfo.json', encoding="utf8") as f:
        airportInfo = json.load(f)

    return airportInfo[airportCode]["City"]