from os import path,mkdir,getcwd
from string import split
from glob import glob
from sys import argv,exit
import csv
from numpy import mean

"""
Function to run dual regression with clinic scores
The first argument is the diagnostic group, the second the clinical score.
Eg python drWithClinScores.py PSP letfluencycorr
"""

diag = argv[1]
cs = argv[2]
ICAroot = diag+cs

# open clinic scores file
f = open("ClinicalScores.csv", "rb")
reader = csv.DictReader(f, delimiter=" ")

# set up diagnosis for subjects
scanSubjs = {}
scanSubjs[diag] = [ path.basename(v) for v in glob(path.join(diag, "*")) if path.isdir(v) ]

subjDict = {}
headers = reader.next()
WBICNum = "wbicNum"
diagnosis='Diagnosis'
funcFile = "functional_reordered_pp_wpd_MNI_cut_smooth_mask.nii.gz"
NAvals=["", "NA","[ND]"]

subjsCsPresent = {}
for l in reader:
	if not l[cs] in NAvals and l[diagnosis] == diag:
		print ' '.join([l[WBICNum], l[cs]])
		subjsCsPresent[l[WBICNum]] = [l[diagnosis],l[cs]]
	elif l[diagnosis] == diag:
		print ' '.join([l[WBICNum], l[cs], " no score available"])

# run group ICA
subjs = [ v for v in subjsCsPresent.keys() if path.exists(path.join(diag,v)) ]
subjs.sort()
print subjs
joiner = '/'+funcFile+','+diag+'/'
fileList = diag+'/'+joiner.join(subjs)+ '/'+funcFile
ICADir = diag+cs.strip(' ')+'.gica'

mf = open(path.join(diag, '_'.join(["melodicCommands",diag, cs+'.sh'])), "wb")
mf.writelines('\n'.join([ '#$ -S /bin/bash', '#$ -cwd', '#$ -l qname=clusterall.q', '#$ -V'+'\n\n']))
mf.writelines('melodic -i '+fileList+' -o '+ICADir+' -m MNI152_T1_2mm_brain_mask.nii.gz -a concat --report --tr=2')
mf.close()
print "Melodic command written, to run it the command is:\nqsub "+path.join(diag, '_'.join(["melodicCommands",diag, cs+'.sh']))

# write dual regression command
# write contrast matrix and 
matFile = path.join(diag, diag+cs+'.mat')
print("Matrix file is: "+matFile)

sl = []
sl.append("/NumWaves\t2")
sl.append("/NumPoints\t"+str(len(subjs)))
sl.append("/PPheights\t1.000000e+00\t1.000000e+00\n")
sl.append("/Matrix")

mat = []
for subj in subjs:
	mat.append(subjsCsPresent[subj][1])  #, '# '+ subj]))

# mean centre values
meanCs = mean([float(v) for v in mat])
mat = [str(float(v)-meanCs) for v in mat]
print mat

mat = ['\t'.join(['1', v]) for v in mat]  #, '# '+ subj]))


#write clinical scores to matrix file
m = open(matFile, "wb")
m.writelines('\n'.join(sl)+'\n')
m.writelines('\n'.join(mat))
m.close()

# write .con file
conFile = path.join(diag, diag+cs+'.con')

sl = []
sl.append("/NumWaves\t2")
sl.append("/NumContrasts\t2")
sl.append("/PPheights\t1.000000e+00\t1.000000e+00\t"+str(len(subjs)))
sl.append("/RequiredEffect\t0.896\t0.896\t0.646\t0.621\t0.466\n")
sl.append("/Matrix")
sl.append("0 1")
sl.append("0 -1")

c = open(conFile, "wb")
c.writelines('\n'.join(sl))
c.close()
print "Contrast file is: "+conFile


# write command file for dual regression
joiner = '/'+funcFile+' '+diag+'/'
fileList = diag+'/'+joiner.join(subjs)+ '/'+funcFile

drFile = path.join(diag, diag+cs+'_drCommand.sh')
dr = open(drFile, "wb")
#dr.writelines('\n'.join([ '#$ -S /bin/bash', '#$ -cwd', '#$ -l qname=clusterall.q', '#$ -V'+'\n\n']))
dr.writelines(' '.join(['dual_regression', path.join(ICADir,'melodic_IC.nii'), '1', matFile, conFile,'5000', diag+cs+'_dr',fileList]) + '\n' )
dr.close()

print "dual regression file saved as: "+drFile
