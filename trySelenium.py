from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


import time
import random
from datetime import datetime
import os

import numpy as np
import pandas as pd

path = str(os.path.dirname(os.path.abspath(__file__)))

#service = Service('/Users/tesla/Mis Cosas/Proyectos/ryanairPricesTracker/chromedriver')
service = Service('/usr/lib/chromium-browser/chromedriver') # RPi

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


ryanair = "https://www.ryanair.com/es/es/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2022-01-15&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata=CPH&destinationIata=MAD&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2022-01-15&tpEndDate=&tpDiscount=20&tpPromoCode=&tpOriginIata=CPH&tpDestinationIata=MAD"

driver = webdriver.Chrome(options=options, service=service)
driver.get(ryanair)
print(driver.page_source)
time.sleep(0.4)
h1 = driver.find_element(By.XPATH, '//span[@data-e2e="flight-card-price"]')
print(h1.text)
