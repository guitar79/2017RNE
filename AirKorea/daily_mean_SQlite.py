#place and date(1day)

# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
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

def create_connection('%s%s%s' %(drbase, drin, infile)):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect('%s%s%s' %(drbase, drin, infile))
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def main():
    database = drbase+drin+infile
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn,1)
 
        print("2. Query all tasks")
        select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()
    
    


def date(n,m):#From n to m-1
    return ((f['측정일시']-n)//(m-n) == 0)
    
def place(n):
    return (f['측정소코드'] == n)

#convert float32 array to string split','
def array2string(x):
    return '\n'.join(','.join('%0.2f' %x for x in y) for y in x)

# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'temp/'
#write directory(output data)
drout = 'daily_mean/'

if not os.path.exists(drbase+drout):
    os.makedirs(drbase+drout)

#make empty dataframe(1,11) with head
#head = ('지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소')
head = ('', '111111', '', '', '', '', '', '', '', '', '')
head = np.array(head)
head = head.reshape(1,11)
f = pd.DataFrame(head)

#set the columns header of empty dataframe(1,11) 
f.columns = (['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소'])

#read data files in input directory 
for i in sorted(os.listdir(drbase+drin)):
    #read csv files
    if i[-4:] == '.csv':
        #make dataframe from reading csv files (like table)
        g = pd.read_csv(drbase+drin+i, encoding='euc_kr')
	#set the columns header of dataframe 
        g.columns = (['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소'])
	# adding all csv files to dataframe
        f = f.append(g,ignore_index=True)

#delete first raw in the dataframe        
f = f.drop(f.index[[0,1]])
#count number of the total data in dataframe
total_datanum = len(f)

#total statistics of total data and make string with ','
total_mean_value = array2string(f.mean().values.reshape(1,11))
total_var_value = array2string(f.var().values.reshape(1,11))
total_std_value = array2string(f.std().values.reshape(1,11))
total_max_value = array2string(f.max().values.reshape(1,11))
total_min_value = array2string(f.min().values.reshape(1,11))

#write files from the total statistics
#with open('%s%sstatistics_total.csv' % (drbase,drout), 'w') as o:
    #print(total_datanum,',','mean,',total_mean_value,'\n','var,',total_var_value,'\n','std,',total_std_value,'\n','max,',total_max_value,'\n','min,',total_min_value,'\n', file=o)

#make observatory code index
#ocode = list(set(np.array(f.ix[:,1])))
ocode = list(set(np.array(f.ix[:,'측정소코드'])))
#count number of the observatory
#onumber = len(ocode)
odate = list(set(np.array(f.ix[:,'측정일시'])//100))

for obs1 in sorted(ocode):
	my_file = Path('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	if my_file.is_file(): # csv file already exists in my folder
		print ('File exists  %s%sstatistics_%s.csv' % (drbase,drout,str(obs1)))
	else:
		with open(('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1))), 'a') as o:
			print('day,Region,RegionCode,RegionName,ObservTime,SO2,CO,O3,NO2,PM10,PM25,Address',file=o)
		output = ''
		for obs2 in sorted(odate):
			fo=f.loc[date(obs2*100+1,obs2*100+25) & place(obs1)]
			#fo=f[f['측정소코드']].isin(obs)
			o_mean_value = array2string(fo.mean().values.reshape(1,11))
			o_var_value = array2string(fo.var().values.reshape(1,11))
			o_std_value = array2string(fo.std().values.reshape(1,11))
			o_max_value = array2string(fo.max().values.reshape(1,11))
			o_min_value = array2string(fo.min().values.reshape(1,11))
            #print data
			output += str(obs2)+','+o_mean_value+'\n'
			output += str(obs2)+','+o_var_value+'\n'
			output += str(obs2)+','+o_std_value+'\n'
			output += str(obs2)+','+o_max_value+'\n'
			output += str(obs2)+','+o_min_value+'\n'
            #obss = str(obs)
		with open(('%s%sstatistics_%s.csv' % (drbase,drout,str(obs1))), 'a') as o:
			print(output, file=o)
