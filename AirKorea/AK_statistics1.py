# -*- coding: utf-8 -*-
import numpy as np
import os

# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']
#th = float(input('input threshold: '))
#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]
#dr = input('input directory: ')
#dt = 'LAC'
#dr1 = '/media/guitar79/8T/rooknpown/'

dr = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/temp/'
for i in sorted(os.listdir(dr)):
    if i[-4:] == '.csv':
        f = open(dr+i, encoding='euc_kr').read().split('\n')
        f = open(dr+i, 'r',encoding='euc_kr').read().split('\n')
        f = np.array(list(map(lambda x: x.split(','), f)))
        totalrecord = len(f)
        g = np.array(list(filter(lambda x: x[8] == '', f)))
        f = np.array(list(filter(lambda x: x[8] != 0 and float(x[8]) > 0, f)))
        statinum = len(f) 
        errornum = len(g)
        if statinum != 0:
            avg_pm10 = np.mean(f[:,8].astype(np.float))
            print = (avg_pm10)    
        #vmed = np.median(f[:,1].astype(np.float))
         #       vstd = np.std(f[:,1].astype(np.float))
          #      vvar = np.var(f[:,1].astype(np.float))
           #     vmax = np.amax(f[:,1].astype(np.float))
            #    vmin = np.amin(f[:,1].astype(np.float))
             #   with open(dr1+'python_programs/statistics'+dt+'.txt', 'a') as o:
                    #print(i, th1+'--',vsum, vavg, vmed, vstd, vvar, vmax, vmin, totalpix, nanpix, statipix, file=o)
          #  else:
          #      with open(dr1+'python_programs/statistics'+dt+'.txt', 'a') as o:
           #         print(i, th1+'--',0, 0, 0, 0, 0, 0, 0, totalpix, nanpix, statipix, file=o)

