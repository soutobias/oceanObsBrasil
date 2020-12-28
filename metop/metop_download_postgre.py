import pandas as pd
from datetime import datetime, timedelta


# Funcao de download dos dados
from metop_sat import metop

import sys
import os

sys.path.append(os.environ['HOME'])
import user_config

sys.path.append(user_config.path )
sys.path.append(user_config.path + "/database" )

import db_function as db



# Datas para download :


date_format = '%Y-%m-%dT%H:%M:%SZ'


# Ultimo dado/data de Metop_A
try:
    date_a = db.query_last_data(['type', 'institution'], ['A', 'ascat']).date_time[0]
except:
    date_a = None

if date_a == None: # Caso não exista dados no banco // Primeira carga
    start_date_a = (datetime.now()- timedelta(days = 3)).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    start_date_a = date_a - timedelta(days = 2) # Iniciando o download em x dias antes do último dado (que serão apagados e substituidos pelos novos)
    start_date_a = datetime.strftime(start_date_a, date_format)




# Ultimo dado/data de Metop_B
try:
    date_b = db.query_last_data(['type', 'institution'], ['B', 'ascat']).date_time[0]
except:
    date_b = None

if date_b == None:
    start_date_b = (datetime.now()- timedelta(days = 3)).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    start_date_b = date_b - timedelta(days = 2) # Iniciando o download em x dias antes do último dado (que serão apagados e substituidos pelos novos)
    start_date_b = datetime.strftime(start_date_b, date_format)





# Ultimo dado/data de Metop_C
try:
    date_c = db.query_last_data(['type', 'institution'], ['C', 'ascat']).date_time[0]
except:
    date_c = None

if date_c == None:
    start_date_c = (datetime.now()- timedelta(days = 3)).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    start_date_c = date_c - timedelta(days = 2) # Iniciando o download em x dias antes do último dado (que serão apagados e substituidos pelos novos)
    start_date_c = datetime.strftime(start_date_c, date_format)


# Fim = agora
end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")



# Ids de cada satelite
metop_a_id = 'PODAAC-ASOP2-25X01'
metop_b_id = 'PODAAC-ASOP2-25B01'
metop_c_id = 'PODAAC-ASOP2-25C01'

import os
cwd = os.getcwd()

try:
    ascat_a = metop(metop_a_id, start_date_a, end_date,cwd+'')
    ascat_a.columns = ['date_time', 'lat', 'lon', 'wdir', 'wspd']
    ascat_a["institution"] = 'ascat'
    ascat_a["type"] = 'A'
    db.delete_old_data_no_station(ascat_a)
    db.insert_new_data_no_station(ascat_a)
except:
    print("Algo errado com Metop-A")

try:
    ascat_b = metop(metop_b_id, start_date_b, end_date,cwd+'')
    ascat_b.columns = ['date_time', 'lat', 'lon', 'wdir', 'wspd']
    ascat_b["institution"] = 'ascat'
    ascat_b["type"] = 'B'
    db.delete_old_data_no_station(ascat_b)
    db.insert_new_data_no_station(ascat_b)
except:
    print("Algo errado com Metop-B")

try:
    ascat_c = metop(metop_c_id, start_date_c, end_date,cwd+'')
    ascat_c.columns = ['date_time', 'lat', 'lon', 'wdir', 'wspd']
    ascat_c["institution"] = 'ascat'
    ascat_c["type"] = 'C'
    db.delete_old_data_no_station(ascat_c)
    db.insert_new_data_no_station(ascat_c)
except:
    print("Algo errado com Metop-C")

print("Programa finalizado.")
