# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:32:32 2016

@author: rlh
"""
from preprocess import preprocess as pre
from solver import solver as solver
import os
import pandas as pd 

working_dir = pre.getAQWAdirectory("Layout:")
os.chdir(working_dir)

runs_file = "RUNS_FILES.txt"

runs = pre.readRuns(runs_file)

#pre.getMotionStats([2,3,4,5,6,7],".\\000\\out\\000_motions.dfs0")
for index, row in runs.iterrows():
	#TODO: Update extraction time for the mike tools
	# Get all motions results
	root = str(index).zfill(4)
	print root
	
	# Get all motions files
	motions_in = ".\\"+root+"\\out\\"+root+"_motions.dfs0"
	motions_out = ".\\"+root+"\\out\\Vessel01_motions.csv"
	lines_out = ".\\"+root+"\\out\\Results.csv"
	
	results = pre.getMotionStats([2,3,4,5,6,7],motions_in)
	results.to_csv(motions_out)
	
	# Get all line files
	lines_in = ".\\"+root+"\\out\\"+root+"_lforces.dfs0"
	template_file = ".\\"+root+"\\"+root+".dvref"
	
	test = []
	lines = pre.getDVRFInfo(template_file)[0]
	fenders = pre.getDVRFInfo(template_file)[1]

	# Get results file
	myfilein = lines_in #os.path.join(os.getcwd(),"DVREF",root,"out","Results_lforces.dfs0")
	# Get file to write		
	myfileout = lines_out #os.path.join(os.getcwd(),"DVREF",root,"out","Results.csv")
	
	# Check if file exists
	if os.path.isfile(myfilein):
		jj = 0
		tmp = []
		for ii in xrange(lines + fenders):
			tmp.append(ii + 2)
			if ((ii + 1) % 10 == 0):
				jj = jj + 1
				reordered = map(list,zip(*pre.getMultiLineStats(tmp,myfilein)))
				for kk in xrange(len(reordered)):
					test.append(reordered[kk])#getMultiLineStats(tmp,myfilein))
				#return test #getMultiLineStats(tmp,myfilein)
				tmp = []
			if (ii == (lines + fenders - 1)):
				reordered = map(list,zip(*pre.getMultiLineStats(tmp,myfilein)))
				for kk in xrange(len(reordered)):
					test.append(reordered[kk])
		
		# Write to dataframe
		test = pd.DataFrame(test)		
		test.columns = ["Line","Mean [N]","Median [N]","Root mean square [N]","Maximum [N]"]#"Std deviation [N]","Maximum [N]","Skewness"]
		test = test.set_index(["Line"])
		# Write results file to local directory
		test.to_csv(myfileout)

# Assumes that all cases have the same number of mooring lines etx
root = str(runs.CASE[0]).zfill(4)
template_file = "./"+root+"/"+root+".dvref"

# Results DF
resultsDF = solver.setResultsDf(str(runs_file), str(template_file))
resultsDF = solver.getAllForcesExtreme(resultsDF)
