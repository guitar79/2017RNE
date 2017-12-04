'''-*- coding: utf-8 -*-
 Auther guitar79@naver.com
'''

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

#all ocode read!!
cur = conn.cursor()
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))

for i in sorted(os.listdir(drbase)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        print(i)
        print("LOAD DATA LOCAL \
              INFILE '%s%s' \
              INTO TABLE %s.%s \
              FIELDS TERMINATED BY ',' \
              ENCLOSED BY '\"' \
              LINES TERMINATED BY '\\n'\
              IGNORE 0 LINES;"\
              %(drbase,i,db_name,tb_name))

        cur.execute("LOAD DATA LOCAL \
                    INFILE '%s%s' \
                    INTO TABLE %s.%s \
                    FIELDS TERMINATED BY ',' \
                    ENCLOSED BY '\"' \
                    LINES TERMINATED BY '\\n'\
                    IGNORE 0 LINES;"\
                    %(drbase,i,db_name,tb_name))
        conn.commit()
#cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)