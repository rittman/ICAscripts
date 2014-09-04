from glob import glob
from os import path,getcwd,chmod,system

diags = ["Control", "PSP", "CBD"]
templateDir = "templates_new"
funcFile = "functional_reordered_pp_wpd_MNI_cut_smooth.nii"

# get templates
templates = [path.basename(v) for v in glob(path.join(templateDir, "*")) if path.isdir(v) ]

# dictionary of subjects
subjsDict = {}

for diag in diags:
	subjsList = [ v for v in glob(path.join(diag, "*")) if path.isdir(v) ]
	subjsDict[diag] = dict(zip(range(len(subjsList)), subjsList))
	
print subjsDict
	
# extract network timeseries
for network in templates:
	tf = path.join(templateDir, network, network+".nii.gz")
	print network
	
	
	for diag in diags:
		# open submission file
		subF = path.join(diag, network+"exTs.sh")
		f = open(subF, "w")
	
		# for diagnosis 1
		for subjN in range(len(subjsDict[diag].keys())):
			f.writelines(' '.join(["fslmeants", "-i", path.join(subjsDict[diag][subjN], funcFile), "-o", path.join(subjsDict[diag][subjN], network+"ts.txt"), "-m", tf])+'\n') 
 		f.close()
 
 		system(' '.join(["fsl_sub", "-t", subF, "-q", "short.q", "-l", diag]))
