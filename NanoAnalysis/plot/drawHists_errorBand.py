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
from operator import truediv
import copy
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



def draw(hists, sys, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()
    hists.Draw()
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/'+ sys +var + ".png")
#    del legend
#    del mg
    del canvas
    gc.collect()

def compareError(histsup,histsdown, sys, ch = "channel", reg = "region", year='2016', var="sample", varname="v", prefix = 'Theory'):
    if not os.path.exists('sys/'+year):
       os.makedirs('sys/'+ year)
    if not os.path.exists('sys/'+year + '/' + ch):
       os.makedirs('sys/'+year + '/' + ch)
    if not os.path.exists('sys/'+year + '/' + ch +'/'+reg):
       os.makedirs('sys/'+year + '/' + ch +'/'+reg)

    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()

    legend = ROOT.TLegend(0.35,0.7,0.9,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetNColumns(3);
    if len(histsup)>15:
        legend.SetTextSize(0.02)

    pad2=ROOT.TPad("pad2", "pad2", 0.0, 0.0, 1, 1 , 0)#used for the ratio plot
    pad2.Draw()
#    pad2.SetGridy()
#    pad2.SetGridx()
    pad2.SetTickx()
    pad2.SetBottomMargin(0.1)
    pad2.SetLeftMargin(0.11)
    pad2.SetRightMargin(0.1)
    pad2.SetFillStyle(0)
    pad2.SetLogx(ROOT.kFALSE)
    pad2.cd()
    maxi=0
    for n,G in enumerate(histsup):
        histsup[n].SetLineColor(n+1)
        histsup[n].SetLineWidth(2)
        histsup[n].SetFillColor(0)
        legend.AddEntry(histsup[n],sys[n],'L')
        if(histsup[n].GetMaximum()>maxi):
            maxi=G.GetMaximum()
        histsdown[n].SetLineColor(n+1)
        histsdown[n].SetFillColor(0)
        histsdown[n].SetLineWidth(2)
        if n==4:
            histsup[n].SetLineColor(ROOT.kOrange)
            histsdown[n].SetLineColor(ROOT.kOrange)
        if n==7:
            histsup[n].SetLineColor(ROOT.kGreen-1)
            histsdown[n].SetLineColor(ROOT.kGreen-1)
        if n==8:
            histsup[n].SetLineColor(28)
            histsdown[n].SetLineColor(28)
        if n==9:
            histsup[n].SetLineColor(46)
            histsdown[n].SetLineColor(46)
        if n==10:
            histsup[n].SetLineColor(30)
            histsdown[n].SetLineColor(30)
        if n==11:
            histsup[n].SetLineColor(38)
            histsdown[n].SetLineColor(38)
        if n==12:
            histsup[n].SetLineColor(17)
            histsdown[n].SetLineColor(17)
        if 'BDT' in varname:
            histsup[n].GetXaxis().SetRangeUser(-0.6, 0.4)
            histsdown[n].GetXaxis().SetRangeUser(-0.6, 0.4)
    histsup[0].SetTitle( '' )
    histsup[0].GetYaxis().SetTitle( 'Uncertainty (%)' )
    histsup[0].GetXaxis().SetTitle(varname)
    histsup[0].GetXaxis().SetLabelSize(0.04)
    histsup[0].GetYaxis().SetLabelSize(0.03)
    histsup[0].GetXaxis().SetTitleSize(0.04)
    histsup[0].GetYaxis().SetTitleSize(0.04)
    histsup[0].GetXaxis().SetTitleOffset(0.95)
    histsup[0].GetYaxis().SetTitleOffset(1)
    histsup[0].GetYaxis().SetNdivisions(804)
    histsup[0].GetXaxis().SetNdivisions(808)
    histsup[0].GetYaxis().SetRangeUser(-20,30)
    histsup[0].Draw('hist')
    for n,G in enumerate(histsup):
        histsup[n].Draw('samehist')
        histsdown[n].Draw('samehist')
    histsup[0].Draw('samehist')
    histsdown[0].Draw('samehist')
    histsup[0].Draw("AXISSAMEY+")
    histsup[0].Draw("AXISSAMEX+")
    Lumi = '137.19'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.74'
    label_cms="CMS Simulation Preliminary"
    Label_cms = ROOT.TLatex(0.22,0.92,label_cms)
    Label_cms.SetTextSize(0.035)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.65,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetTextSize(0.035)
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.15,0.2,year)
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")

    Label_channel2 = ROOT.TLatex(0.15,0.15,ch+" ("+reg+")")
    Label_channel2.SetNDC()
    Label_channel2.SetTextFont(42)
    Label_channel2.Draw("same")

    legend.Draw("same")
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/sys'+ prefix +'_'+var + ".png")
#    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/sys'+ prefix +'_'+var + ".pdf")
    del canvas
    gc.collect()


def stackPlotsError(hists, SignalHists,error, errorRatio, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    if not os.path.exists('sys/'+year):
       os.makedirs('sys/'+ year)
    if not os.path.exists('sys/'+year + '/' + ch):
       os.makedirs('sys/'+year + '/' + ch)
    if not os.path.exists('sys/'+year + '/' + ch +'/'+reg):
       os.makedirs('sys/'+year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
#    for num in range(len(hists)):
#        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
#    for num in range(len(SignalHists)):
#        SignalHists[num].SetBinContent(SignalHists[num].GetXaxis().GetNbins(),SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()) + SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()+1))
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
    legend.SetTextSize(0.03)

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
    pad1.SetLogy(ROOT.kFALSE)

    y_min=0
    y_max=1.7*dummy.GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetTitle("")
    dummy.GetYaxis().SetTitle('Events')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetYaxis().SetTitleOffset(0.8)
    dummy.GetYaxis().SetTitleSize(0.07)
    dummy.GetYaxis().SetLabelSize(0.04)
    dummy.GetYaxis().SetRangeUser(y_min,y_max)
    dummy.Draw("ex0")
    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
    dummy.Draw("ex0SAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    error.SetFillColor(13)
    error.SetLineColor(13)
    error.SetFillStyle(3004)
    error.Draw("2")

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
    legend.AddEntry(error,'Stat. #oplus syst. ','F')
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
    dummy_ratio.GetYaxis().SetRangeUser(0.8,1.2)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw('ex0')
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3004)
    errorRatio.Draw("2")
    dummy_ratio.Draw('ex0same')
    canvas.Print('sys/'+ year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


year=['2017']
LumiErr = [0.025]
channels=["aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"]
channels=["aJets"]
regions=["nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1TtagG0MTs2G300", "nAk8G1nTtag0","nAk8G1nTtag0MTs2G300"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","jet04Phi","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met","nVtx", "nPh", "phoChargedIso", "dPhiGj08", "drGj08", "HT", "HoE", "softdropMass", "tau21", "tau31", "nbjet08","TvsQCD","njet08massG50","njet08massG120","TsMass1", "nTopTag","masstS2", "Sietaieta"]
variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","#Phi(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of vertices","Number of photons","phoChargedIso","#DeltaPhi(#gamma,jet08)", "#DeltaR(#gamma,jet08)", "HT", "H/E", "softdropMass (leading jet (AK8))", "tau21 (leading jet (AK8))", "tau32 (leading jet (AK8))", "num of AK8 jet b-tagged","TvsQCD (leading jet (AK8))", "Number of Ak8 jets with mass > 50","Number of Ak8 jets with mass > 120", "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}"]


HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

sys = ["phIDSf", "pu", "prefiring", "trigSF"]
sysJec= ["Total", "AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]

Samples = ['data.root','Fake.root', 'Gjets.root','ttG.root','other.root', 'TTga_M0800.root', 'TTga_M1600.root']
SamplesName = ['Data','Fake','#gamma+jets', 'ttG', 'other', 't*t* (M=0.8TeV) #times 0.5', 't*t* (M=1.6TeV) #times 10']
SamplesNameLatex = ['Data','Fake','Gjets', 'ttG', 'other', 't*t* (M=0.8TeV)', 't*t* (M=1.6TeV)']
colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue-3,ROOT.kOrange-3, ROOT.kBlack, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]
NormalizationErr = [0, 0.1, 0.1, 0.15, 0.05, 0.1, 0,0]


Hists = []
HistsSysUp = []
HistsSysDown = []
HistsJecUp = []
HistsJecDown = []
Hists_copy =[]
for numyear, nameyear in enumerate(year):
    l0=[]
    copyl0=[]
    SysUpl0=[]
    SysDownl0=[]
    JecUpl0=[]
    JecDownl0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        copyl1=[]
        SysUpl1=[]
        SysDownl1=[]
        JecUpl1=[]
        JecDownl1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            copyl2=[]
            SysUpl2=[]
            SysDownl2=[]
            JecUpl2=[]
            JecDownl2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                copyl3=[]
                SysUpl3=[]
                SysDownl3=[]
                JecUpl3=[]
                JecDownl3=[]
                for numvar, namevar in enumerate(variables):
                    SysUpl4=[]
                    SysDownl4=[]
                    JecUpl4=[]
                    JecDownl4=[]
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                    l3.append(h)
                    copyl3.append(h.Clone())
                    if namech=='aJets':
                        for numsys, namesys in enumerate(sys):
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            SysUpl4.append(h)
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            SysDownl4.append(h)
                        for numsys, namesys in enumerate(sysJec):
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            JecUpl4.append(h)
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            JecDownl4.append(h)
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                    JecUpl3.append(JecUpl4)
                    JecDownl3.append(JecDownl4)
                l2.append(l3)
                copyl2.append(copyl3)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
                JecUpl2.append(JecUpl3)
                JecDownl2.append(JecDownl3)
            l1.append(l2)
            copyl1.append(copyl2)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
            JecUpl1.append(JecUpl2)
            JecDownl1.append(JecDownl2)
        l0.append(l1)
        copyl0.append(copyl1)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
        JecUpl0.append(JecUpl1)
        JecDownl0.append(JecDownl1)
    Hists.append(l0)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)       
    HistsSysDown.append(SysDownl0)
    HistsJecUp.append(JecUpl0)
    HistsJecDown.append(JecDownl0)

tgraph_nominal = []
tgraph_ratio = []
errup = 0
errdown =0
for numyear, nameyear in enumerate(year):
    t1nominal = []
    t1ratio = []
    for numch, namech in enumerate(channels): 
        t2nominal = []
        t2ratio = []
        for numreg, namereg in enumerate(regions):
            t3nominal = []
            t3ratio = []
            for numvar, namevar in enumerate(variables):
                for f in range(1,len(Samples)-3):
                    Hists_copy[numyear][f+1][numch][numreg][numvar].Add(Hists_copy[numyear][f][numch][numreg][numvar])
                if namech=='aJets':
                    for numsys, namesys in enumerate(sys):
                        for f in range(1,len(Samples)-3):
                            HistsSysUp[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsSysUp[numyear][f][numch][numreg][numvar][numsys]) 
                            HistsSysDown[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsSysDown[numyear][f][numch][numreg][numvar][numsys])
                    for numsys, namesys in enumerate(sysJec):
                        for f in range(1,len(Samples)-3):
                            HistsJecUp[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsJecUp[numyear][f][numch][numreg][numvar][numsys])
                            HistsJecDown[numyear][f+1][numch][numreg][numvar][numsys].Add(HistsJecDown[numyear][f][numch][numreg][numvar][numsys])
                binwidth= array( 'd' )
                bincenter= array( 'd' )
                yvalue= array( 'd' )
                yerrup= array( 'd' )
                yerrdown= array( 'd' )
                yvalueRatio= array( 'd' )
                yerrupRatio= array( 'd' )
                yerrdownRatio= array( 'd' )
                content=0
                for b in range(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetNbinsX()):
                    errup = 0
                    errdown =0
                    binwidth.append(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinWidth(b+1)/2)
                    bincenter.append(Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinCenter(b+1))
                    if Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)>0:
                        content = Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)
                    else:
                        content =0.0000001
                    yvalue.append(content)
                    yvalueRatio.append(content/content)
                    if namech=='aJets':
                        for numsys2, namesys2 in enumerate(sys):
                            if HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].Integral()==0 or Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)<=0:
                                continue
                            if HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                                errup = errup + (HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            else:
                                errdown = errdown + (HistsSysUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            if HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                                errup = errup + (HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            else:
                                errdown = errdown + (HistsSysDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2

                        for numsys2, namesys2 in enumerate(sysJec):
                            if HistsJecUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].Integral()==0 or Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)<=0:
                                continue
                            if HistsJecUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                                errup = errup + (HistsJecUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            else:
                                errdown = errdown + (HistsJecUp[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            if HistsJecDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1)  > 0:
                                errup = errup + (HistsJecDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                            else:
                                errdown = errdown + (HistsJecDown[numyear][len(Samples)-3][numch][numreg][numvar][numsys2].GetBinContent(b+1) - Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2

                    errup = errup + Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinError(b+1)**2
                    errdown = errdown + Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinError(b+1)**2
#Add lumi error
                    errup = errup + (LumiErr[numyear]*Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
                    errdown = errdown + (LumiErr[numyear]*Hists_copy[numyear][len(Samples)-3][numch][numreg][numvar].GetBinContent(b+1))**2
#add normalization error only for ttbar reegions 
                    
                    for f in range(len(Samples)):
                        errup = errup + (NormalizationErr[f]*Hists[numyear][f][numch][numreg][numvar].GetBinContent(b+1))**2                    
                        errdown = errdown + (NormalizationErr[f]*Hists[numyear][f][numch][numreg][numvar].GetBinContent(b+1))**2
#add ttbar theory errors
#                    if numch==1 and numreg>1:
#                        errup = errup + (pdfGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (qscaleGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (ISRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (FSRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (CRGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (TuneGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errup = errup + (hdampGraph[numyear][numreg-2][numvar].GetErrorYhigh(b))**2
#                        errdown = errdown + (pdfGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (qscaleGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (ISRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (FSRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (CRGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (TuneGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        errdown = errdown + (hdampGraph[numyear][numreg-2][numvar].GetErrorYlow(b))**2
#                        print str(pdfGraph[numyear][numreg-1][numvar].GetErrorYlow(b)) + '    '+str(pdfGraph[numyear][numreg-1][numvar].GetErrorYlow(b))
                    yerrup.append(math.sqrt(errup))
                    yerrdown.append(math.sqrt(errdown))
                    yerrupRatio.append(math.sqrt(errup)/content)
                    yerrdownRatio.append(math.sqrt(errdown)/content)
                t3nominal.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrup,yerrdown))
                t3ratio.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalueRatio,binwidth,binwidth,yerrupRatio,yerrdownRatio))
            t2nominal.append(t3nominal)
            t2ratio.append(t3ratio)
        t1nominal.append(t2nominal)
        t1ratio.append(t2ratio)
    tgraph_nominal.append(t1nominal)
    tgraph_ratio.append(t1ratio)


for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                for f in range(len(Samples)):
                    if 'TTga' in Samples[f]:
                        HHsignal.append(Hists[numyear][f][numch][numreg][numvar])
                    else:
                        HH.append(Hists[numyear][f][numch][numreg][numvar])
#                stackPlotsError(HH, HHsignal,tgraph_nominal[numyear][numch][numreg][numvar], tgraph_ratio[numyear][numch][numreg][numvar],SamplesName, namech, namereg, nameyear,namevar,variablesName[numvar])

WS=5
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if namech!='aJets':
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                glistup = []
                glistdown = []
                for numsys2, namesys2 in enumerate(sys):
                    hup = HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                    hdown = HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                    if hup.Integral()>0 or hdown.Integral()>0:
                        for b in range(hup.GetNbinsX()):
                            cv = Hists_copy[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)
                            rb = 0
                            if cv>0:
                                rb = 100/cv
                            hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                            hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                compareError(glistup,glistdown, sys, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpWeight')

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if namech!='aJets':
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                glistup = []
                glistdown = []
                for numsys2, namesys2 in enumerate(sysJec):
                    hup = HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                    hdown = HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                    if hup.Integral()>0 or hdown.Integral()>0:
                        for b in range(hup.GetNbinsX()):
                            cv = Hists_copy[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)
                            rb = 0
                            if cv>0:
                                rb = 100/cv
                            hup.SetBinContent(b+1, 0 + abs(max((HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                            hdown.SetBinContent(b+1, 0 - abs(min((HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                compareError(glistup,glistdown, sysJec, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpJec')
