# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:14:07 2019

@author: tobia
"""

import mysql.connector as MySQLdb

from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import datetime
import operator

import pandas as pd
import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db

print('Entrando no site do ndbc')
site='https://www.ndbc.noaa.gov/box_search.php?lat1=-35.8333&lat2=7&lon1=-55.20&lon2=-20&uom=M&ot=A&time=12'

resp=requests.get(site)

soup=BeautifulSoup(resp.text,'html.parser')

# text_file = open('Output.txt', "w")
# text_file.write(str(soup))
# text_file.close()
nome=[]
print('Baixando os dados')
l=soup.find_all('span', attrs={'style': 'background-color: #f0f8fe'})
nome=[]
for i in l:
    i=i.get_text(strip=True)
    i=i.replace("B", " B")
    i=i.replace("          ", ",")
    i=i.replace("         ", ",")
    i=i.replace("        ", ",")
    i=i.replace("       ", ",")
    i=i.replace("      ", ",")
    i=i.replace("     ", ",")
    i=i.replace("    ", ",")
    i=i.replace("   ", ",")
    i=i.replace("  ", ",")
    i=i.replace(" ", ",")
    x=i.split(",");
    nome.append(x)

l=soup.find_all('span', attrs={'style': 'background-color: #fffff0'})
for i in l:
    k=i.get_text(strip=True)
    i=i.get_text(strip=True)
    i=i.replace("B", " B")
    i=i.replace("          ", ",")
    i=i.replace("         ", ",")
    i=i.replace("        ", ",")
    i=i.replace("       ", ",")
    i=i.replace("      ", ",")
    i=i.replace("     ", ",")
    i=i.replace("    ", ",")
    i=i.replace("   ", ",")
    i=i.replace("  ", ",")
    i=i.replace(" ", ",")
#    i=i.replace("-------", "Null")
#    i=i.replace("------", "Null")
#    i=i.replace("-----", "Null")
#    i=i.replace("----", "Null")
#    i=i.replace("---", "Null")
#    i=i.replace("--", "Null")
#    i=i.replace(",-,", ",Null,")
    x=i.split(",");
    nome.append(x)



variables=['ID','T1','datahora','LAT','LON','WDIR','WSPD','GST','WVHT','DPD','APD','MWD','PRES','PTDY','ATMP','WTMP','DEWP','VIS','TCC','TIDE','S1HT','S1PD','S1DIR','S2HT','S2PD','S2DIR']


datahora=time.gmtime(time.time()-24*3600)
ano1=datahora.tm_year
mes1=datahora.tm_mon
if mes1<10:
    mes1="0"+str(mes1)
else:
    mes1=str(mes1)
dia1=datahora.tm_mday

datahora=time.gmtime(time.time())
ano2=datahora.tm_year
mes2=datahora.tm_mon
if mes2<10:
    mes2="0"+str(mes2)
else:
    mes2=str(mes2)
dia2=datahora.tm_mday
hora2=datahora.tm_hour

for i in range(len(variables)):
    exec("%s=[]"%variables[i])
print('Arrumando os dados')
for ii in range(len(nome)):
    ID.append(nome[ii][0])
    T1.append(nome[ii][1])
    t=int(nome[ii][2])/100
    if t>=hora2+2:
        datahora.append(datetime.datetime.strptime(str(ano1)+"-"+mes1+"-"+str(dia1)+" "+str(int(t))+":00:00", '%Y-%m-%d %H:%M:%S'))
    else:
        datahora.append(datetime.datetime.strptime(str(ano2)+"-"+mes2+"-"+str(dia2)+" "+str(int(t))+":00:00", '%Y-%m-%d %H:%M:%S'))
    LAT.append(float(nome[ii][3]))
    LON.append(float(nome[ii][4]))
    try:
        WDIR.append(float(nome[ii][5]))
    except:
        WDIR.append('NULL')
    try:
        WSPD.append(float(nome[ii][6]))
    except:
        WSPD.append('NULL')
    try:
        GST.append(float(nome[ii][7]))
    except:
        GST.append('NULL')
    try:
        WVHT.append(float(nome[ii][8]))
    except:
        WVHT.append('NULL')
    try:
        DPD.append(float(nome[ii][9]))
    except:
        DPD.append('NULL')
    try:
        APD.append(float(nome[ii][10]))
    except:
        APD.append('NULL')
    try:
        MWD.append(float(nome[ii][11]))
    except:
        MWD.append('NULL')
    try:
        PRES.append(float(nome[ii][12]))
    except:
        PRES.append('NULL')
    try:
        PTDY.append(float(nome[ii][13]))
    except:
        PTDY.append('NULL')

    try:
        ATMP.append(float(nome[ii][14]))
    except:
        ATMP.append('NULL')
    try:
        WTMP.append(float(nome[ii][15]))
    except:
        WTMP.append('NULL')
    try:
        DEWP.append(float(nome[ii][16]))
    except:
        DEWP.append('NULL')
    try:
        VIS.append(float(nome[ii][17]))
    except:
        VIS.append('NULL')
    try:
        TCC.append(float(nome[ii][18]))
    except:
        TCC.append('NULL')
    try:
        TIDE.append(float(nome[ii][19]))
    except:
        TIDE.append('NULL')
    try:
        S1HT.append(float(nome[ii][20]))
    except:
        S1HT.append('NULL')
    try:
        S1PD.append(float(nome[ii][21]))
    except:
        S1PD.append('NULL')
    try:
        S1DIR.append(float(nome[ii][22]))
    except:
        S1DIR.append('NULL')
    try:
        S2HT.append(float(nome[ii][23]))
    except:
        S2HT.append('NULL')
    try:
        S2PD.append(float(nome[ii][24]))
    except:
        S2PD.append('NULL')
    try:
        S2DIR.append(float(nome[ii][25]))
    except:
        S2DIR.append('NULL')


data = np.array([datahora,LAT,LON,WDIR,WSPD,WVHT,DPD,MWD,PRES,ATMP,WTMP,DEWP,S1HT,S1DIR])
data = data.transpose()
data3=sorted(data, key=operator.itemgetter(0))

df = pd.DataFrame(data3)

df.columns = ['date_time', 'lat', 'lon', 'wdir', 'wspd', 'swvht', 'tp', 'wvdir', 'pres', 'atmp', 'sst', 'dewpt', 'swvht_swell', 'wvdir_swell']

df = df.replace(to_replace =['None', 'NULL', ' ', ''], value =np.nan)

df["institution"] = 'ndbc'
df["type"] = 'gts'

print(df)

# Deleting existing data // avoid duplicate
db.delete_old_data_no_station(df)

# Insert new data
db.insert_new_data_no_station(df)


print('Programa finalizado.')

