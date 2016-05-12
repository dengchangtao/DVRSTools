# Run model processing
from preprocess import preprocess as pre
from solver import solver as solver
import os

working_dir = pre.getAQWAdirectory("Layout:")
os.chdir(working_dir)

# Runsfile
runs_file = "RUNS_FILES_SCALED.txt"
#template_file = "Layout03Template.dvref"
template_file = "Layout04Template.dvref"
#wcsa_template_file_01 = "templateVessel01.wsca"
#wcsa_template_file_02 = "templateVessel02.wsca"

# Get line stats
pre.getAllLinesStats2(runs_file,template_file)

# Get motions stats
pre.getAllMotionStats(runs_file,1)
pre.getAllMotionStats(runs_file,2)
