import numpy as np
from Scientific.Functions.Interpolation import InterpolatingFunction
lats = np.arange(-90,90.5,0.5)
lons = np.arange(-180,180,0.5)
alts = np.arange(1,1000,21.717)
time = np.arange(8)
data = np.random.rand(len(lats)*len(lons)*len(alts)*len(time)).reshape((len(lats),len(lons),len(alts),len(time)))
axes = (lats, lons, alts, time)
f = InterpolatingFunction(axes, data)