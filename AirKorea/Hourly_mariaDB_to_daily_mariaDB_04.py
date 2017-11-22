'''-*- coding: utf-8 -*-
 Auther guitar79@naver.com
'''
#np.set_printoptions(threshold=100)

import numpy as np
import os
import multiprocessing as proc
import pymysql
#import pymysql.cursorsv
from datetime import datetime

start_time=str(datetime.now())


#define day numbers of each month
D=[0,31,29,31,30,31,30,31,31,30,31,30,31]

#mariaDB info
db_host = '10.114.0.121'
db_user = 'root'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea'
tb_hourly = 'hourly_vc'
tb_daily = 'daily_all_vc'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
drout = 'daily_mean3/'
if not os.path.exists(drbase+drout):
    os.makedirs(drbase+drout)
#db connect
conn= pymysql.connect(host=db_host,user=db_user,password=db_pass,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#all ocode read!!
cur = conn.cursor()
print("SELECT DISTINCT ocode from %s ORDER BY ocode ASC " %(tb_hourly))
cur.execute("SELECT DISTINCT ocode from %s ORDER BY ocode ASC " %(tb_hourly))
ocodes = cur.fetchall()
#print(len(ocodes))
res = []
for i in range(len(ocodes)):
    res.append(ocodes[i]['ocode'])
ocodes=res
#ocodes = ocodes
#cur.execute("SELECT DISTINCT ? FROM hourly", (ocode))
#s = 0
def check_none(x):
    if np.isnan(x): return "NULL"
    return x

def Work(all_rows, ocode):
    pos = 0
    for year in range(2014,2017):
        for Mo in range(1,13):
            for Da in range(1,D[Mo]+1):
                day=year*10000+Mo*100+Da
                sdatetime = day*100
                edatetime = day*100+100
                rows = []
                while pos<len(all_rows):
                    new_row = all_rows[pos]
                    if new_row['otime']>edatetime:break
                    else: rows.append(new_row)
                    pos = pos + 1
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
                    sumSO2 = check_none(np.sum(rows[:,4].astype(np.float)))
                    sumCO = check_none(np.sum(rows[:,5].astype(np.float)))
                    sumO3 = check_none(np.sum(rows[:,6].astype(np.float)))
                    sumNO2 = check_none(np.sum(rows[:,7].astype(np.float)))
                    sumPM10 = check_none(np.sum(rows[:,8].astype(np.float)))
                    sumPM25 = check_none(np.sum(rows[:,9].astype(np.float)))
                    #
                    meanSO2 = check_none(np.mean(rows[:,4].astype(np.float)))
                    meanCO = check_none(np.mean(rows[:,5].astype(np.float)))
                    meanO3 = check_none(np.mean(rows[:,6].astype(np.float)))
                    meanNO2 = check_none(np.mean(rows[:,7].astype(np.float)))
                    meanPM10 = check_none(np.mean(rows[:,8].astype(np.float)))
                    meanPM25 = check_none(np.mean(rows[:,9].astype(np.float)))
                    #
                    varSO2 = check_none(np.var(rows[:,4].astype(np.float)))
                    varCO = check_none(np.var(rows[:,5].astype(np.float)))
                    varO3 = check_none(np.var(rows[:,6].astype(np.float)))
                    varNO2 = check_none(np.var(rows[:,7].astype(np.float)))
                    varPM10 = check_none(np.var(rows[:,8].astype(np.float)))
                    varPM25 = check_none(np.var(rows[:,9].astype(np.float)))
                    #
                    stdSO2 = check_none(np.std(rows[:,4].astype(np.float)))
                    stdCO = check_none(np.std(rows[:,5].astype(np.float)))
                    stdO3 = check_none(np.std(rows[:,6].astype(np.float)))
                    stdNO2 = check_none(np.std(rows[:,7].astype(np.float)))
                    stdPM10 = check_none(np.std(rows[:,8].astype(np.float)))
                    stdPM25 = check_none(np.std(rows[:,9].astype(np.float)))
                    #
                    maxSO2 = check_none(np.max(rows[:,4].astype(np.float)))
                    maxCO = check_none(np.max(rows[:,5].astype(np.float)))
                    maxO3 = check_none(np.max(rows[:,6].astype(np.float)))
                    maxNO2 = check_none(np.max(rows[:,7].astype(np.float)))
                    maxPM10 = check_none(np.max(rows[:,8].astype(np.float)))
                    maxPM25 = check_none(np.max(rows[:,9].astype(np.float)))
                    #
                    minSO2 = check_none(np.min(rows[:,4].astype(np.float)))
                    minCO = check_none(np.min(rows[:,5].astype(np.float)))
                    minO3 = check_none(np.min(rows[:,6].astype(np.float)))
                    minNO2 = check_none(np.min(rows[:,7].astype(np.float)))
                    minPM10 = check_none(np.min(rows[:,8].astype(np.float)))
                    minPM25 = check_none(np.min(rows[:,9].astype(np.float)))
                    
                    #print('%s,,%s,,sum,%s,%s,%s,%s,%s,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25))
                    print("INSERT INTO %s.%s\
                        (`id`, `day`, `ocode`,\
                        `sumSO2`, `sumCO`, `sumO3`, `sumNO2`, `sumPM10`, `sumPM25`,\
                        `meanSO2`, `meanCO`, `meanO3`, `meanNO2`, `meanPM10`, `meanPM25`,\
                        `varSO2`, `varCO`, `varO3`, `varNO2`, `varPM10`, `varPM25`,\
                        `stdSO2`, `stdCO`, `stdO3`, `stdNO2`, `stdPM10`, `stdPM25`,\
                        `maxSO2`, `maxCO`, `maxO3`, `maxNO2`, `maxPM10`, `maxPM25`,\
                        `minSO2`, `minCO`, `minO3`, `minNO2`, `minPM10`, `minPM25`,\
                        `remark`)\
                        VALUES (NULL, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s);"\
                        %(db_name, tb_daily, day, ocode,\
                        sumSO2, sumCO, sumO3, sumNO2, sumPM10, sumPM25,\
                        meanSO2, meanCO, meanO3, meanNO2, meanPM10, meanPM25,\
                        varSO2, varCO, varO3, varNO2, varPM10, varPM25,\
                        stdSO2, stdCO, stdO3, stdNO2, stdPM10, stdPM25,\
                        maxSO2, maxCO, maxO3, maxNO2, maxPM10, maxPM25,\
                        minSO2, minCO, minO3, minNO2, minPM10, minPM25,\
                        len(rows)))
                     
                    cur.execute("INSERT INTO %s.%s\
                        (`id`, `day`, `ocode`,\
                        `sumSO2`, `sumCO`, `sumO3`, `sumNO2`, `sumPM10`, `sumPM25`,\
                        `meanSO2`, `meanCO`, `meanO3`, `meanNO2`, `meanPM10`, `meanPM25`,\
                        `varSO2`, `varCO`, `varO3`, `varNO2`, `varPM10`, `varPM25`,\
                        `stdSO2`, `stdCO`, `stdO3`, `stdNO2`, `stdPM10`, `stdPM25`,\
                        `maxSO2`, `maxCO`, `maxO3`, `maxNO2`, `maxPM10`, `maxPM25`,\
                        `minSO2`, `minCO`, `minO3`, `minNO2`, `minPM10`, `minPM25`,\
                        `remark`)\
                        VALUES (NULL, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s,\
                        %s);"\
                        %(db_name, tb_daily, day, ocode,\
                        sumSO2, sumCO, sumO3, sumNO2, sumPM10, sumPM25,\
                        meanSO2, meanCO, meanO3, meanNO2, meanPM10, meanPM25,\
                        varSO2, varCO, varO3, varNO2, varPM10, varPM25,\
                        stdSO2, stdCO, stdO3, stdNO2, stdPM10, stdPM25,\
                        maxSO2, maxCO, maxO3, maxNO2, maxPM10, maxPM25,\
                        minSO2, minCO, minO3, minNO2, minPM10, minPM25,\
                        len(rows)))
                    
                        #cur.execute("INSERT INTO `AirKorea_parks`.`daily`(`id`, `day`, `ocode`, `type`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`, `remark`) \
                        #VALUES (NULL, %s, %s, 'mean', %s, %s, %s, %s, %s, %s, %s);" \
                        #%(day,ocode,meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25,len(rows)))
                    conn.commit()
                    end_time = str(datetime.now())
                    print("start : "+ start_time+" end: "+end_time)
                    #s = s + 1
                    #print(s)
                    
                    #with open('%s%sdaily_%s.csv' %(drbase,drout,ocode), 'a') as o:
                        #print('%s,,%s,,sum,%s,%s,%s,%s,%s,%s,' % (day,ocode,sumSO2,sumCO,sumO3,sumNO2,sumPM10,sumPM25), file=o)
                        #print('%s,,%s,,mean,%s,%s,%s,%s,%s,%s,' % (day,ocode,meanSO2,meanCO,meanO3,meanNO2,meanPM10,meanPM25), file	=o)
                        #print('%s,,%s,,var,%s,%s,%s,%s,%s,%s,' % (day,ocode,varSO2,varCO,varO3,varNO2,varPM10,varPM25), file=o)
                        #print('%s,,%s,,std,%s,%s,%s,%s,%s,%s,' % (day,ocode,stdSO2,stdCO,stdO3,stdNO2,stdPM10,stdPM25), file=o)
                        #print('%s,,%s,,max,%s,%s,%s,%s,%s,%s,' % (day,ocode,maxSO2,maxCO,maxO3,maxNO2,maxPM10,maxPM25), file=o)
                        #print('%s,,%s,,min,%s,%s,%s,%s,%s,%s,' % (day,ocode,minSO2,minCO,minO3,minNO2,minPM10,minPM25), file=o)
 
q = proc.Queue()
P = []
data = []
#print("Debug1")

for i in range(len(ocodes)):
    ocode = ocodes[i]
    cur.execute("SELECT * from %s where ocode=%s ORDER BY otime ASC" %(tb_hourly, ocode))
    all_data = cur.fetchall()
    data.append(all_data)
    print(len(data[i]))
    

for i in range(len(ocodes)):
    ocode = ocodes[i]
    P.append(proc.Process(target=Work, args=(data[i],ocode)))
    P[len(P)-1].start()
cur.close()