"""
Function to review covariations with clinical scores using FSL's
clusters function

At the moment, the function is commented out to copy original
files from the data drive.

The input is a dual regression directory, eg python review PSPletfluencycorr_dr

"""

from os import path,system,mkdir,rmdir
from glob import glob
from shutil import copy,move
from sys import argv
from string import split
from numpy import max

class evalDR:
	def __init__(self, dirName):
		self.dirName = dirName
		self.dataInDir = "/data/tr332/dualregression_20131015"
		self.dataOutDir = "/data/tr332/dualregression_20140901"
		
		# get file list
		self.fList = glob(path.join(self.dirName, "dr_stage3_ic*_tfce_corrp_tstat*.nii*"))

	def getGOFs(self):
		ICADir = self.dirName.replace("_dr", ".gica")

		# open file with goodness of fit values
		bestGOFfile = path.join(ICADir, "bestGOFs.txt")
		f = open(bestGOFfile, "r")
		lines = f.readlines()

		# construct dictionary of networks and GOF values
		self.nDict = {}
		for line in lines:
			bits = split(line, sep='\t')
			self.nDict[bits[1]] = bits[2]

	def getFiles(self):
		# copy files across
		for f in self.fList:
			if not path.exists(path.join(self.dirName, path.basename(f))):
				print path.basename(f)
				copy(f, path.join(self.dirName, path.basename(f)))

	def doClusters(self):
		# set up log file
		log = path.join(self.dirName, "clusters.txt")
		reviewLog = open(log,"w")
		reviewLog.close()

		# get the number of contrasts
		fNames = [int(split(v,sep="tstat")[1][0]) for v in glob(path.join(self.dirName, "*tstat*"))]
		fNames = set(fNames)
		maxCont = max([v for v in fNames])+1

		# define volumes and iterate through them
		contList = [str(v) for v in range(1,maxCont)]
		for network in self.nDict.keys(): 
			volume = self.nDict[network]
			for i in contList:
				inFile = path.join(self.dirName, 'dr_stage3_ic'+volume+'_tfce_corrp_tstat'+i+'.nii.gz')
	
				print inFile
				# run cluster command
				system(' '.join(['cluster', '--in='+inFile, '--thresh=0.95 --mm']))
				f = open(log, "a")
				f.writelines('\t'.join(['\n',network, volume, "tstat"+i+'\n']))
				f.close()

				# write results of cluster to
				system(' '.join(['cluster', '--in='+inFile, '--thresh=0.95 --mm', '>>', log]))
		
	def returnFile(self):
		temp = raw_input("Are you ready to return files y/n")
		if temp=="y":
			if not path.exists(self.dataOutDir):
				mkdir(self.dataOutDir)
	
			outDir = path.join(self.dataOutDir, self.dirName)
			if not path.exists(outDir):
				mkdir(outDir)
	
			for f in self.fList:
				print f
				move(f, outDir)

			otherFiles = glob(path.join(self.dirName, "*"))
			for f in otherFiles:
				print f
				move(f, path.join(outDir, path.basename(f)))

			rmdir(self.dirName)

a = evalDR(argv[1])
a.getGOFs()
#a.getFiles()
a.doClusters()
a.returnFile()
