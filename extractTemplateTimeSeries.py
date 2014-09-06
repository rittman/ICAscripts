"""
This script writes submits a script to the grid engine to extract network specific timeseries subject-by-subject for use
in between network connectivity analysis.

"""

from glob import glob
from os import path,getcwd,chmod,system

# Define list of diagnosis, directory containing network templates (from the FIND lab) and the name of the preprocessed
# functional imaging file
diags = ["Control", "PSP", "CBD"]
templateDir = "templates_new"
funcFile = "functional_reordered_pp_wpd_MNI_cut_smooth.nii"

# get templates
templates = [path.basename(v) for v in glob(path.join(templateDir, "*")) if path.isdir(v) ]

# dictionary of diagnoses and subject lists
subjsDict = {}

for diag in diags:
	subjsList = [ v for v in glob(path.join(diag, "*")) if path.isdir(v) ] # get all subject directories for the diagnosis
	subjsDict[diag] = dict(zip(range(len(subjsList)), subjsList)) # add the subject list to the dictionary
	
print subjsDict
	
# extract network timeseries
for network in templates:
	tf = path.join(templateDir, network, network+".nii.gz")
	print network
	
	# iterate through diagnoses
	for diag in diags:
		# open submission file
		subF = path.join(diag, network+"exTs.sh")
		f = open(subF, "w")
	
		# iterate through subject list
		for subjN in range(len(subjsDict[diag].keys())):
			# write line to call fslmeants (FSL) function to extract the network timeseries
			f.writelines(' '.join(["fslmeants", "-i", path.join(subjsDict[diag][subjN], funcFile), "-o", path.join(subjsDict[diag][subjN], network+"ts.txt"), "-m", tf])+'\n') 
 		f.close()
 		
 		# submit the submission script to the grid engine
 		system(' '.join(["fsl_sub", "-t", subF, "-q", "short.q", "-l", diag]))
