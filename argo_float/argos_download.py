


import pandas as pd
from datetime import datetime as dt

from argopy import DataFetcher as ArgoDataFetcher

import pathlib
import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)

current_path = pathlib.Path(os.getcwd())
parent_path = str(current_path.parents[0])


# Builded Packages
sys.path.insert(1,parent_path + '/database')
from databaseMySQL import consulta_data_banco, insere_dado_banco, deleta_dado


import user_config
os.chdir( user_config.path )




# List of ARGOs buoy launched by Navy Hidrographyc Center
# WMO ARGOS NUMBERs
list_argos = list([5903118,5903126,5903130,5903131,5903132,5903133,5903134,5903135])



# Details of Launched:

time_format = "%Y-%m-%d %H:%M:%S"


argo1 = ('5903118', dt.strptime('2014-11-13 18:45:00',time_format), -33.965,
        -50.295, 'NOc Antares',dt.strptime('2017-01-23 06:36:00',time_format))

argo2 = ('5903126', dt.strptime('2014-11-12 19:00:00',time_format), -35.581,
        -48.4535, 'NOc Antares', dt.strptime('2017-01-07 06:47:00',time_format))


argo3 = ('5903130', dt.strptime('2015-04-26 17:25:00',time_format), -34.9833,
        -35.0167, 'NHo Cruzeiro do Sul',dt.strptime('2017-05-27 06:37:00',time_format))


argo4 = ('5903131', dt.strptime('2015-05-08 12:05:00',time_format), -29.9867,
        -40.0533, 'NHo Cruzeiro do Sul', dt.strptime('2017-06-08 06:33:00',time_format))


argo5 = ('5903132', dt.strptime('2015-11-19 16:48:00',time_format), -4.988,
        -31.3971, 'NPqHo Vital de Oliveira', dt.strptime('2019-03-05 06:18:00', time_format))


argo6 = ('5903133', dt.strptime('2015-11-22 18:29:00',time_format), -14.2381,
        -36.2003, 'NPqHO Vital de Oliveira', dt.strptime('2019-03-08 06:15:00', time_format))


argo7 = ('5903134', dt.strptime('2015-10-12 21:10:00',time_format), -33.9883,
        -49.3886, 'NOc Antares', dt.strptime('2019-05-26 06:51:00', time_format))


argo8 = ('5903135', dt.strptime('2015-10-15 17:40:00',time_format), -41.212,
        -56.244, 'NOc Antares', dt.strptime('2017-11-15 06:25:00',time_format))


buoys = [argo1, argo2, argo3, argo4, argo5, argo6, argo7, argo8]


columns_details = ['argo_id', 'start_date', 'latitude', 'longitude', 'ship_plataform', 'last_date']
argos_details = pd.DataFrame.from_records(buoys, columns = columns_details)



### Download data from ARGO platform

argo_loader = ArgoDataFetcher()


argo_teste = argo_loader.float(list_argos)

df_argo = argo_teste.to_dataframe()


df_argo_final = df_argo[['CYCLE_NUMBER', 'DIRECTION', 'PLATFORM_NUMBER','PRES','PSAL','TEMP','TIME','LONGITUDE','LATITUDE']]


df_argo_final.loc[:,['PSAL','TEMP']] = df_argo_final[['PSAL','TEMP']].apply(lambda x: pd.Series.round(x, 3))


### INSERTING DATA ON database

# 1 -- ARGO INFO




import sqlalchemy
from sqlalchemy.engine.reflection import Inspector


con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                        format(user_config.username,
                                            user_config.password,
                                            user_config.host,
                                            user_config.database))





table = 'argo_info'
# To insert new data, uncomment below:
# argos_details.to_sql(con=con, name= table, if_exists='append', index = False)



# 2 -- ARGO DATA
df_argo_final.rename(columns = {'PLATFORM_NUMBER':'argo_id',
                                'CYCLE_NUMBER':'cycle_number',
                                'TIME':'date_time',
                                'DIRECTION':'direction',
                                'LATITUDE':'latitude',
                                'LONGITUDE':'longitude',
                                'PRES':'press',
                                'PSAL':'psal',
                                'TEMP': 'temp'}, inplace = True)

table = 'argo_data'
# To insert new data, uncomment below:
# df_argo_final.to_sql(con=con, name= table, if_exists='replace', index = False)
