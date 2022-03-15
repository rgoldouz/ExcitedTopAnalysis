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

def cutFlowTable(hists, samples, regions, ch, year,caption='2016', nsig=6):
    mcSum = list(0 for i in xrange(0,len(regions))) 
#    table = '\\begin{sidewaystable*}' + "\n"
    table = '\\begin{table*}' + "\n"
    table += '\\centering' + "\n"
    table += '\\caption{' + caption +"}\n"
    table += '\\resizebox{\\textwidth}{!}{ \n'
    table += '\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}' + "\n"
    table += '\\hline' + "\n"
    table += 'Samples & ' + ' & '.join(regions) + '\\\\' + "\n"
    table += '\\hline' + "\n"
    for ids, s in enumerate(samples):
        if ids==0:
            continue
        table += s 
        for idr, r in enumerate(regions):
            table += (' & ' + str(round(hists[year][ids][ch][idr][2].Integral(),2)))
            if ids<nsig:
                mcSum[idr] += hists[year][ids][ch][idr][2].Integral()
        table += '\\\\' + "\n"    
    table += '\\hline' + "\n"
    table += 'Prediction '
    for idr, r in enumerate(mcSum):
        table += (' & ' + str(round(r,2)))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += 'Data '
    for idr, r in enumerate(regions):
        table += (' & ' + str(hists[year][0][ch][idr][2].Integral()))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += 'Data$/$Pred. '
    for idr, r in enumerate(mcSum):
        table += (' & ' + str(round(hists[year][0][ch][idr][2].Integral()/r,2)))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += '\\end{tabular}}' + "\n"
    table += '\\end{table*}' + "\n"
#    table += '\\end{sidewaystable*}' + "\n"
    print table

def stackPlots(hists, SignalHists, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch +'/'+reg):
       os.makedirs(year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
    for num in range(len(hists)):
        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
    for num in range(len(SignalHists)):
        SignalHists[num].SetBinContent(SignalHists[num].GetXaxis().GetNbins(),SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()) + SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()+1))
    for num in range(1,len(hists)):
        hs.Add(hists[num])

    dummy = hists[0].Clone()

    
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.7,0.55,0.9,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
#    pad1.SetLogy(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kTRUE)

    y_min=1
    y_max=1.6*dummy.GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetTitle("")
    dummy.GetYaxis().SetTitle('Events')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetYaxis().SetTitleOffset(0.8)
    dummy.GetYaxis().SetTitleSize(0.07)
    dummy.GetYaxis().SetLabelSize(0.04)
    dummy.GetYaxis().SetRangeUser(y_min,y_max)
    dummy.Draw("e")
    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
    dummy.Draw("eSAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    Lumi = '137.42'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'
    label_cms="CMS Preliminary"
    Label_cms = ROOT.TLatex(0.2,0.92,label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.71,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2,0.8,year +" / "+ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")


    legend.AddEntry(dummy,Fnames[0],'ep')
    for num in range(1,len(hists)):
        legend.AddEntry(hists[num],Fnames[num],'F')
    for H in range(len(SignalHists)):
        legend.AddEntry(SignalHists[H], Fnames[len(hists)+H],'L')
    legend.Draw("same")

    if (hs.GetStack().Last().Integral()>0):
        Label_DM = ROOT.TLatex(0.2,0.75,"Data/MC = " + str(round(hists[0].Integral()/hs.GetStack().Last().Integral(),2)))
        Label_DM.SetNDC()
        Label_DM.SetTextFont(42)
        Label_DM.Draw("same")

    pad1.Update()

    pad2.cd()
    SumofMC = hs.GetStack().Last()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.GetXaxis().SetTitle(varname)
#    dummy_ratio.GetXaxis().CenterTitle()
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetXaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.115)
    dummy_ratio.GetYaxis().SetLabelSize(0.089)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.01)
    dummy_ratio.GetYaxis().SetTitleOffset(0.42)
    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetYaxis().SetNdivisions(504)    
    dummy_ratio.GetYaxis().SetRangeUser(0,2)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw()
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    canvas.Print(year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


#year=['2016','2017','2018','All']
year=['2017']


regions=["nAk8G1", "nAk8G1nTtagG0", "nAk8G1MLPG0p8", "nAk8G1MLPG0p8TtagG0", "nAk8G1MLPG0p8TtagG0MassTs2G300","nAk8G1MLPG0p8Ttag0","nAk8G1MLPL0p8TtagG0"]
scaleSig = [0.2,0.002,0.002,0.002, 0.002,0.002,0.002]
channels=["aJets","MuJets","aMuJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"];
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","jet04Phi","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met","nVtx", "nPh", "phoChargedIso", "phoNeutralHadronIso", "phoPhotonIsolation", "drGj04", "dPhiGj08", "HT", "HoE", "softdropMass", "tau21", "tau31", "nbjet08","TvsQCD", "muPt","muEta","muPhi","nBsub", "mifBsub", "tTagifBsub","njet08massG50","njet08massG120","TsMass1", "nTopTag","masstS2", "MLP", "Sietaieta"]
variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","#Phi(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of vertices","Number of photons","phoChargedIso","phoNeutralHadronIso", "phoPhotonIsolation","#DeltaR(#gamma,jet04)", "#DeltaR(#gamma,jet08)", "HT", "H/E", "softdropMass (leading jet (AK8))", "tau21 (leading jet (AK8))", "tau32 (leading jet (AK8))", "num of AK8 jet b-tagged","TvsQCD (leading jet (AK8))","p_{T}(#mu)","#eta(#mu)","#Phi(#mu)", "num of AK8 jet with b-sub", "soft drop mass if Ak8 has b-sub", "TvsQCD if Ak8 has b-sub", "Number of Ak8 jets with mass > 50","Number of Ak8 jets with mass > 120", "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","MLP","#sigma_{i#eta i#eta}"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/hists/'

Samples = ['data.root','QCD.root', 'GJets.root','WG.root','top.root','WJetsToLNu.root','DY.root', 'tptpM1000.root', 'tptpM2000.root']
SamplesName = ['Data','QCD','#gamma+jets', 'W#gamma', 'top','Wjets','DY', 't*t* (M=1TeV)', 't*t* (M=2TeV)']
SamplesNameLatex = ['Data','QCD','Gjets', 'WG', 'tt', 't#bar{t}#gamma', 't*t* (M=1TeV)', 't*t* (M=2TeV)']

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]

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
                    if 'tptp' in Samples[f]:
                       h.Scale(scaleSig[numreg])
                    if 'GJets' in Samples[f]:
                       h.Scale(0.83)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

HistsQCD = []
for numyear, nameyear in enumerate(year):
    l0=[]
    FilesData = ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[0])
    FilesGjets = ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[2])
    for numreg, namereg in enumerate(regions):
        l1=[]
        for numvar, namevar in enumerate(variables):
            h0= FilesData.Get("fakeAJetsIso"     +  '_' + namereg + '_' + namevar)
            h1=h0.Clone()
            h2= FilesData.Get("fakeAJetsSiSi"    +  '_' + namereg + '_' + namevar)
            h3= FilesData.Get("fakeAJetsOthers"  +  '_' + namereg + '_' + namevar)
            h1.Add(h2)
            h1.Add(h3)
            h1.Scale(0.0273/(1-0.0273))
            g0= FilesGjets.Get("fakeAJetsIso"     +  '_' + namereg + '_' + namevar)
            g1=g0.Clone()
            g2= FilesGjets.Get("fakeAJetsSiSi"    +  '_' + namereg + '_' + namevar)
            g3= FilesGjets.Get("fakeAJetsOthers"  +  '_' + namereg + '_' + namevar)
            g1.Add(g2)
            g1.Add(g3)
            g1.Scale(0.0273)
            h1.Add(g1,-1)
            h1.SetFillColor(ROOT.kYellow)
            h1.SetLineColor(ROOT.kYellow)
            l1.append(h1)
        l0.append(l1)
    HistsQCD.append(l0)

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if numch>0:
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'QCD' in Samples[f] and numch==0:
                        HH.append(HistsQCD[numyear][numreg][numvar])
                        continue
                    if 'tp' in Samples[f]:
                        HHsignal.append(Hists[numyear][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][f][numch][numreg][numvar])
                stackPlots(HH, HHsignal, SamplesName, namech, namereg, nameyear,namevar + ' -FR',variablesName[numvar])


for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if numch>0:
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'tp' in Samples[f]:
                        HHsignal.append(Hists[numyear][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][f][numch][numreg][numvar])
                stackPlots(HH, HHsignal, SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar])

le = '\\documentclass{article}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

print le
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        cutFlowTable(Hists, SamplesNameLatex, regions, numch, numyear, nameyear + ' ' + namech, 6 )
print '\\end{document}' + "\n"


