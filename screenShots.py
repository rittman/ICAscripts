"""
Script to visualise dual regression results using fslview and to write localisations to a log file in a file format compatible with latex.

The input is a directory containing all the dual regression results, eg: python screeShots.py PSPcatfluency_dr
"""

import csv
from sys import argv
from os import path,system

class visualise:
	def __init__(self, drDir):
		self.drDir = drDir

		self.templateDict ={"Visuospatial":"Visuospatial",
				"Sensorimotor":"Sensorimotor",
				"prim_Visual":"Primary visual",
				"Auditory":"Auditory",
				"high_Visual":"High visual",
				"Basal_Ganglia":"Basal ganglia",
				"RECN":"Right executive control",
				"Precuneus":"Precuneus",
				"anterior_Salience":"Anterior salience",
				"Language":"Language",
				"post_Salience":"Posterior salience",
				"dDMN":"Dorsal default mode",
				"LECN":"Left executive control",
				"vDMN":"Ventral default mode"}

		self.contDict={"tstat4":["Up", "Down"],
			       "tstat5":["Up", "Up"],
			       "tstat6":["Down", "Down"],
			       "tstat7":["Down", "Down"]}

	def readFile(self):
		# define input file
		inFile = path.join(self.drDir, "clusters.txt")

		# set up output file
		outFile = path.join(self.drDir, "ICAclinCorrs.tex")
		if not path.exists(outFile):
			out = open(outFile, "w")
		else:
			out = open(outFile, "a")
		out.writelines('\n\n% '+self.drDir+'\n')

		# set up reader
		f = open(inFile, "r")
		reader = csv.reader(f, delimiter="\t", skipinitialspace=True)

		# determine what to do with each line
		for l in reader:
			# reset at blank lines
			if not l:
				network = None
				contrast = None
				flag = True

			elif l[1] in self.templateDict.keys():
				network = self.templateDict[l[1]]
				contrast = l[3]
				
				inFile = path.join(self.drDir, 'dr_stage3_ic'+l[2]+'_tfce_corrp_tstat'+l[3][-1]+'.nii.gz')
				if not path.exists(inFile):
					inFile = inFile.replace("tfce", l[1]+"_"+"tfce")

			elif l[0]=="Cluster Index":
				pass

			elif contrast in self.contDict.keys():
				if flag:
					system(' '.join(["fslview", "/app/fsl/fsl-4.1.6/data/standard/MNI152_T1_2mm_brain.nii.gz", inFile, '--lut="Green"',"--bricon=0.9499,0.95", "&> viewErr.txt &"]))
					print network
					flag=False
					out.writelines('multicolumn{5}{l}{'+network+'}\n')
				print l
				loc = raw_input("Location: ")

				out.writelines(' & '.join([' & '.join(self.contDict[contrast]), l[1], ','.join([l[6], l[7],l[8]]), loc+'  \\\\\n']))
		out.close()

a = visualise(argv[1])
a.readFile()
