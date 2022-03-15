import math
import gc
import sys
import ROOT
import numpy as npi
import copy
from array import array
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, THStack
from ROOT import gROOT, gBenchmark, gRandom, gSystem, Double

file_2016_1 = ROOT.TFile.Open('../input/2016_RunBCDEF_SF_ID.root')
H_2016_1 = file_2016_1.Get('NUM_TightID_DEN_genTracks_eta_pt')

file_2016_2 = ROOT.TFile.Open('../input/2016_RunGH_SF_ID.root')
H_2016_2 = file_2016_2.Get('NUM_TightID_DEN_genTracks_eta_pt')

#for x in range(H_2016_1.GetNbinsX()):
#    for y in range(H_2016_1.GetNbinsY()):
#        print str(x) + "   "+str(y)
#        print str(H_2016_1.GetBinContent(x+1,y+1)) + "   "+str(H_2016_1.GetBinError(x+1,y+1))

print str(H_2016_1.GetBinContent(1,1)) + "   "+str(H_2016_1.GetBinError(1,1))
print str(H_2016_2.GetBinContent(1,1)) + "   "+str(H_2016_2.GetBinError(1,1))
H_2016_1.Scale(0.55)
H_2016_2.Scale(0.45)

H_2016_1.Add(H_2016_2)

print str(H_2016_1.GetBinContent(1,1)) + "   "+str(H_2016_1.GetBinError(1,1))

