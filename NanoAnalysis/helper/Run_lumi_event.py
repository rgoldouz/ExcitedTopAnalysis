# This file skims the data and saves the output to ./tmp
# Do not combine files across runs, otherwise you may get inconsistent TTree structures!
# Doing things file by file is the safest way to avoid this problem, and comes at almost
# no extra cost.
# You can copy and paste json sources directly from https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/

import os
import ROOT
path = []

f = ROOT.TFile.Open("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/hists/2017_B_SinglePhoton.root")
#f = ROOT.TFile.Open("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/ANoutput.root")
tree_in = f.Get('TStar')
print "Run, Lumi, Event"
for event in tree_in:
   if event.Ch==0:
        print str(event.Run)+","+str(event.Lumi)+","+str(abs(event.Event))
#    if event.Event==12706422:
#        for i in range(len(event.Ak8_pt)):
#            print str(i)+',' + str(event.Ak8_pt[i]) + ',' + str(event.Ak8_eta[i])

