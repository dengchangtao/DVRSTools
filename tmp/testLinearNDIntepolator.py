import numpy as np
from scipy.interpolate import LinearNDInterpolator

lats = np.arange(-90,90.5,0.5)
lons = np.arange(-180,180,0.5)
alts = np.arange(1,1000,21.717)
time = np.arange(8)
data = np.random.rand(len(lats)*len(lons)*len(alts)*len(time)).reshape((len(lats),len(lons),len(alts),len(time)))

coords = np.zeros((len(lats),len(lons),len(alts),len(time),4),dtype=object)
coords[...,0] = lats.reshape((len(lats),1,1,1))
coords[...,1] = lons.reshape((1,len(lons),1,1))
coords[...,2] = alts.reshape((1,1,len(alts),1))
coords[...,3] = time.reshape((1,1,1,len(time)))
coords = coords.reshape((data.size,4))

interpolatedData = LinearNDInterpolator(coords,data)