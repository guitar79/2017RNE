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
db_host = '10.114.0.126'
db_user = 'modis'
db_pass = 'rudrlrhkgkrrh'
db_name = 'AirKorea'
tb_name = 'hourly'

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/csv/'

#db connect
conn= pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name,\
                      charset='utf8mb4', local_infile=1, cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

output = ''

cur.execute("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\
            SET time_zone = \"+00:00\";")

cur.execute("DROP TABLE IF EXISTS `%s`;" %(tb_name))

cur.execute("DROP TABLE IF EXISTS `Obs_info`;")

cur.execute("CREATE TABLE IF NOT EXISTS `Obs_info` (\
            `Ocode` int(6) NOT NULL,\
            `Oname` varchar(12) DEFAULT NULL,\
            `Region` varchar(20) DEFAULT NULL,\
            `Address` varchar(500) DEFAULT NULL,\
            `Lat` float DEFAULT NULL,\
            `Lon` float DEFAULT NULL,\
            `Alt` float DEFAULT NULL,\
            `Remarks` char(255) DEFAULT NULL,\
            PRIMARY KEY (`Ocode`))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")

cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Ocode` int(6) NOT NULL,\
            `Otime` DATETIME NOT NULL,\
            `SO2` float DEFAULT NULL,\
            `CO` float DEFAULT NULL,\
            `O3` float DEFAULT NULL,\
            `NO2` float DEFAULT NULL,\
            `PM10` int(4) DEFAULT NULL,\
            `PM25` int(4) DEFAULT NULL,\
            `id` int(11) NOT NULL,\
            PRIMARY KEY (`id`))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
            %(tb_name))
'''
cur.execute("CREATE TABLE IF NOT EXISTS `%s` (\
            `Ocode` int(6) NOT NULL,\
            `Otime` varchar(12) NOT NULL,\
            `SO2` float DEFAULT NULL,\
            `CO` float DEFAULT NULL,\
            `O3` float DEFAULT NULL,\
            `NO2` float DEFAULT NULL,\
            `PM10` int(4) DEFAULT NULL,\
            `PM25` int(4) DEFAULT NULL,\
            `id` int(11) NOT NULL AUTO_INCREMENT,\
            PRIMARY KEY (`id`),\
            CONSTRAINT FK_Ocode FOREIGN KEY (`Ocode`) REFERENCES Obs_info(`Ocode`))\
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"\
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


for i in sorted(os.listdir(drbase)):

    #read csv files
    if i[-4:] == '.csv':
        read_file = open(drbase+i,'r')
        raw_lists = read_file.read()
        #print(raw_lists)
        raw_lists = raw_lists.split('\n')
        for j in range(1,(len(raw_lists)-1)):
            #print(raw_lists[j])
            row = raw_lists[j].split(',')
            #print(row)
            for k in range(len(row)):
                if len(row[k])==0 : row[k]=-9999
            print("INSERT INTO %s.%s\
                      (`Ocode`, `Otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM25`, `id`) \
                      VALUES (%s, '%s-%s-%s %s:00:00', %s, %s, %s, %s, %s, %s, NULL);"\
                      %(db_name, tb_name, row[1], row[3][0:4], row[3][4:6], row[3][6:8],(int(row[3][8:10])-1),\
                        row[4], row[5], row[6], row[7], row[8], row[9]))
            output += "INSERT INTO %s.%s\
                      (`Ocode`, `Otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM25`, `id`) \
                      VALUES (%s, '%s-%s-%s %s:00:00', %s, %s, %s, %s, %s, %s, NULL);\n"\
                      %(db_name, tb_name, row[1], row[3][0:4], row[3][4:6], row[3][6:8],(int(row[3][8:10])-1),\
                        row[4], row[5], row[6], row[7], row[8], row[9])
            print(i, j)

            cur.execute("INSERT INTO %s.%s\
                      (`Ocode`, `Otime`, `SO2`, `CO`, `O3`, `NO2`, `PM10`, `PM25`, `id`) \
                      VALUES (%s, '%s-%s-%s %s:00:00', %s, %s, %s, %s, %s, %s, NULL);"\
                      %(db_name, tb_name, row[1], row[3][0:4], row[3][4:6], row[3][6:8],(int(row[3][8:10])-1),\
                        row[4], row[5], row[6], row[7], row[8], row[9]))
            conn.commit()
        
        with open(drbase+i+'.sql', 'w') as f:
            f.write(output)
        
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

pymysql.cursor.executemany()

FOREIGN KEY (키이름) REFERENCES 참조할 테이블 이름(참조할 테이블에서의 키이름)
SELECT AVG(temperature) FROM table WHERE temerature != -9999;
https://www.w3schools.com/sql/sql_foreignkey.asp
http://localhost/phpMyAdmin/sql.php?db=AirKorea&table=houly_vc&back=tbl_operations.php&goto=tbl_operations.php&sql_query=ALTER+TABLE+%60houly_vc%60+ENGINE+%3D+InnoDB%3B&token=746c2350251eec3ab8bef717286d7272



'''
