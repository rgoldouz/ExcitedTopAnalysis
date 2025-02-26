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
from ROOT import TFile
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
import gc
from operator import truediv
import copy
TGaxis.SetMaxDigits(2)
from math import sqrt

def MyRebin(h,b):
    h=h.Rebin(len(b)-1,"",b)
    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
    h.SetBinError(h.GetXaxis().GetNbins(), sqrt((h.GetBinError(h.GetXaxis().GetNbins()))**2 + (h.GetBinError(h.GetXaxis().GetNbins()+1))**2))
    h.SetBinContent(h.GetXaxis().GetNbins()+1,0)
    h.SetBinError(h.GetXaxis().GetNbins()+1,0)
    return h

def SumofWeight(addlist,sname='tt'):
#    print addlist[0]+':'+sname
    genEventSumw = 0
    genEventSumwScale = [0]*9
    genEventSumwPdf = [0]*100
    for add in addlist:
        for root, dirs, files in os.walk(add):
            if sname not in root:
                continue
            if len(files) == 0:
                continue
#            print root
            for f in files:
                filename = root + '/' + f
                if 'fail' in f:
                    continue
                fi = TFile.Open(filename)
                tree_meta = fi.Get('Runs')
                for i in range( tree_meta.GetEntries() ):
                    tree_meta.GetEntry(i)
                    genEventSumw += tree_meta.genEventSumw
                    for pdf in range(100):
                        genEventSumwPdf[pdf] += tree_meta.LHEPdfSumw[pdf]*tree_meta.genEventSumw
                    for Q in range(len(tree_meta.LHEScaleSumw)):
                        genEventSumwScale[Q] += tree_meta.LHEScaleSumw[Q]*tree_meta.genEventSumw
                tree_meta.Reset()
                tree_meta.Delete()
                fi.Close()
    if genEventSumwScale[8]==0:
        del genEventSumwScale[8]
    return [genEventSumw/x for x in genEventSumwScale] , [genEventSumw/x for x in genEventSumwPdf]


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
#    print table



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

def compareError(histsup,histsdown, sys, ch = "channel", reg = "region", year='2016', var="sample", varname="v", prefix = 'Theory',titre=''):
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
            histsup[n].SetLineColor(ROOT.kYellow+1)
            histsdown[n].SetLineColor(ROOT.kYellow+1)
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
        if (n % 2) != 0:
            histsup[n].SetLineStyle(7)
            histsdown[n].SetLineStyle(7)
        histsup[n].Draw('samehist')
        histsdown[n].Draw('samehist')
    histsup[0].Draw('samehist')
    histsdown[0].Draw('samehist')
    histsup[0].Draw("AXISSAMEY+")
    histsup[0].Draw("AXISSAMEX+")
    Lumi = '138'
    if (year == '2016preVFP'):
        Lumi = '19.52'
    if (year == '2016postVFP'):
        Lumi = '16.81'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'

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
    Label_channel = ROOT.TLatex(0.15,0.2,year+' - ' + titre)
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
year=['2016preVFP', '2016postVFP', '2017','2018']
#year=['2018']
LumiErr = [0.025]
categories=["promptG", "fakeGEle","fakeGJet"]
channels=["aJets"]
regions=["nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0",  "nAk8G1nTtag0", "nAk8G1nTtag0XtopMissTagRate",  "nAk81nTtag0XtopMissTagRate","nAk8G1nTtagG0LepG0", "nAk81nTtagOffMt","nAk81nTtagOffMtXtopMissTagRate"]

regionsSys=["nAk81nTtag1", "nAk8G1nTtagG0", "nAk81nTtagOffMt"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met", "nPh", "phoChargedIso",  "HT", "HoE", "softdropMass", "TvsQCD","TsMass1", "nTopTag","masstS2", "Sietaieta","MtGMet","subLeadingjet08Pt"]
variables=["TsMass1"]
variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of photons","phoChargedIso", "HT", "H/E", "softdropMass (leading jet (AK8))","TvsQCD (leading jet (AK8))",  "M(#gamma, top-jet candidate with lowest mass)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}", "M_{T}(#gamma,MET)", "p_{T}(sub-leading jet (AK8))"]
variablesName=["M(#gamma, Subleading mass top-tagged AK8 jet)"]
HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

sys = ["phIDSf", "pu", "prefiring","photonEScale","photonESmear", "JesTotal", "topTagSF","phPixelVetoSf", "SDmassSF", "JerTotal"]
sysJet=["JesTotal", "topTagSF","SDmassSF", "JerTotal"]
sysJec= ["Total","AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","SinglePionECAL","SinglePionHCAL","TimePtEta"]

Samples = ['data.root','Gjets.root','ttG.root','Other.root','TTgaSpin32_M800.root', 'TTgaSpin32_M1200.root']
#Samples = ['data.root','Gjets.root','ttG.root','Other.root','TTgaSpin32_M2750.root', 'TTgaSpin32_M3000.root']
SamplesName = ['Data','#gamma+jets', 'tt#gamma', 'Other prompt #gamma', 'Fake #gamma (ele)', 'Fake #gamma (jet)', 't*t* (M=0.8TeV) #times 0.1', 't*t* (M=1.2TeV) #times 40']
colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue-3,ROOT.kOrange-3, ROOT.kBlack, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]
NormalizationErr = [0, 0.1, 0.1, 0.15, 0.05, 0.1, 0,0]
#bins = array( 'd',[300,500,700,900,1100,1300,1500,1750,2000,2500,3000] )
bins = array( 'd',[300,500,700,900,1100,1300,1500,1750,2000,3000] )

Hists = []
Hists_copy = []

#Get the nominal Histograms
for numyear, nameyear in enumerate(year):
    l0=[]
    l0C=[]
    Files = []
    for numcat,namecat in enumerate(categories):
        c0=[]
        c0C=[]
        for f in range(len(Samples)):
            l1=[]
            l1C=[]
            Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
            for numch, namech in enumerate(channels):
                l2=[]
                l2C=[]
                for numreg, namereg in enumerate(regions):
                    l3=[]
                    l3C=[]
                    for numvar, namevar in enumerate(variables):
#                        print namecat+ '_' +namech + '_' + namereg + '_' + namevar
                        h= Files[f].Get(namecat+ '_' +namech + '_' + namereg + '_' + namevar)
                        if namevar=='TsMass1':
                            h=h.Rebin(len(bins)-1,"",bins)
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        h.SetBinError(h.GetXaxis().GetNbins(), sqrt((h.GetBinError(h.GetXaxis().GetNbins()))**2 + (h.GetBinError(h.GetXaxis().GetNbins()+1))**2))
                        h.SetBinContent(h.GetXaxis().GetNbins()+1,0)
                        h.SetBinError(h.GetXaxis().GetNbins()+1,0)
                        l3.append(h)
                        l3C.append(h.Clone())
                    l2.append(l3)
                    l2C.append(l3C)
                l1.append(l2)
                l1C.append(l2C)
            c0.append(l1)
            c0C.append(l1C)
        l0.append(c0)
        l0C.append(c0C)
    Hists.append(l0)
    Hists_copy.append(l0C)

# Get the Pdf, Qscale and PS Histograms
HistsPdfUp=[]
HistsQscaleUp=[]
HistsPdfDown=[]
HistsQscaleDown=[]
HistsIsrUp=[]
HistsIsrDown=[]
HistsFsrUp=[]
HistsFsrDown=[]

for numyear, nameyear in enumerate(year):
    t0PdfUp=[]
    t0QscaleUp=[]
    t0PdfDown=[]
    t0QscaleDown=[]
    t0IsrUp=[]
    t0FsrUp=[]
    t0IsrDown=[]
    t0FsrDown=[]
    for numcat,namecat in enumerate(categories):
        if namecat!='promptG':
            continue
        tCPdfUp=[]
        tCQscaleUp=[]
        tCPdfDown=[]
        tCQscaleDown=[]
        tCIsrUp=[]
        tCFsrUp=[]
        tCIsrDown=[]
        tCFsrDown=[]
        Files = []
        for f in range(len(Samples)):
            Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
            t1PdfUp=[]
            t1QscaleUp=[]
            t1PdfDown=[]
            t1QscaleDown=[]
            t1IsrUp=[]
            t1FsrUp=[]
            t1IsrDown=[]
            t1FsrDown=[]
            if 'TTga' in Samples[f]:
                SWscale, SWpdf =  SumofWeight(['/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL' + nameyear[2:]+ '/v1'],Samples[f].split(".")[0] )
            if 'ttG' in Samples[f]:
                SWscale, SWpdf =  SumofWeight(['/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL' + nameyear[2:]+ '/v1'],"TTGamma" ) 
            for numch, namech in enumerate(channels):
                t2PdfUp=[]
                t2QscaleUp=[]
                t2PdfDown=[]
                t2QscaleDown=[]
                t2IsrUp=[]
                t2FsrUp=[]
                t2IsrDown=[]
                t2FsrDown=[]
                for numreg, namereg in enumerate(regionsSys):
                    t3PdfUp=[]
                    t3QscaleUp=[]
                    t3PdfDown=[]
                    t3QscaleDown=[]
                    t3IsrUp=[]
                    t3FsrUp=[]
                    t3IsrDown=[]
                    t3FsrDown=[]
                    for numvar, namevar in enumerate(variables):
                        hNom=Hists[numyear][0][f][numch][regions.index(namereg)][numvar].Clone()
                        Pdf_hcUp = hNom.Clone()
                        Pdf_hcDown = hNom.Clone()
                        qs_hcUp = hNom.Clone()
                        qs_hcDown = hNom.Clone()
                        if namevar=='TsMass1' and ('TTga' in Samples[f] or 'ttG' in Samples[f]) :
                            t4Pdf=[]
                            t4Qscale=[]
                            for numsys in range(8):
                                h= Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_Qscale_'+str(numsys))
                                h.SetFillColor(colors[f])
                                h.SetLineColor(colors[f])
                                h=h.Rebin(len(bins)-1,"",bins)
                                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                                h.SetBinError(h.GetXaxis().GetNbins(), sqrt((h.GetBinError(h.GetXaxis().GetNbins()))**2 + (h.GetBinError(h.GetXaxis().GetNbins()+1))**2))
                                h.SetBinContent(h.GetXaxis().GetNbins()+1,0)
                                h.SetBinError(h.GetXaxis().GetNbins()+1,0)
                                h.Scale(SWscale[numsys])
                                t4Qscale.append(h)
                            for numsys in range(100):
                                h= Files[f].Get('reweightingSys/' + namech +'_' + namereg + '_' + namevar+ '_PDF_'+str(numsys))
                                h.SetFillColor(colors[f])
                                h.SetLineColor(colors[f])
                                h=h.Rebin(len(bins)-1,"",bins)
                                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                                h.SetBinError(h.GetXaxis().GetNbins(), sqrt((h.GetBinError(h.GetXaxis().GetNbins()))**2 + (h.GetBinError(h.GetXaxis().GetNbins()+1))**2))
                                h.SetBinContent(h.GetXaxis().GetNbins()+1,0)
                                h.SetBinError(h.GetXaxis().GetNbins()+1,0)
                                print Samples[f]+'--> npdf:' + str(numsys)+' SW='+ str(SWpdf[numsys])
                                h.Scale(SWpdf[numsys])
                                t4Pdf.append(h)
                            for b in range(Pdf_hcUp.GetNbinsX()):
                                QS=np.zeros(8)
                                PDF=0
                                for numsys in range(8):
                                    if numsys==2 or numsys==6:
                                        QS[numsys] = hNom.GetBinContent(b+1)
                                        continue
                                    QS[numsys] = t4Qscale[numsys].GetBinContent(b+1)
                                qs_hcUp.SetBinContent(b+1,max(QS))
                                qs_hcDown.SetBinContent(b+1,min(QS))
                                for numsys in range(100):
                                    if abs(SWpdf[numsys])>3 or SWpdf[numsys]<0:
                                        continue
                                    PDF = PDF + (t4Pdf[numsys].GetBinContent(b+1) - hNom.GetBinContent(b+1))**2
                                Pdf_hcUp.SetBinContent(b+1,hNom.GetBinContent(b+1)+math.sqrt(PDF))
                                Pdf_hcDown.SetBinContent(b+1,hNom.GetBinContent(b+1)-math.sqrt(PDF))
                        if ('TTga' in Samples[f] or 'ttG' in Samples[f]) :
#                            t3IsrUp.append((Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_0')).Rebin(len(bins)-1,"",bins))
#                            t3FsrUp.append((Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_1')).Rebin(len(bins)-1,"",bins))
#                            t3IsrDown.append((Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_2')).Rebin(len(bins)-1,"",bins))
#                            t3FsrDown.append((Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_3')).Rebin(len(bins)-1,"",bins))
                            t3IsrUp.append(MyRebin(Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_0'),bins))
                            t3FsrUp.append(MyRebin(Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_1'),bins))
                            t3IsrDown.append(MyRebin(Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_2'),bins))
                            t3FsrDown.append(MyRebin(Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_3'),bins))

                        else:
                            t3IsrUp.append(hNom)
                            t3FsrUp.append(hNom)
                            t3IsrDown.append(hNom)
                            t3FsrDown.append(hNom)
                        t3QscaleUp.append(qs_hcUp)
                        t3QscaleDown.append(qs_hcDown)
                        t3PdfUp.append(Pdf_hcUp)
                        t3PdfDown.append(Pdf_hcDown)
                    t2PdfUp.append(t3PdfUp)
                    t2PdfDown.append(t3PdfDown)
                    t2QscaleUp.append(t3QscaleUp)
                    t2QscaleDown.append(t3QscaleDown)
                    t2IsrUp.append(t3IsrUp)
                    t2IsrDown.append(t3IsrDown)
                    t2FsrUp.append(t3FsrUp)
                    t2FsrDown.append(t3FsrDown)
                t1PdfUp.append(t2PdfUp)
                t1PdfDown.append(t2PdfDown)
                t1QscaleUp.append(t2QscaleUp)
                t1QscaleDown.append(t2QscaleDown)
                t1IsrUp.append(t2IsrUp)
                t1IsrDown.append(t2IsrDown)
                t1FsrUp.append(t2FsrUp)
                t1FsrDown.append(t2FsrDown)
            tCPdfUp.append(t1PdfUp)
            tCPdfDown.append(t1PdfDown)
            tCQscaleUp.append(t1QscaleUp)
            tCQscaleDown.append(t1QscaleDown)
            tCIsrUp.append(t1IsrUp)
            tCIsrDown.append(t1IsrDown)
            tCFsrUp.append(t1FsrUp)
            tCFsrDown.append(t1FsrDown)
        t0PdfUp.append(tCPdfUp)
        t0PdfDown.append(tCPdfDown)
        t0QscaleUp.append(tCQscaleUp)
        t0QscaleDown.append(tCQscaleDown)
        t0IsrUp.append(tCIsrUp)
        t0IsrDown.append(tCIsrDown)
        t0FsrUp.append(tCFsrUp)
        t0FsrDown.append(tCFsrDown)
    HistsPdfUp.append(t0PdfUp)
    HistsPdfDown.append(t0PdfDown)
    HistsQscaleUp.append(t0QscaleUp)
    HistsQscaleDown.append(t0QscaleDown)
    HistsIsrUp.append(t0IsrUp)
    HistsIsrDown.append(t0IsrDown)
    HistsFsrUp.append(t0FsrUp)
    HistsFsrDown.append(t0FsrDown)


#Get the Up/Down uncertainties
HistsSysUp = []
HistsSysDown = []
HistsJecUp = []
HistsJecDown = []
for numyear, nameyear in enumerate(year):
    SysUpl0=[]
    SysDownl0=[]
    JecUpl0=[]
    JecDownl0=[]
    Files = []
    for f in range(len(Samples)):
        SysUpl1=[]
        SysDownl1=[]
        JecUpl1=[]
        JecDownl1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            SysUpl2=[]
            SysDownl2=[]
            JecUpl2=[]
            JecDownl2=[]
            for numreg, namereg in enumerate(regionsSys):
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
                    if namech=='aJets' and Samples[f]!='data.root':
                        for numsys, namesys in enumerate(sys):
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
#                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            if namevar=='TsMass1':
                                h=MyRebin(h,bins)
                            SysUpl4.append(h)
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
#                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            if namevar=='TsMass1':
                                h=MyRebin(h,bins)
                            SysDownl4.append(h)
                        for numsys, namesys in enumerate(sysJec):
                            if namevar!='TsMass1':
                                continue
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
#                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=MyRebin(h,bins)
                            JecUpl4.append(h)
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
#                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=MyRebin(h,bins)
                            JecDownl4.append(h)
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                    JecUpl3.append(JecUpl4)
                    JecDownl3.append(JecDownl4)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
                JecUpl2.append(JecUpl3)
                JecDownl2.append(JecDownl3)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
            JecUpl1.append(JecUpl2)
            JecDownl1.append(JecDownl2)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
        JecUpl0.append(JecUpl1)
        JecDownl0.append(JecDownl1)
    HistsSysUp.append(SysUpl0)
    HistsSysDown.append(SysDownl0)
    HistsJecUp.append(JecUpl0)
    HistsJecDown.append(JecDownl0)

for WS in range(len(Samples)):
    if 'data' in Samples[WS]:
        continue
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            if namech!='aJets':
                continue
            for numreg, namereg in enumerate(regionsSys):
                for numvar, namevar in enumerate(variables):
                    glistup = []
                    glistdown = []
                    Hnames=[]
                    for numsys2, namesys2 in enumerate(sys):
                        if namesys2 in sysJet:
                            continue                    
                        Hnames.append(sys[numsys2])
                        hup = HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        hdown = HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                    compareError(glistup,glistdown, Hnames, namech, namereg, nameyear,namevar,variablesName[numvar], 'Exp1_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])

for WS in range(len(Samples)):
    if 'data' in Samples[WS]:
        continue
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            if namech!='aJets':
                continue
            for numreg, namereg in enumerate(regionsSys):
                for numvar, namevar in enumerate(variables):
                    glistup = []
                    glistdown = []
                    Hnames=[]
                    for numsys2, namesys2 in enumerate(sys):
                        if namesys2 not in sysJet:
                            continue
                        Hnames.append(sys[numsys2])
                        hup = HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        hdown = HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                    compareError(glistup,glistdown, Hnames, namech, namereg, nameyear,namevar,variablesName[numvar], 'Exp2_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])


for WS in range(len(Samples)):
    if 'data' in Samples[WS]:
        continue
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            if namech!='aJets':
                continue
            for numreg, namereg in enumerate(regionsSys):
                for numvar, namevar in enumerate(variables):
                    glistup = []
                    glistdown = []
                    sysModified=[]
                    if namevar=='TsMass1' and ('TTga' in Samples[WS] or 'ttG' in Samples[WS]):
                        hup = HistsPdfUp[numyear][0][WS][numch][numreg][numvar].Clone()
                        hdown = HistsPdfDown[numyear][0][WS][numch][numreg][numvar].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsPdfUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsPdfDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsPdfUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsPdfDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                        sysModified.append('PDF')
                        hup = HistsQscaleUp[numyear][0][WS][numch][numreg][numvar].Clone()
                        hdown = HistsQscaleDown[numyear][0][WS][numch][numreg][numvar].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsQscaleUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsQscaleDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsQscaleUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsQscaleDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                        sysModified.append('QScale')
                        hup = HistsIsrUp[numyear][0][WS][numch][numreg][numvar].Clone()
                        hdown = HistsIsrDown[numyear][0][WS][numch][numreg][numvar].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsIsrUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsIsrDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsIsrUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsIsrDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                        sysModified.append('ISR')
                        hup = HistsFsrUp[numyear][0][WS][numch][numreg][numvar].Clone()
                        hdown = HistsFsrDown[numyear][0][WS][numch][numreg][numvar].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsFsrUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsFsrDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsFsrUp[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsFsrDown[numyear][0][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                        sysModified.append('FSR')
                    if ('TTga' in Samples[WS] or 'ttG' in Samples[WS]):
                        compareError(glistup,glistdown, sysModified, namech, namereg, nameyear,namevar,variablesName[numvar], 'Theory_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])

for WS in range(len(Samples)):
    if 'data' in Samples[WS]:
        continue
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            if namech!='aJets':
                continue
            for numreg, namereg in enumerate(regionsSys):
                for numvar, namevar in enumerate(variables):
                    if namevar!='TsMass1':
                        continue
                    glistup = []
                    glistdown = []
                    for numsys2, namesys2 in enumerate(sysJec):
                        hup = HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        hdown = HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].Clone()
                        if hup.Integral()>0 or hdown.Integral()>0:
                            for b in range(hup.GetNbinsX()):
                                cv = Hists_copy[numyear][0][WS][numch][regions.index(namereg)][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsJecUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsJecDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                    compareError(glistup,glistdown, sysJec, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpJec_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])

DH2 = ROOT.TFile.Open('/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/topMistagRate2D.root')
h_topMistagRate=DH2.Get('2018_2DMistagRatejetPtvsMass')
NbinsX=h_topMistagRate.GetXaxis().GetNbins();
NbinsY=h_topMistagRate.GetYaxis().GetNbins();
HistsMTUp=[]
HistsMTDown=[]
regionsMT=["nAk8G1nTtag0XtopMissTagRate",  "nAk81nTtag0XtopMissTagRate"]
for numyear, nameyear in enumerate(year):
    l0Up=[]
    l0Down=[]
    F=ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[0])
    for numreg, namereg in enumerate(regionsMT):
        l1Up=[]
        l1Down=[]
        for i in range(NbinsX):
            l2Up=[]
            l2Down=[]
            for j in range(NbinsY):
                l2Up.append((F.Get("topMissTagUnc_"+namereg+"_"+str(i)+"_"+str(j)+"_"+'TsMass1_Up')).Rebin(len(bins)-1,"",bins))
                l2Down.append((F.Get("topMissTagUnc_"+namereg+"_"+str(i)+"_"+str(j)+"_"+'TsMass1_Down')).Rebin(len(bins)-1,"",bins))
            l1Up.append(l2Up)
            l1Down.append(l2Down)
        l0Up.append(l1Up)
        l0Down.append(l1Down)
    HistsMTUp.append(l0Up)
    HistsMTDown.append(l0Down)

for numyear, nameyear in enumerate(year):
    F=ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[0])
    for numreg, namereg in enumerate(regionsMT):
        nominal=(F.Get('promptG_aJets'+ '_' + namereg + '_TsMass1')).Rebin(len(bins)-1,"",bins)
        glistup = []
        glistdown = []
        MTnames=[]
        for i in range(NbinsX):
            for j in range(NbinsY):
                hup = HistsMTUp[numyear][numreg][i][j].Clone()
                hdown = HistsMTDown[numyear][numreg][i][j].Clone()
#                print str(hup.Integral()) +":"+str(hdown.Integral())+":"+str(nominal.Integral())
                if hup.Integral()>0 or hdown.Integral()>0:
                    for b in range(HistsMTUp[numyear][numreg][i][j].GetNbinsX()):
                        cv = nominal.GetBinContent(b+1)
                        rb = 0
                        if cv>0:
                            rb = 100/cv
                        hup.SetBinContent(b+1, 0 + abs(max((HistsMTUp[numyear][numreg][i][j].GetBinContent(b+1)-cv)*rb, (HistsMTDown[numyear][numreg][i][j].GetBinContent(b+1)-cv)*rb,0)))
                        hdown.SetBinContent(b+1, 0 - abs(min((HistsMTUp[numyear][numreg][i][j].GetBinContent(b+1)-cv)*rb, (HistsMTDown[numyear][numreg][i][j].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                    MTnames.append('Bin'+str(i)+str(j))
        compareError(glistup,glistdown, MTnames, 'aJets', namereg, nameyear,'TsMass1',variablesName[numvar], namereg+'_MT_'+'data','data')

os.system('tar -cvf sys.tar sys')
#hfile = ROOT.TFile.Open( HistAddress +'2017_data.root')
#print HistAddress + nameyear+ '_data.root'
#H1=hfile.Get('promptG_aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1')
#H1=H1.Rebin(len(bins)-1,"",bins)
#Hup=hfile.Get('aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1_missTagRate_Up')
#Hup=Hup.Rebin(len(bins)-1,"",bins)
#Hdown=hfile.Get('aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1_missTagRate_Down')
#Hdown=Hdown.Rebin(len(bins)-1,"",bins)
#glistup = []
#glistdown = []
#hup =Hup.Clone()
#hdown =Hdown.Clone()
#for b in range(H1.GetNbinsX()):
#    cv = H1.GetBinContent(b+1)
#    rb = 0
#    if cv>0:
#        rb = 100/cv
#    hup.SetBinContent(b+1, 0 + abs(max((Hup.GetBinContent(b+1)-cv)*rb, (Hdown.GetBinContent(b+1)-cv)*rb,0)))
#    hdown.SetBinContent(b+1, 0 - abs(min((Hup.GetBinContent(b+1)-cv)*rb, (Hdown.GetBinContent(b+1)-cv)*rb,0)))
#glistup.append(hup)
#glistdown.append(hdown)
#compareError(glistup,glistdown, ['missTagRate'], 'aJets', 'aJets', '2017','TsMass1',"M(#gamma, highest mass AK8)", 'ExpGjet','Gjets')
#
