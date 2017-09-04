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
D=[0,31,28,31,30,31,30,31,31,30,31,30,31]

if not os.path.exists(drbase+drout):
	os.makedirs(drbase+drout)

#def create_connection(drbase+drin+infile):
def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

def isNaN(num):
    return num != num

database = '%s%s%s' %(drbase, drin, infile)
conn = create_connection(database)

with conn:
	for ocode in sorted(ocodes): #read from file
    			#ocode = int(ocode)
			#my_file = Path(drbase+drout+'statistics_'+ocode+'.csv')
		my_file = Path('%s%sstatistics_%s.csv' %(drbase,drout,ocode))
		if my_file.is_file(): # csv file already exists in my folder
			print ('exist %s%sstatistics_%s.csv' %(drbase,drout,ocode))
		else:
			with open('%s%sstatistics_%s.csv'%(drbase,drout,ocode), 'a') as o:
				print('day,Region,RegionCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
			for year in range(2014,2017):
				for Mo in range(1,13):
					for Da in range(1,D[Mo]+1):
						day=year*10000+Mo*100+Da							
						sdatetime = day*100
						edatetime = day*100+100
						ocode = int(ocode)
						cur = conn.cursor()
						cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
						rows = cur.fetchall()
						print(rows)
						rows = np.array(rows)
						print(rows)
						print(rows.shape)
						print(type(rows))
						#s.sum(skipna=True)
						sumSO2 = np.sum(rows[:,4].astype(np.float))
						sumCO = np.sum(rows[:,5].astype(np.float))
						sumO3 = np.sum(rows[:,6].astype(np.float))
						sumNO2 = np.sum(rows[:,7].astype(np.float))
						sumPM10 = np.sum(rows[:,8].astype(np.float))
						sumPM25 = np.sum(rows[:,9].astype(np.float))
						
                        '''
						sumSO2 = np.nansum(rows[:,4].astype(np.float))
						sumCO = np.nansum(rows[:,5].astype(np.float))
						sumO3 = np.nansum(rows[:,6].astype(np.float))
						sumNO2 = np.nansum(rows[:,7].astype(np.float))
						sumPM10 = np.nansum(rows[:,8].astype(np.float))
						sumPM25 = np.nansum(rows[:,9].astype(np.float))'''
						with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
							print('%s,,%s,,sum,%s,%s,%s,%s,%s,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
