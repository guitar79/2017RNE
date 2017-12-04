'''-*- coding: utf-8 -*-
 Auther guitar79@naver.com
'''
#import numpy as np
import os
import pymysql
from datetime import datetime

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
#delete all data in the table
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))
#cur.close ()
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
                      VALUES ('NULL', %s, %s, %s, %s, %s, %s, %s, %s, %s);"\
                      %(db_name, tb_name, row[1], row[2], row[3], row[4],\
                        row[5], row[6], row[7], row[8], row[9]))
            '''
            print(i, j)
            cur.execute("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES ('NULL', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"\
                      %(db_name, tb_name, row[1], row[2], row[3], row[4],\
                        row[5], row[6], row[7], row[8], row[9]))
            conn.commit()
        finish_rows = finish_rows + len(raw_lists)
        conn.commit()
conn.commit()
cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)
#print("total %d inserted to the %s.%s") %(finish_rows, db_name, tb_name)

'''
            try:
                print(i, j)
                cur.execute("INSERT INTO %s.%s\
                      (`id`, `ocode`, `oname`, `otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM2.5`) \
                      VALUES ('NULL', %s, %s, %s, %s, %s, %s, %s, %s, %s);"\
                      %(db_name, tb_name, row[1], row[2], row[3], row[4],\
                        row[5], row[6], row[7], row[8], row[9]))
                cur.close()
                conn.commit()
                finish_rows = finish_rows + len(raw_lists)
            except MySQLdb.Error, e:
                print "Transaction failed, rolling back. Error was:"
                print e.args
                try:  # empty exception handler in case rollback fails
                    conn.rollback ()
                except:
                    pass

'''