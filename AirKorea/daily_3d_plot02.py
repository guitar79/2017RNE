#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 17:09:51 2017
@author: guitar79

=======================
Plot 2D data on 3D plot
=======================

Demonstrates using ax.plot's zdir keyword to plot 2D data on
selective axes of a 3D plot.
"""

from mpl_toolkits.mplot3d import Axes3D
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# data head
# ['지역', '측정소코드', '측정소명', '측정일시', 'SO2', 'CO', 'O3', 'NO2', 'PM10', 'PM25', '주소']

#th_list = [0,5,10,15,20,25,30,35,40,45,50,55,60,65]

#base directory
drbase = '/media/guitar79/8T/RS_data/Remote_Sensing/2017RNE/airkorea/'
#read directory(input data)
drin = 'h_daily_mean1/'
#write directory(output data)
drout = 'overdata/'
if not os.path.exists(drbase+drout):
	os.makedirs(drbase+drout)
#array
ocode = [131571]


#read data files 
for i in ocode:
    #read csv files
    if i[-4:] == '.csv':
        #make data frame from reading csv files (like table)
        g = pd.read_csv(drbase+drin+i, encoding='euc_kr')
        
        for i in range(0,954):
            if g.iloc[i*6+1,10] > 45:
        print(g.iloc[i*6+1,0], g.iloc[i*6+1,2], g.iloc[i*6+1,10])
        m+=1


print(m)





#3d plot
fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot a sin curve using the x and y axes.
x = np.linspace(0, 1, 100)
z = np.sin(x * 2 * np.pi) / 2 + 0.5
ax.plot(x, z, zs=0.5, zdir='y', label='ocode)')

# Plot scatterplot data (20 2D points per colour) on the x and z axes.
colors = ('r', 'g', 'b', 'k')
x = np.random.sample(20*len(colors))
z = np.random.sample(20*len(colors))
c_list = []
for c in colors:
    c_list.append([c]*20)
# By using zdir='y', the y value of these points is fixed to the zs value 0
# and the (x,y) points are plotted on the x and z axes.
ax.scatter(x, z, zs=0, zdir='y', c=c_list, label='points in (x,z)')

# Make legend, set axes limits and labels
ax.legend()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ax.set_xlabel('time')
ax.set_ylabel('site')
ax.set_zlabel('concentration')

# Customize the view angle so it's easier to see that the scatter points lie
# on the plane y=0
ax.view_init(elev=20., azim=-60)

plt.show()