import os
from preprocess import preprocess as pre
from solver import solver as solver
import numpy as np
import time
import re

if __name__ == '__main__':
	# Setup working directory
	working_directory = pre.getAQWAdirectory("Working directory:")
	os.chdir(working_directory)

	# Get template file
	template_file = pre.getFile("Template file:")

	# Specify runs file
	runs_file = pre.getFile("Runs file:")
	runsDF = solver.readRuns(str(runs_file))
	
	# Get metocean file
	metocean_file = pre.getFile("Metocean file:")
	metoceanDF = solver.readMetocean(str(metocean_file))

	# Set output results DF - All outputs 
	resultsDF = solver.setResultsDf(str(runs_file), str(template_file))
	resultsDF = solver.getAllForces(resultsDF)
	resultsDF_dict = solver.df_dict(resultsDF)



	# Get unique values from solved data
	WAVE_HEIGHTS = runsDF['WAVE_HEIGHT'].unique()
	WAVE_HEIGHTS.sort(axis=0)
	WAVE_PERIODS = runsDF['WAVE_PERIOD'].unique() 
	WAVE_PERIODS.sort(axis=0)
	WAVE_DIRECTIONS = runsDF['WAVE_DIRECTION'].unique()
	WAVE_DIRECTIONS.sort(axis=0)
	WIND_SPEEDS = runsDF['WIND_SPEED'].unique()
	WIND_SPEEDS.sort(axis=0)
	WIND_DIRECTIONS = runsDF['WIND_DIRECTION'].unique()
	WIND_DIRECTIONS.sort(axis=0)

	#test_point = np.array([2.,12.,110.,10.,175.])
	#print solver.interpolator((WAVE_HEIGHTS,WAVE_PERIODS,WAVE_DIRECTIONS,WIND_SPEEDS,WIND_DIRECTIONS),tmpData,test_point)#[0][0]*test_point[0]

	f = open("InterpolatedResults.txt","w")
	
	# Get index of results
	motions = solver.getDFmatches(resultsDF,"Vessel")
	lines = solver.getDFmatches(resultsDF,"Lines")
	fenders = solver.getDFmatches(resultsDF,"Fenders")
	
	params = motions + lines + fenders
	
	idx_params = []
			
	
	results_data = []

	
	# Get index values for parameters and charge data values 
	for param in params:
		results_data.append(solver.setDataValues3(str(runs_file), resultsDF,resultsDF_dict[param]))
		idx_params.append(resultsDF_dict[param])
	
	# Write header file for csv	
	headers = ["Date","Hm0 [m]","TP [s]","Wave dir [deg TN]","Wind speed [m.s-1]","Wind dir [deg TN]"]
	
	#for x in xrange(min(idx_params) - 1):
	#	headers.append(resultsDF.columns[x]) 
	#return results_data
	headers = headers + params

	# Write column titles
	f.write("\t".join(headers))
	f.write("\n")

	"""
	results_idx = 1
	for x in results_idx:
		# Set results dataframe
		t1 = time.time()
		tmpData = 0
		t2 = time.time()
		
		print t2 - t1
	"""
	#yearStart = 2005
	#yearEnd = 2011
	#year = 2003
	for index, row in metoceanDF.iterrows():
		#if re.match(str(year),str(index)):
		tmpPoint = np.array([row['Hm0'],row['Tp'],row['Wave direction'],row['Wind speed'],row['Wind direction vessel']])
		originalPoint = np.array([row['Hm0'],row['Tp'],row['Wave direction'],row['Wind speed'],row['Wind direction vessel']])
		Hm0 = row['Hm0']

		f.write(str(index)+"\t"+str(row['Hm0'])+"\t"+str(row['Tp'])+"\t"+str(row['Wave direction'])+"\t"+str(row['Wind speed'])+"\t"+str(row["Wind direction vessel"])+"\t")

		if (tmpPoint[0] < WAVE_HEIGHTS[0]):
			tmpPoint[0] = WAVE_HEIGHTS[0] + 0.01
		if (tmpPoint[0] >= WAVE_HEIGHTS[-1]):
			tmpPoint[0] = WAVE_HEIGHTS[-1] -0.01
		if (tmpPoint[1] < WAVE_PERIODS[0]):
			tmpPoint[1] = WAVE_PERIODS[0] + 0.01
		if (tmpPoint[1] >= WAVE_PERIODS[-1]):
			tmpPoint[1] = WAVE_PERIODS[-1] - 0.01
		if (tmpPoint[2] < WAVE_DIRECTIONS[0]):
			tmpPoint[2] = WAVE_DIRECTIONS[0] + 0.01
		if (tmpPoint[2] >= WAVE_DIRECTIONS[-1]):
			tmpPoint[2] = WAVE_DIRECTIONS[-1] - 0.01
		if (tmpPoint[3] < WIND_SPEEDS[0]):
			tmpPoint[3] = WIND_SPEEDS[0] + 0.01
		if (tmpPoint[3] >= WIND_SPEEDS[-1]):
			tmpPoint[3] = WIND_SPEEDS[-1] - 0.01
		if (tmpPoint[4] < WIND_DIRECTIONS[0]):
			tmpPoint[4] = WIND_DIRECTIONS[0] + 0.01
		if (tmpPoint[4] >= WIND_DIRECTIONS[-1]):
			tmpPoint[4] = WIND_DIRECTIONS[-1] - 0.01
			
		tmpInterpolatedPoints = []
		for ii in xrange(0,len(results_data)):
			try:
				tmpInterpolatedPoints.append(solver.interpolator((WAVE_HEIGHTS,WAVE_PERIODS,WAVE_DIRECTIONS,WIND_SPEEDS,WIND_DIRECTIONS),results_data[ii],tmpPoint))
			except Exception, e:
				tmpInterpolatedPoints.append(-1)
			#print e
			else:
				pass
			
		outputstring = ['{:.3f}'.format(x) for x in tmpInterpolatedPoints]
		f.write("\t".join(outputstring))
		f.write("\n")
	f.close()


