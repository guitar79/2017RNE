#place and date(1day)

# -*- coding: utf-8 -*-
# Auther guitar79@naver.com 

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'h_annual_mean2/'
#write directory(output data)
drout = 'overdata/'

#make empty dataframe(1,11) with head
#head = ('지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소')
head = ('day','Region','RegionCode','RegionName','var','SO2','CO','O3','NO2','PM10','PM25','Address')
head = np.array(head)
head = head.reshape(1,12)
f = pd.DataFrame(head)
#empty dataframe(1,11) columns header

#read data files 
for i in sorted(os.listdir(drbase+drin)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        g = pd.read_csv(drbase+drin+i, encoding='euc_kr')

m=0
for i in range(0,954):
    if g.iloc[i*6+1,10] > 45:
        print(g.iloc[i*6+1,0], g.iloc[i*6+1,2], g.iloc[i*6+1,10])
        m+=1


print(m)








