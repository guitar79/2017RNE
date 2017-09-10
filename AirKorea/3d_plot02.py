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
import numpy as np
import matplotlib.pyplot as plt

ocode = [131571, 525142, 437154, 525161]

#x = [20140101, 20140102, 20140103, 20140104, 20140105, 20140106, 20140107, 20140201, 20140202, 20140203]
x = ["20140101", "20140102", "20140103", "20140104", "20140105", "20140106", "20140107", "20140201", "20140202", "20140203"]
z1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
z2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
z3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
z4 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot a sin curve using the x and y axes.
#x = np.linspace(0, 1, 100)
#z = np.sin(x * 2 * np.pi) / 2 + 0.5
#ax.plot(x, z1, zs=0, zdir='y', label='ocode)')
#ax.plot(x, z1, zs=0, zdir='y', label='131571')
#ax.plot(x, z2, zs=1, zdir='y', label='525142')
#ax.plot(x, z3, zs=2, zdir='y', label='437154')
#ax.plot(x, z4, zs=3, zdir='y', label='525161')

ax.scatter(x, z1, zs=0, zdir='y', c='r', label='131571')

# Plot scatterplot data (20 2D points per colour) on the x and z axes.

# Make legend, set axes limits and labels
ax.legend()

#datetick('x','dd/mm/yyyy')
#ax.set_xlim(20140101, 20140203)
#ax.set_xlim(['20140101', '20140102', '20140103', '20140104', '20140105', '20140106', '20140107', '20140201', '20140202', '20140203'])
ax.set_zlim(0, 20)
#ax.set_ylim(['131571', '525142', '437154', '525161'])
#ax.xticks(data)

ax.set_xlabel('time')
ax.set_ylabel('site')
ax.set_zlabel('SO2 concentration(ppm)')

# Customize the view angle so it's easier to see that the scatter points lie
# on the plane y=0
#zx.xticks(x,xticks)
ax.view_init(elev=20, azim=-80)


#plt.show()