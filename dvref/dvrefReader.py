import re
import os
import numpy as np
import pandas as pd
import matplotlib
#import ogr
#import gdal
#import osr

class DVREF(object):
	"""docstring for DVREF"""
	def __init__(self, arg):
		super(DVREF, self).__init__()
		self._datfile = arg
	
	@property
	def datfile(self):
		return self._datfile
		
	@property
	def num_lines(self):
		try:
			return self._num_lines
		except AttributeError:
			f = open(self._datfile,'r')
			tmp = f.read()
			f.close()
			self._num_lines = int(re.search("Number_lines\s+=\s+(\d+)",tmp).group(1))
			return self._num_lines
	
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
	
	@property
	def unstretch_length(self):
		try:
			return self._unstretch_length
		except AttributeError:
			self._unstretch_length = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through all lines and append to unstretched length
			for line in lines:
				if re.match('^\s+Unstretch_length\s+=\s+(\s*.+)',line):
					tmp_length = re.match('^\s+Unstretch_length\s+=\s+(\s*.+)',line)
					self._unstretch_length.append(float(tmp_length.group(1)))
			
			# Return all unstretched line lengths
			return self._unstretch_length
	
	@property
	def restoring_coeff(self):
		try:
			return self._restoring_coeff
		except AttributeError:
			self._restoring_coeff = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through file and get all restoring coefficients
			for line in lines:
				if re.match('^\s+Restoring_coeff\s+=\s+(\s*.+)',line):
					tmp_coeff = re.match('^\s+Restoring_coeff\s+=\s+(\s*.+)',line).group(1)
					tmp_coeff = tmp_coeff.split(",")
					tmp_coeff = tuple([float(i) for i in tmp_coeff])
					self._restoring_coeff.append(tmp_coeff)
	    	return self._restoring_coeff
	
	@property
	def line_restoring_coeff(self):
		try:
			return self._line_restoring_coeff
		except AttributeError:
			self._line_restoring_coeff = self.restoring_coeff[:self.num_lines]
			return self._line_restoring_coeff
	
	@property
	def fender_restoring_coeff(self):
		try:
			return self._fender_restoring_coeff
		except AttributeError:
			self._fender_restoring_coeff = self.restoring_coeff[-self.num_fenders:]
			return self._fender_restoring_coeff	
	
	@property
	def attachment_ship(self):
		try:
			return self._attachment_ship
		except AttributeError:
			self._attachment_ship = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through and get all ship attachment points
			for line in lines:
				if re.match('^\s+Attachment_ship\s+=\s+(\s*.+)',line):
					tmp_attach_ship = re.match('^\s+Attachment_ship\s+=\s+(\s*.+)',line).group(1)
					tmp_attach_ship = tmp_attach_ship.split(",")
					tmp_attach_ship = tuple([float(i) for i in tmp_attach_ship])
					self._attachment_ship.append(tmp_attach_ship)
	    	return self._attachment_ship
	
	@property
	def line_attach_ship(self):
		try:
			return self._line_attach_ship
		except AttributeError:
			self._line_attach_ship = self.attachment_ship[:self.num_lines]
			return self._line_attach_ship

	@property
	def fender_attach_ship(self):
		try:
			return self._fender_attach_ship
		except AttributeError:
			self._fender_attach_ship = self.attachment_ship[-self.num_fenders:]
			return self._fender_attach_ship
	
	@property
	def attachment_quay(self):
		try:
			return self._attachment_quay
		except AttributeError:
			self._attachment_quay = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through and get all quay attachment points
			for line in lines:
				if re.match('^\s+Attachment_quay\s+=\s+(\s*.+)',line):
					tmp_attach_quay = re.match('^\s+Attachment_quay\s+=\s+(\s*.+)',line).group(1)
					tmp_attach_quay = tmp_attach_quay.split(",")
					tmp_attach_quay = tuple([float(i) for i in tmp_attach_quay])
					self._attachment_quay.append(tmp_attach_quay)
	    	return self._attachment_quay
	
	@property
	def line_attach_quay(self):
		try:
			return self._line_attach_quay
		except AttributeError:
			self._line_attach_quay = self.attachment_quay[:self.num_lines]
			return self._line_attach_quay

	@property
	def fender_attach_quay(self):
		try:
			return self._fender_attach_quay
		except AttributeError:
			self._fender_attach_quay = self.attachment_quay[-self.num_fenders:]
			return self._fender_attach_quay
	
	@property
	def attachment_body(self):
		try:
			return self._attachment_body
		except AttributeError:
			self._attachment_body = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through and get all body attachment points
			for line in lines:
				if re.match('^\s+Attached_to_body\s+=\s+(\s*.+)',line):
					tmp_attach_body = re.match('^\s+Attached_to_body\s+=\s+(\s*.+)',line).group(1)
					tmp_attach_body = tmp_attach_body.split(",")
					tmp_attach_body = tuple([float(i) for i in tmp_attach_body])
					self._attachment_body.append(tmp_attach_body)
	    	return self._attachment_body
	
	@property
	def line_attach_body(self):
		try:
			return self._line_attach_body
		except AttributeError:
			self._line_attach_body = self.attachment_body[:self.num_lines]
			return self._line_attach_body

	@property
	def fender_attach_body(self):
		try:
			return self._fender_attach_body
		except AttributeError:
			self._fender_attach_body = self.attachment_body[-self.num_fenders:]
			return self._fender_attach_body

class DVREFGrid(object):
	"""docstring for DVREFGrid"""
	def __init__(self, arg):
		super(DVREFGrid, self).__init__()
		self._datfile = arg

	@property
	def datfile(self):
		return self._datfile

	@property
	def coordinates(self):
		try:
			return self._coordinates
		except AttributeError:
			self._coordinates = []
			f = open(self._datfile,'r')
			lines = f.readlines()
			f.close()

			# Loop through file and get all coordinates
			for line in lines:
				if re.match('^\s+(\S+)\t\s+(\S+)\t\s+(\S+)',line):
					tmpX = re.match('^\s+(\S+)\t\s+(\S+)\t\s+(\S+)',line).group(1)
					tmpY = re.match('^\s+(\S+)\t\s+(\S+)\t\s+(\S+)',line).group(2)
					tmpZ = re.match('^\s+(\S+)\t\s+(\S+)\t\s+(\S+)',line).group(3)
					tmp_coordinates = (float(tmpX),float(tmpY),float(tmpZ))
					self._coordinates.append(tmp_coordinates)
			self._coordinates = pd.DataFrame(self._coordinates)
			return self._coordinates

	@property
	def deckline(self):
		try:
			return self._deckline
		except AttributeError:
			decklineZ = max(self.coordinates[2].unique())

class DVREFShapefile(object):
	"""docstring for DVREFShapefile"""
	def __init__(self, arg):
		super(DVREFShapefile, self).__init__()
		self.arg = arg
		
class DVRSF(object):
	"""Import XML based DVRSF file"""
	def __init__(self, arg):
		super(DVRSF, self).__init__()
		self._datfile = arg
	
	@property
	def datfile(self):
		return self._datfile

	@property
	def dvrsf(self):
		import xml.etree.cElementTree as et
		try:
			return self._dvrsf
		except AttributeError:
			f = open(self._datfile,'r')
			dvrsf = f.read()
			f.close()

			# Modify unicode to avoid reading error
			dvrsf = dvrsf.encode('utf16')
			self._dvrsf = et.fromstring(dvrsf)
			return self._dvrsf

	@property
	def names(self):
		try:
			return self._names
		except AttributeError:
			names = []
			el = t2.dvrsf.find('Scenarios')
			for scn in el:
				print '{:>15}: {:<30}'.format(scn.tag, scn.text) 
	    	return self._names
	

class Fender(object):
	"""Fender class defines a fender based on fender type. Non-dimensional fender information is hardwired. Later stages would link the 
	fender type to an sqlite database."""
	def __init__(self, fender_type, height, reaction_force):
		super(Fender, self).__init__()
		self.type = fender_type
		self.height = height
		self.reaction_force = reaction_force

	def force_response_non_dim(self):
		import matplotlib.pyplot as plt
		try:
			return self._force_response_non_dim
		except AttributeError:
			# Temporary dictionary for fender curves - At a later stage TODO as a sqlite query

			fenders_dict = {"SCN":{\
			
			"Deflection":[0.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,72.0],\
			"Force":[0,19,39,59,75,89,97,99,98,92,84,77,73,77,91,100]},\
			"SCK":{"Deflection":[0,1,2,3,4],\
			"Force":[0,1,8,27,64]}}
			
			self._force_response_non_dim = (fenders_dict[self.type]["Deflection"],fenders_dict[self.type]["Force"])
			return self._force_response_non_dim
	
	def force_response_actual(self):
		try:
			return self._force_response_actual
		except AttributeError:
			deflection_actual = [self.height * i / 100 for i in self.force_response_non_dim()[0]]
			force_actual = [self.reaction_force * i / 100 for i in self.force_response_non_dim()[1]]

			self._force_response_actual = (deflection_actual,force_actual)
			return self._force_response_actual
	
	def plot(self):
		import matplotlib.pyplot as plt
		plt.plot(self.force_response_actual()[0],self.force_response_actual()[1])
		plt.grid()
		plt.show()

	def polyCoefficients(self):
		try:
			return self._polyCoefficients
		except AttributeError:
			import numpy as np
			x = np.array(self.force_response_actual()[0])
			y = np.array(self.force_response_actual()[1])
			self._polyCoefficients = np.polyfit(x,y,5)
			return self._polyCoefficients

class PMFenders(object):
	"""Combination of fenders into parallel motion fenders in series"""
	def __init__(self, fender1, fender2):
		super(PMFenders, self).__init__()
		self.fender1 = fender1
		self.fender2 = fender2
	
"""	
if __name__ == '__main__':
	os.chdir(os.path.dirname(__file__))
	print os.getcwd()

	t1 = DVREF("../data/DVR.dvref")


	spatialReference = osr.SpatialReference()
	spatialReference.ImportFromProj4('+proj=utm +zone=34 +south +datum=WGS84 +units=m +no_defs')

	# TODO: Temporary script to extract connection point data
	# Create connection points
	driver = ogr.GetDriverByName('ESRI Shapefile')
	shapeData = driver.CreateDataSource('./connection_points.shp')

	layer = shapeData.CreateLayer('layer1', spatialReference, ogr.wkbPoint)
	layerDefinition = layer.GetLayerDefn()

	for idx in range(len(t1.line_attach_quay)):

		fairlead = t1.line_attach_quay[idx]

		point = ogr.Geometry(ogr.wkbPoint)
		point.SetPoint(0,fairlead[0],fairlead[1])

		featureIndex = idx
		feature = ogr.Feature(layerDefinition)
		feature.SetGeometry(point)
		feature.SetFID(featureIndex)

		layer.CreateFeature(feature)

	shapeData.Destroy()

	# Create mooring lines
	driver=ogr.GetDriverByName('ESRI Shapefile')
	ds=driver.CreateDataSource('mooring_lines.shp')
	layer=ds.CreateLayer('mooring_lines', geom_type=ogr.wkbLineString)
	fieldDefn=ogr.FieldDefn('id', ogr.OFTInteger)

	layer.CreateField(fieldDefn)
	
	featureDefn=layer.GetLayerDefn()

	for idx in range(len(t1.line_attach_quay)):

		line=ogr.Geometry(ogr.wkbLineString)

		fairlead = t1.line_attach_ship[idx]
		quay 	 = t1.line_attach_quay[idx]

		line.AddPoint(fairlead[0],fairlead[1])
		line.AddPoint(quay[0],quay[1])


		feature=ogr.Feature(featureDefn)
		feature.SetGeometry(line)
		feature.SetField('id',1)
		layer.CreateFeature(feature)

	ds.Destroy()

	# Create fender
	driver = ogr.GetDriverByName('ESRI Shapefile')
	ds = driver.CreateDataSource('fenders.shp')
	layer = ds.CreateLayer('fenders', spatialReference, ogr.wkbPoint)
	
	# Write fenders to shapefile
	layerDefinition = layer.GetLayerDefn()
	for idx in range(len(t1.fender_attach_ship)):

		fairlead = t1.fender_attach_ship[idx]

		point = ogr.Geometry(ogr.wkbPoint)
		point.SetPoint(0,fairlead[0],fairlead[1])

		featureIndex = idx
		feature = ogr.Feature(layerDefinition)
		feature.SetGeometry(point)
		feature.SetFID(featureIndex)

		layer.CreateFeature(feature)

	ds.Destroy()

	print t1.fender_attach_ship
"""
