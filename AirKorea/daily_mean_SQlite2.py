#place and date(1day)

# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
from scipy import stats
import pandas as pd
import os
from pathlib import Path
np.set_printoptions(threshold=100)

import sqlite3
from sqlite3 import Error
 
#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'sqlite/'
infile = 'AirKorea.db'
#write directory(output data)
drout = 'daily_mean1/'

read_file = open(drbase+'observatory.csv','r')
ocodes = read_file.read()
ocodes = ocodes.split('\n')

if not os.path.exists(drbase+drout):
    os.makedirs(drbase+drout)

#def create_connection(drbase+drin+infile):
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

 
def daily_statistics_by_ocode(conn, ocode, day):
    sdatetime = int(day)*100
    edatetime = int(day)*100 +100
    cur = conn.cursor()
    cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime, edatetime))
    rows = cur.fetchall()
    rows = (np.array(rows))
    for i in (4,10):
        sumSO2 = np.sum(rows[:,i].astype(np.float))
        sumCO = np.sum(rows[:,i].astype(np.float))
        sumO3 = np.sum(rows[:,i].astype(np.float))
        sumNO2 = np.sum(rows[:,i].astype(np.float))
        sumPM10 = np.sum(rows[:,i].astype(np.float))
        sumPM25 = np.sum(rows[:,i].astype(np.float))
	with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
		print('%s,,,%s,,,sum,%d,%d,%d,%d,%d,%d,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
			
def main():
	database = '%s%s%s' %(drbase, drin, infile)
	# create a database connection
	conn = create_connection(database)
	with conn:
		for ocode in sorted(ocodes): #read from file
			#ocode = int(ocode)
			#my_file = Path(drbase+drout+'statistics_'+ocode+'.csv')
			my_file = Path('%s%sstatistics_%s.csv' %(drbase,drout,ocode))
			if my_file.is_file(): # csv file already exists in my folder
				print (drbase+drout+'statistics_'+ocode+'.csv exist')
			else:
				with open('%s%sstatistics_%s.csv', 'a' %(drbase,drout,ocode)) as o:
					print('day,Region,RegionCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
				for year in range(2014,2015):
					for Mo in range(1,3):
						for Da in range(1,3):
							daily_statistics_by_ocode(conn,ocode,'%d%02d%02d' %(year,Mo,Da))
 
if __name__ == '__main__':
    main()

