# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 23:34:44 2019

@author: tobia
"""


import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
import datetime
import operator
import mysql.connector as MySQLdb
import numpy as np

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

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

def alimentarbd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora FROM otherbuoys WHERE esta_id = '%s'\
    ORDER BY datahora DESC limit 20" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:

        if Data1[0][1]>max(c1)[0]:
            sql = "INSERT INTO otherbuoys (esta_id,datahora,mwd,hm0,seapeakdir,\
            seahm0,swellpeakdir,swellhm0,wspd,gust)\
            VALUES (%s, '%s', %s, %s, %s, %s, %s, %s, %s, %s)" % \
            ((Data1[0][0]),(Data1[0][1]),(Data1[0][2]),(Data1[0][3]),\
            (Data1[0][4]),(Data1[0][5]),(Data1[0][6]),(Data1[0][7]),(Data1[0][8]),(Data1[0][9]))
            cur.execute(sql)
            db.commit()
        else: #inserir update
            sql = "UPDATE otherbuoys SET esta_id = %s,datahora='%s',mwd=%s,hm0=%s,seapeakdir=%s,\
            seahm0=%s,swellpeakdir=%s,swellhm0=%s,wspd=%s,gust=%s\
            WHERE esta_id = %s and datahora='%s'" % \
            ((Data1[0][0]),(Data1[0][1]),(Data1[0][2]),(Data1[0][3]),\
            (Data1[0][4]),(Data1[0][5]),(Data1[0][6]),(Data1[0][7]),(Data1[0][8]),(Data1[0][9]),(Data1[0][0]),(Data1[0][1]))
            cur.execute(sql)
            db.commit()
    else:
        sql = "INSERT INTO otherbuoys (esta_id, datahora,mwd,hm0,seapeakdir,\
        seahm0,swellpeakdir,swellhm0,wspd,gust)\
        VALUES (%s, '%s', %s, %s, %s, %s, %s, %s)" % \
        ((Data1[0][0]),(Data1[0][1]),(Data1[0][2]),(Data1[0][3]),(Data1[0][4]),(Data1[0][5]),(Data1[0][6]),(Data1[0][7]),(Data1[0][8]),(Data1[0][9]))

        cur.execute(sql)
        db.commit()
    cur.close()
    db.close()



#launch url
# create a new Firefox session

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
#options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.set_preference("dom.disable_beforeunload", True)
options.set_preference("browser.tabs.warnOnClose", False)
print("conectando ao site do buoy_pernambuco")
driver = webdriver.Firefox(options=options)
print("conectado com sucesso")

driver.get(user_config.pernambuco_url)

time.sleep(10)

esta_id,datahora,mwd,hm0,seapeakdir,seahm0,swellpeakdir,swellhm0=[],[],[],[],[],[],[],[]
wdir,wspd,gust=[],[],[]
print("Obtendo dados de onda")
mwd.append(int(driver.find_element_by_xpath("//div[@id='Box01_1631']").text))

hm0.append(float(driver.find_element_by_xpath("//div[@id='Box01_718']").text))

seapeakdir.append(int(driver.find_element_by_xpath("//div[@id='Box04_1633']").text))

seahm0.append(float(driver.find_element_by_xpath("//div[@id='Box04_1627']").text))

swellpeakdir.append(int(driver.find_element_by_xpath("//div[@id='Box07_1634']").text))

swellhm0.append(float(driver.find_element_by_xpath("//div[@id='Box07_1624']").text))

x=driver.find_element_by_css_selector("#highcharts-15 text:nth-child(10) > tspan").text
el = driver.find_element_by_xpath("//*[contains(text(), 'Latest data')]").text
datahora.append((datetime.datetime.strptime(el[13:], '%Y-%m-%d %H:%M')))
datahora[0]=datahora[0]+datetime.timedelta()
esta_id.append(1)


driver.find_element_by_xpath("//a[contains(text(),'PÍER')]").click()
time.sleep(10)
soup=BeautifulSoup(driver.page_source, 'html.parser')
l=soup.find_all(attrs={'id': 'Box01_arrow'})
x=l[0].path.attrs
x2=x['transform']

x1=re.findall("[+-]?\d+\.\d+",x2)
(intens,direc)=uv2intdir(float(x1[0]),float(x1[1]))
wdir.append(arredondar(direc))

l=soup.find_all(attrs={'id': 'Box01_689'})
x=float(l[0].text)*0.514444
wspd.append(arredondar1(x))
l=soup.find_all(attrs={'id': 'Box01_690'})
x=float(l[0].text)*0.514444
gust.append(arredondar1(x))

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
data = np.array([esta_id,datahora,mwd,hm0,seapeakdir,seahm0,swellpeakdir,swellhm0,wspd,gust])
data = data.transpose()

alimentarbd(data,esta_id[0])
print("Banco de dados alimentado")

