'''-*- coding: utf-8 -*-
 Auther guitar79@naver.com
'''
#np.set_printoptions(threshold=100)

import numpy as np
import os
#import multiprocessing as proc
import pymysql
#import pymysql.cursorsv
from datetime import datetime, timedelta
#from datetime import datetime
#from dateutil.relativedelta import relativedelta

start_time=str(datetime.now())

#mariaDB info
db_host = '10.114.0.121'
db_user = 'root'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea'
tb_hourly = 'hourly'
tb_name = 'daily'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
drout = 'daily_mean4/'
if not os.path.exists(drbase+drout):
    os.makedirs(drbase+drout)
#db connect
conn= pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name,\
                      charset='utf8mb4', local_infile=1, cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS `%s`;" %(tb_name))

cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Ocode` int(6) NOT NULL,\
            `Otime` DATE NOT NULL,\
            `sumSO2` float DEFAULT NULL,\
            `sumCO` float DEFAULT NULL,\
            `sumO3` float DEFAULT NULL,\
            `sumNO2` float DEFAULT NULL,\
            `sumPM10` float DEFAULT NULL,\
            `sumPM25` float DEFAULT NULL,\
            `meanSO2` float DEFAULT NULL,\
            `meanCO` float DEFAULT NULL,\
            `meanO3` float DEFAULT NULL,\
            `meanNO2` float DEFAULT NULL,\
            `meanPM10` float DEFAULT NULL,\
            `meanPM25` float DEFAULT NULL,\
            `varSO2` float DEFAULT NULL,\
            `varCO` float DEFAULT NULL,\
            `varO3` float DEFAULT NULL,\
            `varNO2` float DEFAULT NULL,\
            `varPM10` float DEFAULT NULL,\
            `varPM25` float DEFAULT NULL,\
            `stdSO2` float DEFAULT NULL,\
            `stdCO` float DEFAULT NULL,\
            `stdO3` float DEFAULT NULL,\
            `stdNO2` float DEFAULT NULL,\
            `stdPM10` float DEFAULT NULL,\
            `stdPM25` float DEFAULT NULL,\
            `maxSO2` float DEFAULT NULL,\
            `maxCO` float DEFAULT NULL,\
            `maxO3` float DEFAULT NULL,\
            `maxNO2` float DEFAULT NULL,\
            `maxPM10` float DEFAULT NULL,\
            `maxPM25` float DEFAULT NULL,\
            `minSO2` float DEFAULT NULL,\
            `minCO` float DEFAULT NULL,\
            `minO3` float DEFAULT NULL,\
            `minNO2` float DEFAULT NULL,\
            `minPM10` float DEFAULT NULL,\
            `minPM25` float DEFAULT NULL,\
            `id` int(11) NOT NULL,\
            PRIMARY KEY (`id`))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
            %(tb_name))

cur.execute("ALTER TABLE `%s`\
            MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;"  %(tb_name))
conn.commit()

#all ocode read!!
cur = conn.cursor()
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))
conn.commit()

cur = conn.cursor()

#ocodes = ocodes
print("SELECT DISTINCT ocode from %s ORDER BY ocode ASC " %(tb_hourly))
cur.execute("SELECT DISTINCT ocode from %s ORDER BY ocode ASC " %(tb_hourly))
ocode_rows = cur.fetchall()
#print(len(ocodes))
ocodes = []
for i in range(len(ocode_rows)):
    ocodes.append(ocode_rows[i]['ocode'])

#ocodes=[131372]
print(ocodes)

def check_none(x):
    if np.isnan(x): return -9999
    return x

'''
print("SELECT * from %s ORDER BY `Ocode` ASC, `Otime` ASC" %(tb_hourly))
cur.execute("SELECT * from %s ORDER BY `Ocode` ASC, `Otime` ASC" %(tb_hourly))
all_rows = cur.fetchall()
'''  
output = '' 
for ocode in ocodes:
    print("SELECT * from %s WHERE `Ocode` = %s ORDER BY `Otime` ASC" %(tb_hourly,ocode))
    cur.execute("SELECT * from %s WHERE `Ocode` = %s ORDER BY `Otime` ASC" %(tb_hourly,ocode))
    ocode_rows = cur.fetchall()
    print(ocode,len(ocode_rows))
 
    for year in range(2014,2017):
        for Mo in range(1,13):
             #define day numbers of each month
            if year%4==0 : D=[0,31,29,31,30,31,30,31,31,30,31,30,31]
            else : D=[0,31,28,31,30,31,30,31,31,30,31,30,31]
            for Da in range(1,D[Mo]+1):
                sdatetime = datetime(year, Mo, Da,0,0,0)
                edatetime = sdatetime + timedelta(days=1)
                rows = []
                pos=0
                while pos<len(ocode_rows):
                    if ocode_rows[pos]['Otime'] >= sdatetime and ocode_rows[pos]['Otime'] < edatetime :
                        rows.append(ocode_rows[pos])
                    pos = pos + 1
                if len(rows) == 0:
                    print('There is no data at %s from %s to %s' %(ocode, sdatetime,edatetime))
                else:
                    #print(rows)
                    new_rows = []
                    for i in range(len(rows)-1):
                        new_rows.append(list(rows[i].values()))
                    rows = np.array(new_rows)
                    rows[rows==-9999]=np.nan
                    if len(rows) == 0:
                        print(rows)
                        print('data is empty %s from %s to %s' %(ocode, sdatetime,edatetime))
                    else :
                        print(ocode, len(rows))
                        print(rows)
                        #print(rows.shape)
                        #print(type(rows))
                        #s.sum(skipna=True)
                        sumSO2 = "{0:.4f}".format(check_none(np.nansum(rows[:,2].astype(np.float))))
                        sumCO = "{0:.4f}".format(check_none(np.nansum(rows[:,3].astype(np.float))))
                        sumO3 = "{0:.4f}".format(check_none(np.nansum(rows[:,4].astype(np.float))))
                        sumNO2 = "{0:.4f}".format(check_none(np.nansum(rows[:,5].astype(np.float))))
                        sumPM10 = "{0:.4f}".format(check_none(np.nansum(rows[:,6].astype(np.float))))
                        sumPM25 = "{0:.4f}".format(check_none(np.nansum(rows[:,7].astype(np.float))))
                        #
                        meanSO2 = "{0:.4f}".format(check_none(np.nanmean(rows[:,2].astype(np.float))))
                        meanCO = "{0:.4f}".format(check_none(np.nanmean(rows[:,3].astype(np.float))))
                        meanO3 = "{0:.4f}".format(check_none(np.nanmean(rows[:,4].astype(np.float))))
                        meanNO2 = "{0:.4f}".format(check_none(np.nanmean(rows[:,5].astype(np.float))))
                        meanPM10 = "{0:.4f}".format(check_none(np.nanmean(rows[:,6].astype(np.float))))
                        meanPM25 = "{0:.4f}".format(check_none(np.nanmean(rows[:,7].astype(np.float))))
                        #
                        varSO2 = "{0:.4f}".format(check_none(np.nanvar(rows[:,2].astype(np.float))))
                        varCO = "{0:.4f}".format(check_none(np.nanvar(rows[:,3].astype(np.float))))
                        varO3 = "{0:.4f}".format(check_none(np.nanvar(rows[:,4].astype(np.float))))
                        varNO2 = "{0:.4f}".format(check_none(np.nanvar(rows[:,5].astype(np.float))))
                        varPM10 = "{0:.4f}".format(check_none(np.nanvar(rows[:,6].astype(np.float))))
                        varPM25 = "{0:.4f}".format(check_none(np.nanvar(rows[:,7].astype(np.float))))
                        #
                        stdSO2 = "{0:.4f}".format(check_none(np.nanstd(rows[:,2].astype(np.float))))
                        stdCO = "{0:.4f}".format(check_none(np.nanstd(rows[:,3].astype(np.float))))
                        stdO3 = "{0:.4f}".format(check_none(np.nanstd(rows[:,4].astype(np.float))))
                        stdNO2 = "{0:.4f}".format(check_none(np.nanstd(rows[:,5].astype(np.float))))
                        stdPM10 = "{0:.4f}".format(check_none(np.nanstd(rows[:,6].astype(np.float))))
                        stdPM25 = "{0:.4f}".format(check_none(np.nanstd(rows[:,7].astype(np.float))))
                        #
                        maxSO2 = "{0:.4f}".format(check_none(np.nanmax(rows[:,2].astype(np.float))))
                        maxCO = "{0:.4f}".format(check_none(np.nanmax(rows[:,3].astype(np.float))))
                        maxO3 = "{0:.4f}".format(check_none(np.nanmax(rows[:,4].astype(np.float))))
                        maxNO2 = "{0:.4f}".format(check_none(np.nanmax(rows[:,5].astype(np.float))))
                        maxPM10 = "{0:.4f}".format(check_none(np.nanmax(rows[:,6].astype(np.float))))
                        maxPM25 = "{0:.4f}".format(check_none(np.nanmax(rows[:,7].astype(np.float))))
                        #
                        minSO2 = "{0:.4f}".format(check_none(np.nanmin(rows[:,2].astype(np.float))))
                        minCO = "{0:.4f}".format(check_none(np.nanmin(rows[:,3].astype(np.float))))
                        minO3 = "{0:.4f}".format(check_none(np.nanmin(rows[:,4].astype(np.float))))
                        minNO2 = "{0:.4f}".format(check_none(np.nanmin(rows[:,5].astype(np.float))))
                        minPM10 = "{0:.4f}".format(check_none(np.nanmin(rows[:,6].astype(np.float))))
                        minPM25 = "{0:.4f}".format(check_none(np.nanmin(rows[:,7].astype(np.float))))
                        
        
                        print("INSERT INTO '%s'.'%s'\
                            (`Ocode`,`Otime`\
                            `sumSO2`, `sumCO`, `sumO3`, `sumNO2`, `sumPM10`, `sumPM25`,\
                            `meanSO2`, `meanCO`, `meanO3`, `meanNO2`, `meanPM10`, `meanPM25`,\
                            `varSO2`, `varCO`, `varO3`, `varNO2`, `varPM10`, `varPM25`,\
                            `stdSO2`, `stdCO`, `stdO3`, `stdNO2`, `stdPM10`, `stdPM25`,\
                            `maxSO2`, `maxCO`, `maxO3`, `maxNO2`, `maxPM10`, `maxPM25`,\
                            `minSO2`, `minCO`, `minO3`, `minNO2`, `minPM10`, `minPM25`,\
                            `id`)\
                            VALUES ('%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            '%s', '%s', '%s', '%s', '%s', '%s',\
                            NULL);"\
                            %(db_name, tb_name,\
                            ocode, sdatetime, \
                            sumSO2, sumCO, sumO3, sumNO2, sumPM10, sumPM25,\
                            meanSO2, meanCO, meanO3, meanNO2, meanPM10, meanPM25,\
                            varSO2, varCO, varO3, varNO2, varPM10, varPM25,\
                            stdSO2, stdCO, stdO3, stdNO2, stdPM10, stdPM25,\
                            maxSO2, maxCO, maxO3, maxNO2, maxPM10, maxPM25,\
                            minSO2, minCO, minO3, minNO2, minPM10, minPM25))
        
                        output += "INSERT INTO %s.%s\
                            (`Ocode`,`Otime`,\
                            `sumSO2`, `sumCO`, `sumO3`, `sumNO2`, `sumPM10`, `sumPM25`,\
                            `meanSO2`, `meanCO`, `meanO3`, `meanNO2`, `meanPM10`, `meanPM25`,\
                            `varSO2`, `varCO`, `varO3`, `varNO2`, `varPM10`, `varPM25`,\
                            `stdSO2`, `stdCO`, `stdO3`, `stdNO2`, `stdPM10`, `stdPM25`,\
                            `maxSO2`, `maxCO`, `maxO3`, `maxNO2`, `maxPM10`, `maxPM25`,\
                            `minSO2`, `minCO`, `minO3`, `minNO2`, `minPM10`, `minPM25`,\
                            `id`)\
                            VALUES (%s, '%s',\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            NULL);\n"\
                            %(db_name, tb_name,\
                            ocode, sdatetime, \
                            sumSO2, sumCO, sumO3, sumNO2, sumPM10, sumPM25,\
                            meanSO2, meanCO, meanO3, meanNO2, meanPM10, meanPM25,\
                            varSO2, varCO, varO3, varNO2, varPM10, varPM25,\
                            stdSO2, stdCO, stdO3, stdNO2, stdPM10, stdPM25,\
                            maxSO2, maxCO, maxO3, maxNO2, maxPM10, maxPM25,\
                            minSO2, minCO, minO3, minNO2, minPM10, minPM25)
        
                        cur.execute("INSERT INTO %s.%s\
                            (`Ocode`,`Otime`,\
                            `sumSO2`, `sumCO`, `sumO3`, `sumNO2`, `sumPM10`, `sumPM25`,\
                            `meanSO2`, `meanCO`, `meanO3`, `meanNO2`, `meanPM10`, `meanPM25`,\
                            `varSO2`, `varCO`, `varO3`, `varNO2`, `varPM10`, `varPM25`,\
                            `stdSO2`, `stdCO`, `stdO3`, `stdNO2`, `stdPM10`, `stdPM25`,\
                            `maxSO2`, `maxCO`, `maxO3`, `maxNO2`, `maxPM10`, `maxPM25`,\
                            `minSO2`, `minCO`, `minO3`, `minNO2`, `minPM10`, `minPM25`,\
                            `id`)\
                            VALUES (%s, '%s',\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s,\
                            NULL);"\
                            %(db_name, tb_name,\
                            ocode, sdatetime, \
                            sumSO2, sumCO, sumO3, sumNO2, sumPM10, sumPM25,\
                            meanSO2, meanCO, meanO3, meanNO2, meanPM10, meanPM25,\
                            varSO2, varCO, varO3, varNO2, varPM10, varPM25,\
                            stdSO2, stdCO, stdO3, stdNO2, stdPM10, stdPM25,\
                            maxSO2, maxCO, maxO3, maxNO2, maxPM10, maxPM25,\
                            minSO2, minCO, minO3, minNO2, minPM10, minPM25))
                        
                        conn.commit()

with open('%s%scalculate_hourly_mariaDB_to_daily_all.sql'%(drbase,drout), 'w')  as f:
    f.write(output)
            

print("CHECK TABLE %s.%s;" %(db_name, tb_name))
cur.execute("CHECK TABLE %s.%s;" %(db_name, tb_name))
conn.commit()
print("ALTER TABLE %s.%s ENGINE = InnoDB;" %(db_name, tb_name))
cur.execute("ALTER TABLE %s.%s ENGINE = InnoDB;" %(db_name, tb_name))
conn.commit()
print("OPTIMIZE TABLE %s.%s;" %(db_name, tb_name))
cur.execute("OPTIMIZE TABLE %s.%s;" %(db_name, tb_name))
conn.commit()

cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)

