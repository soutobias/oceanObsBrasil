# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 02:54:25 2019

@author: tobia
"""

import json
from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import datetime
import pandas as pd
from pandas.io import sql
import sqlalchemy
import mysql.connector as MySQLdb

import re

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

def deleta_dado(tabela,tempoini,boia):

    db = MySQLdb.connect(host = user_config.host,
                         user = user_config.username,
                         password = user_config.password,
                         database = user_config.database)

    cur=db.cursor()

    cur.execute("DELETE FROm %s WHERE datahora>='%s' AND id = '%s'"% (tabela, tempoini, boia))
    # cur.execute("SELECT wmo FROm deriva_estacao")
    db.commit()
    cur.close()
    db.close()

    return

print ("Conectando ao site do epagri")
url="http://ciram.epagri.sc.gov.br/index.php?option=com_content&view=article&id=2440&Itemid=753"

resp=requests.get(url)
soup=BeautifulSoup(resp.text,'html.parser')
text_file = open('Output.txt', "w")
text_file.write(str(soup))
text_file.close()

x = re.search('updatepage.*\s*</script>', soup.decode('ascii'))
x = x.group(0).replace('},','};').replace("'","\"")

match = re.findall('{.*}', x)[0]

print ("Baixando os dados")
match = match.split(";")
# parse x:

df = pd.DataFrame()
for m in match:
    m = json.loads(m)
    df = pd.concat([df,  pd.DataFrame([m])])

df["id"] = df["estacao"]
df.time = df.time + 3600000 * 3
df.index = df.id
df.time = pd.to_datetime(df.time, unit = 'ms')
df["datahora"] = df["time"]

df = df[['datahora','nivel',\
        'temp', 'vento',\
        'direcaoRajadaNum']]


df_mare = df.loc[df.index > 2000]

df_mare.columns = ['datahora', 'Water_l','Air_Tmp','Wnd_Sp','Wnd_dir_N']

df_mare.Water_l = df_mare.Water_l * 1000

df_mare = df_mare.replace(to_replace =['None', 'NULL', ' ', ''],
                        value =np.nan)

print ("deletando dados antigos")
for i in df_mare.index:
    deleta_dado("maregrafos",str(df_mare.datahora[i]), i)
print ("Dados deletados")

con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                        format(user_config.username,
                                            user_config.password,
                                            user_config.host,
                                            user_config.database))




print ("Alimentando banco de dados")
df_mare.to_sql(con=con, name='maregrafos', if_exists='append')

print ("Banco de dados atualizado")


df_meteoro = df.loc[df.index < 1100]

df_meteoro = df_meteoro.loc[df_meteoro.index > 1040]

df_meteoro = df_meteoro[['datahora','temp', 'vento','direcaoRajadaNum']]

df_meteoro.columns = ['datahora', 'atmp','wspd','wdir']

df_meteoro = df_meteoro.replace(to_replace =['None', 'NULL', ' ', ''],
                        value =np.nan)

print ("deletando dados antigos")
for i in df_meteoro.index:
    deleta_dado("meteorologia",str(df_meteoro.datahora[i]), i)
print ("Dados deletados")


con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                        format(user_config.username,
                                            user_config.password,
                                            user_config.host,
                                            user_config.database))



print ("Alimentando banco de dados")
df_meteoro.to_sql(con=con, name='meteorologia', if_exists='append')

print ("Banco de dados atualizado")
