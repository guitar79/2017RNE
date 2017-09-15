from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import matplotlib.dates as dates
import datetime, random
import matplotlib.ticker as ticker

al=be=ga=0#exact number
Al=Be=Ga=0#ocode

def comp(de,De):
    global al,be,ga,Al,Be,Ga
    if de>=ga:
        al=be
        Al=Be
        be=ga
        Be=Ga
        ga=de
        Ga=De
        return
    if de>=be:
        al=be
        Al=Be
        be=de
        Be=De
        return
    if de>=al:
        al=de
        Al=De
        return


# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin1 = 'h_annual_mean2/'
drin2 = 'h_daily_mean1/'
#write directory(output data)
drout = 'dailyintograph/SO2/'

#make empty dataframe(1,11) with head
#head = ('지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소')
head = ('day','Region','RegionCode','RegionName','var','SO2','CO','O3','NO2','PM10','PM25','Address')
head = np.array(head)
head = head.reshape(1,12)
f = pd.DataFrame(head)
#empty dataframe(1,11) columns header

#read data files 
for i in sorted(os.listdir(drbase+drin1)):
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        g = pd.read_csv(drbase+drin1+i, encoding='euc_kr')

Aldata=np.array([0])
Bedata=np.array([0])
Gadata=np.array([0])


fig = plt.figure()
ax = fig.gca(projection='3d')

ax.scatter(1, 1, zs=0, zdir='y', c='black', label='points in (x,z)')


# By using zdir='y', the y value of these points is fixed to the zs value 0
# and the (x,y) points are plotted on the x and z axes.
for i in range(1,1097):
    ax.scatter(i, 1, zs=1, zdir='y', c='black')

# Make legend, set axes limits and labels
ax.legend()
ax.set_xlim(0, 1097)
ax.set_ylim(0, 2)
ax.set_zlim(0, 50)
ax.set_xlabel('time')
ax.set_ylabel('site')
ax.set_zlabel('concentration')

# Customize the viehttp://pixinsight.com/w angle so it's easier to see that the scatter points lie
# on the plane y=0
ax.view_init(elev=20., azim=-60)









http://pixinsight.com/










m=0
for i in range(0,954):
    if g.iloc[i*6+1,10] > 25:
        comp(g.iloc[i*6+1,10],g.iloc[i*6+1,2])

Feb29 = pd.read_csv(drbase+drin2+'statistics_20160229.csv', encoding='euc_kr')

for i in sorted(os.listdir(drbase+drin2)):
    #read csv files
    if i[-4:] == '.csv':
        lolol=i[11:-4]
        #print(lolol)
        if int(lolol) == int(Ga) or int(lolol) == int(Be) or int(lolol) == int(Al):
            G = pd.read_csv(drbase+drin2+i, encoding='euc_kr')
        if int(lolol) == int(Ga):
            for j in range(0,954):
                ax.scatter(j, G.iloc[j*6+1,10], zs=1, zdir='y', c='black')
        if int(lolol) == int(Be):
            for j in range(0,954):
                ax.scatter(j, G.iloc[j*6+1,10], zs=1, zdir='y', c='black')
        if int(lolol) == int(Al):
            for j in range(0,954):
                ax.scatter(j, G.iloc[j*6+1,10], zs=1, zdir='y', c='black')
        #
for j in range(0,320):
    if Feb29.iloc[j*6+1,2] == int(lolol):
        ax.scatter(j, Feb29.iloc[j*6+1,2], zs=1, zdir='y', c='black')
        break
for j in range(0,320):
    if Feb29.iloc[j*6+1,2] == int(lolol):
        np.insert(Gadata,p,Feb29.iloc[j*6+1,10])
        break
for j in range(0,320):
    if Feb29.iloc[j*6+1,2] == int(lolol):
        np.insert(Gadata,p,Feb29.iloc[j*6+1,10])
        break


plt.show()