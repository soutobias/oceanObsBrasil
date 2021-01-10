# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 02:54:25 2019

@author: tobias
"""

import json
import pandas as pd
import numpy as np

from pandas.io import sql
import sqlalchemy
import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import operator
import requests
import re

import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db

print ("Conectando ao site do epagri")
url="https://ciram.epagri.sc.gov.br/index.php/maregrafos/"

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
#options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.set_preference("dom.disable_beforeunload", True)
options.set_preference("browser.tabs.warnOnClose", False)


driver = webdriver.Firefox(options=options)
print("conectado com sucesso")

driver.get(url)

time.sleep(3)


table_NM = pd.read_html(driver.page_source)
soup=BeautifulSoup(driver.page_source, 'html.parser')

stations = db.select_station(["institution", "data_type"], ["epagri", "tide"]).sort_values(by=['id'])
for i in range(len(stations)):
    # l = soup.find("div", {"id": stations.url[i] }).get_text().split("Mare Obser")[0].strip()
    df = table_NM[i]
    station = stations.id[i]
    df["date_time"] = pd.to_datetime(df.Topping, format='%d/%m %H:%M') + pd.offsets.DateOffset(years=120)

    try:
        del df["BSO"]
    except:
        print("não tem coluna BS0")
    del df["Mare Astron"]
    del df["NMM"]
    del df["Topping"]

    df.columns = ["water_level", "meteorological_tide", "date_time"]

    df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)
    df = df.loc[np.isnan(df.water_level) == False]

    df['station_id'] = station

    db.delete_old_data(df, station)
    db.insert_new_data(df)

    print('dados da epagri '+ str(station) + ' inseridos no banco')

