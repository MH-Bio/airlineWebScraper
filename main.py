from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import csv
import random
import time
import airlineInfo
import dateManagement

# My version of Edge is Version 113.0.1774.42 (Official build) (64-bit)
# useful website: https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python

DEPARTURE_DATE = None
RETURN_DATE = None

driver = webdriver.Edge()
#action = ActionChains(driver) # See: https://www.geeksforgeeks.org/key_down-method-action-chains-in-selenium-python/#

def unitedAirlines(originCode, destinationCode):
    """Gets info from the United Airlines Website"""
    driver.get(airlineInfo.AIRLINE_WEBSITES['United'])

    depart = dateManagement.departureDate(2023, 8, 1)

    departDate = driver.find_element(By.ID, 'DepartDate')
    returnDate = driver.find_elements(By.ID, 'ReturnDate')
    #departStr = '%s %s' % (dateManagement.getMonthStrShort(depart.month), dateManagement.getDayStr(depart.day))
    #departDate.send_keys(departStr)
    #departDate.click()
    #departDate.clear()
    #departDate.send_keys('Aug 20')
    #returnDate.clear()
    #returnDate.send_keys('Aug 27')

    try:
        departDate = driver.find_element(By.CLASS_NAME, 'DateInput_input DateInput_input_1')
    except:

        print('ffo')
        import pdb
        pdb.set_trace()

    asdfDate = driver.find_element(By.ID, 'passengersSlidingInputContainer')

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
