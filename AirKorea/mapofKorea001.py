#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:31:51 2017

@author: guitar79
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import Polygon

# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

# setup mercator map projection.
m = Basemap(llcrnrlon=125.,llcrnrlat=33.,urcrnrlon=132.,urcrnrlat=39.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=0.,lon_0=0.,lat_ts=1)
#def plot_rec(m, lower_left, upper_left, lower_right, upper_right):
#    upper_left = (127, 34)
#    upper_right= (135, 44)
#    plot_rec(m, lower_left, upper_left, lower_right, upper_right)


m.drawcoastlines()
m.drawcountries()
m.fillcontinents()

# draw parallels
m.drawparallels(np.arange(10,90,0.5),labels=[1,1,1,1])
# draw meridians
m.drawmeridians(np.arange(-180,180,0.5),labels=[1,1,0,0])
m.drawmeridians(np.arange(-180,180,1),labels=[0,0,1,1])
#ax.set_title('Great Circle from New York to London')
fig = plt.gcf()
plt.show()
fig.savefig('GG.pdf')