# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:50:01 2016

@author: pbs
"""

import numpy as np
from scipy.interpolate import LinearNDInterpolator
from itertools import product

# Define the dimensions
lats = np.array((-90,-87, -80))
lons = np.arange(-180,-170,5)
alts = np.arange(1,10,5)
time = np.arange(4)
#Dim5 = np.arange(5)

# Populate an n dimensional array with data
data = np.random.rand(len(lats)*len(lons)*len(alts)*len(time)).reshape((len(lats),len(lons),len(alts),len(time)))

#Create an n + 1 dimensoinal array
coords = np.zeros((len(lats),len(lons),len(alts),len(time),4))
coords[...,0] = lats.reshape((len(lats),1,1,1))
coords[...,1] = lons.reshape((1,len(lons),1,1))
print coords
coords[...,2] = alts.reshape((1,1,len(alts),1))
coords[...,3] = time.reshape((1,1,1,len(time)))

coords = coords.reshape((data.size,4))
#print coords

def interpolator(coords, data, point) :
    """
    n dimensional interpolator
    """
    dims = len(point)
    indices = []
    sub_coords = []
    for j in xrange(dims) :
        idx = np.digitize([point[j]], coords[j])[0]
        indices += [[idx - 1, idx]]
        sub_coords += [coords[j][indices[-1]]]
    indices = np.array([j for j in product(*indices)])
    sub_coords = np.array([j for j in product(*sub_coords)])
    sub_data = data[list(np.swapaxes(indices, 0, 1))]
    li = LinearNDInterpolator(sub_coords, sub_data)
    return li([point])[0]

point = np.array([-88,-176, 5, 2.5])

print interpolator((lats, lons, alts, time), data, point)