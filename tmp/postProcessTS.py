"""
Class for post-processing DVRS results from ascii output file format
"""

import re
import os
import fortranformat as ff 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as sg 


class DVRSTimeSeries(object):
	"""docstring for DVRSTimeSeries"""
	def __init__(self, arg):
		super(DVRSTimeSeries, self).__init__()
		self._datfile = arg

	@property
	def datfile(self):
	    return self._datfile
	
	@property
	def results_type(self):
	    return self._results_type
	
	@property
	def time_series(self):
		try:
			return self._time_series
		except AttributeError:
			f = open(self._datfile,'r')
			tmp = f.readlines()
			f.close()
			self._time_series = tmp
			return self._time_series

	@property
	def statistics(self):
	    return self._statistics
		
	
if __name__ == '__main__':
	ts_file = "../data/DynamicVRengine.lforces"
	t1 = DVRSTimeSeries(ts_file)
	t1.time_series
	print t1.time_series[1]


