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
drout = 'h_annual_mean2/'
prefix = 'h_annual_mean_1file'
#read_file = open(drbase+'observatory.csv','r')
#ocodes = read_file.read()
#ocodes = ocodes.split('\n')
#D=[0,31,28,31,30,31,30,31,31,30,31,30,31]

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
	with open('%s%s%s_all.csv' %(drbase,drout,prefix), 'a') as o:
		print('Month,Region,RegionCode,DataCount,var,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
	for ocode in sorted(ocodes): #read total obs code
		#ocode = str(ocode[0])
		ocode = ocode[0]
		print(ocode)
		for year in range(2014,2017):
			for Mo in range(1,2):
				sdatetime = year*1000000+Mo*10000
				edatetime = sdatetime+1000000
				month=sdatetime/10000
				#ocode = str(ocode[0])
				print(ocode)
				cur = conn.cursor()
				cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
				rows = cur.fetchall()
				if len(rows) == 0:
					print('result is empty %s from %s to %s' %(ocode, sdatetime,edatetime))
				else:
					#print(rows)
					rows = np.array(rows)
					print(rows)
					#print(rows.shape)
					#print(type(rows))
					#s.sum(skipna=True)
					sumSO2 = np.nansum(rows[:,4].astype(np.float))
					sumCO = np.nansum(rows[:,5].astype(np.float))
					sumO3 = np.nansum(rows[:,6].astype(np.float))
					sumNO2 = np.nansum(rows[:,7].astype(np.float))
					sumPM10 = np.nansum(rows[:,8].astype(np.float))
					sumPM25 = np.nansum(rows[:,9].astype(np.float))
					#
					meanSO2 = np.nanmean(rows[:,4].astype(np.float))
					meanCO = np.nanmean(rows[:,5].astype(np.float))
					meanO3 = np.nanmean(rows[:,6].astype(np.float))
					meanNO2 = np.nanmean(rows[:,7].astype(np.float))
					meanPM10 = np.nanmean(rows[:,8].astype(np.float))
					meanPM25 = np.nanmean(rows[:,9].astype(np.float))
					#
					varSO2 = np.nanvar(rows[:,4].astype(np.float))
					varCO = np.nanvar(rows[:,5].astype(np.float))
					varO3 = np.nanvar(rows[:,6].astype(np.float))
					varNO2 = np.nanvar(rows[:,7].astype(np.float))
					varPM10 = np.nanvar(rows[:,8].astype(np.float))
					varPM25 = np.nanvar(rows[:,9].astype(np.float))
					#
					stdSO2 = np.nanstd(rows[:,4].astype(np.float))
					stdCO = np.nanstd(rows[:,5].astype(np.float))
					stdO3 = np.nanstd(rows[:,6].astype(np.float))
					stdNO2 = np.nanstd(rows[:,7].astype(np.float))
					stdPM10 = np.nanstd(rows[:,8].astype(np.float))
					stdPM25 = np.nanstd(rows[:,9].astype(np.float))
					#
					maxSO2 = np.nanmax(rows[:,4].astype(np.float))
					maxCO = np.nanmax(rows[:,5].astype(np.float))
					maxO3 = np.nanmax(rows[:,6].astype(np.float))
					maxNO2 = np.nanmax(rows[:,7].astype(np.float))
					maxPM10 = np.nanmax(rows[:,8].astype(np.float))
					maxPM25 = np.nanmax(rows[:,9].astype(np.float))
					#
					minSO2 = np.nanmin(rows[:,4].astype(np.float))
					minCO = np.nanmin(rows[:,5].astype(np.float))
					minO3 = np.nanmin(rows[:,6].astype(np.float))
					minNO2 = np.nanmin(rows[:,7].astype(np.float))
					minPM10 = np.nanmin(rows[:,8].astype(np.float))
					minPM25 = np.nanmin(rows[:,9].astype(np.float))
					with open('%s%s%s_all.csv' %(drbase,drout,prefix), 'a') as o:
						print('%s,,%s,%s,sum,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
						print('%s,,%s,%s,mean,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25), file	=o)
						print('%s,,%s,%s,var,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),varSO2,varCO,varO3,varNO2,varPM10,varPM25), file=o)
						print('%s,,%s,%s,std,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),stdSO2,stdCO,stdO3,stdNO2,stdPM10,stdPM25), file=o)
						print('%s,,%s,%s,max,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),maxSO2,maxCO,maxO3,maxNO2,maxPM10,maxPM25), file=o)
						print('%s,,%s,%s,min,%s,%s,%s,%s,%s,%s,' % (month,ocode,len(rows),minSO2,minCO,minO3,minNO2,minPM10,minPM25), file=o)