#place and date(1day)

# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
from scipy import stats
import pandas as pd
import os
from pathlib import Path
np.set_printoptions(threshold=10)

import sqlite3
from sqlite3 import Error
 
D=[0,31,28,31,30,31,30,31,31,30,31,30,31]

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'sqlite/'
infile = 'AirKorea.db'
#write directory(output data)
drout = 'daily_mean1/'
if not os.path.exists(drbase+drout):
	os.makedirs(drbase+drout)

read_file = open(drbase+'observatory.csv','r')
ocodes = read_file.read()
ocodes = ocodes.split('\n')

def array2string(x):
    return '\n'.join(','.join('%0.2f' %x for x in y) for y in x)

#def create_connection(drbase+drin+infile):
def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

 
def daily_statistics_by_ocode(conn, ocode, day):
	sdatetime = int(day)*100
	edatetime = int(day)*100 + 100
	ocode = int(ocode)
	cur = conn.cursor()
	cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
	rows = cur.fetchall()
	#print(rows)
	rows = np.array(rows)
	print(rows)
	print(rows.shape)
	print(type(rows))
	f = pd.DataFrame(rows,index=rows[:,0])
	print(f)	
	f.columns = (['','ocode','','date','SO2','CO','O3','NO2','PM10','PM25',''])
	#f.astype('float')
	PM10lalala=np.array([0]*24)
	SO2lalala=np.array([0]*24)
	COlalala=np.array([0]*24)
	O3lalala=np.array([0]*24)
	NO2lalala=np.array([0]*24)
	PM25lalala=np.array([0]*24)
	top1=0
	top2=0
	top3=0
	top4=0
	top5=0
	top6=0
	for i in range(0,24):
		if(f.iloc[i]['PM10']!=''):
			PM10lalala[top1]=float(f.iloc[i]['PM10'])
			top1+=1
		if(f.iloc[i]['SO2']!=''):
			SO2lalala[top2]=1000*float(f.iloc[i]['SO2'])
			top2+=1
		if(f.iloc[i]['CO']!=''):
			COlalala[top3]=1000*float(f.iloc[i]['CO'])
			top3+=1
		if(f.iloc[i]['O3']!=''):
			O3lalala[top4]=1000*float(f.iloc[i]['O3'])	
			top4+=1
		if(f.iloc[i]['NO2']!=''):
			NO2lalala[top5]=1000*float(f.iloc[i]['NO2'])
			top5+=1
		if(f.iloc[i]['PM25']!=''):
			PM25lalala[top5]=float(f.iloc[i]['PM25'])
			top6+=1
	PM10lalala=np.split(PM10lalala,[top1])[0]
	SO2lalala=np.split(SO2lalala,[top2])[0]
	COlalala=np.split(COlalala,[top3])[0]
	O3lalala=np.split(O3lalala,[top4])[0]
	NO2lalala=np.split(NO2lalala,[top5])[0]
	PM25lalala=np.split(PM25lalala,[top6])[0]
	
	meanPM10 = PM10lalala.mean()
	meanSO2=SO2lalala.mean()/1000
	meanCO=COlalala.mean()/1000
	meanO3=O3lalala.mean()/1000
	meanNO2=NO2lalala.mean()/1000
	meanPM25=PM25lalala.mean()

	'''print("%0.7f"% PM10lalala.mean(),  SO2lalala.mean()/1000, COlalala.mean()/1000, O3lalala.mean()/1000 ,NO2lalala.mean()/1000)
	print("%0.7f"% PM10lalala.var(),  SO2lalala.var()/1000, COlalala.var()/1000, O3lalala.var()/1000 ,NO2lalala.var()/1000)
	print("%0.7f"% PM10lalala.std(),  SO2lalala.std()/1000, COlalala.std()/1000, O3lalala.std()/1000 ,NO2lalala.std()/1000)
	print("%0.7f"% PM10lalala.max(),  SO2lalala.max()/1000, COlalala.max()/1000, O3lalala.max()/1000 ,NO2lalala.max()/1000)
	print("%0.7f"% PM10lalala.min(),  SO2lalala.min()/1000, COlalala.min()/1000, O3lalala.min()/1000 ,NO2lalala.min()/1000)'''
	with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
		#print('%s,,%s,,sum,%d,%d,%d,%d,%d,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
		print('%s,,%s,,%s,%d,%d,%d,%d,%d,' % (day,ocode,'mean',meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25), file=o)
	
	
	
	#o_mean_value = array2string(f.mean())
	#o_var_value = array2string(f.var())
	#o_std_value = array2string(f.std())
	#o_max_value = array2string(f.max())
	#o_min_value = array2string(f.min())
	#print(o_mean_value)
	#sumSO2 = np.sum(rows[:,4].astype(np.float))
	#sumCO = np.sum(rows[:,5].astype(np.float))
	#sumO3 = np.sum(rows[:,6].astype(np.float))
	#sumNO2 = np.sum(rows[:,7].astype(np.float))
	#sumPM10 = np.sum(rows[:,8].astype(np.float))
	#sumPM25 = 'nan'
	#sumPM25 = np.sum(rows[:,9].astype(np.float))
    #with open('%s%sstatistics_%s.csv' %(drbase,drout,ocode), 'a') as o:
		#print('%s,,,%s,,,sum,%d,%d,%d,%d,%d,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
			
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
				with open('%s%sstatistics_%s.csv'%(drbase,drout,ocode), 'a') as o:
					print('day,Region,oCode,RegionName,var,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
				for year in range(2014,2015):
					for Mo in range(1,3):
						for Da in range(1,D[Mo]+1):
							daily_statistics_by_ocode(conn,ocode,'%d%02d%02d' %(year,Mo,Da))
 
if __name__ == '__main__':
    main()


'''	o_mean_value = array2string(f.mean().values.reshape(1,11))
	o_var_value = array2string(f.var().values.reshape(1,11))
	o_std_value = array2string(f.std().values.reshape(1,11))
	o_max_value = array2string(f.max().values.reshape(1,11))
	o_min_value = array2string(f.min().values.reshape(1,11))'''

