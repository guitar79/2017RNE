#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 18:55:20 2017

@author: guitar79
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as dates
import datetime, random
import matplotlib.ticker as ticker

def random_date():
    date = datetime.date(2008, 12, 1)
    while 1:
        date += datetime.timedelta(days=30)
        yield (date)

def format_date(x, pos=None):
    return dates.num2date(x).strftime('%Y-%m-%d') #use FuncFormatter to format dates
r_d = random_date()
#some_dates = [dates.date2num(r_d.next()) for i in range(0,20)]
some_dates = [dates.date2num(next(r_d)) for i in range(0,20)]

fig = plt.figure()
ax = Axes3D(fig,rect=[0,0.1,1,1]) #make room for date labels

for c, z in zip(['r', 'g', 'b', 'y'], [115, 60, 10, 0]):
    xs = np.array(some_dates)
    ys = np.random.rand(20)
    ax.bar(xs, ys, zs=z, zdir='y', color=c, alpha=0.8,width=8)

ax.w_xaxis.set_major_locator(ticker.FixedLocator(some_dates)) # I want all the dates on my xaxis
ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

for tl in ax.w_xaxis.get_ticklabels(): # re-create what autofmt_xdate but with w_xaxis
    tl.set_ha('right')
    tl.set_rotation(30)     

ax.set_ylabel('Series')
ax.set_zlabel('Amount')
ptint(some_dates)
plt.show()