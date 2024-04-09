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


def compareNeffHist(A, textA, label_name="sample", can_name="can"):
    canvas = ROOT.TCanvas(can_name,can_name,10,10,1100,628)
    canvas.SetGrid();
    canvas.cd()
    for l in range(len(A)):
        A[l].SetLineColor( l+1 )
        A[l].SetLineWidth(2)
    if len(A)==2:
        A[0].SetLineColor(4)
    if len(A)==3:
        A[2].SetLineColor(4)

#    A[0].SetMaximum(1.1)
    A[0].SetMinimum(0)
    A[0].SetTitle("")
    A[0].GetXaxis().SetTitle(label_name)
    A[0].GetYaxis().SetTitle('top mistag probability (105<m<210)')
    A[0].GetXaxis().SetTitleSize(0.05)
    A[0].GetYaxis().SetTitleSize(0.05)
    for l in range(len(A)):
        A[l].Draw('esame')
    A[0].Draw("AXISSAMEY+")
    A[0].Draw("AXISSAMEX+")

    leg = ROOT.TLegend(0.2,0.6,0.4,0.85)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.04)
    for l in range(len(A)):
        leg.AddEntry(A[l] ,textA[l],'l')
    leg.Draw("same")

    label = ROOT.TLatex()
    label.SetTextAlign(12)
    label.SetTextFont(42)
    label.SetTextSize(0.06)
    label.SetNDC(ROOT.kTRUE)
    canvas.Print( can_name +"_"+ label_name + ".png")
    del canvas
    gc.collect()

def draw1dHist(A,textA="A", label_name="sample", can_name="can"):
    canvas = ROOT.TCanvas(can_name,can_name,10,10,1100,628)
    canvas.cd()

    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0.05, 0.05, 1, 0.99 , 0)
    pad1.Draw()

    A.SetLineColor( 1 )
    A.SetLineWidth( 2 )
    A.SetTitle("")
    A.GetYaxis().SetTitle('Events')
    A.GetXaxis().SetTitleSize(0.05)
    A.GetYaxis().SetTitleSize(0.05)
    A.SetMaximum(1.2*A.GetMaximum())
    A.SetMinimum(0);
    A.GetYaxis().SetTitleOffset(0.7)
    A.GetYaxis().SetTitle('top Mistag Rate')
    A.Draw()
    legend = ROOT.TLegend(0.6,0.9,1,1)
    legend.AddEntry(A ,textA,'l')
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.Draw("same")

    label = ROOT.TLatex()
    label.SetTextAlign(12)
    label.SetTextFont(42)
    label.SetTextSize(0.08)
    label.SetNDC(ROOT.kTRUE)
    canvas.Print(can_name +"_"+ label_name + ".png")
    del canvas
    gc.collect()

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

colors =  [ROOT.kBlack,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue+8,ROOT.kOrange-3, ROOT.kYellow, ROOT.kBlack, ROOT.kBlue]
def stackPlots(hists, SignalHists, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v", dirName='Hists'):
    for f in range(0,len(hists)):
        hists[f].SetFillColor(colors[f])
        hists[f].SetLineColor(colors[f])
    for f in range(0,len(SignalHists)):
        SignalHists[f].SetFillColor(colors[len(hists)+f])
        SignalHists[f].SetLineColor(colors[len(hists)+f])
    Blinded=False
    if reg=='nAk8G1nTtagG0':
        Blinded=True
    if not os.path.exists(dirName):
       os.makedirs(dirName)
    if not os.path.exists(dirName + '/' + ch):
       os.makedirs(dirName + '/' + ch)
    if not os.path.exists(dirName + '/' + ch +'/'+reg):
       os.makedirs(dirName + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
    for num in range(len(hists)):
        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
    for num in range(len(SignalHists)):
        SignalHists[num].SetBinContent(SignalHists[num].GetXaxis().GetNbins(),SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()) + SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()+1))
    for num in range(1,len(hists)):
        hs.Add(hists[len(hists)-num])

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
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)
    y_min=0
    y_max=1.6*dummy.GetMaximum()
    if 'Pt' in var:
        pad1.SetLogy(ROOT.kTRUE)
        y_min=0.1
        y_max=10*dummy.GetMaximum()
    pad1.cd()
    y_min=0.01
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

    if Blinded:
        dummy.SetMarkerColor(0)
        dummy.SetLineColor(0)
        dummy.SetFillColor(0)
    dummy.Draw("e")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")
    if not Blinded:
        dummy.Draw("eSAME")
        dummy.Draw("AXISSAMEY+")
        dummy.Draw("AXISSAMEX+")


    Lumi = '138'
    if (year == '2016preVFP'):
        Lumi = '19.52'
    if (year == '2016postVFP'):
        Lumi = '16.81'
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

    if (hs.GetStack().Last().Integral()>0 and not Blinded):
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
    if Blinded:
        for b in range(dummy_ratio.GetNbinsX()):
            dummy_ratio.SetBinContent(b+1,100)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw()
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    canvas.Print(dirName + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


#year=['2016','2017','2018','All']
year=['2017']
year=['2016preVFP', '2016postVFP', '2017','2018']
#year=['2018']
categories=["promptG", "fakeGEle","fakeGJet"]
regions=["nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0",  "nAk8G1nTtag0", "nAk8G1nTtag0XtopMissTagRate",  "nAk81nTtag0XtopMissTagRate","nAk8G1nTtagG0LepG0", "nAk81nTtagOffMt","nAk81nTtagOffMtXtopMissTagRate"]
scaleSig = [1,1,1,1,0.1,40,1,1,1,1,1,1,1,1]
scaleSigRegion = [500,1,1,1,1,1,1,1,1,1,1,1]
channels=["aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"]
channels=["aJets"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met", "nPh", "phoChargedIso",  "HT", "HoE", "softdropMass", "TvsQCD","TsMass1", "nTopTag","masstS2", "Sietaieta","MtGMet","subLeadingjet08Pt","nVtxApu","nVtxBpu"]
#variables=["GammaPt"]
variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of photons","phoChargedIso", "HT", "H/E", "softdropMass (leading jet (AK8))","TvsQCD (leading jet (AK8))",  "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}", "M_{T}(#gamma,MET)", "p_{T}(sub-leading jet (AK8))","nVtxApu","nVtxBpu"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'
Samples = ['data.root','Gjets.root','ttG.root','Other.root','TTgaSpin32_M800.root', 'TTgaSpin32_M1600.root']
SamplesName = ['Data','#gamma+jets', 'tt#gamma', 'Other prompt #gamma', 'Fake #gamma (ele)', 'Fake #gamma (jet)', 't*t* (M=0.8TeV) #times 0.1', 't*t* (M=1.6TeV) #times 40']
SamplesNameLatex = ['Data','Non-prompt #gamma','Gjets', 'ttG', 't*t* (M=0.8TeV)', 't*t* (M=1.6TeV)']
bins = array( 'd',[0.0,100.0,200.0,300.0,400.0,500.0,700.0, 1000.0] )

channelsFR=["fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsIsoSiSi","fakeAJetsOthers"]
regionsFR=["nAk8G0","nAk81nTtag1", "nAk8G1nTtagG0", "nAk81nTtagOffMt"]
variablesFR=["GammaPt","GammaEta","TsMass1"]

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for numcat,namecat in enumerate(categories):
        c0=[]
        for f in range(len(Samples)):
            l1=[]
            Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
            for numch, namech in enumerate(channels):
                l2=[]
                for numreg, namereg in enumerate(regions):
                    l3=[]
                    for numvar, namevar in enumerate(variables):
                        h= Files[f].Get(namecat+ '_' +namech + '_' + namereg + '_' + namevar)
                        if 'jet08Pt' in namevar:
                            h=h.Rebin(len(bins)-1,"",bins)
                        if 'TTga' in Samples[f]:
                           h.Scale(scaleSig[f])
                           h.Scale(scaleSigRegion[numreg])
#                        if 'Gjets' in Samples[f]:
#                           h.Scale(1.84)
                        l3.append(h)
                    l2.append(l3)
                l1.append(l2)
            c0.append(l1)
        l0.append(c0)
    Hists.append(l0)       

HistsFR = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for numcat,namecat in enumerate(categories):
        c0=[]
        for f in range(len(Samples)):
            l1=[]
            Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
            for numch, namech in enumerate(channelsFR):
                l2=[]
                for numreg, namereg in enumerate(regionsFR):
                    l3=[]
                    for numvar, namevar in enumerate(variablesFR):
                        h= Files[f].Get(namecat+ '_' +namech + '_' + namereg + '_' + namevar)
                        if 'jet08Pt' in namevar:
                            h=h.Rebin(len(bins)-1,"",bins)
                        if 'TTga' in Samples[f]:
                           h.Scale(scaleSig[f])
                           h.Scale(scaleSigRegion[numreg])
#                        if 'Gjets' in Samples[f]:
#                           h.Scale(1.84)
                        l3.append(h)
                    l2.append(l3)
                l1.append(l2)
            c0.append(l1)
        l0.append(c0)
    HistsFR.append(l0)

##
##Fakedata1jet = Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81")][variables.index("jet08Pt")].Clone()
##Fakedata1jet.Add(Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81")][variables.index("jet08Pt")])
##Fakedata1jet.Add(Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81")][variables.index("jet08Pt")])
##Fakedata1jet1tag = Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
##Fakedata1jet1tag.Add(Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Fakedata1jet1tag.Add(Hists[0][0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Top1jet1tag =Hists[0][1][Samples.index("Other.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
##Top1jet1tag.Add(Hists[0][1][Samples.index("Other.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Top1jet1tag.Add(Hists[0][1][Samples.index("Other.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Top1jet1tag.Add(Hists[0][0][Samples.index("ttG.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Top1jet1tag.Add(Hists[0][0][Samples.index("ttG.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Top1jet1tag.Add(Hists[0][0][Samples.index("ttG.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
##Fakedata1jet1tag.Add(Top1jet1tag,-1)
##Fakedata1jet1tag.Divide(Fakedata1jet)
##draw1dHist(  Fakedata1jet1tag, 'topMistagRatePNFake','topMistagRatePNFake','topMistagRatePNFake' )
##Fakedata1jet1tag.SetName('topMistagRateFake')
##compareNeffHist([data1jet1tag, Fakedata1jet1tag], ['Gamma+1jet', 'FakeG+jet'], label_name="jet08Pt", can_name="MTRatePN")
##
##hfile = ROOT.TFile( 'topMistagRate.root', 'RECREATE', 'mis top tag rate histogram' )
##data1jet1tag.Write()
##Fakedata1jet1tag.Write()
##hfile.Write()
##hfile.Close()

#draw MC predicted 
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'TTga' in Samples[f]:
                        HHsignal.append(Hists[numyear][0][f][numch][numreg][numvar])
                    elif 'Other' in Samples[f]:
                        HH.append(Hists[numyear][0][f][numch][numreg][numvar])
                        HH.append(Hists[numyear][1][f][numch][numreg][numvar])
                        HH.append(Hists[numyear][2][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][0][f][numch][numreg][numvar])

                stackPlots(HH, HHsignal, SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar],"MC"+nameyear)
    os.system('tar -cvf MC'+nameyear+'.tar ' + "MC"+nameyear)

for numch, namech in enumerate(channels):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variables):
            HH=[]
            HHsignal=[]
            for f in range(len(Samples)):
                h0=Hists[0][0][f][numch][numreg][numvar].Clone()
                h1=Hists[0][1][f][numch][numreg][numvar].Clone()
                h2=Hists[0][2][f][numch][numreg][numvar].Clone()
                for y in range(1,len(year)):
                    h0.Add(Hists[y][0][f][numch][numreg][numvar])
                    h1.Add(Hists[y][1][f][numch][numreg][numvar])
                    h2.Add(Hists[y][2][f][numch][numreg][numvar])
                if 'TTga' in Samples[f]:
                    HHsignal.append(h0)
                elif 'Other' in Samples[f]:
                    HH.append(h0)
                    HH.append(h1)
                    HH.append(h2)
                else:
                    HH.append(h0)

            stackPlots(HH, HHsignal, SamplesName, namech, namereg, "All",namevar,variablesName[numvar],"MCAll")
os.system('tar -cvf MCAll.tar ' + "MCAll")
#for numvar, namevar in enumerate(variables):
#    data1nAK4jet = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81")][variables.index(namevar)].Clone()
#    data1nAK4jet1tag = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index(namevar)].Clone()
#    Top1nAK4jet1tag = Hists[0][Samples.index("ttG.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index(namevar)].Clone()
#    data1nAK4jet1tag.Add(Top1nAK4jet1tag,-1)
#    data1nAK4jet1tag.Divide(data1nAK4jet)
#    draw1dHist(  data1nAK4jet1tag, 'topMistagRate' + namevar,'topMistagRatenAK4'+ namevar,'topMistagRatenAK4'+ namevar )

#Data Driven Gamma Jet
###for numvar, namevar in enumerate(variables):
for numyear, nameyear in enumerate(year):
    for numvar, namevar in enumerate(variables):
        Hists[numyear][0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar] = Hists[numyear][0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar]
        Hists[numyear][0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar] = Hists[numyear][0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtag0XtopMissTagRate")][numvar]
        Hists[numyear][0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk81nTtagOffMt")][numvar] = Hists[numyear][0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtagOffMtXtopMissTagRate")][numvar]    
    ####Data Driven Fake photon
        if namevar in variablesFR:
            for numreg, namereg in enumerate(regionsFR):
                HistsFR[numyear][0][0][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][0][1][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][0][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][0][2][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][0][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][0][3][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][Samples.index("Gjets.root")][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][Samples.index("Gjets.root")][1][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][Samples.index("Gjets.root")][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][Samples.index("Gjets.root")][2][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][Samples.index("Gjets.root")][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][Samples.index("Gjets.root")][3][numreg][variablesFR.index(namevar)])
                HistsFR[numyear][0][0][0][numreg][variablesFR.index(namevar)].Add(HistsFR[numyear][0][Samples.index("Gjets.root")][0][numreg][variablesFR.index(namevar)],-1)
#        hDataCR1 = Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1nTtagG0")][numvar].Clone()
#        hDataCR1.Add(Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1nTtagG0")][numvar])
#        hDataCR1.Add(Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1nTtagG0")][numvar])
#        hDataCR1.Scale(0.022/(1-0.022))
#        hGjetsCR1 = Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1nTtagG0")][numvar].Clone()
#        hGjetsCR1.Add(Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1nTtagG0")][numvar])
#        hGjetsCR1.Add(Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1nTtagG0")][numvar])
#        hGjetsCR1.Scale(0.022/(1-0.022))
#        hDataCR1.Add(hGjetsCR1,-1)
#        Hists[numyear][2][Samples.index("Other.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar] = hDataCR1
#    
#        hDataCR3 = Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][numvar].Clone()
#        hDataCR3.Add(Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][numvar])
#        hDataCR3.Add(Hists[numyear][0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][numvar])
#        hDataCR3.Scale(0.022/(1-0.022))
#        hGjetsCR3 = Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][numvar].Clone()
#        hGjetsCR3.Add(Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][numvar])
#        hGjetsCR3.Add(Hists[numyear][0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][numvar])
#        hGjetsCR3.Scale(0.022/(1-0.022))
#        hDataCR3.Add(hGjetsCR3,-1)
#        Hists[numyear][2][Samples.index("Other.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar] = hDataCR3

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'TTga' in Samples[f]:
                        HHsignal.append(Hists[numyear][0][f][numch][numreg][numvar])
                    elif 'Other' in Samples[f]:
                        HH.append(Hists[numyear][0][f][numch][numreg][numvar])
                        HH.append(Hists[numyear][1][f][numch][numreg][numvar])
                        if namevar in variablesFR and namereg in regionsFR:
                            HH.append(HistsFR[numyear][0][0][numch][regionsFR.index(namereg)][variablesFR.index(namevar)])
                        else:
                            HH.append(Hists[numyear][2][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][0][f][numch][numreg][numvar])

                stackPlots(HH, HHsignal, SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar],"DD"+nameyear)
    os.system('tar -cvf DD'+nameyear+'.tar ' + "DD"+nameyear)

for numch, namech in enumerate(channels):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variables):
            HH=[]
            HHsignal=[]
            for f in range(len(Samples)):
                for y in range(1,len(year)):
                    Hists[0][0][f][numch][numreg][numvar].Add(Hists[y][0][f][numch][numreg][numvar])
                    Hists[0][1][f][numch][numreg][numvar].Add(Hists[y][1][f][numch][numreg][numvar])
                    Hists[0][2][f][numch][numreg][numvar].Add(Hists[y][2][f][numch][numreg][numvar])
                    if namevar in variablesFR and namereg in regionsFR:
                        print namereg + namevar
                        HistsFR[0][0][0][numch][regionsFR.index(namereg)][variablesFR.index(namevar)].Add(HistsFR[y][0][0][numch][regionsFR.index(namereg)][variablesFR.index(namevar)])
                if 'TTga' in Samples[f]:
                    HHsignal.append(Hists[0][0][f][numch][numreg][numvar])
                elif 'Other' in Samples[f]:
                    HH.append(Hists[0][0][f][numch][numreg][numvar])
                    HH.append(Hists[0][1][f][numch][numreg][numvar])
                    if namevar in variablesFR and namereg in regionsFR:
                        HH.append(HistsFR[0][0][0][numch][regionsFR.index(namereg)][variablesFR.index(namevar)])
                    else:
                        HH.append(Hists[0][2][f][numch][numreg][numvar])
                else:
                    HH.append(Hists[0][0][f][numch][numreg][numvar])

            stackPlots(HH, HHsignal, SamplesName, namech, namereg, "All",namevar,variablesName[numvar],"DDAll")
os.system('tar -cvf DDAll.tar ' + "DDAll")

le = '\\documentclass{article}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

print le
#for numyear, nameyear in enumerate(year):
#    for numch, namech in enumerate(channels):
#        cutFlowTable(Hists, SamplesNameLatex, regions, numch, numyear, nameyear + ' ' + namech, 6 )
print '\\end{document}' + "\n"


