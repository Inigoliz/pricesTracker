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

combinations = {"MAD": ["CPH"], "CPH": ["MAD", "DUB", "KRK",
                                        "EDI", "PRG", "TRN", "OPO", "CGN", "CRL", "ALC", "BTS"]}
#combinations = {"MAD": ["CPH"], "CPH": ["DUB", "KRK"]}
#combinations = {"MAD": ["CPH"]}

# Auxiliary functions


def correct_format(d):
    if d < 10:
        return "0" + str(d)
    else:
        return str(d)


def last_day_of_month(year, month):
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


def main_loop():
    monthsAhead = 4
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentDay = datetime.now().day

    datesToCheck = []
    monthsToCheck = []
    year = currentYear

    monthsToCheck = list(range(currentMonth, currentMonth+monthsAhead+1))
    monthsToCheck = [(x-1) % 12+1 for x in monthsToCheck]

    for m in monthsToCheck:
        if m == monthsToCheck[0]:
            for d in range(currentDay, last_day_of_month(year, m)+1):
                datesToCheck.append(str(year) + "-" + correct_format(m) + "-" + correct_format(d))
        elif m == monthsToCheck[-1]:
            for d in range(1, min(currentDay, last_day_of_month(year, m))+1):
                datesToCheck.append(str(year) + "-" + correct_format(m) + "-" + correct_format(d))
        else:
            for d in range(1, last_day_of_month(year, m)+1):
                datesToCheck.append(str(year) + "-" + correct_format(m) + "-" + correct_format(d))
        if m == 12:
            year += 1

    for origin in list(combinations.keys()):
        for destination in combinations[origin]:

            print("Setting up webdriver...")
            print(origin, destination)

            if is_RPi:
                service = Service('/usr/lib/chromium-browser/chromedriver')
            else:
                service = Service(
                    '/Users/tesla/Mis Cosas/Proyectos/pricesTracker/chromedriver')

            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options, service=service)

            prices = {}

            print("Starting iteration...")
            print(origin, destination)

            for date in datesToCheck:
                full_url = f"https://www.ryanair.com/es/es/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut={date}&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata={origin}&destinationIata={destination}&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate={date}&tpEndDate=&tpDiscount=20&tpPromoCode=&tpOriginIata={origin}&tpDestinationIata={destination}"
                # print(full_url)
                driver.get(full_url)
                # print(driver.page_source)

                # With 0.3, 1 result in 2 months was misread
                time.sleep(0.5)

                try:
                    price = driver.find_element(
                        By.XPATH, '//span[@data-e2e="flight-card-price"]').text
                    prices.update({date: price})
                    print('Price on %s: %s' % (date, price))
                except:
                    print('No flight on %s' % date)
                    time.sleep(random.uniform(0.5, 3))

            today = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + \
                str(datetime.now().day) + "at" + str(datetime.now().hour) + \
                "-" + str(datetime.now().minute)

            df = pd.DataFrame(list(prices.items()), columns=['Departure', 'Price'])

            folder = "/data-" + origin + "-" + destination + "/"

            try:
                print(f"Creating folder {origin} to {destination}")
                os.mkdir(file_path + folder)
            except OSError:
                print(f"Folder {origin} to {destination} already exists")
                pass

            print("Writing to file...")
            df.to_csv(file_path + folder + today + ".csv")

            driver.quit()

            time.sleep(1)  # before setting up driver again


if __name__ == '__main__':
    main_loop()
