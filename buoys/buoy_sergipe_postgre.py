# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 23:34:44 2019

@author: tobia
"""

import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
import operator
import numpy as np

import pandas as pd
import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db

def arredondar(num):
    return float( '%.0f' % ( num ) )

def arredondar1(num):
    return float( '%.1f' % ( num ) )


def uv2intdir(u, v):

    from numpy import arctan,rad2deg,arcsin

    if u>0 and v>0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=90-rad2deg(arctan(v/u))
    elif u<0 and v>0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(arcsin(v/(-u)))+270
    elif u<0 and v<0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=270-rad2deg(arctan((-v)/(-u)))
    elif u>0 and v<0:
        intensidade=np.sqrt((u*u)+(v*v))
        direcao=rad2deg(arctan((-v)/u))+90
    elif u==0 and v==0:
        intensidade=0
        direcao=0
    elif u==0 and v>0:
        intensidade=v
        direcao=0
    elif u==0 and v<0:
        intensidade=v
        direcao=180
    elif u>0 and v==0:
        intensidade=u
        direcao=90
    elif u<0 and v==0:
        intensidade=u
        direcao=270

    return intensidade,direcao

# create a new Firefox session
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
# #options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage")
options.set_preference("dom.disable_beforeunload", True)
options.set_preference("browser.tabs.warnOnClose", False)
print("conectando ao site do buoy_sergipe")
driver = webdriver.Firefox(options=options)
print("conectado com sucesso")

driver.get(user_config.sergipe_url)

time.sleep(6)
print("digitando usuario")
driver.find_element_by_css_selector("#id_username").send_keys(user_config.sergipe_user)
print("digitando senha")
driver.find_element_by_css_selector("#id_password").send_keys(user_config.sergipe_psw)
print("clicando em ok")
driver.find_element_by_css_selector("#wp-submit").click()

time.sleep(6)


print("Obtendo dados de onda")

number = 0  # first frame
driver.switch_to.frame(number)

soup=BeautifulSoup(driver.page_source, 'lxml')

try:
    mwd=float(soup.find("div", {"id": "Box02_1560"}).get_text(strip=True))
except:
    mwd=None
try:
    hm0=float(soup.find("div", {"id": "Box02_1544"}).get_text(strip=True))
except:
    hm0=None
try:
    wspd=float(soup.find("div", {"id": "Box11_0_1555"}).get_text(strip=True))
except:
    wspd=None
try:
    gust=float(soup.find("div", {"id": "Box01_1564"}).get_text(strip=True))
except:
    gust=None
try:
    seahm0=float(soup.find("div", {"id": "Box11_0_1551"}).get_text(strip=True))
except:
    seahm0=None
try:
    seapeakperiod=float(soup.find("div", {"id": "Box11_0_1553"}).get_text(strip=True))
except:
    seapeakperiod=None
try:
    seapeakdir=float(soup.find("div", {"id": "Box11_0_1552"}).get_text(strip=True))
except:
    seapeakdir=None
try:
    swellhm0=float(soup.find("div", {"id": "Box11_0_1548"}).get_text(strip=True))
except:
    swellhm0=None
try:
    swellpeakperiod=float(soup.find("div", {"id": "Box11_0_1550"}).get_text(strip=True))
except:
    swellpeakperiod=None
try:
    swellpeakdir=float(soup.find("div", {"id": "Box11_0_1549"}).get_text(strip=True))
except:
    swellpeakdir=None

data=soup.find("div", {"id": "Box11_h0"}).get_text(strip=True)
data1=time.gmtime(time.time()-3600*3)

datahora1=str(data1.tm_year)+'-'+str(data1.tm_mon)+'-'+str(data1.tm_mday)+' '+data
datahora=datetime.datetime.strptime(datahora1, '%Y-%m-%d %H:%M')
datahora=datahora+datetime.timedelta()
esta_id=2

if wspd!=None:
    wspd=wspd*0.514444
    wspd=(arredondar1(wspd))
if gust!=None:
    gust=gust*0.514444
    gust=(arredondar1(gust))

driver_process = psutil.Process(driver.service.process.pid)
#driver.quit()

if driver_process.is_running():
    print ("driver is running")

    firefox_process = driver_process.children()
    if firefox_process:
        firefox_process = firefox_process[0]

        if firefox_process.is_running():
            print("Firefox is still running, we can quit")
            driver.quit()
        else:
            print("Firefox is dead, can't quit. Let's kill the driver")
            firefox_process.kill()
    else:
        print("driver has died")

print("alimentando banco de dados")
data = np.array([[datahora, mwd, hm0, seapeakdir, seahm0, swellpeakdir, swellhm0, wspd, gust]])
df = pd.DataFrame(data)

df.columns = ['date_time', 'wvdir', 'swvht', 'wvdir_sea', 'swvht_sea', 'wvdir_swell', 'swvht_swell', 'wspd', 'gust']

station = db.select_station(['institution', 'name'], ['hidromares', 'celse']).id[0]

df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)

df['station_id'] = station

db.delete_old_data(df, station)
db.insert_new_data(df)
