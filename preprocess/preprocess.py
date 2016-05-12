import os
import wx
from PyQt4.QtGui import QFileDialog
import PyQt4.QtGui as QtGui
import pandas as pd
import re	
import numpy as np
import pandas as pd
import sys
from subprocess import call
import struct
import json
import matplotlib.pyplot as plt
import time

def readRuns(runsfile):
	"""
	Read into pandas dataframe a csv file with runs information
	"""
	runs = pd.read_csv(str(runsfile),sep="\t")
	return(runs)

def folderSetup(layout,runs):
    root_dir = os.getcwd()
    level1 = ['Models','Data']
    level2 = {'Models':['DVRS'],'Data':['Wind','Current','Waves','Vessels']}
    level3 = {'DVRS':[layout],'Wind':[],'Current':[],'Waves':[],'Vessels':[]}
    level4 = {layout:['FVREF','Statics','DVREF']}
    level5 = {'DVREF':runs,'FVREF':[],'Statics':[]}
    
    for item in level1:
        if not os.path.exists(os.path.join(root_dir,item)):
            os.mkdir(os.path.join(root_dir,item))
        for levels in level2[item]:
            if not os.path.exists(os.path.join(root_dir,item,levels)):
                os.mkdir(os.path.join(root_dir,item,levels))
            for subs in level3[levels]:
                if not os.path.exists(os.path.join(root_dir,item,levels,subs)):
                    os.mkdir(os.path.join(root_dir,item,levels,subs))
                for ssubs in level4[subs]:
                    if not os.path.exists(os.path.join(root_dir,item,levels,subs,ssubs)):
                        os.mkdir(os.path.join(root_dir,item,levels,subs,ssubs))
                    for cases in level5[ssubs]:
                        if not os.path.exists(os.path.join(root_dir,item,levels,subs,ssubs,cases)):
                            os.mkdir(os.path.join(root_dir,item,levels,subs,ssubs,cases))

def modifyTemplate(template_file,findlist,replacelist):
	#TODO
	"""
	Pass a template file and a list of variable to find and the values to replace. This requires that the lists are the same length 
	"""
	if(len(findlist) != len(replacelist)):
		print "Length of findlist different to length of replacelist!"
		pass
	else:
		f = open(template_file,'r')
		tmp = f.read()
		f.close()

		for idx, val in enumerate(findlist):
			tmp = re.sub(findlist[idx],replacelist[idx],tmp)
		return(tmp)

def makeRunsFolders(runsfile,data_index,wave_folder,wave_file,wind_folder,template_file):#working_directory,layout,runsfile,wind_folder,wave_folder):
	# Get working directory
	working_directory = os.getcwd()

	runs = readRuns(runsfile)
	


	# Get unique values for wave heights
	var01 =runs[runs.columns[data_index[0]]].unique()
	var01.sort(axis=0)

	# Get the maximum wave height solver
	if len(var01) > 1:
		H_max = var01[-2]
	else:
		H_max = var01[0]
	for index, row in runs.iterrows():
		if (re.match("false",str(row[runs.columns[data_index[6]]]),re.IGNORECASE)):
			Hm0 = H_max
		else:
			Hm0 = row[runs.columns[data_index[0]]]

		# Get runs directory in order to get relative path of wind files
		runs_dir = os.path.join(working_directory,"DVREF",str(row[runs.columns[0]]).zfill(4))

		# Wind folder
		wind_dir = os.path.join(wind_folder)
		wind_relative_path = os.path.relpath(wind_dir,runs_dir)

		# Make waves folder string
		waves_folderstring = "H0%.1F_T%02d_D%03d" % (Hm0,row[runs.columns[data_index[1]]],row[runs.columns[data_index[2]]])
		waves_folderstring = os.path.join(wave_folder,waves_folderstring + ".bw - Result Files",wave_file).replace("\\","/")


		# Make wind file relative
		wind_filestring = "WS%02dWD%03d" % (row[runs.columns[data_index[3]]],row[runs.columns[data_index[4]]])
		
		wind_folderstring = os.path.join(wind_relative_path,wind_filestring + ".dfs0").replace("\\","/")
		#wind_folderstring = os.path.join(wind_folder,wind_filestring + ".dfs0").replace("\\","/")
		
		# Write template
		scale_factor_waves = "%.2F" % row[runs.columns[data_index[5]]]
		
		# Select template files
		template_file_flag = int(row[runs.columns[data_index[7]]])

		# Modify template file
		tmp_dvref_file = modifyTemplate(template_files[template_file_flag],["SCALEFACTORSCALEFACTOR","WINDFILEWINDFILE","WAVEFILEWAVEFILE"],[scale_factor_waves,wind_folderstring,waves_folderstring])
		root_dir = os.getcwd()
		outputfile = os.path.join(root_dir,"DVREF",str(row[runs.columns[0]]).zfill(4),"DVR.dvref").replace("\\","/")
		f = open(outputfile,'w')
		f.write(tmp_dvref_file)
		f.close()
                   
def copyTemplate(template_file,wave_file,wind_file,current_file,out_dir):
	f = open(template_file,'r')
	tmp = f.read()
	f.close()

def getDVRFInfo(template_file):
	f = open(template_file,'r')
	tmp = f.read()
	f.close()
	
	# Get required info from template file for processing results data	
	number_of_lines = int(re.search("Number_lines = (\d+)",tmp).group(1))
	number_of_fenders = int(re.search("Number_fenders\s+=\s+(\d+)",tmp).group(1))
	number_of_vessels = int(re.search("no_moving_bodies\s+=\s+(\d+)",tmp).group(1))
	
	# Line polys
	
	
	
	return (number_of_lines,number_of_fenders,number_of_vessels)

def runDVREF(run_file="DVR",max_itterations = 10):
	"""
	Function to call DVREF engine for each of the *.dvref files in the runs folder.
	"""
	inputCommand = "\"/wait C:\\\"Program Files (x86)\"\\DHI\\2016\\bin\\x64\\DynamicVRengine.exe DVR.dvref"
	#inputCommand = "C:\\\"Program Files (x86)\"\\DHI\\2016\\bin\\x64\\DynamicVRengine.exe "# + run_file + ".dvref" 
	for ii in xrange(max_itterations):
		try:
			call(["start",inputCommand],shell=True)
		except Exception, e:
			raise e
		else:
			pass
	
		# Check log file
		f = open(run_file +".log")
		tmp = f.read()
		f.close()
		print ii
		if re.search("Error: No valid DVRS license.",tmp) is None:
			print "No Licence"
			break	

def processDVREFresults ():
	"""
	Call template *.mzt files a run the Mike Engine in order get processed results for all lines, fenders and motions
	"""
	pass

def selectMetric ():
	"""
	Select the parameter compared i.e. time series maximum, statistical maximum etc.
	"""
	pass

def getStats(item,myfile="..\\out\\Results_lforces.dfs0"):
	# Helper function to get line forces
	#pass
	#item = "2"
	#myfile = "..\\out\\Results_lforces.dfs0"
	t1 = time.time()
	statsMztString ="// Created     : 2015-11-6 13:33:47\n// DLL id      : C:\\Program Files (x86)\\DHI\\2016\\bin\\x64\\pfs2004.dll\n// PFS version : Oct 20 2015 19:46:44\n[MzTxStat]\n   CLSID = '{0C17C8E5-A30E-11D3-B4B4-006097834BE6}'\n   TypeName = 'MzTxStat'\n   CREATEDTIME = '2015-11-06T13:33:11'\n   MODIFIEDTIME = '2015-11-06T13:33:11'\n   NOTES = ''\n   [Setup]\n      Name = 'tmpStats'\n      DimensionOfTool = 0\n      InputFileName = |"+myfile+"|\n      Items = "+item+"\n   FirstTimeStep = 7198\n   LastTimeStep = 50398\n   ReferenceLevelType = 1\n   ConstantReferenceLevel = 0\n   EndSect  // Setup\nEndSect  // MzTxStat"
	t2 = time.time()	
	f = open("tmp.mzt","w")
	f.write(statsMztString)
	f.close()
	t3 = time.time()
	inputCommand = "\"/wait C:\\\"Program Files (x86)\"\\DHI\\2016\\bin\\x64\\ToolboxShell.exe -run tmp.mzt"
	t4 = time.time()
	call(["start",inputCommand],shell=True)
	t5 = time.time()
	f = open("tmpStats.out")
	tmp = f.read()
	f.close()
	t6 = time.time()
	#number_of_fenders = int(re.search("Number_fenders\s+=\s+(\d+)",tmp).group(1))
	line_num = re.search("Item\s+\d+\s+:\s+(\D.+)\s+\n",tmp).group(1)
	line_max = float(re.search("Maximum\s+:\s+(\d+.*)\n",tmp).group(1))
	line_mean = float(re.search("Mean\s+:\s+(\d+.*)\n",tmp).group(1))
	line_median = float(re.search("Median\s+:\s+(\d+.*)\n",tmp).group(1))
	line_rms = float(re.search("Root Mean Square\s+:\s+(\d+.*)\n",tmp).group(1))
	try:
		line_std_dev = float(re.search("Standard deviation\s+:\s+(\d+.*)\n",tmp).group(1))
	except Exception, e:
		line_std_dev = 0
	else:
		line_std_dev = float(re.search("Standard deviation\s+:\s+(\d+.*)\n",tmp).group(1))
	try:
		line_skew = float(re.search("Skewness\s+:(\s+.*)\n",tmp).group(1))
	except Exception, e:
		line_skew = 0
	else:
		line_skew = float(re.search("Skewness\s+:(\s+.*)\n",tmp).group(1))
	#print tmpArray[13:18]
	#tmp_array.append(line_max)
	
	results = [line_num,line_mean,line_median,line_rms,line_std_dev,line_max,line_skew]	
	t7 = time.time()
	print (t5-t4)
	return (results)

def getMultiLineStats(items,myfile):
	test = ", ".join(str(e) for e in items)

	statsMztString = "// Created     : 2016-02-24 9:0:16\n// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll\n// PFS version : Nov 22 2015 02:58:09\n[MzTxStat]\n   DimensionOfTool = 0\n   InputFileName = |"+myfile+"|\n   Items = "+test+"\n   FirstTimeStep = 7198\n   LastTimeStep = 50398\n   ReferenceLevelType = 1\n   ConstantReferenceLevel = 0\nEndSect  // MzTxStat"
	f = open("tmpStats.pfs","w")
	f.write(statsMztString)
	f.close()

	call(["t0stat.exe","tmpStats.pfs"])

	f = open("tmpStats.out")
	tmp = f.read()
	f.close
	
	line_num = re.findall("Item\s+\d+\s+:\s+(\D.+)\s+\n",tmp)
	line_max = [float(x) for x in re.findall("Maximum\s+:\s+(\d+.*)\n",tmp)]
	line_mean = [float(x) for x in re.findall("Mean\s+:\s+(\d+.*)\n",tmp)]
	line_median = [float(x) for x in re.findall("Median\s+:\s+(\d+.*)\n",tmp)]
	line_rms = [float(x) for x in re.findall("Root Mean Square\s+:\s+(\d+.*)\n",tmp)]
	try:
		line_std_dev = [float(x) for x in re.findall("Standard deviation\s+:\s+(\d+.*)\n",tmp)]
	except Exception, e:
		line_std_dev = 0
	else:
		line_std_dev = [float(x) for x in re.findall("Standard deviation\s+:\s+(\d+.*)\n",tmp)]
	try:
		line_skew = [float(x) for x in re.findall("Skewness\s+:(\s+.*)\n",tmp)]
	except Exception, e:
		line_skew = 0
	else:
		line_skew = [float(x) for x in re.findall("Skewness\s+:(\s+.*)\n",tmp)]

	results = [line_num,line_mean,line_median,line_rms,line_max]
	return results
	
	
def getMotionStats2(items,myfile):
	test = ", ".join(str(e) for e in items)

	#statsMztString = "// Created     : 2016-02-24 9:0:16\n// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll\n// PFS version : Nov 22 2015 02:58:09\n[MzTxStat]\n   DimensionOfTool = 0\n   InputFileName = |"+myfile+"|\n   Items = "+test+"\n   FirstTimeStep = 4798\n   LastTimeStep = 41998\n   ReferenceLevelType = 1\n   ConstantReferenceLevel = 0\nEndSect  // MzTxStat"
	statsMztString = "// Created     : 2016-02-24 9:0:16\n// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll\n// PFS version : Nov 22 2015 02:58:09\n[MzTxStat]\n   DimensionOfTool = 0\n   InputFileName = |"+myfile+"|\n   Items = "+test+"\n   FirstTimeStep = 7198\n   LastTimeStep = 50398\n  ReferenceLevelType = 1\n   ConstantReferenceLevel = 0\nEndSect  // MzTxStat"
	
	f = open("tmpStats.pfs","w")
	f.write(statsMztString)
	f.close()

	call(["t0stat.exe","tmpStats.pfs"])

	f = open("tmpStats.out")
	tmp = f.read()
	f.close
	
	line_num = re.findall("Item\s+\d+\s+:\s+(\D.+)\s+\n",tmp)
	line_min = [float(x) for x in re.findall("Minimum\s+:\s+(\d+.*)\n",tmp)]
	line_max = [float(x) for x in re.findall("Maximum\s+:\s+(\d+.*)\n",tmp)]
	line_mean = [float(x) for x in re.findall("Mean\s+:\s+(\d+.*)\n",tmp)]
	line_median = [float(x) for x in re.findall("Median\s+:\s+(\d+.*)\n",tmp)]
	line_rms = [float(x) for x in re.findall("Root Mean Square\s+:\s+(\d+.*)\n",tmp)]
	try:
		line_std_dev = [float(x) for x in re.findall("Standard deviation\s+:\s+(\d+.*)\n",tmp)]
	except Exception, e:
		line_std_dev = 0
	else:
		line_std_dev = [float(x) for x in re.findall("Standard deviation\s+:\s+(\d+.*)\n",tmp)]
	try:
		line_skew = [float(x) for x in re.findall("Skewness\s+:(\s+.*)\n",tmp)]
	except Exception, e:
		line_skew = 0
	else:
		line_skew = [float(x) for x in re.findall("Skewness\s+:(\s+.*)\n",tmp)]

	results = [line_num,line_mean,line_median,line_rms,line_min,line_max]
	return results

def getMotionStats(var_idx,myfile="..\\out\\Results_lforces.dfs0"):
	myList = ','.join(map(str, var_idx))
	statsMztString = "// Created     : 2016-02-24 9:0:16\n// DLL id      : C:\Program Files (x86)\DHI\2016\bin\x64\pfs2004.dll\n// PFS version : Nov 22 2015 02:58:09\n[MzTxStat]\n   DimensionOfTool = 0\n   InputFileName = |"+myfile+"|\n   Items = "+myList+"\n   FirstTimeStep = 7198\n   LastTimeStep = 50398\n   ReferenceLevelType = 1\n   ConstantReferenceLevel = 0\nEndSect  // MzTxStat"
	f = open("tmpStats.pfs","w")
	f.write(statsMztString)
	f.close()

	call(["t0stat.exe","tmpStats.pfs"])

	f = open("tmpStats.out")
	tmp = f.read()
	f.close

	header_regex = "Item\s+\d+\s:\s+(\D+.\d)"
	max_regex = "Maximum\s+:(\s+.*)\n"
	mean_regex = "Mean\s+:(\s+.*)\n"
	median_regex = "Median\s+:(\s+.*)\n"
	rms_regex = "Root Mean Square\s+:(\s+.*)\n"
	min_regex = "Minimum\s+:(\s+.*)\n"
	#std_dev_regex = "Standard deviation\s+:(\s+.*)\n"
	#skew_regex = "Skewness\s+:(\s+.*)\n"

	#tt = re.search(header_regex,tmp).group(0)
	headers = re.findall(header_regex,tmp)
	maxes = [float(x) for x in re.findall(max_regex,tmp)]
	mins = [float(x) for x in re.findall(min_regex,tmp)]
	means = [float(x) for x in re.findall(mean_regex,tmp)]
	medians = [float(x) for x in re.findall(median_regex,tmp)]
	rmss = [float(x) for x in re.findall(rms_regex,tmp)]
	#std_devs = [float(x) for x in re.findall(std_dev_regex,tmp)]
	#skews = [float(x) for x in re.findall(skew_regex,tmp)]	
	l = [headers,means,medians,rmss,mins,maxes]
	# Get inverse	
	l = map(list,zip(*l))
	tmp = pd.DataFrame(l)
	
	tmp.columns = ["DOF","Mean [m:deg]","Median [m:deg]","Root mean square [m:deg]","Minimum [m:deg]","Maximum [m:deg]"]
	tmp = tmp.set_index(["DOF"])	
	
	return (tmp)

def getDVRFInfo(template_file):
	f = open(template_file,'r')
	tmp = f.read()
	f.close()
	
	# Get required info from template file for processing results data	
	number_of_lines = int(re.search("Number_lines = (\d+)",tmp).group(1))
	number_of_fenders = int(re.search("Number_fenders\s+=\s+(\d+)",tmp).group(1))
	number_of_vessels = int(re.search("no_moving_bodies\s+=\s+(\d+)",tmp).group(1))
	
	# Return layout info
	return (number_of_lines,number_of_fenders,number_of_vessels)

def setResultsDf(runsfile,template_file):
	layout_info = getDVRFInfo(template_file)
	df_runs = readRuns(runsfile)

	num_lines = layout_info[0]
	num_fenders = layout_info[1]
	num_vessesls = layout_info[2]

	results_headers = []
	motions = ["Surge","Sway","Heave","Roll","Sway","Yaw"]
	for ii in xrange(num_vessesls):
		for motion in motions:
			results_headers.append("Vessel%02d_%s" % (float(ii + 1),motion))
	for jj in xrange(num_lines):
		results_headers.append("Lines%02d" % float(jj+1))
	for kk in xrange(num_fenders):
		results_headers.append("Fenders%02d" % float(kk+1))
	for header in results_headers:
		df_runs[header] = np.nan
		df_runs.ix[:,header] = 1.
	return df_runs
	
def getAllLinesStats(runsfile,template_file):
	runs = readRuns(runsfile)
	
	for index, row in runs.iterrows():
		
		tmpcase = str(row[runs.columns[0]]).zfill(4)
		print tmpcase
		
		test = []
		lines = getDVRFInfo(template_file)[0]
		fenders = getDVRFInfo(template_file)[1]
		
		remainder = (lines + fenders) % 10


		integer = (lines + fenders) / 10

		for ii in xrange(0,lines + fenders):
			print ii

		myfilein = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results_lforces.dfs0")
		myfileout = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results.csv")
		
		if os.path.isfile(myfilein):
			for line in range(2,lines+1+fenders+1):
				test.append(getStats(str(line),myfilein))
			
			test = pd.DataFrame(test)	
			test.columns = ["Line","Mean [N]","Median [N]","Root mean square [N]","Std deviation [N]","Maximum [N]","Skewness"]
			test = test.set_index(["Line"])
			# Write results file to local directory
			test.to_csv(myfileout)
			
def getAllLinesStats2(runsfile,template_file):
	runs = readRuns(runsfile)
	
	for index, row in runs.iterrows():
		
		tmpcase = str(row[runs.columns[0]]).zfill(4)
		
		test = []
		lines = getDVRFInfo(template_file)[0]
		fenders = getDVRFInfo(template_file)[1]

		# Get results file
		myfilein = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results_lforces.dfs0")
		# Get file to write		
		myfileout = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results.csv")
		
		# Check if file exists
		if os.path.isfile(myfilein):
			jj = 0
			tmp = []
			for ii in xrange(lines + fenders):
				tmp.append(ii + 2)
				if ((ii + 1) % 10 == 0):
					jj = jj + 1
					reordered = map(list,zip(*getMultiLineStats(tmp,myfilein)))
					for kk in xrange(len(reordered)):
						test.append(reordered[kk])#getMultiLineStats(tmp,myfilein))
					#return test #getMultiLineStats(tmp,myfilein)
					tmp = []
				if (ii == (lines + fenders - 1)):
					reordered = map(list,zip(*getMultiLineStats(tmp,myfilein)))
					for kk in xrange(len(reordered)):
						test.append(reordered[kk])
			
			# Write to dataframe
			test = pd.DataFrame(test)		
			test.columns = ["Line","Mean [N]","Median [N]","Root mean square [N]","Maximum [N]"]#"Std deviation [N]","Maximum [N]","Skewness"]
			test = test.set_index(["Line"])
			# Write results file to local directory
			test.to_csv(myfileout)

def getAllMotionStats(runsfile,flag):
	outputcsv = "Vessel0"+str(flag)+"_Motions.csv"
	if flag == 1:
		items = [2,3,4,5,6,7]
	elif flag == 2:
		items = [8,9,10,11,12,13]

	runs = readRuns(runsfile)
	
	for index, row in runs.iterrows():
		
		tmpcase = str(row[runs.columns[0]]).zfill(4)

		# Get results file
		myfilein = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results_motions.dfs0")

		# Get file to write		
		myfileout = os.path.join(os.getcwd(),"DVREF",tmpcase,"out",outputcsv)
		
		# Check if file exists
		if os.path.isfile(myfilein):
			test = getMotionStats(items,myfilein)
			# Write results file to local directory
			test.to_csv(myfileout)

def testLines(template_file):
	lines = getDVRFInfo(template_file)[0]
	fenders = getDVRFInfo(template_file)[1]
	jj = 0
	tmp = []
	for ii in xrange(lines + fenders):
		print ii + 2
		tmp.append(ii + 2)
		if ((ii + 1) % 10 == 0):
			jj = jj + 1
			print "file" + str(jj)
			print tmp
			tmp = []
		if (ii == (lines + fenders - 1)):
			print tmp
		
def check_solve(checkfile):
	try:
		f = open(checkfile,'r')
	except Exception, e:
		return "File does not exist"
	else:
		tmp = f.read()
		f.close()

	if re.search("READ_M21: Unable to read the M21 elevation",tmp) is not None:
		failed_case = checkfile.split("\\")
		#failed_case = checkfile.split("/")
		print failed_case
		return int(failed_case[-2])

def get_failed_list():
	f = open("ReRun.bat",'w')
	tmp = os.listdir(os.path.join(os.getcwd(),'DVREF'))
	for folders in tmp:
		checkfile = os.path.join(os.getcwd(),'DVREF',folders,"DVR.log")
		checkfile = check_solve(checkfile)
		if checkfile is not None:
			f.write(str(checkfile).zfill(4))
			f.write("\n")
	f.close()

def getAQWAdirectory(title):
	app = QtGui.QApplication(sys.argv)
	tmpdir = str(QtGui.QFileDialog.getExistingDirectory(None,title))

	#app.exec_()
	#app.quit()
	#app.closeAllWindows()
	return (tmpdir)

def getFile(title):
	app = QtGui.QApplication(sys.argv)
	return (QtGui.QFileDialog.getOpenFileName(None,title))

def getMultipleFiles(title):
	app = QtGui.QApplication(sys.argv)
	files = []
	for myfile in QtGui.QFileDialog.getOpenFileNames(None, title):
		files.append(str(myfile))
	return(files)

def getMotionsTS(myfile):
	# Process time series data for zero upcrossing statistics
	f = open(myfile,"r")
	tmp = f.read()
	f.close()
	pp_regex = "(.*\s+PP\s+:\s+.+)"
	tp_regex = "(.*\s+D\s+:\s+.+)"
	zc_regex = "(.*\s+ZC\s+:\s+.+)"
	zt_regex = "(.*\s+ZT\s+:\s+.+)"
	
	fieldwidths = (-4,-12,12,12,-12,-7,-4,7)
	fmtstring = ' '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's')for fw in fieldwidths)
	fieldstruct = struct.Struct(fmtstring)
	parse = fieldstruct.unpack_from
	pp_mean = []
	pp_max = []
	tp_mean = []
	tp_max = []
	zc_mean = []
	zc_max = []
	zt_mean = []
	zt_max = []
	items = []
	
	pp = re.findall(pp_regex,tmp)
	tp = re.findall(tp_regex,tmp)
	zc = re.findall(zc_regex,tmp)
	zt = re.findall(zt_regex,tmp)
	
	for line in xrange(0,len(pp)):
		tmppp = parse(pp[line])
		tmptp = parse(tp[line])
		tmpzc = parse(zc[line])
		tmpzt = parse(zt[line])
		
		# Append to arrays
		pp_mean.append(float(tmppp[1]))
		pp_max.append(float(tmppp[0]))
		tp_mean.append(float(tmptp[1]))
		tp_max.append(float(tmptp[0]))
		zc_mean.append(float(tmpzc[1]))
		zc_max.append(float(tmpzc[0]))
		zt_mean.append(float(tmpzt[1]))
		zt_max.append(float(tmpzt[0]))
		items.append(tmppp[2])
		
	l = [items,pp_mean,pp_max,tp_mean,tp_max,zc_mean,zc_max,zt_mean,zt_max]
	# Get inverse	
	l = map(list,zip(*l))
	tmp = pd.DataFrame(l)
	
	tmp.columns = ["Items","PtoP Mean","PtoP Max","Tz Mean","Tz Max","`+ZtoP Mean","`+ZtoP Max","`-ZtoP Mean","`-ZtoP Max"]
	tmp = tmp.set_index(["Items"])	
	
	return(tmp)

def readWSCALogFile(log_file):
	# Open log file
	f = open(log_file,"r")
	tmp = f.read()
	f.close()
	
	# Check 
	if re.search("Unable to acquire license seat from network license server",tmp)is not None:
		return 1
	elif re.search("Error in License System",tmp) is not None:
		return 1
	else:
		return 0
		
def SandboxWSCA(inputCommand,logfile):
	check_flag = 1
	ii = 0
	while (check_flag != 0 and ii < 20):
		time.sleep(2)
		call(["wsca.exe",inputCommand],shell=True)
		check_flag = readWSCALogFile(logfile)
		print check_flag
		ii = ii + 1
		print ii
	
def copyWSCAtemplate(runs_file,vessel,template_file):
	# Runs from the working directory
	#template_file = getFile(str("WSCA Template file" + vessel))
	
	# Open the template file for reading	
	f = open(template_file,"r")
	tmp = f.read()
	f.close()
		
	# Get the runs 
	runs = readRuns(runs_file)
	
	# Copy the template file and run
	for index, row in runs.iterrows():
		tmpcase = str(row[runs.columns[0]]).zfill(4)
		
		outputfile = vessel + "_Motions.csv"		
		
		resultsFile = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","Results_motions.dfs0").replace("\\","/")
		timeseriesFile = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","LC01_motions_WSCA.dfs0").replace("\\","/")
		logresultsFile = os.path.join(os.getcwd(),"DVREF",tmpcase,"out","tmpWSCA.log").replace("\\","/")
		summaryresultsfile = os.path.join(os.getcwd(),"DVREF",tmpcase,"out",outputfile).replace("\\","/")
		
		if os.path.isfile(resultsFile):
			# Write to the WSCA and run
			tmpwsca =os.path.join(os.getcwd(),"DVREF",tmpcase,"out","tmpWSCA.wsca").replace("\\","/") 		
			f = open(tmpwsca,"w")
			tmp = modifyTemplate(template_file,["INPUTFILEINPUTFILE","OUTPUTOUTPUT"],[resultsFile,timeseriesFile])
			f.write(tmp)
			f.close()
	
			inputCommand = str(tmpwsca).replace("/","\\") 
			print inputCommand
			
			#call(["wsca.exe",inputCommand],shell=False)
			#time.sleep(2)
			SandboxWSCA(inputCommand,logresultsFile)			
			tmpMotionsDF = getMotionsTS(logresultsFile)
			tmpMotionsDF.to_csv(summaryresultsfile)
			
def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                props[key_value[0].strip()] = key_value[1].strip('" \t') 
    return props

def getText(title):
	app = QtGui.QApplication(sys.argv)
	text = QtGui.QInputDialog.getText(None, 'Input Dialog',title)
	return (text)

def plotMooringLines(template_file):
	app = QtGui.QApplication(sys.argv)
	f = open(template_file,'r')
	tmp = f.read()
	f.close()
	
	num_lines = getDVRFInfo(template_file)[0]
	
	# Plot all lines
	lines = re.findall("Restoring_coeff =\s+(.+)\n",tmp)
	xs = np.arange(0,3,0.1)
	for line in xrange(0,num_lines):
		tmp = [float(i) for i in lines[line].split(',')]
		polynomial = np.poly1d(tmp)
		ys = polynomial(xs)
		plt.plot(xs,ys)
	plt.show()
	plt.grid()

def plotFenders(template_file):
	app = QtGui.QApplication(sys.argv)
	f = open(template_file,'r')
	tmp = f.read()
	f.close()
	
	num_lines = getDVRFInfo(template_file)[0]
	num_fenders = getDVRFInfo(template_file)[1]
	num_vessels = getDVRFInfo(template_file)[2]
	
	# Plot all lines
	lines = re.findall("Restoring_coeff =\s+(.+)\n",tmp)
	xs = np.arange(0,3,0.1)
	for line in xrange(0,num_lines):
		tmp = [float(i) for i in lines[line].split(',')]
		polynomial = np.poly1d(tmp)
		ys = polynomial(xs)
		plt.plot(xs,ys)
	plt.show()
	plt.grid()



if __name__ == '__main__':
	pass
	# Select working directory

	working_directory = getAQWAdirectory("Select working directory:") 
	os.chdir(unicode(working_directory))

	# Select runs file
	runsfile = "RUNS_FILES.txt"

	# Select template file
	template_files = getMultipleFiles("Select template files:")

	# Select wave folder:
	wave_folder = str(getAQWAdirectory("Select waves folder:"))
#	wave_folder = "X:/1. Projects/1. Current/SA (S2018) LNG Medium Term IPP/Working/Engineers/CMB/Richards_Bay/Models/BW/07_PostProcess/Runs"
	
	# Select wind folder:
	wind_folder = str(getAQWAdirectory("Select wind folder:"))

	# Make runs
	makeRunsFolders(runsfile,[1,2,3,4,5,6,7,8],wave_folder,"Deterministic05b.dfs2",wind_folder,template_files) 
	
'''
	#df = readRuns(runsfile)
	#
	# Get index for wave parameters
	#unicode_idx = getText("Input parameter indices: Hm0, Tp, Dir, Wind speed and wind direction")
	#unicode_idx = str(unicode_idx[0]).encode('utf-8').split(',')
	#data_idx = []
	#for idx in unicode_idx:
		#data_idx.append(int(idx))
	#print data_idx
	
	#f = open("README.txt",'w+')
	#inputs = {"working_directory":unicode(working_directory)}
	#json.dump(inputs,f)
	#f.close()
	#working_directory = getAQWAdirectory("Select working directory:") 
	#os.chdir(working_directory)	

	#runsfile = getFile("Select runs file:")
	#print str(runsfile)

	#checkfile = getFile("Select test file:")

	#os.chdir("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process")
	#print os.getcwd()	
	#runsfile = os.path.join("C:\\Users\\rlh.PRDW\\Dropbox\\AQWA_PRDW\\Process\\RUNS_FILES.txt")
	#df = readRuns(runsfile)
	#runs = df['CASE'].apply(lambda x: str(x).zfill(4))
	#folderSetup('Layout01',runs)
	#folderSetup('Layout02',runs)
	#folderSetup('Layout03',["A","B","C"])
	#findlist = ["WAVEFILEWAVEFILE","Restoring_coeff"]
	#replacelist = [os.path.join("..","fromChris","H10.1_T18_D110.bw - Result Files","Deterministic05.dfs2"),"BBubbles"]
	#template_file = ".\\DVR.dvref"
	#myfile = "F:\\PROJECT_BACKUP\\SA (S2018) LNG Medium Term IPP\\RB\\Models\\DVRS\\Extreme\\11u\\H10.1_T18_D110\\001\\out\\Results_lforces.dfs0"
	#mymotionsfile = "F:\\PROJECT_BACKUP\\SA (S2018) LNG Medvium Term IPP\\RB\\Models\\DVRS\\Extreme\\11u\\H10.1_T18_D110\\001\\out\\Results_motions.dfs0"
	#test = getStats("2",myfile)
	#lines = getDVRFInfo(template_file)[0]
	#fenders = getDVRFInfo(template_file)[1]
	#for line in range(lines+1+fenders):
	#	getStats(str(line+1),myfile)
	#print test
	#test = getAllStats(template_file,myfile)
	#test1 = getMotionStats([2,3,4,5,6,7],mymotionsfile)
	#test2 = getMotionStats([2,3,4,5,6,7],mymotionsfile)
	#print test1
	#print test2
	#mymotionstsfile = "F:\\PROJECT_BACKUP\\SA (S2018) LNG Medium Term IPP\\RB\\Models\\DVRS\\Extreme\\11u\\H10.1_T18_D110\\001\\Analysis\\LC01_motions_WSCA.log"
	#test = getMotionsTS(mymotionstsfile)
	#print test
	#test = getAQWAdirectory()
	#print unicode(test)
'''


