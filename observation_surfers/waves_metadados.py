#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:22:52 2019

@author: producao
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import MySQLdb

def bancodedados():

    local="pnboia-uol.mysql.uhserver.com"
    usr="pnboia"
    password="Ch@tasenha1"
    data_base="pnboia_uol"

    return local,usr,password,data_base

lines = open('internet.txt', 'rb')
sta=[]
for line in lines:
    dataline = line.strip()
    columns = dataline.split()
    sta.append(columns[0])


lat=[]
lon=[]
latlon=[]
nome=[]
for url in sta:
    
    print(url);
#open with GET method 
    resp=requests.get(url) 
      
    soup=BeautifulSoup(resp.text,'html.parser')     
    
    latlonglist = soup.find_all(attrs={"data-geo": True})

    for latlong in latlonglist:
        latlon=(latlong['data-geo'])
        [lat1,lon1]=latlon.split("_");
        lat.append(float(lat1))
        lon.append(float(lon1))    
    
    
    l=soup.find_all("td", {"class": "spot_bar"})

    for latlong in l:
        x1=(latlong.get_text(strip=True))
        if x1=='':
            continue
        elif x1[0]=='1' or x1[0]=='2' or x1[0]=='3' or x1[0]=='4' or x1[0]=='5' or x1[0]=='0':
            continue
        else:
            nome.append(x1)

cabecalho=" nome,lat,lon"
data = np.array([nome, lat,lon])
data = data.transpose()
np.savetxt("wave.csv", data,'%s',delimiter=",",header=cabecalho)


(local,usr,password,data_base)=bancodedados()

db = MySQLdb.connect(local,usr,password,data_base)

cur=db.cursor()

for i in range(len(site)):
    sql = "INSERT INTO wavecheck_estacao (nome,lat,lon,site)\
    VALUES ('%s', '%s', '%s', '%s')" % \
    (nome[i],lat[i],lon[i],site[i])
    cur.execute(sql)
    db.commit()

