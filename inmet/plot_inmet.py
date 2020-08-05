



import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config
os.chdir( user_config.path )

import pandas as pd
from datetime import datetime
from datetime import date


### DataViz Packages
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy import config
from shapely import geometry
from matplotlib.font_manager import FontProperties

# Builded Packages
sys.path.insert(1,'/home/oceanObsBrasil/database')
from databaseMySQL import consulta_dados




estacoes_meteo = consulta_dados('meteorologia', "SELECT * FROM meteorologia")

coords_meteo = consulta_dados('meteorologia_estacao', "SELECT * FROM meteorologia_estacao")



ids_estacao = estacoes_meteo.id.unique()
datas_max_estacao = estacoes_meteo.groupby(['id'])['datahora'].max()



dados_meteo = pd.DataFrame()

for id in ids_estacao:
    data_max = datas_max_estacao[id]
    dado = estacoes_meteo[(estacoes_meteo['id'] == id) & (estacoes_meteo['datahora'] == data_max)]
    lat_estacao = coords_meteo[coords_meteo['id'] == id]['lat']
    lon_estacao = coords_meteo[coords_meteo['id'] == id]['lon']
    dado = dado.assign(lat = lat_estacao.values[0])
    dado = dado.assign(lon = lon_estacao.values[0])
    dados_meteo = dados_meteo.append(dado)





# Create DATA and HORA to plot tables

dados_meteo['datahora'] = dados_meteo['datahora'].apply(lambda data: data.strftime('%m-%d %H-%M'))

datahora_df = dados_meteo['datahora']

data_df = datahora_df.str.slice(stop =5)
hora_df = pd.DataFrame(datahora_df.str.slice(start = 6))


dados_meteo.insert(1, 'DATA', data_df)
dados_meteo.insert(2, 'HORA', hora_df)


# Converting WindSpeed from meters to seconds to knots :



wspd = dados_meteo['wspd']


estacoes_meteo[estacoes_meteo['wspd']>15]

wspd_km_h = wspd * 3.6
wspd_knots = (wspd_km_h/1.852).round(2)

dados_meteo['wspd'] = wspd_knots



############# MetaAreas Contours ####

lines = open('metareav.txt', 'r')

lat1,lat2,lat3,lat4,lat5,lat6,lat7,lat8,lat9,lat10=[],[],[],[],[],[],[],[],[],[]
lon1,lon2,lon3,lon4,lon5,lon6,lon7,lon8,lon9,lon10=[],[],[],[],[],[],[],[],[],[]
i=1
for line in lines:
    dataline = line.strip()
    columns = dataline.split()
    if columns[0]!='0':
        exec("lat%s.append(float(columns[1]))"%str(i))
        exec("lon%s.append(float(columns[2]))"%str(i))
    else:
        i=i+1




lons = [lon1, lon2, lon3, lon4, lon5, lon6, lon7, lon8, lon9, lon10]
lats = [lat1, lat2, lat3, lat4, lat5, lat6, lat7, lat8, lat9, lat10]



# Limites das áreas para plot

# Area Alfa
lat_a_1=-34
lat_a_2=-28.5
lon_a_1=-55
lon_a_2=-48


# Area Bravo
lat_b_1=-32
lat_b_2=-22
lon_b_1=-49
lon_b_2=-37

# Area Charlie
lat_c_1=-29
lat_c_2=-22
lon_c_1=-49
lon_c_2=-42


# Area Alfa
lat_a_1=-37
lat_a_2=-28
lon_a_1=-55
lon_a_2=-42


# Area Bravo
lat_b_1=-32
lat_b_2=-22
lon_b_1=-49
lon_b_2=-37


# Area Delta
lat_d_1=-27
lat_d_2=-16
lon_d_1=-42
lon_d_2=-32

# Area ECHO
lat_e_1=-22
lat_e_2=-12
lon_e_1=-40
lon_e_2=-32


# Area FOXTROT
lat_f_1=-16
lat_f_2=-3
lon_f_1=-39
lon_f_2=-25


# Area GOLF
lat_g_1 = -6
lat_g_2= 2
lon_g_1=-45
lon_g_2=-28


# Area HOTEL
lat_h_1=-2
lat_h_2= 7
lon_h_1= -53
lon_h_2= -40


# Box Coords das Metareas
# ex: lat_x_1 = min_coord , lat_x_2 = max_coord



metareas = pd.DataFrame({'Area':['Alfa','Bravo','Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf','Hotel'],
                            'Lat_1': [lat_a_1, lat_b_1, lat_c_1, lat_d_1, lat_e_1, lat_f_1,lat_g_1, lat_h_1],
                            'Lat_2': [lat_a_2, lat_b_2, lat_c_2, lat_d_2, lat_e_2, lat_f_2,lat_g_2, lat_h_2],
                            'Lon_1': [lon_a_1, lon_b_1, lon_c_1, lon_d_1, lon_e_1, lon_f_1,lon_g_1, lon_h_1],
                            'Lon_2': [lon_a_2, lon_b_2, lon_c_2, lon_d_2, lon_e_2, lon_f_2,lon_g_2, lon_h_2]})

#







########## PLOTS AREAS ####################





#######################################################
######################## AREA ALFA




area = 0
#fig = plt.figure(figsize=(12,9))
ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area])
ax.set_ylim(metareas['Lat_1'][area] , metareas['Lat_2'][area])
ax.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.1)



ax.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > metareas['Lat_1'][area]) & (dados_meteo['lat'] < metareas['Lat_2'][area])]
dados_area.reset_index(inplace = True)
ax.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

dados_area = dados_area.sort_values(by = 'lat', ascending= True)


# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    if dados_area['id'][pos] == 'A867':
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]-0.7,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))
    else:
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax.margins(0.005,0.005)





### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)



teste_box = [0.5,0.3,0.4,0.22]
#
ax.set_axis_off()
table = ax.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = teste_box)

table.auto_set_font_size(False)
table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)

#table.get_celld()[0,0].get_width()


plt.savefig("estacoes_meteo_alfa.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - ALFA Feita.")


plt.cla()
plt.clf()




#############################################################
######################### AREA CHARLIE #######################





area = 2
#fig = plt.figure(figsize=(12,9))
ax2 = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax2.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area]+1)
ax2.set_ylim(metareas['Lat_1'][area] , metareas['Lat_2'][area])
ax2.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax2.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax2.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.3)



ax2.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax2.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > metareas['Lat_1'][area] + 0.5) & (dados_meteo['lat'] < metareas['Lat_2'][area]-0.9)]
dados_area.reset_index(inplace = True)
ax2.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

# Plotando temp em cada ponto :

for pos in range(len(dados_area)):
    ax2.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax2.margins(0.005,0.005)

dados_area = dados_area.sort_values(by = 'lat', ascending= True)


### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns

# val1 = list(dados_area.datahora)
#
# cols_val = [str(t) for t in val1]
#
# time_cols = [];
# for item in cols_val:
#     new_time = item.replace(" ", "\n")
#     time_cols.append(new_time)


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)

len(values_list[0])


teste_box_charlie = [0.2,0.18,0.8,0.22]
#
ax2.set_axis_off()
table = ax2.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list[0]),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = teste_box_charlie)

table.auto_set_font_size(False)
#table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)


plt.savefig("estacoes_meteo_charlie.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - CHARLIE Feita.")



plt.cla()
plt.clf()


############################################################################################
####################################### AREA DELTA




area = 3

min_lat_lim_delta = metareas['Lat_1'][area] +3.5
max_lat_lim_delta = metareas['Lat_2'][area] -1
min_lon_lim_delta = metareas['Lon_1'][area] - .3
max_lon_lim_delta = metareas['Lon_2'][area] -2



ax3 = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax3.add_feature(cfeature.LAND)
ax3.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax3.set_xlim(min_lon_lim_delta, max_lon_lim_delta)
ax3.set_ylim(min_lat_lim_delta , max_lat_lim_delta)
ax3.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax3.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax3.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.3)



ax3.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > min_lat_lim_delta) & (dados_meteo['lat'] < max_lat_lim_delta) & (dados_meteo['lon']> min_lon_lim_delta)]
dados_area.reset_index(inplace = True)
ax3.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    ax3.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax3.margins(0.005,0.005)

dados_area = dados_area.sort_values(by = 'lat', ascending= True)


### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns

# val1 = list(dados_area.datahora)
#
# cols_val = [str(t) for t in val1]
#
# time_cols = [];
# for item in cols_val:
#     new_time = item.replace(" ", "\n")
#     time_cols.append(new_time)


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)

len(values_list[0])


teste_box_delta= [0.4,0.21,0.4,0.22]
#
ax3.set_axis_off()
table = ax3.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list[0]),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = teste_box_delta)

table.auto_set_font_size(False)
#table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)



plt.savefig("estacoes_meteo_delta.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - DELTA Feita.")

plt.cla()
plt.clf()


##############################################################################
####################################### AREA ECHO ##############################




area = 4

min_lat_lim_echo = metareas['Lat_1'][area] + 3.8
max_lat_lim_echo = metareas['Lat_2'][area] -1





#fig = plt.figure(figsize=(12,9))
ax4 = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax4.add_feature(cfeature.LAND)
ax4.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax4.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area])
ax4.set_ylim(min_lat_lim_echo, max_lat_lim_echo)
ax4.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax4.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax4.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.3)



ax4.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax4.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > min_lat_lim_echo) & (dados_meteo['lat'] < max_lat_lim_echo)]
dados_area.reset_index(inplace = True)
ax4.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    ax4.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax4.margins(0.005,0.005)


dados_area = dados_area.sort_values(by = 'lat', ascending= True)


### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns

# val1 = list(dados_area.datahora)
#
# cols_val = [str(t) for t in val1]
#
# time_cols = [];
# for item in cols_val:
#     new_time = item.replace(" ", "\n")
#     time_cols.append(new_time)


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)

len(values_list[0])


box_echo= [0.4,0.3,0.4,0.22]
#
ax4.set_axis_off()
table = ax4.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list[0]),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = box_echo)

table.auto_set_font_size(False)
#table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)


plt.savefig("estacoes_meteo_echo.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - ECHO Feita.")






plt.cla()
plt.clf()

####################################### AREA FOXTROT




area = 5

min_lat_lim_fox = metareas['Lat_1'][area]+1
min_lon_lim_fox = metareas['Lon_1'][area] -0.5
#fig = plt.figure(figsize=(12,9))
ax5 = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax5.add_feature(cfeature.LAND)
ax5.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax5.set_xlim(min_lon_lim_fox , metareas['Lon_2'][area])
ax5.set_ylim(min_lat_lim_fox , metareas['Lat_2'][area])
ax5.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax5.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax5.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.3)



ax5.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax5.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > metareas['Lat_1'][area]+1) & (dados_meteo['lat'] < metareas['Lat_2'][area]-2)]
dados_area.reset_index(inplace = True)
ax5.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    ax5.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax5.margins(0.005,0.005)



dados_area = dados_area.sort_values(by = 'lat', ascending= True)


### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns

# val1 = list(dados_area.datahora)
#
# cols_val = [str(t) for t in val1]
#
# time_cols = [];
# for item in cols_val:
#     new_time = item.replace(" ", "\n")
#     time_cols.append(new_time)


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)

len(values_list[0])


box_fox= [0.4,0.3,0.8,0.22]
#
ax5.set_axis_off()
table = ax5.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list[0]),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = box_fox)

table.auto_set_font_size(False)
#table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)



plt.savefig("estacoes_meteo_fox.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - FOX Feita.")






#######################################################
######################## AREA GOLF



area = 6

max_lon_lim_golf = metareas['Lon_2'][area]
max_lat_lim_golf = metareas['Lat_2'][area]

#fig = plt.figure(figsize=(12,9))
ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax.set_xlim(metareas['Lon_1'][area] , max_lon_lim_golf)
ax.set_ylim(metareas['Lat_1'][area] , max_lat_lim_golf)
ax.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.1)



ax.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > metareas['Lat_1'][area]) & (dados_meteo['lat'] < metareas['Lat_2'][area]) & (dados_meteo['lon'] > metareas['Lon_1'][area])]
dados_area.reset_index(inplace = True)
ax.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

dados_area = dados_area.sort_values(by = 'lat', ascending= True)


# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    if dados_area['id'][pos] == 'A867':
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]-0.7,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))
    else:
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax.margins(0.005,0.005)





### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)



box_golf = [0.5,0.5,0.4,0.22]
#
ax.set_axis_off()
table = ax.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = box_golf)

table.auto_set_font_size(False)
table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)

#table.get_celld()[0,0].get_width()


plt.savefig("estacoes_meteo_golf.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - GOLF Feita.")


plt.cla()
plt.clf()











#######################################################
######################## AREA HOTEL



area = 7
#fig = plt.figure(figsize=(12,9))
ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(states_provinces, edgecolor='gray')
# ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='0.8'))
ax.set_xlim(metareas['Lon_1'][area] , metareas['Lon_2'][area])
ax.set_ylim(metareas['Lat_1'][area] , metareas['Lat_2'][area])
ax.set_position([0.05,.05,1,1])

# Colocando a zona
gr = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
             linewidth=0.5, color='gray', alpha=0.6, linestyle='--')

gr.top_labels = False
gr.right_labels = False
gr.xlabel_style = {'size':6}
gr.ylabel_style = {'size':6}

# Lines zones

for zona in range(len(lats)):
    ax.plot(lons[zona],lats[zona],linewidth=0.5,color='k', alpha = 0.1)



ax.set_title("Área %s - Estações Meteorológicas" % metareas['Area'][area], loc = 'left')
ax.set_box_aspect(1)


# Colocando os pontos

dados_area = dados_meteo[(dados_meteo['lat'] > metareas['Lat_1'][area]) & (dados_meteo['lat'] < metareas['Lat_2'][area]) & (dados_meteo['lon'] > metareas['Lon_1'][area])]
dados_area.reset_index(inplace = True)
ax.scatter(dados_area['lon'],dados_area['lat'], s = 10, cmap = 'Reds', edgecolor = 'k')

dados_area = dados_area.sort_values(by = 'lat', ascending= True)


# Plotando temp em cada ponto :
## Condicional em Golf para mudar a posição dos valores
for pos in range(len(dados_area)):
    if dados_area['id'][pos] == 'A867':
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]-0.7,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))
    else:
        ax.annotate(dados_area['id'][pos],xy=(dados_area['lon'][pos]+0.15,dados_area['lat'][pos]),color='r',fontsize=5, fontweight = 'bold',bbox=dict(boxstyle="round4,pad=.5", fc="0.9"))


ax.margins(0.005,0.005)





### COLETANDO OS DADOS DA AREA


 ## CRIANDO AS TABELAS :




rows_table = dados_area.columns


rows_val = list(rows_table[2:-3].values)




# Values to String
date = list(dados_area['DATA'])
hora = list(dados_area['HORA'])
atmp = list(dados_area['atmp'].apply(lambda var: str(var)))
humi = list(dados_area['humi'].apply(lambda var: str(var)))
dewp = list(dados_area['dewp'].apply(lambda var: str(var)))
pres = list(dados_area['pres'].apply(lambda var: str(var)))
wspd = list(dados_area['wspd'].apply(lambda var: str(var)))
wdir = list(dados_area['wdir'].apply(lambda var: str(var)))
gust = list(dados_area['gust'].apply(lambda var: str(var)))

# Replace nan by '-'

atmp = [v.replace('nan','-') for v in atmp]
humi = [v.replace('nan','-') for v in humi]
dewp = [v.replace('nan','-') for v in dewp]
pres = [v.replace('nan','-') for v in pres]
wspd = [v.replace('nan','-') for v in wspd]
wdir = [v.replace('nan','-') for v in wdir]
gust = [v.replace('nan','-') for v in gust]


values_list = [date, hora,atmp,humi,dewp, pres, wspd, wdir, gust]

### HEADERS - IDs Stations

ids_station = list(dados_area.id)



box_hotel = [0.5,0.5,0.2,0.22]
#
ax.set_axis_off()
table = ax.table(
    cellText = values_list,
    rowLabels = rows_val,
    colLabels = ids_station,
    rowColours =["lightcyan"] * len(values_list),
    colColours =["lightcyan"] * len(values_list),
    cellColours = [['white'] * len(ids_station)]*len(values_list),
    cellLoc ='center',
    rowLoc = 'center',
    loc = 'best',
    bbox = box_hotel)

table.auto_set_font_size(False)
table.auto_set_column_width([0,1,2,3,4,5,6,7])



# Font Bold

for (row, col), cell in table.get_celld().items():
    cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    if (row==1 or row==2) and col >= 0:
        cell.set_color('k')
        cell.set_alpha(1)
        cell.get_text().set_color('w')


# Header Height

#cellDict = table.get_celld()
#for i in range(len(time_cols)):
#    cellDict[0,i].set_height(0.08)





table.set_fontsize(4)
#table.scale(4,0.5)

#table.get_celld()[0,0].get_width()


plt.savefig("estacoes_meteo_hotel.jpg", dpi = 300, bbox_inches="tight")
print("Figura Estacoes - HOTEL Feita.")


plt.cla()
plt.clf()







print("Script Figuras Estacoes Meteorologicas Finalizado.")
