#place and date(1day)

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
drin = 'temp/'
#write directory(output data)
drout = 'output/'

#make empty dataframe(1,11) with head
#head = ('지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소')
head = ('', '111111', '', '', '', '', '', '', '', '', '')
head = np.array(head)
head = head.reshape(1,11)
f = pd.DataFrame(head)
#empty dataframe(1,11) columns header
f.columns = (['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소'])

#read data files 
for i in sorted(os.listdir(drbase+drin)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        g = pd.read_csv(drbase+drin+i, encoding='euc_kr')
        g.columns = (['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소'])

        f = f.append(g,ignore_index=True)
        #count number of the total data 
        
f = f.drop(f.index[[0,1]])
total_datanum = len(f)

#statistics of total data
total_mean_value = array2string(f.mean().values.reshape(1,11))
total_var_value = array2string(f.var().values.reshape(1,11))
total_std_value = array2string(f.std().values.reshape(1,11))
total_max_value = array2string(f.max().values.reshape(1,11))
total_min_value = array2string(f.min().values.reshape(1,11))

#write files from statistics
with open(drbase+drout+'statistics_total.csv', 'w') as o:
    print(total_datanum,',','mean,',total_mean_value,'\n','var,',total_var_value,'\n','std,',total_std_value,'\n','max,',total_max_value,'\n','min,',total_min_value,'\n', file=o)

#make observatory code index
#ocode = list(set(np.array(f.ix[:,1])))
ocode = list(set(np.array(f.ix[:,'측정소코드'])))
#count number of the observatory
#onumber = len(ocode)
odate = list(set(np.array(f.ix[:,'측정일시'])//100))

for obs1 in sorted(ocode):
    with open(drbase+drout+'statistics_'+str(obs1)+'.csv', 'a') as o:
        print('day,지역,측정소코드,측정소명,측정일시,SO2,CO,O3,NO2,PM10,PM25,주소', file=o)
    for obs2 in sorted(odate):
        fo=f.loc[date(obs2*100+1,obs2*100+25) & place(obs1)]
		#fo=f[f['측정소코드']].isin(obs)
        o_mean_value = array2string(fo.mean().values.reshape(1,11))
        o_var_value = array2string(fo.var().values.reshape(1,11))
        o_std_value = array2string(fo.std().values.reshape(1,11))
        o_max_value = array2string(fo.max().values.reshape(1,11))
        o_min_value = array2string(fo.min().values.reshape(1,11))
        #obss = str(obs)
        with open(drbase+drout+'statistics_'+str(obs1)+'.csv', 'a') as o:
            print(obs2, ',', o_mean_value, file=o)
            print(obs2, ',,', o_var_value, file=o)
            print(obs2, ',,', o_std_value, file=o)
            print(obs2, ',', o_max_value, file=o)
            print(obs2, ',', o_min_value, file=o)

