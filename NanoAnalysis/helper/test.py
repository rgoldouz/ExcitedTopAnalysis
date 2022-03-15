# This file skims the data and saves the output to ./tmp
# Do not combine files across runs, otherwise you may get inconsistent TTree structures!
# Doing things file by file is the safest way to avoid this problem, and comes at almost
# no extra cost.
# You can copy and paste json sources directly from https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/

import os
import ROOT
path = []


for subdir, dirs, files in os.walk('/hadoop/store/user/rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_B_SinglePhoton/210427_112656/0000'):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = file
        print '------>' + subdir + os.sep +filepath
        if filepath.endswith(".root"):
            f = ROOT.TFile.Open(subdir + os.sep +filepath)
#f = ROOT.TFile.Open("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/ANoutput.root")
            tree_in = f.Get('IIHEAnalysis')
            for event in tree_in:
                if event.ev_event==11122160:
                    print filepath
#    if event.Event==12706422:
#        for i in range(len(event.Ak8_pt)):
#            print str(i)+',' + str(event.Ak8_pt[i]) + ',' + str(event.Ak8_eta[i])

