# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:14:07 2019

@author: tobia
"""
from bs4 import BeautifulSoup
import requests
import time
import datetime
import numpy as np
import operator
import mysql.connector as MySQLdb

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def alimentarbd(Data1,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    c1=[]
    cur.execute("SELECT datahora FROM ricosurf WHERE esta_id='%s'\
    ORDER BY datahora DESC limit 40" % boia)
    for row in cur.fetchall():
        c1.append(row)
    if c1!=[]:
        for i in range(len(Data1)):
            if Data1[i][1]>max(c1)[0]:
                sql = "INSERT INTO ricosurf (esta_id,datahora,wvht,periodo,tsm,\
                direcao)\
                VALUES (%s, '%s', %s, %s, %s, '%s')" % \
                ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]))
                cur.execute(sql)
                db.commit()
            else: #inserir update
                sql = "UPDATE ricosurf SET esta_id=%s,datahora='%s',wvht=%s,\
                periodo=%s,tsm=%s,direcao='%s'\
                WHERE esta_id=%s and datahora='%s'" % \
                ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
                (Data1[i][4]),(Data1[i][5]),(Data1[i][0]),(Data1[i][1]))
                cur.execute(sql)
                db.commit()
    else:
        for i in range(len(Data1)):
            sql = "INSERT INTO ricosurf (esta_id,datahora,wvht,periodo,tsm,\
            direcao)\
            VALUES (%s, '%s', %s, %s, %s, '%s')" % \
            ((Data1[i][0]),(Data1[i][1]),(Data1[i][2]),(Data1[i][3]),\
            (Data1[i][4]),(Data1[i][5]))
            cur.execute(sql)
            db.commit()

    cur.close()
    db.close()


def buscabd():

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    rico=[]
    cur.execute("SELECT id, nome, site FROM ricosurf_estacao")
    for row in cur.fetchall():
        rico.append(row)
    cur.close()
    db.close()

    return rico


site='https://ricosurf.com.br/boletim-das-ondas/rio-janeiro'

resp=requests.get(site)

soup=BeautifulSoup(resp.text,'html.parser')

#text_file = open('Output.txt', "w")
#text_file.write(str(soup))
#text_file.close()
picosatuais=[]
l=soup.find_all('a', attrs={'class': 'beach-peak col-xxs-12 col-xs-6 col-md-4'})
for i in l:
    l1=i.find('div', attrs={'class': 'place'}).get_text(strip=True)
    picosatuais.append(l1)

#l=soup.find_all('a', attrs={'class': 'beach-peak disabled col-xxs-12 col-xs-6 col-md-4'})
#for i in l:
#    l1=i.find('div', attrs={'class': 'place'}).get_text(strip=True)
#    nome.append(l1)



datahora=time.gmtime(time.time())
ano2=(datahora.tm_year)
mes2=(datahora.tm_mon)
dia2=(datahora.tm_mday)
dia=datetime.date(ano2, mes2, dia2)

rico=buscabd()

wvht,periodo,tsm,direcao,datahora=[],[],[],[],[]

for i in range(len(rico)):
    wvht,periodo,tsm,direcao,datahora=[],[],[],[],[]
    rico_id=[]
    for ii in range(len(picosatuais)):
        if rico[i][1]==picosatuais[ii]:
            print(rico[i][1])
            resp=requests.get(rico[i][2])
            soup=BeautifulSoup(resp.text,'html.parser')
            l=soup.find("div", {"class": "h5 text-primary margin-xxs-bottom"}).get_text(strip=True)
            kk=l
            kk=kk.replace(",", ".")
            wvht.append(float(kk[0:-1]))
            l=soup.find_all('div', attrs={'class': 'h5 no-margin text-primary'})
            kk=l[0].get_text(strip=True)
            kk=kk.replace(",", ".")
            periodo.append(float(kk[0:-1]))
            kk=l[1].get_text(strip=True)
            tsm.append(float(kk[0:-2]))

            l=soup.find("div", {"class": "small line-height-xs"}).get_text(strip=True)
            direcao.append(l)
            datahora.append(dia)
            rico_id.append(rico[i][0])
            data = np.array([rico_id,datahora,wvht,periodo,tsm,direcao])
            data3 = data.transpose()
            alimentarbd(data3,rico[i][0])

            continue

