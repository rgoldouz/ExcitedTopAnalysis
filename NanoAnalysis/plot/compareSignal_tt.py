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


def compareHists(hists,Fnames, ch = "channel", reg = "region", var="sample", varname="v"):
    for num in range(len(hists)):
        if (hists[num].Integral() <= 0):
            return  
    Fol = 'compareHists'
    if not os.path.exists(Fol):
       os.makedirs(Fol)
    if not os.path.exists(Fol + '/' + ch):
       os.makedirs(Fol + '/' + ch)
    if not os.path.exists(Fol + '/' + ch +'/'+reg):
       os.makedirs(Fol + '/' + ch +'/'+reg)
    for num in range(len(hists)):
        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
        hists[num].Scale(1/hists[num].Integral())

    canvas = ROOT.TCanvas(ch+reg+var,ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.6,0.7,0.85,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)

    pad1=ROOT.TPad("pad1", "pad1", 0.05, 0.05, 1, 0.99 , 0)#used for the hist plot
    pad1.Draw()
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    y_min=0
    y_max=1.2* max(hists[0].GetMaximum(), hists[1].GetMaximum(), hists[2].GetMaximum())
    hists[0].SetTitle("")
    hists[0].GetYaxis().SetTitle('Fraction')
    hists[0].GetXaxis().SetLabelSize(0.03)
    hists[0].GetYaxis().SetTitleOffset(0.8)
    hists[0].GetYaxis().SetTitleSize(0.05)
    hists[0].GetYaxis().SetLabelSize(0.04)
    hists[0].GetYaxis().SetRangeUser(y_min,y_max)
    hists[0].GetXaxis().SetTitle(varname)
    hists[0].Draw("Hist")
    hists[0].SetLineWidth(2)
    hists[0].SetFillColor(0)
    for H in range(1,len(hists)):
        hists[H].SetLineWidth(2)
        hists[H].SetFillColor(0)
        hists[H].Draw("histSAME")
    hists[0].Draw("AXISSAMEY+")
    hists[0].Draw("AXISSAMEX+")

    for num in range(0,len(hists)):
        legend.AddEntry(hists[num],Fnames[num],'L')
    legend.Draw("same")

    pad1.Update()
    canvas.Print(Fol + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

year=['2017']
regions=[ "nAk8G1nTtagG0"]
channels=["aJets"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","jet04Phi","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met","nVtx", "nPh", "phoChargedIso", "dPhiGj08", "drGj08", "HT", "HoE", "softdropMass", "tau21", "tau31", "nbjet08","TvsQCD","njet08massG50","njet08massG120","TsMass1", "nTopTag","masstS2", "Sietaieta","Mll"]

variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","#Phi(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of vertices","Number of photons","phoChargedIso","#DeltaPhi(#gamma,jet08)", "#DeltaR(#gamma,jet08)", "HT", "H/E", "softdropMass (leading jet (AK8))", "tau21 (leading jet (AK8))", "tau32 (leading jet (AK8))", "num of AK8 jet b-tagged","TvsQCD (leading jet (AK8))", "Number of Ak8 jets with mass > 50","Number of Ak8 jets with mass > 120", "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}", "Mll"]

variablesGen=["excitedTop_genPt",
"excitedTop_genEta",  
"top_genPt",          
"top_genEta",         
"gamma_genPt",        
"gamma_genEta",       
"gluon_genPt",        
"gluon_genEta",       
"excitedTop_mass",    
"genMassPhtop",       
"genMassGluontop",    
"geDrPhtop",          
"geDrPGluontop",      
"genMassTTbar",       
]
HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

Samples = ['TTga_M800.root','TTga_M1000.root', 'TTga_M1200.root', 'TTga_M1400.root', 'TTga_M1600.root']
SamplesName = ['TTga_M800','TTga_M1000', 'TTga_M1200', 'TTga_M1400', 'TTga_M1600']

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue+8,ROOT.kOrange-3, ROOT.kBlack, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]
Style =[1,1,1,1,1,1,1,1]

Hists = []
HistsGen=[]
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        print HistAddress + nameyear+ '_' + Samples[f]
        for numch, namech in enumerate(channels):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variables):
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    h.SetLineStyle(Style[f])
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

Files = []
for f in range(len(Samples)):
    l1=[]
    Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
    for numvar, namevar in enumerate(variablesGen):
        h= Files[f].Get(namevar)
        h.SetFillColor(colors[f])
        h.SetLineColor(colors[f])
        h.SetLineStyle(Style[f])
        l1.append(h)            
    HistsGen.append(l1)

for numreg, namereg in enumerate(regions):
    for numvar, namevar in enumerate(variables):
        HH=[]
        HHname=[]
        for f in range(len(Samples)):
            HH.append(Hists[0][f][0][numreg][numvar])
            HHname.append(SamplesName[f])
        compareHists(HH,HHname, channels[0], namereg,namevar,variablesName[numvar])

for numvar, namevar in enumerate(variablesGen):
    HH=[]
    HHname=[]
    for f in range(len(Samples)):
        HH.append(HistsGen[f][numvar])
        HHname.append(SamplesName[f])
    compareHists(HH,HHname, "Gen", "",namevar,namevar)
