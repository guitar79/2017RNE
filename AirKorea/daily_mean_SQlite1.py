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
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    sdatetime = day*100
    edatetime = day*100 +100
    cur = conn.cursor()
    cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime, edatetime))
 
    rows = cur.fetchall()
    #print(rows.shape)
    rows = (np.array(rows))
    print(rows.shape)
    print(type(rows))
    for i in (4,11)
        sumSO2 = np.sum(rows[:,i].astype(np.float))
        sumCO = np.sum(rows[:,i].astype(np.float))
        sumO3 = np.sum(rows[:,i].astype(np.float))
        sumNO2 = np.sum(rows[:,i].astype(np.float))
        sumPM10 = np.sum(rows[:,i].astype(np.float))
        sumPM25 = np.sum(rows[:,i].astype(np.float))
    
#    rows = np.matrix(rows)
    #rows = rows.astype(float)
    #o_mean_value = rows.mean(0)
 #   print(rows.shape)
    print(vsum)
    #print(o_mean_value)
    #o_mean_value = rows.mean()
    #print(rows)
    #o_mean_value = np.amin(rows[4],0)
    #print(o_mean_value)

    #head = ('지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소')
    #head = ('region', 'ocode', 'oname', 'datetime', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', 'remark')
    '''daily_all = ()
    for row in rows:
        print(rows)
        #c = np.array(row)
        daily_all += row
    daily_all = np.array(daily_all)
    
    
    #daily_all = daily_all.reshape(rows,11)
    print(daily_all)
    #print(daily_all2)'''

'''('', 111121, '', 2016010101, 0.007, 1, 0.002, 0.076, 77, 53, '')
('', 111121, '', 2016010102, 0.007, 1.1, 0.002, 0.077, 70, 48, '')
('', 111121, '', 2016010103, 0.007, 1.2, 0.002, 0.078, 75, 53, '')
('', 111121, '', 2016010104, 0.006, 1.4, 0.002, 0.078, 77, 53, '')
('', 111121, '', 2016010105, 0.006, 1.5, 0.002, 0.077, 83, 52, '')
('', 111121, '', 2016010106, 0.007, 1.4, 0.002, 0.076, 72, 50, '')
('', 111121, '', 2016010107, 0.007, 1.3, 0.002, 0.074, 72, 46, '')
('', 111121, '', 2016010108, 0.007, 1.3, 0.002, 0.072, 68, 50, '')
('', 111121, '', 2016010109, 0.007, 1.3, 0.003, 0.073, 83, 48, '')
('', 111121, '', 2016010110, 0.007, 1.1, 0.004, 0.067, 92, 48, '')
('', 111121, '', 2016010111, 0.007, 1, 0.004, 0.067, 92, 47, '')
('', 111121, '', 2016010112, 0.008, 1.1, 0.004, 0.072, 88, 52, '')
('', 111121, '', 2016010113, 0.008, 0.7, 0.006, 0.064, 80, 43, '')
('', 111121, '', 2016010114, 0.008, 0.6, 0.008, 0.058, 52, 28, '')
('', 111121, '', 2016010115, 0.007, 0.5, 0.008, 0.057, 52, 28, '')
('', 111121, '', 2016010116, 0.007, 0.3, 0.016, 0.042, 40, 18, '')
('', 111121, '', 2016010117, 0.007, 0.2, 0.015, 0.042, 28, 17, '')
('', 111121, '', 2016010118, 0.007, 0.3, 0.011, 0.048, 32, 17, '')
('', 111121, '', 2016010119, 0.007, 0.3, 0.009, 0.052, 43, 16, '')
('', 111121, '', 2016010120, 0.007, 0.3, 0.004, 0.063, 36, 18, '')
('', 111121, '', 2016010121, 0.007, 0.3, 0.004, 0.063, 35, 16, '')
('', 111121, '', 2016010122, 0.007, 0.4, 0.003, 0.065, 44, 15, '')
('', 111121, '', 2016010123, 0.007, 0.4, 0.004, 0.061, 38, 12, '')
('', 111121, '', 2016010124, 0.007, 0.3, 0.004, 0.059, 37, 16, '')'''

#convert float32 array to string split','
def array2string(x):
    return '\n'.join(','.join('%0.2f' %x for x in y) for y in x)
 
 
def main():
    database = '%s%s%s' %(drbase, drin, infile)
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        for obs1 in sorted(ocode):
            file = Path('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	if my_file.is_file(): # csv file already exists in my folder
		print ('File exists  %s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	else:
		with open(('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1))), 'a') as o:
			print('day,Region,RegionCode,RegionName,ObservTime,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
		for obs2 in sorted(odate):
        
        print("1. Query task by priority:")
        daily_statistics_by_ocode(conn,111121,20160101)
 
        #print("2. Query all tasks")
        #select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()
    
    
    for obs1 in sorted(ocode):
	my_file = Path('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	if my_file.is_file(): # csv file already exists in my folder
		print ('File exists  %s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	else:
		with open(('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1))), 'a') as o:
			print('day,Region,RegionCode,RegionName,ObservTime,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
		for obs2 in sorted(odate):
			fo=f.loc[date(obs2*100+1,obs2*100+25) & place(obs1)]
			#fo=f[f['측정소코드']].isin(obs)
			o_mean_value = array2string(fo.mean().values.reshape(1,11))
			o_var_value = array2string(fo.var().values.reshape(1,11))
			o_std_value = array2string(fo.std().values.reshape(1,11))
			o_max_value = array2string(fo.max().values.reshape(1,11))
			o_min_value = array2string(fo.min().values.reshape(1,11))
            #print data
			output = ''
			output += str(obs2)+','+o_mean_value+'\n'
			output += str(obs2)+','+o_var_value+'\n'
			output += str(obs2)+','+o_std_value+'\n'
			output += str(obs2)+','+o_max_value+'\n'
			output += str(obs2)+','+o_min_value
            #obss = str(obs)
			with open(('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1))), 'a') as o:
				print(output, file=o)