import re
import os
import numpy as np
import pandas as pd
import matplotlib

class FVREF(object):
	"""docstring for DVREF"""
	def __init__(self, arg):
		super(FVREF, self).__init__()
		self._datfile = arg
	
	@property
	def datfile(self):
		return self._datfile
		
	@property
	def num_bodies(self):
		try:
			return self._num_bodies
		except AttributeError:
			f = open(self._datfile,'r')
			tmp = f.read()
			f.close()
			self._num_bodies = int(re.search("Number_of_Bodies\s+=\s+(\d+)",tmp).group(1))
			return self._num_bodies
	
	@property
	def num_fenders(self):
		try:
			return self._num_fenders
		except AttributeError:
			f = open(self._datfile,'r')
			tmp = f.read()
			f.close()
			self._num_fenders = int(re.search("Number_fenders\s+=\s+(\d+)",tmp).group(1))
			return self._num_fenders

	@property
	def num_vessels(self):
		try:
			return self._num_vessels
		except AttributeError:
			f = open(self._datfile,'r')
			tmp = f.read()
			f.close()
			self._num_vessels = int(re.search("no_moving_bodies\s+=\s+(\d+)",tmp).group(1))
	   		return self._num_vessels