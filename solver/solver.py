import os
import wx
from PyQt4.QtGui import QFileDialog
import pandas as pd
import re
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from itertools import product
import linecache
import matplotlib as plt
import math
"""
This solves 5 DOF interpolation.
"""
def readMetocean(metoceanfile):
	"""
	Read into pandas dataframe a tab delimited metocean file format from 
	"""
	headers = None
	headers = re.split(r"\t",linecache.getline(metoceanfile,2).rstrip('\n'))
	print headers
	metocean = pd.read_csv(metoceanfile, sep="\t",skiprows=3,parse_dates=0,names=headers,index_col=0)
	return metocean

def readHm0(logfile,point):
	with open(logfile) as f:
		lines = f.readlines()

	search_string = "Results of directional wave analysis \["+str(point)+"\]"
	results_idx = [ii for ii, item in enumerate(lines) if re.search(search_string,item)]

	hm0_idx = results_idx[0] + 5
	m = re.search(':\s+(\d*.+)\s+m',lines[hm0_idx])
	return(m.group(1))

def readRuns(runsfile):
	"""
	Read into pandas dataframe a csv file with runs information
	"""
	runs = pd.read_csv(runsfile,sep="\t")
	return(runs)

def readResults(resultsfile):
	"""
	Read into pandas dataframe a csv file with runs information
	"""
	runs = pd.read_csv(resultsfile,sep=",")
	return(runs)

def getArrayDims(runsfile):
	# Get runs file for discrete unique cases
	df = readRuns(runsfile)
	WAVE_HEIGHTS = df['WAVE_HEIGHT'].unique()
	WAVE_HEIGHTS.sort(axis=0)
	WAVE_PERIODS = df['WAVE_PERIOD'].unique() 
	WAVE_PERIODS.sort(axis=0)
	WAVE_DIRECTIONS = df['WAVE_DIRECTION'].unique()
	WAVE_DIRECTIONS.sort(axis=0)
	WIND_SPEEDS = df['WIND_SPEED'].unique()
	WIND_SPEEDS.sort(axis=0)
	WIND_DIRECTIONS = df['WIND_DIRECTION'].unique()
	WIND_DIRECTIONS.sort(axis=0)
	# TODO: GET DATA FUNCTION HERE
	# Set all values to zero
	data = np.empty((len(WAVE_HEIGHTS)*len(WAVE_PERIODS)*len(WAVE_DIRECTIONS)*len(WIND_SPEEDS)*len(WIND_DIRECTIONS)))
	data[:] = np.NAN
	data = data.reshape((len(WAVE_HEIGHTS),len(WAVE_PERIODS),len(WAVE_DIRECTIONS),len(WIND_SPEEDS),len(WIND_DIRECTIONS)))

	coords = np.zeros((len(WAVE_HEIGHTS),len(WAVE_PERIODS),len(WAVE_DIRECTIONS),len(WIND_SPEEDS),len(WIND_DIRECTIONS),5))
	coords[:] = np.NAN

	coords[...,0] = WAVE_HEIGHTS.reshape((len(WAVE_HEIGHTS),1,1,1,1))
	coords[...,1] = WAVE_PERIODS.reshape((1,len(WAVE_PERIODS),1,1,1))
	coords[...,2] = WAVE_DIRECTIONS.reshape((1,1,len(WAVE_DIRECTIONS),1,1))
	coords[...,3] = WIND_SPEEDS.reshape((1,1,1,len(WIND_SPEEDS),1))
	coords[...,4] = WIND_DIRECTIONS.reshape((1,1,1,1,len(WIND_DIRECTIONS)))
	#print coords
	#return coords
	coords = coords.reshape((data.size,5))
	#print coords
	return coords

def getArrayDims2(runsfile,array_index):
	# Get runs file for discrete unique cases
	df = readRuns(runsfile)
	var01 =df[df.columns[array_index[0]]].unique()
	var01.sort(axis=0)
	var02 = df[df.columns[array_index[1]]].unique() 
	var02.sort(axis=0)
	var03 = df[df.columns[array_index[2]]].unique()
	var03.sort(axis=0)
	var04 = df[df.columns[array_index[3]]].unique()
	var04.sort(axis=0)
	var05 = df[df.columns[array_index[4]]].unique()
	var05.sort(axis=0)
	# TODO: GET DATA FUNCTION HERE
	# Set all values to zero
	data = np.empty((len(var01)*len(var02)*len(var03)*len(var04)*len(var05)))
	data[:] = np.NAN
	data = data.reshape((len(var01),len(var02),len(var03),len(var04),len(var05)))

	coords = np.zeros((len(var01),len(var02),len(var03),len(var04),len(var05),5))
	coords[:] = np.NAN

	coords[...,0] = var01.reshape((len(var01),1,1,1,1))
	coords[...,1] = var02.reshape((1,len(var02),1,1,1))
	coords[...,2] = var03.reshape((1,1,len(var03),1,1))
	coords[...,3] = var04.reshape((1,1,1,len(var04),1))
	coords[...,4] = var05.reshape((1,1,1,1,len(var05)))
	#print coords
	#return coords
	coords = coords.reshape((data.size,5))
	#print coords
	return coords

def getLocationDicts(runsfile):
	df = readRuns(runsfile)
	WAVE_HEIGHTS = df['WAVE_HEIGHT'].unique()
	WAVE_HEIGHTS.sort(axis=0)
	WAVE_PERIODS = df['WAVE_PERIOD'].unique() 
	WAVE_PERIODS.sort(axis=0)
	WAVE_DIRECTIONS = df['WAVE_DIRECTION'].unique()
	WAVE_DIRECTIONS.sort(axis=0)
	WIND_SPEEDS = df['WIND_SPEED'].unique()
	WIND_SPEEDS.sort(axis=0)
	WIND_DIRECTIONS = df['WIND_DIRECTION'].unique()
	WIND_DIRECTIONS.sort(axis=0)

	WAVE_HEIGHTS_DICT = {}
	for ii in xrange(0,len(WAVE_HEIGHTS)):
		WAVE_HEIGHTS_DICT[WAVE_HEIGHTS[ii]] = ii
	WAVE_PERIODS_DICT = {}
	for ii in xrange(0,len(WAVE_PERIODS)):
		WAVE_PERIODS_DICT[WAVE_PERIODS[ii]] = ii
	WAVE_DIRECTIONS_DICT = {}
	for ii in xrange(0,len(WAVE_DIRECTIONS)):
		WAVE_DIRECTIONS_DICT[WAVE_DIRECTIONS[ii]] = ii
	WIND_DIRECTIONS_DICT = {}
	for ii in xrange(0,len(WIND_DIRECTIONS)):
		WIND_DIRECTIONS_DICT[WIND_DIRECTIONS[ii]] = ii
	WIND_SPEEDS_DICT = {}
	for ii in xrange(0,len(WIND_SPEEDS)):
		WIND_SPEEDS_DICT[WIND_SPEEDS[ii]] = ii

	return([WAVE_HEIGHTS_DICT,WAVE_PERIODS_DICT,WAVE_DIRECTIONS_DICT,WIND_SPEEDS_DICT,WIND_DIRECTIONS_DICT])

def getLocationDicts2(runsfile,array_index):
	df = readRuns(runsfile)
	var01 = df[df.columns[array_index[0]]].unique()
	var01.sort(axis=0)
	var02 = df[df.columns[array_index[1]]].unique() 
	var02.sort(axis=0)
	var03 = df[df.columns[array_index[2]]].unique()
	var03.sort(axis=0)
	var04 = df[df.columns[array_index[3]]].unique()
	var04.sort(axis=0)
	var05 = df[df.columns[array_index[4]]].unique()
	var05.sort(axis=0)

	var01_dict = {}
	for ii in xrange(0,len(var01)):
		var01_dict[var01[ii]] = ii
	var02_dict = {}
	for ii in xrange(0,len(var02)):
		var02_dict[var02[ii]] = ii
	var03_dict = {}
	for ii in xrange(0,len(var03)):
		var03_dict[var03[ii]] = ii
	var05_dict = {}
	for ii in xrange(0,len(var05)):
		var05_dict[var05[ii]] = ii
	var04_dict = {}
	for ii in xrange(0,len(var04)):
		var04_dict[var04[ii]] = ii

	return([var01_dict,var02_dict,var03_dict,var04_dict,var05_dict])

def loopCases(runsfile,wavefolder,logfile):
	runs = readRuns(runsfile)
	WAVE_AGITATION = []
	for index, row in runs.iterrows():
		folderstring = "H0%.1F_T%02d_D%03d" % (row['WAVE_HEIGHT'],row['WAVE_PERIOD'],row['WAVE_DIRECTION'])
		folderstring = folderstring + ".bw - Result Files"
		WAVE_AGITATION.append(float(readHm0(os.path.join(wavefolder,folderstring,"Analysis",logfile),16))/row['WAVE_HEIGHT'])
	#print WAVE_AGITATION
	runs['WAVE_AGITATION'] = WAVE_AGITATION
	return runs
	
def df_dict(df):
	tmp_dict = {}
	for ii in xrange(0,len(df.columns)):
		tmp_dict[df.columns[ii]] = ii
	return tmp_dict

def loopCases2(runsfile,wavefolder,logfile,data_index,output_point,var_name):
	# Get and set values from results files - this code needs to change to account for results for the vessel motions response
	runs = readRuns(runsfile)
	var_array = []
	for index, row in runs.iterrows():
		folderstring = "H0%.1F_T%02d_D%03d" % (row[runs.columns[data_index[0]]],row[runs.columns[data_index[1]]],row[runs.columns[data_index[2]]])
		folderstring = folderstring + ".bw - Result Files"
		# Non-dimensionalise results with respect to the incident wave height
		var_array.append(float(readHm0(os.path.join(wavefolder,folderstring,"Analysis",logfile),output_point))/row[runs.columns[data_index[0]]])

	# Set variable data to runs data frame
	runs[var_name] = var_array
	return runs

def getDataFrameVal(df,query_variables,required_val):
	"""
	Helper function to extract variable value from a pandas data frame - fixed values are specified:
	WAVE_HEIGHT,WAVE_PERIOD,WAVE_DIRECTION,WIND_SPEED,WIND_DIRECTION,variable
	"""
	return_val = df[df['WAVE_HEIGHT'].isin([query_variables[0]])]\
	[df['WAVE_PERIOD'].isin([query_variables[1]])]\
	[df['WAVE_DIRECTION'].isin([query_variables[2]])]\
	[df['WIND_SPEED'].isin([query_variables[3]])]\
	[df['WIND_DIRECTION'].isin([query_variables[4]])]\
	[required_val].values[0]

	return(return_val)

def getDataFrameVal2(df,query_variables,required_val):
	"""
	Helper function to extract variable value from a pandas data frame - fixed values are specified:
	WAVE_HEIGHT,WAVE_PERIOD,WAVE_DIRECTION,WIND_SPEED,WIND_DIRECTION,variable
	"""
	return_val = df[df['WAVE_HEIGHT'].isin([query_variables[0]])]\
	[df['WAVE_PERIOD'].isin([query_variables[1]])]\
	[df['WAVE_DIRECTION'].isin([query_variables[2]])]\
	[df['WIND_SPEED'].isin([query_variables[3]])]\
	[df['WIND_DIRECTION'].isin([query_variables[4]])]\
	[required_val].values[0]

	return(return_val)

def interpolator(coords, data, point) :
	# n dimensional interpolator
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

def readForces(resultsfile):
	df = pd.read_csv(resultsfile)
	return df

def readMotions(motionsfile):
	pass

def getDVRFInfo(template_file):
	f = open(template_file,'r')
	tmp = f.read()
	f.close()
	
	# Get required info from template file for processing results data	
	number_of_lines = int(re.search("Number_lines = (\d+)",tmp).group(1))
	number_of_fenders = int(re.search("Number_fenders\s+=\s+(\d+)",tmp).group(1))
	number_of_vessels = int(re.search("no_moving_bodies\s+=\s+(\d+)",tmp).group(1))
	
	print number_of_vessels
	# Return layout info
	return (number_of_lines,number_of_fenders,number_of_vessels)

def setResultsDf(runsfile,template_file):
	layout_info = getDVRFInfo(template_file)
	df_runs = readRuns(runsfile)

	num_lines = layout_info[0]
	num_fenders = layout_info[1]
	num_vessesls = layout_info[2]

	results_headers = []
	motions = ["Surge","Sway","Heave","Roll","Pitch","Yaw"]
	for ii in xrange(num_vessesls):
		for motion in motions:
			results_headers.append("Vessel%02d_%s" % (float(ii + 1),motion))
	for jj in xrange(num_lines):
		results_headers.append("Lines%02d" % float(jj+1))
	for kk in xrange(num_fenders):
		results_headers.append("Fenders%02d" % float(kk+1))
	for header in results_headers:
		df_runs[header] = np.nan
		df_runs.ix[:,header] = np.nan #1.
	return df_runs


"""
TODO:
Loop through folders and read agitation coefficients - Hm0 input required
Populate arrays with agitation coefficients - numpy.fromfunction(function,shape,**kwargs)
Loop through wave time series and populate time series dataframe
"""	
"""

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
	coords[...,2] = alts.reshape((1,1,len(alts),1))
	coords[...,3] = time.reshape((1,1,1,len(time)))

	coords = coords.reshape((data.size,4))
	#print coords

	def interpolator(coords, data, point) :
		# n dimensional interpolator
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
"""

def setDataValues(runsfile,wavefolder,logfile):
	# Get runs file for discrete unique cases
	df = readRuns(runsfile)
	WAVE_HEIGHTS = df['WAVE_HEIGHT'].unique()
	WAVE_HEIGHTS.sort(axis=0)
	WAVE_PERIODS = df['WAVE_PERIOD'].unique() 
	WAVE_PERIODS.sort(axis=0)
	WAVE_DIRECTIONS = df['WAVE_DIRECTION'].unique()
	WAVE_DIRECTIONS.sort(axis=0)
	WIND_SPEEDS = df['WIND_SPEED'].unique()
	WIND_SPEEDS.sort(axis=0)
	WIND_DIRECTIONS = df['WIND_DIRECTION'].unique()
	WIND_DIRECTIONS.sort(axis=0)
	# TODO: GET DATA FUNCTION HERE
	# Set all values to zero
	data = np.empty((len(WAVE_HEIGHTS)*len(WAVE_PERIODS)*len(WAVE_DIRECTIONS)*len(WIND_SPEEDS)*len(WIND_DIRECTIONS)))
	data[:] = np.NAN
	data = data.reshape((len(WAVE_HEIGHTS),len(WAVE_PERIODS),len(WAVE_DIRECTIONS),len(WIND_SPEEDS),len(WIND_DIRECTIONS)))

	results = loopCases(runsfile,wavefolder,logfile)

	indexDict = getLocationDicts(runsfile)
	#data[0,0,0,0,0] = 100.
	for index, row in results.iterrows():
		var1_idx = indexDict[0][row['WAVE_HEIGHT']]
		var2_idx = indexDict[1][row['WAVE_PERIOD']]
		var3_idx = indexDict[2][row['WAVE_DIRECTION']]
		var4_idx = indexDict[3][row['WIND_SPEED']]
		var5_idx = indexDict[4][row['WIND_DIRECTION']]

		data[var1_idx,var2_idx,var3_idx,var4_idx,var5_idx] = row['WAVE_AGITATION']
		

		#print var1_idx, var2_idx, var3_idx, var4_idx,var5_idx, row['WAVE_AGITATION']
	return data

def setDataValues2(runsfile,wavefolder,logfile,array_index):
	# Get runs file for discrete unique cases
	df = readRuns(runsfile)
	var01 =df[df.columns[array_index[0]]].unique()
	var02 = df[df.columns[array_index[1]]].unique() 
	var03 = df[df.columns[array_index[2]]].unique()
	var04 = df[df.columns[array_index[3]]].unique()
	var05 = df[df.columns[array_index[4]]].unique()

	# TODO: GET DATA FUNCTION HERE
	# Set all values to zero
	data = np.empty((len(var01)*len(var02)*len(var03)*len(var04)*len(var05)))
	data[:] = np.NAN
	data = data.reshape((len(var01),len(var02),len(var03),len(var04),len(var05)))

	results = loopCases(runsfile,wavefolder,logfile)
	
	indexDict = getLocationDicts(runsfile)
	#data[0,0,0,0,0] = 100.
	for index, row in results.iterrows():
		var1_idx = indexDict[0][row[results.columns[array_index[0]]]]
		var2_idx = indexDict[1][row[results.columns[array_index[1]]]]
		var3_idx = indexDict[2][row[results.columns[array_index[2]]]]
		var4_idx = indexDict[3][row[results.columns[array_index[3]]]]
		var5_idx = indexDict[4][row[results.columns[array_index[4]]]]

		data[var1_idx,var2_idx,var3_idx,var4_idx,var5_idx] = row['WAVE_AGITATION']
		

		#print var1_idx, var2_idx, var3_idx, var4_idx,var5_idx, row['WAVE_AGITATION']
	return data

def setDataValues3(runsfile,df,results_idx,array_index = [1,2,3,4,5]):
	print array_index	
	print results_idx
	# Get unique values from input data
	var01 =df[df.columns[array_index[0]]].unique()
	var02 = df[df.columns[array_index[1]]].unique() 
	var03 = df[df.columns[array_index[2]]].unique()
	var04 = df[df.columns[array_index[3]]].unique()
	var05 = df[df.columns[array_index[4]]].unique()

	# Set all initial data values to zero
	data = np.empty((len(var01)*len(var02)*len(var03)*len(var04)*len(var05)))
	data[:] = np.NAN
	data = data.reshape((len(var01),len(var02),len(var03),len(var04),len(var05)))

	indexDict = getLocationDicts(runsfile)	

	for index, row in df.iterrows():
		var1_idx = indexDict[0][row[df.columns[array_index[0]]]]
		var2_idx = indexDict[1][row[df.columns[array_index[1]]]]
		var3_idx = indexDict[2][row[df.columns[array_index[2]]]]
		var4_idx = indexDict[3][row[df.columns[array_index[3]]]]
		var5_idx = indexDict[4][row[df.columns[array_index[4]]]]

		data[var1_idx,var2_idx,var3_idx,var4_idx,var5_idx] = row[df.columns[results_idx]]

	return data

def convertWindSpeed(wind_mag,wind_dir):
	'''
	Function to convert wind speed and direction of wind from to wind vectors wind to.
	'''
	angle_rad = math.radians(wind_dir)
	# Need to multiply the vectors by -1 because of wind from and wind to
	u_vec = -1*wind_mag*math.sin(angle_rad)
	v_vec = -1*wind_mag*math.cos(angle_rad)
	vector = (u_vec,v_vec)
	return(vector)

def convert_mike_to_aqwa(mike_angle,vessel_orientation):
    '''
    Function to convert input wave conditions from TN orientation from to AQWA/DVRS direction toward.
    '''
    if (vessel_orientation == 0):
        return float(mike_angle)
    else:
        alpha = vessel_orientation
        theta = float(mike_angle)
        # Get change in wave angle with respect to orientation
        theta_prime = (360. - alpha) + theta
        if theta_prime >= 360.:
            theta_prime = theta_prime - 360.
        # Convert to angle wrt vessel orientation
        beta = (180. - theta_prime)
        if beta <= 0.:
            beta = beta + 360.
        return float(beta)

def add_aqwa_orienation(dfmetocean,direction_idx,orientationTN):
	aqwa_direction = []
	for index, row in dfmetocean.iterrows():
		aqwa_direction.append(convert_mike_to_aqwa(row[dfmetocean.columns[direction_idx]],orientationTN))
	dfmetocean['AQWA_Directions'] = aqwa_direction
	return dfmetocean
		
def getAllForces(runsDF,vessel_files = ["Vessel01_Motions.csv","Vessel02_Motions.csv"]):
	for index, row in runsDF.iterrows():
		tmpcase = str(row[runsDF.columns[0]]).zfill(4)		

		# Open results file
		tmpResultsLines = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results.csv")
		#tmpResultsMotions = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Motions.csv")
		
		# Check if file exists, if true, convert to dataframe
		if os.path.isfile(tmpResultsLines):
			tmpdf_lines = readResults(tmpResultsLines)
			tmpforces = list(tmpdf_lines['Maximum [N]'])
			
			vessel_results = []
			# Iterate through list of vessel files
			for vessel in vessel_files:
				tmpResultsMotions = os.path.join(os.getcwd(),"DVREF",tmpcase,"out",vessel)
				tmpdf_motions = readResults(tmpResultsMotions)
				#tmpmotions = list(tmpdf_motions['PtoP Max'])

				tmpmotions = []

				tmpMax = list(tmpdf_motions['Maximum [m:deg]'])
				tmpMin = list(tmpdf_motions['Minimum [m:deg]'])
				tmpMean = list(tmpdf_motions['Mean [m:deg]'])


				for dof in xrange(0,len(tmpMax)):
					tmpPosZ = abs(tmpMax[dof] - tmpMean[dof])
					tmpNegZ = abs(tmpMean[dof] - tmpMin[dof])
					#tmpmotions.append(max(tmpPosZ,tmpNegZ))
					tmpmotions = max(abs(tmpMax[dof]),abs(tmpMin[dof]))
					#print tmpMotions
					print type(tmpmotions)				
					vessel_results.append(tmpmotions)
			tmpVesselResults = vessel_results
			#tmpVesselResults = list([item for sublist in vessel_results for item in sublist])
			tmpall = tmpVesselResults + tmpforces
			#print tmpall
			
			# 
			idx_end = 9 + len(tmpall)
			# TODO: Modiy for multiple files
			runsDF.loc[index,runsDF.columns[9:idx_end]] = tmpall
	
	# Output results all
	summaryOutputResults = os.path.join(os.getcwd(),"DVREF","Summary_Results.csv")
	runsDF.to_csv(summaryOutputResults,index=False)
	return runsDF

# Modified to account for processing of extreme evenets
def getAllForcesExtreme(runsDF,vessel_files = ["Vessel01_Motions.csv","Vessel02_Motions.csv"]):
	for index, row in runsDF.iterrows():
		tmpcase = str(row[runsDF.columns[0]]).zfill(3)		

		# Open results file
		tmpResultsLines = os.path.join(os.getcwd(),tmpcase,"out","Results.csv")
		#tmpResultsMotions = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Motions.csv")
		
		# Check if file exists, if true, convert to dataframe
		if os.path.isfile(tmpResultsLines):
			tmpdf_lines = readResults(tmpResultsLines)
			tmpforces = list(tmpdf_lines['Maximum [N]'])
			
			vessel_results = []
			# Iterate through list of vessel files
			for vessel in vessel_files:
				tmpResultsMotions = os.path.join(os.getcwd(),tmpcase,"out",vessel)
				tmpdf_motions = readResults(tmpResultsMotions)
				#tmpmotions = list(tmpdf_motions['PtoP Max'])

				tmpmotions = []

				tmpMax = list(tmpdf_motions['Maximum [m:deg]'])
				tmpMin = list(tmpdf_motions['Minimum [m:deg]'])
				tmpMean = list(tmpdf_motions['Mean [m:deg]'])


				for dof in xrange(0,len(tmpMax)):
					tmpPosZ = abs(tmpMax[dof] - tmpMean[dof])
					tmpNegZ = abs(tmpMean[dof] - tmpMin[dof])
					#tmpmotions.append(max(tmpPosZ,tmpNegZ))
					tmpmotions = max(abs(tmpMax[dof]),abs(tmpMin[dof]))
					#print tmpMotions
					print type(tmpmotions)				
					vessel_results.append(tmpmotions)
			tmpVesselResults = vessel_results
			#tmpVesselResults = list([item for sublist in vessel_results for item in sublist])
			tmpall = tmpVesselResults + tmpforces
			#print tmpall
			
			# 
			idx_end = 9 + len(tmpall)
			# TODO: Modiy for multiple files
			runsDF.loc[index,runsDF.columns[9:idx_end]] = tmpall
	
	# Output results all
	summaryOutputResults = os.path.join(os.getcwd(),"Summary_Results.csv")
	runsDF.to_csv(summaryOutputResults,index=False)
	return runsDF
			
def getDFmatches(df,mysearch):
	tmp = [col for col in df.columns if mysearch in col]
	return tmp
		

#if __name__ == '__main__':
	#from preprocess import preprocess as pre
	#os.chdir("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process")
	#runsfile = os.path.join("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process\\RUNS_FILES.txt")
#	metoceanfile = os.path.join("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process\\TestIputData.txt")
#	logfile = os.path.join("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process\\Deterministic03_5s-25s.log")
#   logfile = "Deterministic03_5s-25s.log"
#   wavefolder = "X:\\1. Projects\\1. Current\\SA (S2018) LNG Medium Term IPP\\Working\\Engineers\\CMB\\Richards_Bay\\Models\\BW\\07_PostProcess\\Runs"
#	df = readRuns(runsfile)
#	tt = getArrayDims(runsfile)
#	wave_time_series = readMetocean(metoceanfile)
#	#df['Tp interpolated'].plot()
#	waveboundaryfile = os.path.join("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process\\Waves_RB041427_Lat-28.8265_Lon32.104_2002-2015_UTC+2.txt")
#	boundary_time_series = readMetocean(waveboundaryfile)
#	#ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
#	#ts.plot()
#	#tt = readHm0(logfile,6)
#	#
#	f = open("TestOutputInterpolatedTS.txt","w")
#	coords = getArrayDims(runsfile)
#	indexDict = getLocationDicts2(runsfile,[1,2,3,4,5])	
#	#data = setDataValues2(runsfile,wavefolder,logfile,[1,2,3,4,5])
#	#print data
#	#print wave_time_series
#	#print coords
#
#	# Required input data:
#	results = loopCases(runsfile,wavefolder,logfile)
#
#	df = readRuns(runsfile)
#	WAVE_HEIGHTS = df['WAVE_HEIGHT'].unique()
#	WAVE_HEIGHTS.sort(axis=0)
#	WAVE_PERIODS = df['WAVE_PERIOD'].unique() 
#	WAVE_PERIODS.sort(axis=0)
#	WAVE_DIRECTIONS = df['WAVE_DIRECTION'].unique()
#	WAVE_DIRECTIONS.sort(axis=0)
#	WIND_SPEEDS = df['WIND_SPEED'].unique()
#	WIND_SPEEDS.sort(axis=0)
#	WIND_DIRECTIONS = df['WIND_DIRECTION'].unique()
#	WIND_DIRECTIONS.sort(axis=0)
#
#
#	#test_point = np.array([4,14.5,130.0])
#	#print interpolator((WAVE_HEIGHTS,WAVE_PERIODS,WAVE_DIRECTIONS),data,test_point)[0][0]*test_point[0]
#
#	for index, row in boundary_time_series.iterrows():
#		#print row['Hm0'],row['Tp interpolated'],row['Dir mean at Tp']
#		tmpPoint = np.array([row['Hm0'],row['Tp'],row['Peak Direction']])
#		originalPoint = np.array([row['Hm0'],row['Tp'],row['Peak Direction']])
#		Hm0 = row['Hm0']
#		#print tmpPoint
#		f.write(str(index)+"\t"+str(row['Hm0'])+"\t"+str(row['Tp'])+"\t"+str(row['Peak Direction'])+"\t")
#		#if ((tmpPoint[2] >= 190.) or (tmpPoint[2] > 18.) or (tmpPoint[0] > 5.)):
#			 #f.write(str(-999)+"\n")
#		#else:
#			#f.write(str(interpolator((WAVE_HEIGHTS,WAVE_PERIODS,WAVE_DIRECTIONS),data,tmpPoint)[0][0]*tmpPoint[0])+"\n")
#		#print tmpPoint
#		if (tmpPoint[0] < WAVE_HEIGHTS[0]):
#			tmpPoint[0] = WAVE_HEIGHTS[0] + 0.01
#		if (tmpPoint[0] >= WAVE_HEIGHTS[-1]):
#			tmpPoint[0] = WAVE_HEIGHTS[-1] -0.01
#		if (tmpPoint[1] < WAVE_PERIODS[0]):
#			tmpPoint[1] = WAVE_PERIODS[0] + 0.01
#		if (tmpPoint[1] >= WAVE_PERIODS[-1]):
#			tmpPoint[1] = WAVE_PERIODS[-1] - 0.01
#		if (tmpPoint[2] < WAVE_DIRECTIONS[0]):
#			tmpPoint[2] = WAVE_DIRECTIONS[0] + 0.01
#		if (tmpPoint[2] >= WAVE_DIRECTIONS[-1]):
#			tmpPoint[2] = WAVE_DIRECTIONS[-1] - 0.01
#		try:
#			f.write(str(interpolator((WAVE_HEIGHTS,WAVE_PERIODS,WAVE_DIRECTIONS),data,tmpPoint)[0][0]*Hm0)+"\n")
#		except Exception, e:
#			f.write(str(-1)+"\n")
#			print originalPoint
#		else:
#			pass
##
##
#	#f.close()
#
#	orientation = 5.
#	#mike_angles = [230.,272.5,305.,317.5,322.5,327.5,330.]
#	mike_angles = [0.,45.,90.,135.,180.,195.,270.]
#	for angle in mike_angles:
#		print convert_mike_to_aqwa(angle,orientation)
#		print convertWindSpeed(1.0,convert_mike_to_aqwa(angle,orientation))
	#resultsfile = ".\\Results.csv"
	#test = readForces(resultsfile)
	#print test
	#print test[test.columns[1]][0:24]
	#template_file = ".\\DVR.dvref"
	#test = setResultsDf(runsfile,template_file)
	#print test