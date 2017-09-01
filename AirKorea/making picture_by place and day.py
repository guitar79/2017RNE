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
drin = 'output/'
#write directory(output data)
drout = 'output2/'


#read data files 
for i in sorted(os.listdir(drbase+drin)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        g = pd.read_csv(drbase+drin+i, encoding='euc_kr')
        #count number of the total data 
        #ooo = np.array(g.ix[:,'PM10'])
        ooo = g[" PM10 "].tolist()
        oPM10=[]
        j=0
        for j in range(0,len(ooo)):
            if j%5==0:
                oPM10.append(ooo[j])
            j=j+1
        e=[]
        for j in range(1,182):
            e.append(j)
        plt.plot(e,oPM10)
        plt.savefig(drbase+drout+i[-10:-4]+'-daily.png')
        plt.savefig(drbase+drout+i[-10:-4]+'-daily.pdf')
        plt.close()

#savefig('fooooo.pdf')

'''
total_mean_value = f.mean().values.reshape(11,1)
total_var_value = f.var().values.reshape(11,1)
total_std_value = f.std().values.reshape(11,1)
total_max_value = f.max().values.reshape(11,1)
total_min_value = f.min().values.reshape(11,1)

#self.output += tds.text
#csv delimeter
#self.output += ','
#csv delimeter
#self.output += '\n'



      for obs in ocode:
                fo=f.loc[f[:,1] == obs]
                #fo=f[f['측정소코드']].isin(obs)
                o_datanum = len(fo)
                if o_datanum != 0:
                    o_mean_value = fo.mean().reshape(1,11)
                    o_var_value = fo.var().reshape(1,11)
                    o_std_value = fo.std().reshape(1,11)
                    o_max_value = fo.max().reshape(1,11)
                    o_min_value = fo.min().reshape(1,11)
                    with open(drbase+drout+'statistics_'+obs+'o.txt', 'a') as o:
                        print(i, obs, o_datanum, o_mean_value, o_var_value, o_std_value, o_max_value, o_min_value, file=o)
                else:
                    with open(drbase+drout+'statistics_'+obs+'o.txt', 'a') as o:
                        print(i, obs, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', file=o)
'''