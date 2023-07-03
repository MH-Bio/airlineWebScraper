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

    time.sleep(3)
    driver = webdriver.Edge()
    driver.get(utils.AIRLINE_WEBSITES['ZipAir'])
    time.sleep(20)

    # click on the "one way" button
    oneWay = driver.find_element(By.XPATH, '//*[@id="appMain"]/div/div[1]/div/ul/li[2]/button')
    oneWay.click()

    # Find the origin button
    originButton = driver.find_element(By.XPATH, '//*[@id="panel2"]/div/div[1]/button')

    # Click on the origin airport button
    originButton.click()

    # Wait for the list to load
    time.sleep(random.uniform(2, 5))

    # Find a list of all possible airports to depart from
    departureAirportButtonList = driver.find_elements(By.XPATH, '//*[@id="dialogDescription"]/div/div/div')

    airportFound = False
    # Find the airport we are actually interested in departing from by iterating through all possible airports in the list
    for buttonDepartureAirport in departureAirportButtonList:
        time.sleep(1) # allow stuff to load properly
        airportCityList = buttonDepartureAirport.find_elements(By.CLASS_NAME, 'city')
        for departureCity in airportCityList:
            if departureFullCityName in buttonDepartureAirport.text:
                departureCity.click()
                airportFound = True
        if airportFound == True:
            break

    # Wait a random amount of time so the website is less likely to think that we are using a bot
    time.sleep(random.uniform(2, 5))

    # Find the destination button
    destinationButton = driver.find_elements(By.XPATH, '//*[@id="panel2"]/div/div[2]/button') # returns a list for some reason

    # Click on the destination airport button
    destinationButton[0].click()

    # Find a list of all possible airports to arrive at
    arrivalAirportButtonList = driver.find_elements(By.XPATH, '//*[@id="dialogDescription"]/div/div/div')

    airportFound = False
    # Find the airport we are actually interested in arriving at by iterating through all possible airports in the list
    for buttonArrivalAirport in arrivalAirportButtonList:
        time.sleep(1) # allow stuff to load properly
        airportCityList = buttonArrivalAirport.find_elements(By.CLASS_NAME, 'city')
        for arrivalCity in airportCityList:
            if arrivalCity.text == arrivalFullCityName:
                arrivalCity.click()
                airportFound = True
        if airportFound == True:
            break

    # Click the search flight button now that we have entered in the desired departure/arrival information
    searchFlightButton = driver.find_elements(By.XPATH, '//*[@id="appMain"]/div/div[1]/div/div[2]/button')
    searchFlightButton[0].click()

    # Click through the "Please keep your Passport ready" screen
    passportReadyNextButton = driver.find_elements(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[2]/button[1]')
    passportReadyNextButton[0].click()

    # Wait for the next screen to load properly
    time.sleep(90)

    # We are now in the select number of passengers screen, it defaults to 1 adult age 15+ so just click next
    numberPassengersNextButton = driver.find_elements(By.XPATH, '//*[@id="appMain"]/div[2]/div/div/section/div[2]/form/div[2]/button')
    numberPassengersNextButton[0].click()

    # Wait for the next screen to load properly
    time.sleep(90)

    zip_air_base_calendar = '//*[@id="appMain"]/div[2]/div/div/section/div[1]/div[%s]/table/tbody/tr[%s]/td[%s]/button'
    depart_week_index_XPathIndex = dateManagement.get_week_of_month(year=departObj.year, month=departObj.month, day=departObj.day)
    depart_weekday_index_XPathIndex = dateManagement.get_day_of_week(year=departObj.year, month=departObj.month, day=departObj.day)

    # for some reason the month that is used to depart starts at 2, so we adjust our calculation for that
    time_until_departure_months = departObj.month - dateManagement.getCurrentMonth()

    # Convert the difference in months to be used in the calendar XPATH
    calendarXpathMonth = 2 + time_until_departure_months

    # Combine our finds into an XPATH to be used to get our position on the calendar
    zipAirCalendarXpathFinal = zip_air_base_calendar %(calendarXpathMonth, depart_week_index_XPathIndex, depart_weekday_index_XPathIndex)

    calendarButton = driver.find_elements(By.XPATH, zipAirCalendarXpathFinal)

    if "$" not in calendarButton[0].get_attribute("aria-label"): # we branch from here depending if there is a flight or not
        print("we have now entered the problem zone")
        departureTime = utils.PRICE_UNAVILABLE
        arrivalTime = utils.PRICE_UNAVILABLE
        standardPriceFloat = utils.PRICE_UNAVILABLE
        firstClassPriceFloat = utils.PRICE_UNAVILABLE
        flightDuration = utils.PRICE_UNAVILABLE
        departYear = departObj.year
        departMonth = departObj.month
        departDay = departObj.day
        arriveYear = departObj.year
        arriveMonth = departObj.month
        arriveDay = departObj.day
    else:
        calendarButton[0].send_keys(Keys.RETURN) # Click() doesn't work for some reason, but hitting the enter key does???

        time.sleep(60)

        departureTimeElement = driver.find_elements(By.CLASS_NAME,'start')
        departureTimeElement_breakdown = departureTimeElement[0].text
        departureTime = departureTimeElement_breakdown[0]
        if '+1' in departureTimeElement_breakdown:
            departAdjustedDateInfo = dateManagement.convert_to_next_day(year=departObj.year, month=departObj.month, day=departObj.day)
            departYear = departAdjustedDateInfo[0]
            departMonth = departAdjustedDateInfo[1]
            departDay = departAdjustedDateInfo[2]
        else:
            departYear = departObj.year
            departMonth = departObj.month
            departDay = departObj.day

        arrivalTimeElement = driver.find_elements(By.CLASS_NAME,'end')
        arrivalTimeElement_breakdown = arrivalTimeElement[0].text.split()
        arrivalTime = arrivalTimeElement_breakdown[0]
        if '+1' in arrivalTimeElement_breakdown:
            arrivalAdjustedDateInfo = dateManagement.convert_to_next_day(year=departObj.year, month=departObj.month, day=departObj.day)
            arriveYear = arrivalAdjustedDateInfo[0]
            arriveMonth = arrivalAdjustedDateInfo[1]
            arriveDay = arrivalAdjustedDateInfo[2]
        else:
            arriveYear = departObj.year
            arriveMonth = departObj.month
            arriveDay = departObj.day

        flightTimeXpath = driver.find_elements(By.XPATH, '//*[@id="appMain"]/div[2]/div/div/section/div/div[1]/div[2]/div/div/div/div[2]/span')
        flightTimeString = flightTimeXpath[0].text
        flightTimeList = flightTimeString.split()
        flightTimeHours = int(flightTimeList[0])
        flightTimeMinutes = int(flightTimeList[2])

        standardPriceStr = driver.find_elements(By.XPATH, '//*[@id="cabinContainer_undefined"]/div/ul/li[1]/div/label/div/div[3]/div/div/div[1]')
        firstClassPriceStr = driver.find_elements(By.XPATH, '//*[@id="cabinContainer_undefined"]/div/ul/li[2]/div/label/div/div[3]/div/div/div[1]')

        standardPriceStrList = standardPriceStr[0].text.split()
        firstClassPriceStrList = firstClassPriceStr[0].text.split()

        for item in standardPriceStrList:
            if '$' in item:
                standardPriceUnformatted = item # returns something similar to '$422.20'
                break
        for item in firstClassPriceStrList:
            if '$' in item:
                firstClassPriceUnformatted = item # returns something similar to '$1,395.20'
                break

        # First pass, remove the '$' symbols
        standardPriceDollarRemoved = standardPriceUnformatted.replace('$','')
        firstClassPriceDollarRemoved = firstClassPriceUnformatted.replace('$','')

        # Second pass, remove the ',' symbols
        standardPriceCommaRemoved = standardPriceDollarRemoved.replace(',','')
        firstClassPriceCommaRemoved = firstClassPriceDollarRemoved.replace(',','')

        # Convert the resulting string to a float
        standardPriceFloat = float(standardPriceCommaRemoved)
        firstClassPriceFloat = float(firstClassPriceCommaRemoved)

        flightDuration = (flightTimeHours * 60) + flightTimeMinutes

    # Create a dictionary that we can write to a JSON file
    dictionary = {
        "Airline": "ZipAir",
        "Departure Time": departureTime,
        "Departure Date": str(departMonth) + '/' + str(departDay) + '/' + str(departYear),
        "Departure Airport": originCode,
        "Arrival Time": arrivalTime,
        "Arrival Date": str(arriveMonth) + '/' + str(arriveDay) + '/' + str(arriveYear),
        "Arrival Airport": destinationCode,
        "Economy Price": standardPriceFloat,
        "Business Class Price": firstClassPriceFloat,
        "Stops": 0,
        "Flight Duration": flightDuration
    }

    '''
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("zipAir.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_object)
    '''
    driver.close()



    return dictionary
