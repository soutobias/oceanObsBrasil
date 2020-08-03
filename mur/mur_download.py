
import os
import time

from datetime import date, datetime, timedelta


import xarray as xr
import pandas as pd
import numpy as np
# Pontos de coleta:

import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )


# Builded Packages
sys.path.insert(1,'/home/oceanObsBrasil/database')
from databaseMySQL import consulta_data_banco, insere_dado_banco, deleta_dado



# Last date of data to start the download
start_date = consulta_data_banco('mur')


date_format = "%Y%m%d"


if start_date == None:
    start_date = (date.today() - timedelta(days = 5)).strftime(date_format)
else:
    start_date = start_date.strftime(date_format)

end_date = date.today().strftime(date_format)




pontos = pd.read_csv('Pontos MUR - CPTEC.csv',sep=',')

pontos_num = pontos['Ponto']
pontos_lat = pontos['Lat']
pontos_lon = pontos['Lon']

# Transformando lons 0 - 360 para -180 +180
pontos_lon = ((pontos_lon + 180) % 360 - 180)
pontos_lon = pontos_lon.round(2)
pontos_lat = pontos_lat.round(2)



range_coord = 0.00



for p in range(len(pontos_lat)):
    lat_coleta = pontos_lat[p]
    lon_coleta = pontos_lon[p]

    # lon_min lon_max lat_min lat_max

    box_coord = [str(lon_coleta -range_coord),\
     str(lon_coleta + range_coord), \
     str(lat_coleta - range_coord),\
     str(lat_coleta + range_coord)]


    str_coord = ' '.join(box_coord)


    str_download = 'python3.8 mur/subset_mur.py -s %s -f %s -b %s -x MUR-JPL-L4-GLOB-v4.1' % (start_date, end_date,str_coord)

    download_status = os.system(str_download)

    print('Download - Ponto %s OK!' % str(pontos_num[p]))




# Loading data into a xarray
data = xr.open_mfdataset('*.nc', combine = 'by_coords', concat_dim = 'ponto')


dados_df = data.to_dataframe()


###
# Delete Files Downloaded

list_all_files = os.listdir('.')

list_files = [file for file in list_all_files if file.endswith("subset_MUR.nc")]


if list_files:
    for file in list_files:
        os.remove(file)

###



#
# len(dados_df)
#
sst = dados_df['analysed_sst']
sst = pd.DataFrame(sst.loc[pd.notnull(sst)])

# Transformando Index Para Colunas
sst.reset_index(inplace = True)



# Formatando valores :
sst['lat'] = sst['lat'].round(2)
sst['lon'] = sst['lon'].round(2)


# SST Kelvin to Celsius
sst['analysed_sst'] = (sst['analysed_sst'] - 273.15).round(2)

# Rename Columns
sst = sst.rename(columns = {'analysed_sst':'sst', 'time':'datahora'})



# Coletando valores nas localizações exatas dos pontos requisitados:

sst_final = pd.DataFrame()

for p in range(len(pontos_lat)):
    lat_coleta = pontos_lat[p]
    lon_coleta = pontos_lon[p]

    sst_value = sst[(sst['lat'] == lat_coleta) & (sst['lon'] == lon_coleta)]


    sst_final = sst_final.append(sst_value)



sst_final.reset_index(drop= True, inplace=True)




# Data Formatting




sst_final['lat'] = sst_final['lat'].astype(np.float64)
sst_final['lon'] = sst_final['lon'].astype(np.float64)
sst_final['sst'] = sst_final['sst'].astype(np.float64)
sst_final['datahora'] = sst_final['datahora'].apply(lambda data: datetime.strftime(data,"%Y-%m-%d %H:%M:%S"))

print(sst_final)



# Deleting existing data // avoid duplicate

min_date = min(sst_final['datahora'])

condition = "WHERE datahora >= '%s'" % min_date

deleta_dado('mur', condition)

insere_dado_banco('mur', sst_final)






print('Programa MUR finalizado.')
