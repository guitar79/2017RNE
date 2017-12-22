'''
-*- coding: utf-8 -*-
 Auther guitar79@naver.com
 
'''
#import numpy as np
import os
import pymysql
from datetime import datetime
#import warning
#import time

start_time=str(datetime.now())

#mariaDB info
db_host = '10.114.0.121'
db_user = 'modis'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea'
tb_name = 'houly_vc'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/csv/'

#db connect
conn= pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name,\
                      charset='utf8mb4', local_infile=1, cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

cur.execute("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\
            SET time_zone = \"+00:00\";")

cur.execute("DROP TABLE IF EXISTS `%s`;" %(tb_name))

cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Region` varchar(20) DEFAULT NULL,\
            `Ocode` varchar(6) NOT NULL,\
            `Oname` varchar(20) DEFAULT NULL,\
            `Otime` varchar(12) NOT NULL,\
            `SO2` varchar(20) DEFAULT NULL,\
            `CO` varchar(20) DEFAULT NULL,\
            `O3` varchar(20) DEFAULT NULL,\
            `NO2` varchar(20) DEFAULT NULL,\
            `PM10` varchar(20) DEFAULT NULL,\
            `PM25` varchar(20) DEFAULT NULL,\
            `Address` varchar(100) DEFAULT NULL,\
            `id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
             %(tb_name))

cur.execute("ALTER TABLE `%s` \
            ADD PRIMARY KEY (`id`);" %(tb_name))

cur.execute("ALTER TABLE `%s`\
            MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;"  %(tb_name))
             
#delete all data in the table
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))
conn.commit()

#log file
insert_log = open(drbase+'hourly_import_result.log', 'a')
error_log = open(drbase+'hourly_import_error.log', 'a')

for i in sorted(os.listdir(drbase)):
    
    #read csv files
    if i[-4:] == '.csv':
        
        print(i)
        try :
            print("LOAD DATA LOCAL \
                  INFILE '%s%s' \
                  INTO TABLE %s.%s \
                  FIELDS TERMINATED BY ',' \
                  ENCLOSED BY '\"' \
                  LINES TERMINATED BY '\\n'\
                  set id= ''\
                  IGNORE 1 LINES;"\
                  %(drbase,i,db_name,tb_name))
            cur.execute("LOAD DATA LOCAL \
                  INFILE '%s%s' \
                  INTO TABLE %s.%s \
                  FIELDS TERMINATED BY ',' \
                  ENCLOSED BY '\"' \
                  LINES TERMINATED BY '\\n'\
                  IGNORE 1 LINES;"\
                  %(drbase,i,db_name,tb_name))
            conn.commit()
            insert_log.write(drbase+i+" is inserted to the %s - %s\n"\
                             %(tb_name, datetime.now()))
        except :
            print(drbase+i+" is error : %s - %s\n"\
                             %(tb_name, datetime.now()))
            error_log.write(drbase+i+" is error : %s - %s\n"\
                             %(tb_name, datetime.now()))
        
insert_log.close()
error_log.close()

print("CHECK TABLE %s;" %(tb_name))
cur.execute("CHECK TABLE %s;" %(tb_name))
conn.commit()
print("ALTER TABLE %s ENGINE = InnoDB;" %(tb_name))
cur.execute("ALTER TABLE %s ENGINE = InnoDB;" %(tb_name))
conn.commit()
print("OPTIMIZE TABLE %s;" %(tb_name))
cur.execute("OPTIMIZE TABLE %s;" %(tb_name))
conn.commit()
print("FLUSH TABLE %s;" %(tb_name))
cur.execute("FLUSH TABLE %s;" %(tb_name))
conn.commit()

cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)


'''
http://localhost/phpMyAdmin/sql.php?db=AirKorea&table=houly_vc&back=tbl_operations.php&goto=tbl_operations.php&sql_query=ALTER+TABLE+%60houly_vc%60+ENGINE+%3D+InnoDB%3B&token=746c2350251eec3ab8bef717286d7272



'''
