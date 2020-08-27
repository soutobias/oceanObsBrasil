# -*- coding: utf-8 -*-
"""
Created on Tue May 03 10:08:32 2016

@author: Tobias
"""

import sql_queries
import telnet_download
import sys
import os
from os.path import expanduser
home = expanduser("~")
sys.path.insert(0,home)
import user_config1 as user_config
os.chdir( user_config.path )


buoys = sql_queries.working_buoys(user_config)

for buoy in buoys:
    print(buoy["nome"])
    raw_data = telnet_download.download_raw_data(buoy["argos_id"], user_config)
    sql_queries.insert_raw_data_bd(raw_data, buoy["argos_id"], user_config)
