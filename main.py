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

# My version of Edge is Version 113.0.1774.42 (Official build) (64-bit)
# useful website: https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python

DEPARTURE_DATE = None
RETURN_DATE = None
FILENAME = os.path.basename(__file__)

'''
option = EdgeOptions()
option.add_argument("--InPrivate")
'''
driver = webdriver.Edge()
#action = ActionChains(driver) # See: https://www.geeksforgeeks.org/key_down-method-action-chains-in-selenium-python/#
#driver.add_argument("--InPrivate")

_depart_obj = dateManagement.departureDate(2023, 8, 1)
_return_obj = dateManagement.returnDate(2023, 8, 7)


def unitedAirlines(originCode, destinationCode):
    """Gets info from the United Airlines Website"""
    fun_name = _getframe().f_code.co_name
    driver.get(utils.AIRLINE_WEBSITES['United'])

    # click on the "one way" button
    oneWay = driver.find_element(By.XPATH, '//*[@id="bookFlightForm"]/div[1]/fieldset/div/label[2]/span[2]')
    oneWay.click()

    departDate = driver.find_element(By.ID, 'DepartDate')
    returnDate = driver.find_elements(By.ID, 'ReturnDate')
    #departStr = '%s %s' % (dateManagement.getMonthStrShort(_depart_obj.month), dateManagement.getDayStr(_depart_obj.day))
    #departDate.send_keys(departStr)
    departDate.click()
    #departDate.clear()
    #departDate.send_keys('Aug 20')
    #returnDate.clear()
    #returnDate.send_keys('Aug 27')

    # asdfDate = driver.find_element(By.ID, 'passengersSlidingInputContainer')

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

    current_dateTime = dateManagement.currentTime(0,0,0,0,0,0)
    difference_between_months = _depart_obj.month - calendar_default_month_index

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



    #                                              || Jumps around, not sure of pattern yet
    united_date_calculation_base = '/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[%s]/td[%s]'


    depart_week_index_XPathIndex = dateManagement.get_week_of_month(year=_depart_obj.year, month=_depart_obj.month, day=_depart_obj.day)
    depart_weekday_index_XPathIndex = dateManagement.get_day_of_week(year=_depart_obj.year, month=_depart_obj.month, day=_depart_obj.day)

    return_week_index_XPathIndex = dateManagement.get_week_of_month(year=_return_obj.year, month=_return_obj.month, day=_return_obj.day)
    return_weekday_index_XPathIndex = dateManagement.get_day_of_week(year=_return_obj.year, month=_return_obj.month, day=_return_obj.day)

    depart_calendar_selection = united_date_calculation_base %(depart_week_index_XPathIndex, depart_weekday_index_XPathIndex)
    return_calendar_selection = united_date_calculation_base %(return_week_index_XPathIndex, return_weekday_index_XPathIndex)
    #/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[1]/td[3]
    #/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[5]/td[1]

    depart_date_button = driver.find_elements(By.XPATH, depart_calendar_selection)
    depart_date_button[0].click()

    # Select origin airport
    originElement = driver.find_element(By.ID, 'bookFlightOriginInput')
    originElement.clear()  # Clear out United trying to use your current location
    originElement.send_keys(originCode)
    time.sleep(random.uniform(3, 5))
    originElement.send_keys(Keys.DOWN)
    originElement.send_keys(Keys.RETURN)

    destinationElement = driver.find_element(By.ID, 'bookFlightDestinationInput')
    destinationElement.send_keys(destinationCode)
    time.sleep(random.uniform(3, 5))
    destinationElement.send_keys(Keys.DOWN)
    destinationElement.send_keys(Keys.RETURN)

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
        try:
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
        except:
            return utils.ERROR_CODE['WEBSITE_ACCESS_FAILURE']

        flightInfoObj = utils.flightInfo(airline = 'United Airlines',
                                         departureClass = utils.departureInfo(departureTime=departureTimeStr, departureAirport=departureAirportStr),
                                         arrivalClass = utils.arrivalInfo(arrivalTime=arrivalTimeStr, arrivalAirport=arrivalAirportStr),
                                         priceClass = utils.priceInformation(economyPrice=economyPriceStr, economyRefundablePrice=economyRefundablePriceStr, economyPremiumPrice=economyPremiumCostStr, businessClassPrice=businessClassPriceBaseStr),
                                         stops = utils.getStops(stopsStr),
                                         duration = utils.getFlightDuration(durationStr),
                                         date = _depart_obj) # Probably will have to change this to handle depart / return dates later
        flightObjList.append(flightInfoObj)
        i = i + 1

    return flightObjList


if __name__ == '__main__':
    unitedAirlines('NRT','LAX')
