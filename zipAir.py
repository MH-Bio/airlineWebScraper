import random
import time
import utils
import json
import dateManagement
import os # used to get file name
from sys import _getframe # Used to get function names from within function
from csv import writer
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILENAME = os.path.basename(__file__)

def zipAir(originCode, destinationCode, departObj):
    fun_name = _getframe().f_code.co_name

    # Convert three letter airport codes to a city name
    if originCode == "TYO":
        departureFullCityName = "Tokyo"
    else:
        departureFullCityName = utils.getLongAirportCityName(originCode)
    if destinationCode == "TYO":
        arrivalFullCityName = "Tokyo"
    else:
        arrivalFullCityName = utils.getLongAirportCityName(destinationCode)

    zipAirDepartureAirportCode = airportInfo

    time.sleep(3)
    driver = webdriver.Edge()
    driver.get(utils.AIRLINE_WEBSITES['ZipAir'])
    time.sleep(20)

    # click on the "one way" button
    oneWay = driver.find_element(By.XPATH, '//*[@id="appMain"]/div/div[1]/div/ul/li[2]/button')
    oneWay.click()

    # Find the origin and destination buttons
    originButton = driver.find_element(By.XPATH, '//*[@id="panel2"]/div/div[1]/button')
    destinationButton = driver.find_elements(By.XPATH, '//*[@id="panel2"]/div/div[2]/button') # This will return a list for some reason

    # Click on the origin airport button
    originButton.click()

    # Find a list of all possible airports to depart from
    departureAirportButtonList = driver.find_elements(By.XPATH, '//*[@id="dialogDescription"]/div/div/div')

    # Find the airport we are actually interested in departing from by iterating through all possible airports in the list
    for buttonDepartureAirport in departureAirportButtonList:
        airportCityList = buttonDepartureAirport.find_elements(By.CLASS_NAME, 'city')
        for departureCity in airportCityList:
            if departureCity == departureFullCityName:
                departureCity.click()

    # Click on the destination airport button
    destinationButton.click()

    # Find a list of all possible airports to arrive at
    arrivalAirportButtonList = driver.find_elements(By.XPATH, '//*[@id="dialogDescription"]/div/div/div')

    # Find the airport we are actually interested in arriving at by iterating through all possible airports in the list
    for buttonArrivalAirport in arrivalAirportButtonList:
        airportCityList = buttonArrivalAirport.find_elements(By.CLASS_NAME, 'city')
        for arrivalCity in airportCityList:
            if arrivalCity == arrivalFullCityName:
                arrivalCity.click()



    return 0