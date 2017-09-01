# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd

# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

#directory name
dr = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/temp1/'

for i in sorted(os.listdir(dr)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame (like table)
        f = pd.read_csv(dr+i, encoding='euc_kr')
        total_datanum = len(f)
        ocode = list(set(np.array(f.ix[:,'측정소코드'])))
        onumber = len(ocode)
        total_mean_value = f.mean()
        total_var_value = f.var()
        total_std_value = f.std()
        total_max_value = f.max()
        total_min_value = f.min()
        with open(dr+'statistics_total.txt', 'a') as o:
            print(i, total_datanum, total_mean_value, total_var_value, total_std_value, total_max_value, total_min_value, file=o)
            for obs in ocode:
                fo=f.loc[f['측정소코드'] == obs]
                #fo=f[f['측정소코드']].isin(obs)
                o_datanum = len(fo)
                if o_datanum != 0:
                    o_mean_value = fo.mean()
                    o_var_value = fo.var()
                    o_std_value = fo.std()
                    o_max_value = fo.max()
                    o_min_value = fo.min()
                    with open(dr+'statistics_o.txt', 'a') as o:
                        print(i, obs, o_datanum, o_mean_value, o_var_value, o_std_value, o_max_value, o_min_value, file=o)
                else:
                    with open(dr+'statistics_o.txt', 'a') as o:
                        print(i, obs, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', file=o)
