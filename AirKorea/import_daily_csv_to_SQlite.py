#place and date(1day)
'''CREATE TABLE "hourly" (
	`reagion`	TEXT,
	`ocode`	INTEGER,
	`oname`	TEXT,
	`datetime`	INTEGER,
	`SO2`	NUMERIC,
	`CO`	NUMERIC,
	`O3`	NUMERIC,
	`NO2`	NUMERIC,
	`PM10`	NUMERIC,
	`PM25`	NUMERIC,
	`remark`	TEXT
)
'''
# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import os
from pathlib import Path
import sqlite3
from sqlite3 import Error
import csv, sqlite3

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'daily_mean1/'
dbfilename = 'sqlite/AirKorea.db'
#write directory(output data)
#drout = 'daily_mean1/'

con = sqlite3.connect('%s%s'%(drbase,dbfilename)) 
cur = con.cursor()
#cur.execute("CREATE TABLE daily (day,Region,RegionCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address);") # use your column names here
cur.execute("CREATE TABLE daily (`day` INTEGER, `Region` TEXT, `RegionCode` INTEGER, `RegionName` TEXT, `var` TEXT, `SO2` NUMERIC, `CO` NUMERIC, 	`O3` NUMERIC, `NO2` NUMERIC, `PM10` NUMERIC, `PM25` NUMERIC, `Address` TEXT);")
for file in sorted(os.listdir(drbase+drin)):
	#read csv files
	print(file)
	if file[-4:] == '.csv':
		print('start %s' %(file))
		with open('%s%s%s' %(drbase,drin,file),'rt') as fin:
			# csv.DictReader uses first line in file for column headings by default
			dr = csv.DictReader(fin) # comma is default delimiter
			to_db = [(i['day'], i['Region'],i['RegionCode'],i['RegionName'],i['var'],i['SO2'],i['CO'],i['O3'],i['NO2'],i['PM10'],i['PM25'],i['Address']) for i in dr]
			cur.executemany("INSERT INTO daily (day,Region,RegionCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
			con.commit()
		#print('finished %s' % (file))
con.close()
