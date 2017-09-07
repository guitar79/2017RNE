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
    #for ocode in sorted(ocodes, reverse=True): #read from file
    	#ocode = int(ocode)
	#my_file = Path(drbase+drout+'statistics_'+ocode+'.csv')
		my_file = Path('%s%sstatistics_%s.csv' %(drbase,drout,ocode))
		if my_file.is_file(): # csv file already exists in my folder
			print ('exist %s%sstatistics_%s.csv' %(drbase,drout,ocode))
		else:
			with open('%s%sstatistics_%s.csv'%(drbase,drout,ocode), 'a') as o:
				print('day,Region,RegionCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
			for year in range(2016,2013,-1):
				for Mo in range(12,0,-1):
					for Da in range(D[Mo],0,-1):
						day=year*10000+Mo*100+Da							
						sdatetime = day*100
						edatetime = day*100+100
						ocode = int(ocode)
						cur = conn.cursor()
						cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
						rows = cur.fetchall()
						#print(rows)
						rows = np.array(rows)
						#print(rows)
						#print(rows.shape)
						#print(type(rows))
						#s.sum(skipna=True)
						sumSO2 = np.sum(rows[:,4].astype(np.float))
						sumCO = np.sum(rows[:,5].astype(np.float))
						sumO3 = np.sum(rows[:,6].astype(np.float))
						sumNO2 = np.sum(rows[:,7].astype(np.float))
						sumPM10 = np.sum(rows[:,8].astype(np.float))
						sumPM25 = np.sum(rows[:,9].astype(np.float))
						#
						meanSO2 = np.mean(rows[:,4].astype(np.float))
						meanCO = np.mean(rows[:,5].astype(np.float))
						meanO3 = np.mean(rows[:,6].astype(np.float))
						meanNO2 = np.mean(rows[:,7].astype(np.float))
						meanPM10 = np.mean(rows[:,8].astype(np.float))
						meanPM25 = np.mean(rows[:,9].astype(np.float))
						#
						varSO2 = np.var(rows[:,4].astype(np.float))
						varCO = np.var(rows[:,5].astype(np.float))
						varO3 = np.var(rows[:,6].astype(np.float))
						varNO2 = np.var(rows[:,7].astype(np.float))
						varPM10 = np.var(rows[:,8].astype(np.float))
						varPM25 = np.var(rows[:,9].astype(np.float))
						#
						stdSO2 = np.std(rows[:,4].astype(np.float))
						stdCO = np.std(rows[:,5].astype(np.float))
						stdO3 = np.std(rows[:,6].astype(np.float))
						stdNO2 = np.std(rows[:,7].astype(np.float))
						stdPM10 = np.std(rows[:,8].astype(np.float))
						stdPM25 = np.std(rows[:,9].astype(np.float))
						#
						maxSO2 = np.max(rows[:,4].astype(np.float))
						maxCO = np.max(rows[:,5].astype(np.float))
						maxO3 = np.max(rows[:,6].astype(np.float))
						maxNO2 = np.max(rows[:,7].astype(np.float))
						maxPM10 = np.max(rows[:,8].astype(np.float))
						maxPM25 = np.max(rows[:,9].astype(np.float))
						#
						minSO2 = np.min(rows[:,4].astype(np.float))
						minCO = np.min(rows[:,5].astype(np.float))
						minO3 = np.min(rows[:,6].astype(np.float))
						minNO2 = np.min(rows[:,7].astype(np.float))
						minPM10 = np.min(rows[:,8].astype(np.float))
						minPM25 = np.min(rows[:,9].astype(np.float))
						with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
							print('%s,,%s,,sum,%s,%s,%s,%s,%s,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
							print('%s,,%s,,mean,%s,%s,%s,%s,%s,%s,' % (day,ocode,meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25), file=o)
							print('%s,,%s,,var,%s,%s,%s,%s,%s,%s,' % (day,ocode,varSO2,varCO,varO3,varNO2,varPM10,varPM25), file=o)
							print('%s,,%s,,std,%s,%s,%s,%s,%s,%s,' % (day,ocode,stdSO2,stdCO,stdO3,stdNO2,stdPM10,stdPM25), file=o)
							print('%s,,%s,,max,%s,%s,%s,%s,%s,%s,' % (day,ocode,maxSO2,maxCO,maxO3,maxNO2,maxPM10,maxPM25), file=o)
							print('%s,,%s,,min,%s,%s,%s,%s,%s,%s,' % (day,ocode,minSO2,minCO,minO3,minNO2,minPM10,minPM25), file=o)
