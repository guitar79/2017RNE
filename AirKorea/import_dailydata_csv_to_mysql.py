# -*- coding: utf-8 -*-
#LOAD DATA INFILE '/home/guitar79/AK_CSV/2016-4.csv'  INTO TABLE hourly  FIELDS TERMINATED BY ','  ENCLOSED BY '"' LINES TERMINATED BY '\n'; ignore 1 rows;

import mysql.connector
from mysql.connector import errorcode

try:
	cnx = mysql.connector.connect(user='root', password='rudrlrhkgkrrh', host='127.0.0.1', database='AirKorea')
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:

cnx.close()
