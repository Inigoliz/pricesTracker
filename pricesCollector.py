from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
import random
from datetime import datetime
import os

import pandas as pd

file_path = str(os.path.dirname(os.path.abspath(__file__)))

is_RPi = False

if "pi" in file_path:
    is_RPi = True
else:
    is_RPi = False

print(f'Executing on RapsberryPi = {is_RPi}')

# Auxiliary functions


def formatDay(d):
    if d < 10:
        return "0" + str(d)
    else:
        return str(d)


def lastDayOfMonth(year, month):
    """ Work out the last day of the month """
    last_days = [31, 30, 29, 28, 27]
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date().day
    return None


def mainLoop():
    monthsAhead = 1
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentDay = datetime.now().day

    datesToCheck = []
    monthsToCheck = []
    year = currentYear

    if currentDay != lastDayOfMonth(currentYear, currentMonth):
        monthsToCheck = list(range(currentMonth, currentMonth+monthsAhead+1))
        monthsToCheck = [(x-1) % 12+1 for x in monthsToCheck]

    for m in monthsToCheck:
        if m == monthsToCheck[0]:
            for d in range(currentDay, lastDayOfMonth(year, m)+1):
                datesToCheck.append(str(year) + "-" + str(m) + "-" + formatDay(d))
        elif m == monthsToCheck[-1]:
            for d in range(1, currentDay+1):
                datesToCheck.append(str(year) + "-" + str(m) + "-" + formatDay(d))
        else:
            for d in range(1, lastDayOfMonth(year, m)+1):
                datesToCheck.append(str(year) + "-" + str(m) + "-" + formatDay(d))
        if m == 12:
            year += 1

    if is_RPi:
        service = Service('/usr/lib/chromium-browser/chromedriver')
    else:
        service = Service('/Users/tesla/Mis Cosas/Proyectos/ryanairPricesTracker/chromedriver')

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, service=service)

    url1 = "https://www.ryanair.com/es/es/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut="
    url2 = "&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata=CPH&destinationIata=MAD&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2021-10-30&tpEndDate=&tpDiscount=20&tpPromoCode=&tpOriginIata=CPH&tpDestinationIata=MAD"

    prices = {}
    """
    for date in datesToCheck:
        full_url = url1 + date + url2
        # print(full_url)
        driver.get(full_url)
        # print(driver.page_source)

        # With 0.3, 1 result in 2 months was misread
        time.sleep(0.4)

        try:
            price = driver.find_element(By.XPATH, '//span[@data-e2e="flight-card-price"]').text
            prices.update({date: price})
            # print(f'Price on %s: %s' % (date, price))
        except:
            # print(f'No flight on %s' % date)
            time.sleep(random.uniform(0.5, 3))
"""
    driver.quit()

    today = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + \
        str(datetime.now().day) + "at" + str(datetime.now().hour) + "-" + str(datetime.now().minute)

    df = pd.DataFrame(list(prices.items()), columns=['Departure', 'Price'])
    df.to_csv(file_path + "/data/" + today + ".csv")


if __name__ == '__main__':
    mainLoop()
