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



HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'
year=['2016preVFP', '2016postVFP', '2017','2018']
Hists2D=[]
for numyear, nameyear in enumerate(year):
    hfileData = ROOT.TFile.Open( HistAddress +nameyear +'_data.root')
    H1Den=hfileData.Get('jetPtvsTmass1jetFakePh')
    H1Nom=hfileData.Get('jetPtvsTmass1jet1tagFakePh')
    hfileTTG = ROOT.TFile.Open( HistAddress +nameyear+'_ttG.root')
    H1NomttG=hfileTTG.Get('jetPtvsTmass1jet1tagFakePh')
    H1Nom.Add(H1NomttG,-1)
    hfileTOP = ROOT.TFile.Open( HistAddress +nameyear+'_TOP.root')
    H1Nomtop=hfileTTG.Get('jetPtvsTmass1jet1tagFakePh')
    H1Nom.Add(H1Nomtop,-1)
    hfileData.Close()
    hfileTOP.Close()
    hfileTTG.Close()
    canvas = ROOT.TCanvas('can_name','can_name',10,10,1100,628)
    canvas.cd()
    
    pEff = ROOT.TEfficiency(H1Nom,H1Den);
    pEff.SetStatisticOption(ROOT.TEfficiency.kFFC);
    pEff.SetConfidenceLevel(0.68);
    heff = pEff.GetPaintedHistogram()
    
    newH=H1Den.Clone()
    for i in range(1,5):
        for j in range(1,5):
            print str(i)+str(j)
            print str(pEff.GetEfficiency(pEff.GetGlobalBin(i,j))) + ":"+str(pEff.GetEfficiencyErrorLow(pEff.GetGlobalBin(i,j))) + ":"+str(pEff.GetEfficiencyErrorUp(pEff.GetGlobalBin(i,j))) + ":"
            if pEff.GetEfficiency(pEff.GetGlobalBin(i,j))>0:
                newH.SetBinContent(i,j,pEff.GetEfficiency(pEff.GetGlobalBin(i,j)))
                newH.SetBinError(i,j,pEff.GetEfficiencyErrorUp(pEff.GetGlobalBin(i,j)))
            else:
                newH.SetBinContent(i,j,0)
                newH.SetBinError(i,j,0)        
    
    
    
    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0.05, 0.05, 1, 0.99 , 0)
    pad1.Draw("")
    newH.SetName(nameyear+"_2DMistagRatejetPtvsMass")
    newH.SetTitle("ParticleNet miss-tag rate " + nameyear)
    newH.GetYaxis().SetTitle('Soft drop mass')
    newH.GetXaxis().SetTitle('Ak8-Jet pt')
    newH.GetXaxis().SetTitleSize(0.05)
    newH.GetYaxis().SetTitleSize(0.05)
    newH.GetYaxis().SetTitleOffset(0.7)
    newH.Draw("colz error text")
    #pEff.Draw("ey");
    canvas.Print(nameyear +"_2DMistagRatejetPtvsMass_fakeGamma.png")
    Hists2D.append(newH)

hfile = ROOT.TFile( 'topMistagRate2D.root', 'RECREATE', 'mis top tag rate histogram' )
for numyear, nameyear in enumerate(year):
    Hists2D[numyear].Write()
hfile.Write()
hfile.Close()
