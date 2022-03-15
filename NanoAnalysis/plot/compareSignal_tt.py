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

#year=['2016','2017','2018','All']
year=['2017']
regions=["ll","llOffZ","llB1", "llBg1", "llMetl30", "llMetg30", "llMetl30Jetg2B1", "llMetl30Jetg2Bg1", "llMetg30Jetg2B1", "llMetg30Jetg2Bg1"]
channels=["ee", "emu", "mumu"];
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw"]
#variables=["lep1Pt"]
variablesName=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]"]



HistAddress = '/user/rgoldouz/NewAnalysis2020/Analysis/hists/'

Samples = ['TTTo2L2Nu.root', 'LFVVecC.root', 'LFVVecU.root', 'LFVStVecC.root', 'LFVStVecU.root', 'LFVTtVecC.root', 'LFVTtVecU.root']
SamplesName = ['t#bar{t}', 'LFV-vec [e#mutc]', 'LFV-vec [e#mutu]', 'LFV-vec ST[e#mutc]', 'LFV-vec St[e#mutu]', 'LFV-vec tT[e#mutc]', 'LFV-vec tt[e#mutu]']

colors =  [ROOT.kRed-4,ROOT.kOrange-6, ROOT.kCyan-6,ROOT.kOrange-6,ROOT.kCyan-6,ROOT.kOrange-6, ROOT.kCyan-6]
Style =[1,1,1,7,7,3,3]

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
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    h.SetLineStyle(Style[f])
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

for numreg, namereg in enumerate(regions):
    for numvar, namevar in enumerate(variables):
        HH=[]
        HHname=[]
        for f in range(len(Samples)):
            HH.append(Hists[0][f][1][numreg][numvar])
            HHname.append(SamplesName[f])
        compareHists(HH,HHname, 'emu', namereg,namevar,variablesName[numvar])
