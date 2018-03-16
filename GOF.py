# -*- coding: utf-8 -*- """ Created on Sun Nov  6 11:48:51 2011
"""
@author: -
"""

from os import getcwd,path,system,chmod,chdir
from sys import argv
import glob,string

#class BestFit:
#    """
#    A script for calculating goodness of fit values for individuals
#    """
#    def __init__(self, fname, networks = None,
#                     mainDir='/scratch/tr332/ICA',
#                     template_dir ):
#        self.fname = path.basename(fname)
#        self.mainDir = mainDir
#        ica_dir = path.split(fname)[0]
#        template_dir = template_dir
#
#        if not networks:
#            self.
#        else:
#            networks = networks

def GOF(template_dir='/home/tr332/Functional_ROIs'):
    outfile = open('bestGOF.txt',"w")
    tempscript = 'tempscript'

    # get a list of the network templates
    networks = [path.basename(v) for v in glob.glob(path.join(template_dir,'*')) if path.isdir(v)]

    # create dictionary of GOF
    gof_dict = {}

    # split ICA result in to individual components
    system(' '.join(['fslsplit', "melodic_IC.nii.gz", "vol"]))

    # network by component GOF value
    for network in networks:
        networkGOF = {}
        print network        

        # Create file to write GOF values to
        g = open(network, "w")
        g.close()
        
        # create a temporary script to run goodness of fit analysis
        
        f = open(tempscript,"w")
        f.writelines('#!/bin/bash\necho component within without GOF >>'+network+'\n')
        f.writelines("for i in `ls vol*`\ndo\n")
        f.writelines('A=`fslstats '+'$i -k '+path.join(template_dir,network,network+'.nii.gz')+' -m`\n')
        f.writelines('B=`fslstats '+'$i -k '+path.join(template_dir,network,network+'_inv.nii.gz')+' -m`\n')
        f.writelines('echo $i $A $B >> '+network+'\ndone\n')
        f.close()
        
        # change permissions and run temporary script
        chmod(tempscript,0755)
        system(tempscript)

        lines = open(network,"r").readlines()
        h = open(network,"w")
        h.writelines('\t'.join(string.split(lines[0]))+'\n')
        
        network_gof = {}
        for line in lines[1:]:
            bits = string.split(line.strip('\n'))
            gof = float(bits[1])-float(bits[2])
            h.writelines('\t'.join([bits[0],bits[1],bits[2],str(gof)])+'\n')
            network_gof[bits[0]] = gof
            gof_dict[network] = network_gof
        h.close()

        # write best GOF
        inverse = [(values,keys) for keys,values in gof_dict[network].items()]
        # take only the volume name of the highest rank component            
        bestvol = max(inverse)[1]
        
        outfile.writelines('\t'.join([path.basename(network),bestvol.strip('vol.nii'),str(max(gof_dict[network].values())),'\n']))
    outfile.close()
    system('rm -f ' + 'vol*')
   
GOF()

