# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 23:34:44 2019

@author: tobia
"""

import mysql.connector as MySQLdb

import psutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import operator
import requests

import pandas as pd

import mysql.connector as MySQLdb
import numpy as np

from pandas.io import sql
import sqlalchemy

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def deleta_dado(tempoini,boia):

    x=time.gmtime(int(tempoini))
    tempo1=str(x.tm_year)+'-'+str(x.tm_mon).zfill(2)+'-'+str(x.tm_mday).zfill(2)+' 00:00:00'

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    cur.execute("DELETE FROm meteorologia WHERE datahora>='%s' AND id = '%s'"% (tempo1,boia))
    # cur.execute("SELECT wmo FROm deriva_estacao")
    db.commit()
    cur.close()
    db.close()

    return

def boiasfuncionando():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT id FROM inmet_estacao \
    ORDER BY id")
    for row in cur.fetchall():
        c1.append(row)

    return c1

def remove_dup_columns(frame):
     keep_names = set()
     keep_icols = list()
     for icol, name in enumerate(frame.columns):
          if name not in keep_names:
               keep_names.add(name)
               keep_icols.append(icol)
     return frame.iloc[:, keep_icols]


tempoini=str(int(np.ceil(time.time()-3600)))

estacoes = ["A899","A802","A878","A834","A808","A867","A866", "A806", "A868", "A851", "A873", "A712", "A744", "A765", "A767", "A619", "A628", "A602", "A652", "A627", "A667", "A606", "A608", "A620", "A634", "A612", "A422", "A405", "A427", "A437", "A410", "A438", "A401", "A456", "A431", "A409", "A421", "A355", "A303", "A356", "A301", "A320", "A304", "A344", "A317", "A318", "A305", "A359", "A360", "A218", "A217", "A203", "A219", "A226", "A215", "A227", "A249", "A242"]

for estacao in estacoes:
    print(estacao)
    url = "https://tempo.inmet.gov.br/TabelaEstacoes/" + estacao

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    #options.add_argument("--no-sandbox");
    options.add_argument("--disable-dev-shm-usage");
    options.set_preference("dom.disable_beforeunload", True)
    options.set_preference("browser.tabs.warnOnClose", False)


    print("conectando ao site do inmet")
    driver = webdriver.Firefox(options=options)
    print("conectado com sucesso")

    driver.get(url)

    time.sleep(8)

    soup=BeautifulSoup(driver.page_source, 'lxml')

    l=soup.find("table", {"id": "tabela"})
    l1=l.find("tbody", {"class": "tbodyEstacoes"})

    l2 = l1.find_all(attrs={"class": "center"})

    l3 = l1.find_all(attrs={"class": "right"})

    variables = ["data", "hora", "atmp", "humi", "dewp", "pres", "wspd", "wdir", "gust"]
    for i in range(len(variables)):
        exec("%s=[]"%variables[i])

    ii = 0
    for i in l3:
        if ii == 0:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                atmp.append(float(var))
            else:
                atmp.append(np.nan)
            ii += 1
        elif ii == 3:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                humi.append(float(var))
            else:
                humi.append(np.nan)
            ii += 1
        elif ii == 6:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                dewp.append(float(var))
            else:
                dewp.append(np.nan)
            ii += 1
        elif ii == 9:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                pres.append(float(var))
            else:
                pres.append(np.nan)
            ii += 1
        elif ii == 12:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                wspd.append(float(var))
            else:
                wspd.append(np.nan)
            ii += 1
        elif ii == 13:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                wdir.append(float(var))
            else:
                wdir.append(np.nan)
            ii += 1
        elif ii == 14:
            var = (i.get_text(strip=True).replace(',','.'))
            if var != '':
                gust.append(float(var))
            else:
                gust.append(np.nan)
            ii += 1
        elif ii == 16:
            ii = 0
        else:
            ii += 1


    data, hora = [], []
    ii = 0
    for i in l2:
        if ii == 0:
            data.append(i.get_text(strip=True))
            ii += 1
        elif ii == 1:
            hora.append(i.get_text(strip=True)[0:2])
            ii = 0

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


    datahora = []
    for i in range(len(data)):
        datet = datetime.datetime.strptime(data[i] + " " + hora[i], '%d/%m/%Y %H')
        datahora.append(datet.strftime('%Y-%m-%d %H:00:00'))

    df = pd.DataFrame (np.array([datahora,atmp, humi, dewp, pres, wspd, wdir, gust]).transpose())

    df.columns = ['datahora', 'atmp', 'humi', 'dewp', 'pres', 'wspd', 'wdir', 'gust']

    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    df['datahora'] = pd.to_datetime(df.datahora)

    df.index = df['datahora']


    del df['datahora']

    df['id'] = estacao

    x = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
    df = df.loc[df.index < x]

    df = df.loc[df.wspd != 'nan']
    df = df.replace(to_replace =['None', 'NULL',  'nan', ' ', ''],
                            value =np.nan)


    if len(df) != 0:
        deleta_dado(tempoini,estacao)

        con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(user_config.username,
                                                    user_config.password,
                                                    user_config.host,
                                                    user_config.database))

        df.to_sql(con=con, name='meteorologia', if_exists='append')
        print('dados da estacao '+estacao+' inseridos no banco')
    else:
        print('Não há dados para a estação  '+estacao+'!')
