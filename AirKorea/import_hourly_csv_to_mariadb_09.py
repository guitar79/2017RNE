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
tb_name = 'hourly_vc'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/csv1/'

#db connect
conn= pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name,\
                      charset='utf8mb4', local_infile=1, cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

cur.execute("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\
            SET time_zone = \"+00:00\";")

cur.execute("DROP TABLE IF EXISTS `%s`;" %(tb_name))

cur.execute("DROP TABLE IF EXISTS `Obs_info`;")

cur.execute("CREATE TABLE IF NOT EXISTS `Obs_info` (\
            `Ocode` int(6) NOT NULL,\
            `Oname` varchar(12) NOT NULL,\
            `Region` varchar(20) NOT NULL,\
            `Address` varchar(500) DEFAULT NULL,\
            `Lat` float DEFAULT NULL,\
            `Lon` float DEFAULT NULL,\
            `Alt` float DEFAULT NULL,\
            `Remarks` char(255) DEFAULT NULL,\
            PRIMARY KEY (`Ocode`))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")

cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Region` varchar(20) DEFAULT NULL,\
            `Ocode` int(6) NOT NULL,\
            `Oname` varchar(12) DEFAULT NULL,\
            `Otime` int(12) NOT NULL,\
            `SO2` float DEFAULT NULL,\
            `CO` float DEFAULT NULL,\
            `O3` float DEFAULT NULL,\
            `NO2` float DEFAULT NULL,\
            `PM10` int(4) DEFAULT NULL,\
            `PM25` int(4) DEFAULT NULL,\
            `Address` varchar(200) DEFAULT NULL,\
            `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
            CONSTRAINT FK_Ocode FOREIGN KEY (`Ocode`) REFERENCES Obs_info(`Ocode`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
            %(tb_name))

'''
cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Ocode` int(6) NOT NULL,\
            `Otime` int(12) NOT NULL,\
            `SO2` float DEFAULT NULL,\
            `CO` float DEFAULT NULL,\
            `O3` float DEFAULT NULL,\
            `NO2` float DEFAULT NULL,\
            `PM10` int(4) DEFAULT NULL,\
            `PM25` int(4) DEFAULT NULL,\
            `id` int(11) NOT NULL AUTO_INCREMENT,\
            PRIMARY KEY (`id`),\
            CONSTRAINT FK_Ocode FOREIGN KEY (`Ocode`) REFERENCES Obs_info(`Ocode`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
            %(tb_name))
'''


cur.execute("ALTER TABLE `%s`\
            MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;"  %(tb_name))
             
#delete all data in the table
print("TRUNCATE TABLE %s;" %(tb_name))
cur.execute("TRUNCATE TABLE %s;" %(tb_name))
conn.commit()

#log file
insert_log = open(drbase+'hourly_import_result.log', 'a')
error_log = open(drbase+'hourly_import_error.log', 'a')

for i in sorted(os.listdir(drbase),reverse=True):
    
    #read csv files
    if i[-4:] == '.csv':
        
        print(i)
        try :
            print("LOAD DATA LOCAL \
                  INFILE '%s%s' \
                  INTO TABLE %s.%s \
                  FIELDS TERMINATED BY '\|' \
                  ENCLOSED BY '\"' \
                  LINES TERMINATED BY '\\n'\
                  IGNORE 1 LINES \
                  (`Region`, `Ocode`, `Oname`, `Otime`, \
                  `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM25`, `Address`);"\
                  %(drbase,i,db_name,tb_name))
            cur.execute("LOAD DATA LOCAL \
                  INFILE '%s%s' \
                  INTO TABLE %s.%s \
                  FIELDS TERMINATED BY '\|' \
                  ENCLOSED BY '\"' \
                  LINES TERMINATED BY '\\n'\
                  IGNORE 1 LINES \
                  (`Region`, `Ocode`, `Oname`, `Otime`, \
                  `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM25`, `Address`);"\
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

print("CHECK TABLE %s.%s;" %(db_name, tb_name))
cur.execute("CHECK TABLE %s.%s;" %(db_name, tb_name))
conn.commit()
print("ALTER TABLE %s.%s ENGINE = InnoDB;" %(db_name, tb_name))
cur.execute("ALTER TABLE %s.%s ENGINE = InnoDB;" %(db_name, tb_name))
conn.commit()
print("OPTIMIZE TABLE %s.%s;" %(db_name, tb_name))
cur.execute("OPTIMIZE TABLE %s.%s;" %(db_name, tb_name))
conn.commit()
'''
print("FLUSH TABLE %s.%s;" %(db_name, tb_name))
cur.execute("FLUSH TABLE %s.%s;" %(db_name, tb_name))
conn.commit()
'''
cur.close()

end_time = str(datetime.now())
print("start : "+ start_time+" end: "+end_time)


'''
http://localhost/phpMyAdmin/sql.php?db=AirKorea&table=houly_vc&back=tbl_operations.php&goto=tbl_operations.php&sql_query=ALTER+TABLE+%60houly_vc%60+ENGINE+%3D+InnoDB%3B&token=746c2350251eec3ab8bef717286d7272



'''
