# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 11:48:51 2011

@author: -
"""

from os import getcwd,path,system,chmod,chdir
from sys import argv
import glob,string

class bestfit:
	"""
	A script for calculating goodness of fit values for individuals
	"""
	def __init__(self, fname, networks = None, mainDir='/scratch/tr332/rsICA', templatedir = '/scratch/tr332/rsICA/templates_new'):
		self.fname = path.basename(fname)
		self.mainDir = mainDir
		self.ICADir = path.split(fname)[0]
		self.templateDir = templatedir

		if not networks:
			self.networks = [path.basename(v) for v in glob.glob(path.join(templatedir,'*')) if path.isdir(v)]
		else:
			self.networks = networks



	def GOFs(self):
		chdir(self.ICADir)
		outfile = open('bestGOFs.txt',"w")
		tempscript = 'tempscript'
		
		# create dictionary of GOFs
		GOFs = {}
   
		# split ICA result in to individual components
		system(' '.join(['fslsplit', self.fname, "vol"]))

		# network by component GOF value
		for network in self.networks:
			networkGOFs = {}
			print network+' '+self.fname
			
			# Create file to write GOF values to
			g = open(network, "w")
			g.close()
			
			# create a temporary script to run goodness of fit analysis
			
			f = open(tempscript,"w")
			f.writelines('#!/bin/bash\necho component within without GOF >>'+network+'\n')
			f.writelines("for i in `ls vol*`\ndo\n")
			f.writelines('A=`fslstats '+'$i -k '+path.join(self.templateDir,network,network+'.nii')+' -m`\n')
			f.writelines('B=`fslstats '+'$i -k '+path.join(self.templateDir,network,network+'_inv.nii')+' -m`\n')
			f.writelines('echo $i $A $B >> '+network+'\ndone\n')
			f.close()
			
			# change permissions and run temporary script
			chmod(tempscript,0755)
			system(tempscript)

			lines = open(network,"r").readlines()
			h = open(network,"w")
			h.writelines('\t'.join(string.split(lines[0]))+'\n')
			
			for line in lines[1:]:
				bits = string.split(line.strip('\n'))
				GOF = float(bits[1])-float(bits[2])
				h.writelines('\t'.join([bits[0],bits[1],bits[2],str(GOF)])+'\n')
				networkGOFs[bits[0]] = GOF
				GOFs[network] = networkGOFs
			h.close()

		# write best GOFs
			inverse = [(values,keys) for keys,values in GOFs[network].items()]
			# take only the volume name of the highest rank component			
			bestvol = max(inverse)[1]
			
			outfile.writelines('\t'.join([self.ICADir,path.basename(network),bestvol.strip('vol.nii'),str(max(GOFs[network].values())),'\n']))
		outfile.close()
		system('rm -f ' + 'vol*')
   

mainDir = getcwd()

ICADir = argv[1]

a = bestfit(path.join(ICADir,'melodic_IC'))

a.GOFs()

