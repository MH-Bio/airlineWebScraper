from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
import csv
import random
import time
import utils
import dateManagement
import os # used to get file name
from sys import _getframe # Used to get function names from within function
import json
import unitedAirlines
import time
import random

# My version of Edge is Version 113.0.1774.42 (Official build) (64-bit)
# useful website: https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python

DEPARTURE_DATE = None
RETURN_DATE = None
FILENAME = os.path.basename(__file__)

'''
option = EdgeOptions()
option.add_argument("--InPrivate")
'''
time.sleep(3)
driver = webdriver.Edge()
#action = ActionChains(driver) # See: https://www.geeksforgeeks.org/key_down-method-action-chains-in-selenium-python/#
#driver.add_argument("--InPrivate")

_depart_obj = dateManagement.departureDate(2023, 8, 1)
_return_obj = dateManagement.returnDate(2023, 8, 7)

def checkWebsites():
    with open('results.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([#'Date',
                             'Airline',
                             'Departure Time',
                             'Departure Airport',
                             'Arrival Time',
                             'Arrival Airport',
                             'Price (Basic Economy)',
                             'Price (Refundable Economy)',
                             'Price (Premium Economy)',
                             'Price (Business Class)',
                             'Stops',
                             'Duration (Minutes)'])

    #f = open('C:\\Users\\micha\\PycharmProjects\\airlineWebScraper\\airlineRoutes.json')
    with open('airlineRoutes.json') as f:
        airlineData = json.load(f)

    united_destinationList = []
    unitedRoutes = airlineData['United Airlines']['Routes']
    for destination in unitedRoutes:
        united_destinationList.append(destination)

    for destinationCode in united_destinationList:
        originCodeList = airlineData['United Airlines']['Routes'][destinationCode]
        for originCode in originCodeList:
            united_obj_list, UA_return_code = unitedAirlines.unitedAirlines(originCode=originCode,
                                                                            destinationCode=destinationCode,
                                                                            departObj=_depart_obj, driver=driver)
            time.sleep(random.uniform(10, 30))
            if UA_return_code != utils.ERROR_CODE['NO_ERROR']:
                print("Unable to get information from United Airlines for route %s - %s."%(originCode, destinationCode))

def main():
    checkWebsites()


if __name__ == '__main__':
    main()
