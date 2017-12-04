# -*- coding: utf-8 -*-
# Auther guitar79@naver.com
#

import numpy as np
from scipy import stats
import pandas as pd
import os
from pathlib import Path
np.set_printoptions(threshold=100)

import pymysql
import pymysql.cursors

#define day numbers of each month
D=[0,31,28,31,30,31,30,31,31,30,31,30,31]

#mariaDB info
db_user = 'modis'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
drout = 'daily_mean3/'
if not os.path.exists(drbase+drout):
    os.makedirs(drbase+drout)
#db connect
conn= pymysql.connect(host='localhost',user=db_user,password=db_pass,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#all ocode read!!
ocodecur = conn.cursor()
ocodecur.execute("SELECT DISTINCT ocode FROM hourly")
ocodes = ocodecur.fetchall()
#print(len(ocodes))
res = []
for i in range(len(ocodes)):
    res.append(ocodes[i]['ocode'])
ocodes=res

#ocodes = ocodes
	#cur.execute("SELECT DISTINCT ? FROM hourly", (ocode))
for ocode in sorted(ocodes):
    ocode = str(ocode)
    for year in range(2014,2017):
        for Mo in range(1,13):
            for Da in range(1,D[Mo]):
                day=year*10000+Mo*100+Da
                sdatetime = day*100
                edatetime = day*100+100
                #print(ocode,sdatetime,edatetime)
                cur = conn.cursor()
                cur.execute("SELECT * FROM hourly WHERE ocode=%s and otime>=%s and otime<%s", (ocode,sdatetime,edatetime))
                rows = cur.fetchall()
                if len(rows) == 0:
                    print('data is empty %s from %s to %s' %(ocode, sdatetime,edatetime))
                else:
                    #print(rows)
                    new_rows = []
                    for i in range(len(rows)):
                        new_rows.append(list(rows[i].values()))
                    rows = np.array(new_rows)
                    print(rows)
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
                    with open('%s%sdaily_%s.csv' %(drbase,drout,ocode), 'a') as o:
                        print('%s,,%s,,sum,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25,len(rows)), file=o)
                        print('%s,,%s,,mean,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25,len(rows)), file	=o)
                        print('%s,,%s,,var,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,varSO2,varCO,varO3,varNO2,varPM10,varPM25,len(rows)), file=o)
                        print('%s,,%s,,std,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,stdSO2,stdCO,stdO3,stdNO2,stdPM10,stdPM25,len(rows)), file=o)
                        print('%s,,%s,,max,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,maxSO2,maxCO,maxO3,maxNO2,maxPM10,maxPM25,len(rows)), file=o)
                        print('%s,,%s,,min,%s,%s,%s,%s,%s,%s,%s,' % (day,ocode,minSO2,minCO,minO3,minNO2,minPM10,minPM25,len(rows)), file=o)