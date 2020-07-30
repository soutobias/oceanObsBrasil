# Script para download de dados de vento // dir and speed //

# Source: PO.DAAC Drive
# Satelite: Metop-A
# Lifetime: Desde 19/10/2006
# Posição: Low Earth Orbit

# Semi-major axis 	7189 km
# Orbit altitude (mean) 	817 km
# Inclination angle 	98.7°
# Orbital period 	101.3 min
# Orbit 	polar, sun synchronous
# Overflight time 	09:30 am
# Orbits per day 	14.2
# Revisit 	29 days

# Short name : ASCATA-L2-25km
# Persistent ID: PODAAC-ASOP2-25X01

# Mais informações:
# https://www.eumetsat.int/website/home/Satellites/CurrentSatellites/Metop/index.html


#########################################################################################
#########################################################################################
########################################################################################
########################################################################################


def metop(dataset_id, start_date, end_date,down_path, remove_down = True):

    import numpy as np
    # Modulos do pacote podaac
    from podaac import podaac
    from podaac import podaac_utils as utils
    from podaac import drive as drive
    # ----------
    from datetime import datetime
    import os

    import sys
    from os.path import expanduser
    home = expanduser("~")
    sys.path.insert(0,home)
    import user_config



    # Criando as instâncias de classe

    p = podaac.Podaac()
    u = utils.PodaacUtils()

#  Credenciais para autenticacao
    d = drive.Drive(file = '', username = user_config.podaac_user, password = user_config.podaac_psw, webdav_url = 'https://podaac-tools.jpl.nasa.gov/drive/files')


# Limites de coordenadas:

    lat_max = 7
    lat_min = -35
    lon_max = -20
    lon_min = -55

    coords = [str(lon_min), str(lat_min), str(lon_max), str(lat_max)]
    box = ','.join(coords)


    #######################################################
    #######################################################
    #start_date = '2020-06-15T00:00:00Z'
#


    # Procurando se há dados novos:

    newData = p.granule_search(dataset_id = dataset_id,
                            start_time = start_date,
                            end_time = end_date,
                            bbox = box,
                            sort_by = 'timeAsc',
                            items_per_page = '400',
                            _format = 'atom')



    searchStr = 'totalResults'
    nFiles = [str(i) for i in newData.strip().split() if searchStr in i]



    if nFiles == '':
        final_df = []

        return final_df

    else:

        granules = d.mine_drive_urls_from_granule_search(granule_search_response = (str(newData)))

        list_granules = u.mine_granules_from_granule_search(granule_search_response=str(newData))


        ############### Fazendo download de dados inteiros ###########
        # d.download_granules(granule_collection = granules, path = down_path)


        ### Lista das variaveis do dataset, caso seja necessário outras variáveis

        # result_variabels = p.dataset_variables(dataset_id='PODAAC-ASOP2-25X01')


        # Fazendo download de dados já recortados :

        from podaac import l2ss


        l = l2ss.L2SS()


        query = {
            "email": '',
            'query':
            [
                {
                    "compact": "false",
                    "datasetId": dataset_id,
                    "bbox": box,
                    "variables": ["lat","lon","time","wind_speed","wind_dir","wvc_quality_flag"],
                    "granuleIds": list_granules
                }
            ]
        }

        actual_path = os.getcwd()
        os.chdir(down_path)

        l.granule_download(query_string = query)

        ############################ TRATAMENTO DOS DADOS ####################################




        import xarray as xr
        import pandas as pd



        # Abrindo os arquivos e concatenando os valores, sem nenhum tratamento


        wind_flag = pd.DataFrame([], dtype = 'float64')
        wind_dir = pd.DataFrame([], dtype = 'float64')
        wind_speed = pd.DataFrame([], dtype = 'float64')
        wind_time = pd.DataFrame([], dtype = 'float64')
        wind_lat = pd.DataFrame([], dtype = 'float64')
        wind_lon = pd.DataFrame([], dtype = 'float64')




        for i in range(len(list_granules)):
            file = xr.open_dataset('subsetted-' + list_granules[i])
            wind_flag = wind_flag.append(pd.DataFrame(file['wvc_quality_flag'].values))
            wind_dir = wind_dir.append(pd.DataFrame(file['wind_dir'].values))
            wind_speed = wind_speed.append(pd.DataFrame(file['wind_speed'].values))
            wind_time = wind_time.append(pd.DataFrame(file['time'].values))
            wind_lat = wind_lat.append(pd.DataFrame(file['lat'].values))
            wind_lon = wind_lon.append(pd.DataFrame(file['lon'].values))



        # Transformando os dataframes em vetores:
        # Retira coluna com nome "variable", que faz referência ao número da coluna original
        # Nome o Index como "Index" para facilitar junção


        ## TODO: Melhorar este trecho; Verificar uma melhor maneira
        tempo = pd.melt(wind_time, value_name = 'datahora');
        tempo = tempo.drop(columns = 'variable');
        tempo.index.name = 'Index'

        win_dir = pd.melt(wind_dir, value_name = 'wdir');
        win_dir = win_dir.drop(columns = 'variable');
        win_dir.index.name = 'Index'

        win_spe = pd.melt(wind_speed, value_name = 'wspd');
        win_spe = win_spe.drop(columns = 'variable');
        win_spe.index.name = 'Index'

        win_flag = pd.melt(wind_flag, value_name = 'win_flag');
        win_flag = win_flag.drop(columns = 'variable');
        win_flag.index.name = 'Index'

        win_lat = pd.melt(wind_lat, value_name = 'lat');
        win_lat = win_lat.drop(columns = 'variable');
        win_lat.index.name = 'Index'

        win_lon = pd.melt(wind_lon, value_name = 'lon');
        win_lon = win_lon.drop(columns = 'variable');
        win_lon.index.name = 'Index'


        # Lista de todos os dataframes de variáveis
        allData = [tempo, win_lat, win_lon, win_dir, win_spe, win_flag]

        # Unindo os dataframes

        from functools import reduce
        final_df = reduce(lambda left,right: pd.merge(left,right, on = ['Index']), allData)


        # Limpando o dataframe (retirando os pontos em que não há registro de dado):

        # Se os dois parâmetros são NaN, o dado é excluído.
        final_df.dropna(subset = ['wdir', 'wspd'], how = 'all', inplace = True)


        # Retirando valores que possuem flags:

        # Explorando as flags:

        flagMeaning = file['wvc_quality_flag'].flag_meanings
        flagsValues = file['wvc_quality_flag'].flag_masks


        flagMeaning = flagMeaning.split(' ')

        flags = pd.DataFrame({'flagValue':flagsValues, 'flagMeaning':flagMeaning})


        # Apenas dados sem flag
        final_df = final_df[final_df['win_flag'] == 0]

        # Removendo coluna de flag e arrumando o index
        final_df = final_df.drop(columns = 'win_flag')
        final_df = final_df.reset_index(drop=True)


        # formatando os valores para o banco :

        # Arrumando a longitude :
        final_df['lon'] = (final_df['lon'] + 180) % 360 - 180


        # formatando os valores:
        final_df['lat'] = (final_df['lat'].round(4)).astype(np.float64)
        final_df['lon'] = (final_df['lon'].round(4)).astype(np.float64)
        final_df['wdir'] = (final_df['wdir'].round(1)).astype(np.float64)
        final_df['wspd'] = (final_df['wspd'].round(3)).astype(np.float64)
        final_df['datahora'] = final_df['datahora'].apply(lambda data: datetime.strftime(data,"%Y-%m-%d %H:%M:%S"))


        #removendo dados 1990..
        final_df.drop(final_df[final_df['datahora']=='1990-01-01 00:00:00'].index, inplace = True)




        # Removendo arquivos baixados:
        if remove_down == True:
            [os.remove('subsetted-' + x) for x in list_granules]


        # Voltando ao diretorio original
        os.chdir(actual_path)

        print("Dados %s OK!" % dataset_id)

        return final_df
