from os import path,mkdir,chdir,getcwd,system
import glob
from shutil import move
from sys import argv

diag = argv[1]

try:
	qname= argv[2]
except:
	qname = "clusterall.q"

curDir=getcwd()

funcScan = "functional_reordered_pp_wpd_MNI.nii"
cutScan = funcScan.replace('.nii', '_cut.nii')
smoothScan = cutScan.replace('.nii', '_smooth.nii')
volroot = 'vol'
MNImask=path.join(curDir, "MNI152_T1_2mm_brain_mask.nii.gz")

scans = glob.glob(path.join(diag,"*",funcScan))
origDir = path.join(getcwd(), diag,"originals")

if not path.exists(origDir):
	mkdir(origDir)



for scan in scans:
	print scan
	scanDir = path.split(scan)[0]
	chdir(scanDir)
	
	sl = ['\n'.join(["#$ -S /bin/bash", "#$ -cwd", "#$ -l qname="+qname, "#$ -V\n"])]

	
	# cut scan to 135 volumes
	sl.append(' '.join(['fslsplit', funcScan, volroot,'-t']))
	sl.append('if [ -f "'+volroot+'0134.nii" ]\nthen\n')
	sl.append( ' '.join( [' fslmerge -t', cutScan, ' '.join([volroot+str(v).zfill(4)+'.nii' for v in range(0,135)]) ] ) )	
	sl.append('fi')
	
	# archive original scan
	if not path.exists(path.join(origDir, path.basename(scanDir))):
		mkdir(path.join(origDir, path.basename(scanDir)))

	sl.append(' '.join( ['mv', funcScan, path.join(origDir, path.basename(scanDir), funcScan)]))
	sl.append(' '.join(['rm', 'vol*']))
	
	# do smoothing and mask by MNI space
	sl.append(' '.join(['fslmaths', cutScan, '-s 3', '-mas', MNImask, smoothScan ]))
	
	
	f = open("submitPrepare.sh", "w")
	f.writelines('\n'.join(sl)+'\n')
	f.close()
	
	system("qsub submitPrepare.sh")
	chdir(curDir)