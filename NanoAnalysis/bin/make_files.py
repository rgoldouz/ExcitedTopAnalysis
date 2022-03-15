import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
import gc
import sys
import os
import subprocess
import readline
import string

import Files_2017
MCSAMPLES = {}
MCSAMPLES.update(Files_2017.mc2017_samples)

text = ''
text += 'import sys \n'
text += 'import os \n'
text += 'import subprocess \n'
text += 'import readline \n'
text += 'import string \n'
text += '\n'

diremc = '/hadoop/store/user/rgoldouz/Etop_nanoAODv9_MC'
#dire = '/hadoop/store/user/rgoldouz/ExitedTopSamplesMCJan2021/'

neventsweight = 0
for key, value in MCSAMPLES.items():
    if 'tp' in key:
        continue
    value[0] =[]
    value[7] = str(0)

for root, dirs, files in os.walk(diremc):
#    if '40to130' not in root:
#        continue
    if len(files) > 0:
        print root
        neventsweight = 0
        for fname in files:
            filename = root + '/' + fname
            if 'fail' in fname:
                continue
            f = ROOT.TFile.Open(filename)
#            tree_in = f.Get('Runs')
            tree_meta = f.Get('Runs')
            tree_meta.GetEntry(0)
            neventsweight += tree_meta.genEventCount
            f.Close()
        for key, value in MCSAMPLES.items():
            print key.split('_')[1]
            if key.split('_')[1] in root: 
                value[0].append(root[19:])
                value[7] = str( float(value[7]) + neventsweight)
text += 'mc2017_samples='                
text += str(MCSAMPLES)
text += '\n'

diredata = '/hadoop/store/user/rgoldouz/Etop_nanoAODv9_DATA/'
DATASAMPLES = {}
DATASAMPLES.update(Files_2017.data2017_samples)

for key, value in DATASAMPLES.items():
    value[0] =[]
for root, dirs, files in os.walk(diredata):
    if len(files) > 0:
        for key, value in DATASAMPLES.items():
            if key in root:
                value[0].append(root[19:])
text += '\n'
text += 'data2017_samples='
text += str(DATASAMPLES)

open('Files_2017_nano.py', 'wt').write(text)
