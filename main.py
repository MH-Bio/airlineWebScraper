from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
import csv
import random
import time
import airlineInfo
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


def unitedAirlines(originCode, destinationCode):
    """Gets info from the United Airlines Website"""
    fun_name = _getframe().f_code.co_name
    driver.get(airlineInfo.AIRLINE_WEBSITES['United'])

    _depart_obj = dateManagement.departureDate(2023, 8, 1)
    _return_obj = dateManagement.returnDate(2023, 8, 7)

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

    '''
    Here is an example of an xpath on the united website
    
    							                        STATIC                STATIC	    STATIC STATIC STATIC	L/R		   WEEK OF MONTH  DAY OF WEEK
    //*[@id="passengersSlidingInputContainer"]/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[5]/td[1]
    
    or possibly this
    /html/body/div[19]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/td[1] where the last two indicies are week of month and day of week (assuming our month is at the top of the list)
    
    In this case L/R refers to the left or right side of the calendar
    The week of the month is the 1st - 5th week
    
    Algorthim for calculating xpath
    1. calculate out how many months in advance the date is
    2. click the right button that many time, the correct month should now be in [2] in the L/R index
    
    3. Calculate the day of the week, place this in the final index
    
    4. Calculate the week of the month.
        -Take the day of the week and set this as week 1
        -Subtract the 7 from the current day until your result is less than or equal to 0
            -The total number of times until you hit the exception is the value for week of the month
    
    '''

    # Find whatever month United is defaulting to

    default_month_xpath = driver.find_element(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[3]') # Should always be on the calendar
    default_month_aria_label = default_month_xpath.get_attribute("aria-label")

    confirmed_default_month = ''
    i = 1
    while i < 12:
        assert i < 13, "Unable to find current month in calendar format date picker.  See: %s, Function: %s()" %(FILENAME, fun_name)
        if dateManagement.getMonthStrLong(i) in default_month_aria_label:
            confirmed_default_month = dateManagement.getMonthStrLong(i)
            break
        else:
            i = i + 1

    print(confirmed_default_month)
    current_dateTime = dateManagement.currentTime(0,0,0,0,0,0)
    difference_between_months = _depart_obj.month - current_dateTime.currentMonth

    prev_month_button = driver.find_elements(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[1]/button[1]')
    next_month_button = driver.find_elements(By.XPATH, '/html/body/div[14]/div/div/div/div[1]/div[2]/div[1]/button[2]')

    retry_counter = 0

    i = 1 # remember we are counting the current month as month 1
    while i < difference_between_months:
        if retry_counter > 10:
            break
        time.sleep(random.uniform(1, 3))
        try:
            next_month_button[0].click() # advance one month
            i = i + 1
        except:
            print('clicking next button on calendar didn\'t work.  Trying again')
            retry_counter = retry_counter + 1

    #                                              || Jumps around, not sure of pattern yet
    united_date_calculation_base = '/html/body/div[14]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div/table/tbody/tr[%s]/td[%s]'


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
    #depart_date_button.click()

    import pdb
    pdb.set_trace()

    destinationElement = driver.find_element(By.ID, 'bookFlightDestinationInput')
    destinationElement.send_keys(destinationCode)
    time.sleep(random.uniform(3, 5))
    destinationElement.send_keys(Keys.DOWN)
    destinationElement.send_keys(Keys.RETURN)

    originElement = driver.find_element(By.ID, 'bookFlightOriginInput')
    originElement.clear() # Clear out United trying to use your current location


    originElement.send_keys(originCode)

    time.sleep(random.uniform(3, 5))
    originElement.send_keys(Keys.DOWN)
    originElement.send_keys(Keys.RETURN)

    submitButton = driver.find_element(By.ID, 'bookFlightForm')
    #submitButton.submit()
    while(1):
        time.sleep(10)

if __name__ == '__main__':
    unitedAirlines('NRT','LAX')
