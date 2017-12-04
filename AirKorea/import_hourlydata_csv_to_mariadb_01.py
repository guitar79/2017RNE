'''-*- coding: utf-8 -*-
 Auther guitar79@naver.com
'''
#import numpy as np
import os
import pymysql
from datetime import datetime
import time

start_time=str(datetime.now())

#mariaDB info
db_host = '10.114.0.121'
db_user = 'modis'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea_parks'
tb_name = 'hourly_vc'

#base directory
drbase = '/home/guitar79/AK/'
#query_file='sql.txt'
#db connect
conn= pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name,\
                      charset='utf8mb4', local_infile=1, cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))
conn.commit()
finish_rows = 0
#read the list of csv files
for i in sorted(os.listdir(drbase)):
    #read csv files
    if i[-4:] == '.csv':
        read_file = open(drbase+i,'r')
        raw_lists = read_file.read()
        #print(raw_lists)
        raw_lists = raw_lists.split('\n')
        for j in range(0,(len(raw_lists)-1)):
            #print(raw_lists[j])
            row = raw_lists[j].split(',')
            #print(row)
            '''
            print("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES (%s);"\
                      %(db_name,tb_name,row))
            
            cur.execute("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES (%s, %s, %s,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`,`%s`);"\
                      %(db_name,tb_name,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            print("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES ('NULL', %s, %s, %s, %s, %s, %s, %s, %s, %s);"\
                      %(db_name, tb_name, row[1], row[2], row[3], row[4],\
                        row[5], row[6], row[7], row[8], row[9]))
            '''
            print(i,j)
            cur.execute("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES ('NULL', %s, %s, %s, %s, %s, %s, %s, %s, %s);"\
                      %(db_name, tb_name, row[1], row[2], row[3], row[4],\
                        row[5], row[6], row[7], row[8], row[9]))
            #if j%10000 == 0:
            #    time.sleep(1)
        finish_rows = finish_rows + len(raw_lists)
conn.commit()
cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)
print(finish_rows)

'''
 aa=a.split(']')

aa
Out[16]: ['[,123456,,11,22,33,44,55,66', '']

aaa=aa[0].split('[')

aaa
Out[18]: ['', ',123456,,11,22,33,44,55,66']

aaaa=aaa[1].split(',')

aaaa
Out[20]: ['', '123456', '', '11', '22', '33', '44', '55', '66']
'''