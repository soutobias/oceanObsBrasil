

import pandas as pd
from datetime import datetime, timedelta


# Funcao de download dos dados
from metop_sat import metop
# Funcoes para consultar, inserir e deletar dados no banco
import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

from databaseMySQL import consulta_data_banco, insere_dado_banco, deleta_dado


# Datas para download :


date_format = '%Y-%m-%dT%H:%M:%SZ'


# Ultimo dado/data de Metop_A
date_a = consulta_data_banco(table = 'ascat', filter = 'sat = "A"')

if date_a == None: # Caso não exista dados no banco // Primeira carga
    start_date_a = (datetime.now()- timedelta(days = 4)).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    start_date_a = date_a - timedelta(days = 2) # Iniciando o download em x dias antes do último dado (que serão apagados e substituidos pelos novos)
    start_date_a = datetime.strftime(start_date_a, date_format)




# Ultimo dado/data de Metop_B
date_b = consulta_data_banco(table = 'ascat', filter = 'sat = "B"')

if date_b == None:
    start_date_b = (datetime.now()- timedelta(days = 4)).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    start_date_b = date_b - timedelta(days = 2) # Iniciando o download em x dias antes do último dado (que serão apagados e substituidos pelos novos)
    start_date_b = datetime.strftime(start_date_b, date_format)





# Ultimo dado/data de Metop_C
date_c = consulta_data_banco(table = 'ascat', filter = 'sat = "C"')
if date_c == None:
    start_date_c = (datetime.now()- timedelta(days = 4)).strftime("%Y-%m-%dT%H:%M:%SZ")
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
    ascat_a['sat'] = 'A'
except:
    ascat_a = []
    print("Algo errado com Metop-A")

try:
    ascat_b = metop(metop_b_id, start_date_b, end_date,cwd+'')
    ascat_b['sat'] = 'B'
except:
    ascat_b = []
    print("Algo errado com Metop-B")

try:
    ascat_c = metop(metop_c_id, start_date_c, end_date,cwd+'')
    ascat_c['sat'] = 'C'
except:
    ascat_c = []
    print("Algo errado com Metop-C")





# Unindo os dataframes


list_dataframes = [ascat_a, ascat_b, ascat_c]

ascat_completo = pd.DataFrame()
for df in list_dataframes:
    if len(df) > 3: # Apenas verificando se não é dataframe vazio
        ascat_completo = ascat_completo.append(df, ignore_index = True)




# Deletando dados para sobrescrever

satellites = ascat_completo['sat'].unique()

if 'A' in satellites:
    primeiro_dado = min(ascat_completo['datahora'].loc[ascat_completo['sat'] == 'A',])
    condition = "WHERE datahora >= '%s' and sat = 'A'" % primeiro_dado
    deleta_dado('ascat', condition)

if 'B' in satellites:
    primeiro_dado = min(ascat_completo['datahora'].loc[ascat_completo['sat'] == 'B',])
    condition = "WHERE datahora >= '%s' and sat = 'B'" % primeiro_dado
    deleta_dado('ascat', condition)

if 'C' in satellites:
    primeiro_dado = min(ascat_completo['datahora'].loc[ascat_completo['sat'] == 'C',])
    condition = "WHERE datahora >= '%s' and sat = 'C'" % primeiro_dado
    deleta_dado('ascat', condition)



if not ascat_completo.empty:
    insere_dado_banco('ascat', ascat_completo)
else:
    print("Sem dado algum para inserir.")


print("Programa finalizado.")
