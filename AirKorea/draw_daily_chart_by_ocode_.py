#place and date(1day)
#
# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(threshold=100)
def date(n,m):#From n to m-1
    return ((f['측정일시']-n)//(m-n) == 0)
    
def place(n):
    return (f['측정소코드'] == n)

def array2string(x):
    return '\n'.join(','.join('%0.2f' %x for x in y) for y in x)


# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'h_daily_mean1/'
#write directory(output data)
drout = 'h_daily_chart1/'

filein = '111121'
#'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25'
data = 'PM10'

if not os.path.exists(drbase+drout):
	os.makedirs(drbase+drout)
    
#read data files and make data frame from reading csv files (like table)
g = pd.read_csv('%s%sstatistics_%s.csv' %(drbase,drin,filein), encoding='euc_kr')
#count number of the total data 
print(g)
print('total number of data: %s' %(len(g)))
#
g=g.loc[g['var'] == 'mean']
#ooday = np.array(g.ix[:,'day'])
#oodata = np.array(g.ix[:,data])
ooday = np.array(g.loc[:,'day'])
oodata = np.array(g.loc[:,data])
#ooo = g["PM10"].tolist()
print(ooday)
print('total number of data: %s' %(len(ooday)))
print(oodata)
print('total number of data: %s' %(len(oodata)))
oday=[]
odata=[]
j=0
for j in range(0,len(ooday)):
    if j%5==1:
        #oday.append(ooday[j])
        oday.append(j)
        odata.append(oodata[j])
print(oday)
print('total number of data: %s' %(len(oday)))
print(odata)
print('total number of data: %s' %(len(odata)))
plt.plot(oday,odata)
plt.scatter(oday,odata)

plt.xlabel('time')
plt.ylabel('daily mean concentration')
plt.rcParams["figure.figsize"] = (16,9)

plt.savefig('%s%sdaily_%s_%s.pdf' %(drbase,drout,filein,data),dpi=300)
plt.savefig('%s%sdaily_%s_%s.png' %(drbase,drout,filein,data),dpi=300)
plt.close()