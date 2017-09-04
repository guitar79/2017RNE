"""
@author: guitar79@naver.com, yyyyy@snu.ac.kr
view-source:http://www.kma.go.kr/cgi-bin/aws/nph-aws_txt_min?201008262022&0&MINDB_01M&0&a
www.kma.go.kr/cgi-bin/aws/nph-aws_txt_min?201708270810&0&MINDB_10M&0&m
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import time
from datetime import date
from pathlib import Path

#threading library
import threading

import sys

prefix = 'AWS-60min'

#single thread class
class crawler():
	def __init__(self, year, month, day, hour, minute, threadno):
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
		self.output = ''
		self.threadno = threadno

	def fetch(self):
		my_file = Path(prefix + '_%d%02d%02d%02d%02d.csv' % (self.year, self.month, self.day, self.hour, self.minute))
		if my_file.is_file(): # csv file already exists in my folder
			print ('File exists ' + prefix + '_%d%02d%02d%02d%02d.csv' % (self.year, self.month, self.day, self.hour, self.minute))
		else:	
			while True:
				try:
					url = "http://www.kma.go.kr/cgi-bin/aws/nph-aws_txt_min?%d%02d%02d%02d%02d&0&MINDB_60M&0&m" % (self.year, self.month, self.day, self.hour, self.minute)
					soup = BeautifulSoup(urlopen(url), "html.parser")
					mytable = soup.find_all('table')
					#mytable = soup.find_all('table')
					#only mytable[1] contains weather data
					for trs in mytable[1].find_all('tr'):
						for tds in trs.find_all('td'):
							#print data
							self.output += tds.text
							#csv delimeter
							self.output += ','
						#csv delimeter
						self.output += '\n'
					#open output file
					with open(prefix + '_%d%02d%02d%02d%02d.csv' % (self.year, self.month, self.day, self.hour, self.minute), 'w') as f:
						#write
						f.write(self.output)
					break
				except:
					sys.stderr.write("Thread #%d failed...retry\n" % self.threadno)
					pass

#crawler for single month
class crawler_month(threading.Thread):
	def __init__(self, year, month, day, threadno):
		threading.Thread.__init__(self)
		self.year = year
		self.month = month
		self.day = day
		self.threadno = threadno
		sys.stderr.write('Thread #%d started...\n' % (self.threadno))

	def run(self):
		for Ho in range(0,24):
			for Mn in range(0,60,60): 
				fetcher = crawler(self.year, self.month, self.day, Ho, Mn, self.threadno)
				fetcher.fetch()
				sys.stderr.write('Thread #%d - fetched %d-%02d-%02d %02d:%02d...\n' % (self.threadno, self.year, self.month, self.day, Ho, Mn))


threadno = 0
for year in range(2008,2009):
	for Mo in range(1,7):
		for Da in range(1,32):
			cmonth = crawler_month(year, Mo, Da, threadno)
			cmonth.start()
			threadno += 1
