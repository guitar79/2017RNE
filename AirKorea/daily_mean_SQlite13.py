# -*- coding: utf-8 -*-
# Auther guitar79@naver.com
#

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
drout = 'daily_mean2/'
prefix = 'daily_mean'

#read_file = open(drbase+'observatory.csv','r')
#ocodes = read_file.read()
#ocodes = ocodes.split('\n')
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

database = '%s%s%s' %(drbase, drin, infile)
conn = create_connection(database)

with conn:
	ocodecur = conn.cursor()
	ocodecur.execute("SELECT DISTINCT ocode FROM hourly")
	ocodes = ocodecur.fetchall()
	#cur.execute("SELECT DISTINCT ? FROM hourly", (ocode))
	for ocode in sorted(ocodes): #read from file
		#for ocode in sorted(ocodes, reverse=True): #read from file
		#ocode = int(ocode)
		#my_file = Path(drbase+drout+'statistics_'+ocode+'.csv')
		ocode = str(ocode[0])
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
						#ocode = str(ocode[0])
						cur = conn.cursor()
						cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
						rows = cur.fetchall()
						if len(rows) == 0:
							print('result is empty %s from %s to %s' %(ocode, sdatetime,edatetime))
						else:
							print(rows)
							rows = np.array(rows)
							print(rows)
							#print(rows.shape)
							#print(type(rows))
							#s.sum(skipna=True)
							meanSO2 = np.mean(rows[:,4].astype(np.float))
							meanCO = np.mean(rows[:,5].astype(np.float))
							meanO3 = np.mean(rows[:,6].astype(np.float))
							meanNO2 = np.mean(rows[:,7].astype(np.float))
							meanPM10 = np.mean(rows[:,8].astype(np.float))
							meanPM25 = np.mean(rows[:,9].astype(np.float))
							#
							with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
								print('%s,,%s,,mean,%s,%s,%s,%s,%s,%s,' % (day,ocode,meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25), file=o)
