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
TGaxis.SetMaxDigits(2)

def draw2d(hists, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    if not os.path.exists('2D_' + year):
       os.makedirs('2D_' +year)
    if not os.path.exists('2D_' +year + '/' + ch):
       os.makedirs('2D_' +year + '/' + ch)
    if not os.path.exists('2D_' +year + '/' + ch +'/'+reg):
       os.makedirs('2D_' +year + '/' + ch +'/'+reg)
    
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.7,0.55,0.9,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.05, 1, 0.99 , 0)#used for the hist plot
    pad1.Draw()
    pad1.SetBottomMargin(0.1)
    pad1.SetLeftMargin(0.1)
    pad1.SetRightMargin(0.1)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    hists.SetTitle(Fnames)
    hists.GetXaxis().SetTitle(varname)


    hists.Draw()

    canvas.Print('2D_' +year + '/' + ch +'/'+reg+'/'+ Fnames +var + ".png")
    del canvas
    gc.collect()


#year=['2016','2017','2018','All']
year=['2017']


#regions=["allB", "g1B", "g2B"]
regions=["all"]
channels=["aJets","MuJets","aMuJets"];
#variables=["topTagvsJetPt", "massvsJetPt", "t21vsJetPt", "t32vsJetPt"]
variables=["topTagvsJetPt", "massvsJetPt", "t21vsJetPt", "t32vsJetPt", "topTagvsmass", "massJ1vsmassJ2","npvsJetPt","npvsmass", "npvstopTag","mergedvsTopPt", "nSubbvsPt", "nSubbvsmass","nSubbvstopTag","nSubbvsBdis","subFlavorvsSubBTag"]
#variablesName=['Top tagger vs Ak8jet pt',  'Softt drop mass vs Ak8jet pt', 'tau21 vs Ak8jet pt', 'tau32 vs Ak8jet pt']
variablesName=["topTagvsJetPt", "massvsJetPt", "t21vsJetPt", "t32vsJetPt", "topTagvsmass", "massJ1vsmassJ2","npvsJetPt","npvsmass", "npvstopTag","mergedvsTopPt", "nSubbvsPt", "nSubbvsmass","nSubbvstopTag","nSubbvsBdis","subFlavorvsSubBTag"]
HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/hists/'

#Samples = [ 'GJets.root','ttToSemiLeptonic.root','tptpM2000.root']
#SamplesName = ['Gjets', 'top', 'tstar2TeV']
#SamplesNameLatex = ['Gjets', 'tt',  't*t* (M=2TeV)']


Samples = ['tptpM1000.root']
SamplesName = ['tstar1TeV']
SamplesNameLatex =['t*t* (M=1TeV)']

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, ROOT.kCyan-6,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variables):
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                for f in range(len(Samples)):
                    draw2d(Hists[numyear][f][numch][numreg][numvar], SamplesName[f], namech, namereg, nameyear,namevar,variablesName[numvar])

