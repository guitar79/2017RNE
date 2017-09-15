#place and date(1day)
#
# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
import os
import matplotlib.pyplot as plt
np.set_printoptions(threshold=100)
from pathlib import Path
import datetime, random
#from netcdftime import utime
from datetime import  datetime
#cdftime = utime('hours since 0001-01-01 00:00:00')

import sqlite3
from sqlite3 import Error

import pylab

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'

#read directory(input data)
drin = 'sqlite/'
infile = 'AirKorea.db'
#write directory(output data)
drout = 'h_hourly_chart1/'

#make drout if not exist
if not os.path.exists(drbase+drout):
	os.makedirs(drbase+drout)

ocodes = ['111121','131125','131144']
#'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25'

data = 5

def format_date(x, pos=None):
    return dates.num2date(x).strftime('%Y-%m-%d') #use FuncFormatter to format dates

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

print(ocode)
cur = conn.cursor()

for ocode in sorted(ocodes): 
    #cur.execute("SELECT * FROM hourly WHERE ocode=? and datetime>=? and datetime<?", (ocode,sdatetime,edatetime))
    #SELECT `_rowid_`,* FROM `daily` WHERE 1=1 AND `ocode` LIKE '831492' AND `var` LIKE 'mean' ORDER BY `day` ASC LIMIT 0, 50000;
    cur.execute("SELECT * FROM daily WHERE ocode=? and var=? ORDER BY `day` ASC", (ocode,'mean'))
    rows = cur.fetchall()

    if len(rows) == 0:
        print('result is empty %s from %s to %s' %(ocode, sdatetime, edatetime))
    else:
        rows = np.array(rows)
        print(rows)
        print('total number of data: %s' %(len(rows)))
        #
        a=rows[:,0]
        print(rows[:,0])
        stringrows=[0]*len(a)
        xdata=range(len(a))
        for ii in range(len(a)):
            stringrows[ii]=a[ii][:4]+'-'+a[ii][4:6]+'-'+a[ii][6:]
        print(stringrows)
        '''
        In [63]: date = datetime.datetime.strptime("20130125", '%Y%m%d')
        IN [64] date
        Out[64]: datetime.datetime(2013, 1, 25, 0, 0)
        '''
        pylab.figure(1)
        print(rows[:,5])
        pylab.xticks(xdata, stringrows)
        pylab.plot(xdata,rows[:,5],"g")
        pylab.savefig('%s%sdaily_%s_%s.pdf' %(drbase,drout,ocode,data),dpi=300)
        pylab.savefig('%s%sdaily_%s_%s.png' %(drbase,drout,ocode,data),dpi=300)
        pylab.show()
        #plt.scatter(oday,odata)
        #
        
        #ax.w_xaxis.set_major_locator(ticker.FixedLocator(some_dates)) # I want all the dates on my xaxis
        #plt.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        #
        #plt.xlabel('time')
        #plt.ylabel('daily mean concentration')
        #plt.rcParams["figure.figsize"] = (16,9)
        #plt.savefig('%s%sdaily_%s_%s.pdf' %(drbase,drout,ocode,data),dpi=300)
        #plt.savefig('%s%sdaily_%s_%s.png' %(drbase,drout,ocode,data),dpi=300)
        #plt.close()