import random
import time
import utils
import dateManagement
import os # used to get file name
from sys import _getframe # Used to get function names from within function
from csv import writer
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILENAME = os.path.basename(__file__)

def unitedAirlines(originCode, destinationCode, departObj, driver):
    """Gets info from the United Airlines Website"""
    fun_name = _getframe().f_code.co_name
    driver.get(utils.AIRLINE_WEBSITES['United'])

    # click on the "one way" button
    oneWay = driver.find_element(By.XPATH, '//*[@id="bookFlightForm"]/div[1]/fieldset/div/label[2]/span[2]')
    oneWay.click()

    departDate = driver.find_element(By.ID, 'DepartDate')
    departDate.click()
    '''
    if returnObj is not None:
        returnDate = driver.find_elements(By.ID, 'ReturnDate')
        returnDate.clear()
    '''

    # Example here: https://learn-automation.com/handle-calender-in-selenium-webdriver/
    # finding elements in the calnedar: zzz = driver.find_elements(By.XPATH, '//*[@id="passengersSlidingInputContainer"]//td')

    # Find whatever month United is defaulting to
    default_month_xpath = driver.find_element(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[3]') # Should always be on the calendar
    default_month_aria_label = default_month_xpath.get_attribute("aria-label")

    confirmed_default_month = ''
    calendar_default_month_index = 1
    while calendar_default_month_index < 12:
        if calendar_default_month_index == 13:
            print("Unable to find current month in calendar format date picker.  See: %s, Function: %s()" %(FILENAME, fun_name))
            return utils.ERROR_CODE['CALENDAR_FAILURE']
        if dateManagement.getMonthStrLong(calendar_default_month_index) in default_month_aria_label:
            confirmed_default_month = dateManagement.getMonthStrLong(calendar_default_month_index)
            break
        else:
            calendar_default_month_index = calendar_default_month_index + 1

    difference_between_months = departObj.month - calendar_default_month_index

    prev_month_button = driver.find_elements(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[1]/button[1]')
    next_month_button = driver.find_elements(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[1]/button[2]')

    # Work our way over to the correct date on the calendar
    retry_counter = 0
    if difference_between_months > 0:
        i = 1 # remember we are counting the current month as month 1
        while i < difference_between_months:
            if retry_counter > 10:
                return utils.ERROR_CODE['TIMEOUT']
            time.sleep(random.uniform(1, 3))
            try:
                next_month_button[0].click() # advance one month
                i = i + 1
            except:
                print('Clicking next button on calendar didn\'t work.  Trying again')
                retry_counter = retry_counter + 1
    elif difference_between_months < 0:
        difference_between_months_corrected = difference_between_months * -1
        i = 1
        while i < difference_between_months_corrected:
            if retry_counter > 10:
                return utils.ERROR_CODE['TIMEOUT']
            time.sleep(random.uniform(1, 3))
            try:
                prev_month_button[0].click() # advance one month
                i = i + 1
            except:
                print('Clicking previous button on calendar didn\'t work.  Trying again')
                retry_counter = retry_counter + 1


    # Figure out where in the element matrix we need to pull from
    united_date_calculation_base = '/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[%s]/td[%s]'
    depart_week_index_XPathIndex = dateManagement.get_week_of_month(year=departObj.year, month=departObj.month, day=departObj.day)
    depart_weekday_index_XPathIndex = dateManagement.get_day_of_week(year=departObj.year, month=departObj.month, day=departObj.day)
    depart_calendar_selection = united_date_calculation_base % (depart_week_index_XPathIndex, depart_weekday_index_XPathIndex)
    '''
    if returnObj is not None:
        return_week_index_XPathIndex = dateManagement.get_week_of_month(year=returnObj.year, month=returnObj.month, day=returnObj.day)
        return_weekday_index_XPathIndex = dateManagement.get_day_of_week(year=returnObj.year, month=returnObj.month, day=returnObj.day)
        return_calendar_selection = united_date_calculation_base %(return_week_index_XPathIndex, return_weekday_index_XPathIndex)
    '''

    depart_date_button = driver.find_elements(By.XPATH, depart_calendar_selection)
    depart_date_button[0].click()

    # Select origin airport
    originElement = driver.find_element(By.ID, 'bookFlightOriginInput')
    originElement.clear()  # Clear out United trying to use your current location
    originElement.send_keys(originCode)
    time.sleep(random.uniform(3, 5))
    originElement.send_keys(Keys.DOWN)
    originElement.send_keys(Keys.RETURN)

    # Select destination airport
    destinationElement = driver.find_element(By.ID, 'bookFlightDestinationInput')
    destinationElement.send_keys(destinationCode)
    time.sleep(random.uniform(3, 5))
    destinationElement.send_keys(Keys.DOWN)
    destinationElement.send_keys(Keys.RETURN)

    # Let's see which flights we can choose from
    submitButton = driver.find_element(By.ID, 'bookFlightForm')
    submitButton.submit()

    departureTimeBase =     '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[2]/div[1]/div[2]/span[1]'
    arrivalTimeBase =       '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/span[1]'
    departureAirportBase =  '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[2]/div[3]/div/span[1]'
    arrivalAirportBase =    '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[2]/div[5]/div/span[1]'
    durationBase =          '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[2]/div[4]/div/div/span[1]'
    economyBase =           '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[2]/div[1]/div[2]/div/div[2]/button/span/div/div[2]/span/span'
    economyRefundableBase = '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[2]/div[2]/div[2]/div/div[2]/button/span/div/div[2]/span/span'
    economyPremiumBase =    '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[2]/div[3]/div[2]/div/div[2]/button/span/div/div[2]/span/span'
    businessClassBase =     '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[2]/div[4]/div[2]/div/div[2]/button/span/div/div[2]/span/span'
    stopsBase =             '//*[@id="flightResults-content"]/div[3]/div[%i]/div/div[1]/div[2]/div/div[1]/div[2]'

    flightObjList = []
    i = 1
    while i < 6: # Just look at the first 5 flights listed on the page.  We probaby don't even care about that many...
        # Create the strings for finding each element on the page
        departureTimeXpath = departureTimeBase %i
        arrivalTimeXpath = arrivalTimeBase %i
        departureAirportXpath = departureAirportBase %i
        arrivalAirportXpath = arrivalAirportBase %i
        durationXpath = durationBase %i
        economyPriceXpath = economyBase %i
        economyRefundablePriceXpath = economyRefundableBase %i
        economyPremiumCostXpath = economyPremiumBase %i
        businessClassPriceBaseXpath = businessClassBase %i
        stopsXpath = stopsBase %i

        time.sleep(10)

        # create objects we can interact with
        departureTimeStr = driver.find_element(By.XPATH, departureTimeXpath).text
        arrivalTimeStr = driver.find_element(By.XPATH, arrivalTimeXpath).text
        departureAirportStr = driver.find_element(By.XPATH, departureAirportXpath).text
        arrivalAirportStr = driver.find_element(By.XPATH, arrivalAirportXpath).text
        durationStr = driver.find_element(By.XPATH, durationXpath).text
        economyPriceStr = driver.find_element(By.XPATH, economyPriceXpath).text
        economyRefundablePriceStr = driver.find_element(By.XPATH, economyRefundablePriceXpath).text
        economyPremiumCostStr = driver.find_element(By.XPATH, economyPremiumCostXpath).text
        businessClassPriceBaseStr = driver.find_element(By.XPATH, businessClassPriceBaseXpath).text
        stopsStr = driver.find_element(By.XPATH, stopsXpath).text

        flightInfoObj = utils.flightInfo(airline = 'United Airlines',
                                         departureClass = utils.departureInfo(departureTime=departureTimeStr, departureAirport=departureAirportStr),
                                         arrivalClass = utils.arrivalInfo(arrivalTime=arrivalTimeStr, arrivalAirport=arrivalAirportStr),
                                         priceClass = utils.priceInformation(economyPrice=economyPriceStr, economyRefundablePrice=economyRefundablePriceStr, economyPremiumPrice=economyPremiumCostStr, businessClassPrice=businessClassPriceBaseStr),
                                         stops = getStops(stopsStr),
                                         duration = getFlightDuration(durationStr),
                                         date = departObj) # Probably will have to change this to handle depart / return dates later

        with open('results.csv', 'a') as f:
            writer_object = writer(f)
            writer_object.writerow([flightInfoObj.airline,
                                    flightInfoObj.departureClass.departureTime,
                                    flightInfoObj.departureClass.departureAirport,
                                    flightInfoObj.arrivalClass.arrivalTime,
                                    flightInfoObj.arrivalClass.arrivalAirport,
                                    flightInfoObj.priceClass.economyPrice,
                                    flightInfoObj.priceClass.economyRefundablePrice,
                                    flightInfoObj.priceClass.economyPremiumPrice, # errors out on third pass, likely due to bad xpath
                                    flightInfoObj.priceClass.businessClassPrice,
                                    flightInfoObj.stops,
                                    flightInfoObj.duration])
            f.close()
        i = i + 1
        if i == 3:
            import pdb
            pdb.set_trace()

    return utils.ERROR_CODE['NO_ERROR']

def getStops(stopsString):
    """Takes a string for the number of stops and returns an integer"""
    if stopsString == 'NONSTOP':
        stops = 0
    else:
        strippedList = re.findall('[0-9]+', stopsString) # returns a value such as ['1']
        stops = int(strippedList[0])

    return stops

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
