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

def SumofWeight(addlist):
    genEventSumw = 0
    genEventSumwScale = [0]*9
    genEventSumwPdf = [0]*100
    for add in addlist:
        for root, dirs, files in os.walk(add):
            if len(files) == 0:
                continue
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
LumiErr = [0.025]
channels=["aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"]
channels=["aJets"]
regions=["nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1TtagG0MTs2G300", "nAk8G1nTtag0","nAk8G1nTtag0MTs2G300"]
regions=["nAk8G1nTtagG0"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","jet04Phi","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met","nVtx", "nPh", "phoChargedIso", "dPhiGj08", "drGj08", "HT", "HoE", "softdropMass", "tau21", "tau31", "nbjet08","TvsQCD","njet08massG50","njet08massG120","TsMass1", "nTopTag","masstS2", "Sietaieta"]
variables=["TsMass1"]
regions=["nAk8G1nTtagG0"]
variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","#Phi(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of vertices","Number of photons","phoChargedIso","#DeltaPhi(#gamma,jet08)", "#DeltaR(#gamma,jet08)", "HT", "H/E", "softdropMass (leading jet (AK8))", "tau21 (leading jet (AK8))", "tau32 (leading jet (AK8))", "num of AK8 jet b-tagged","TvsQCD (leading jet (AK8))", "Number of Ak8 jets with mass > 50","Number of Ak8 jets with mass > 120", "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}"]
variablesName=["M(#gamma, highest mass AK8)"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

sys = ["phIDSf", "pu", "prefiring","photonEScale","photonESmear", "topTagSF","JesTotal"]
sysJec= ["Total", "AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]

Samples = ['TTga_M1000.root',  'TTga_M1200.root',  'TTga_M1300.root',  'TTga_M1400.root',  'TTga_M1500.root',  'TTga_M1600.root',  'TTga_M700.root',   'TTga_M800.root']
Samples = ['TTga_M1000.root','TTgaSpin32_M1000.root']
SamplesName = ['t*t* (M=1TeV)', 't*t* (M=1.2TeV)', 't*t* (M=1.3TeV)', 't*t* (M=1.4TeV)','t*t* (M=1.5TeV)', 't*t* (M=1.6TeV)','t*t* (M=0.7TeV)', 't*t* (M=0.8TeV)']
SamplesNameLatex = ['t*t* (M=1TeV)', 't*t* (M=1.2TeV)', 't*t* (M=1.3TeV)', 't*t* (M=1.4TeV)','t*t* (M=1.5TeV)', 't*t* (M=1.6TeV)','t*t* (M=0.7TeV)', 't*t* (M=0.8TeV)']
colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue-3,ROOT.kOrange-3, ROOT.kBlack, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]
NormalizationErr = [0, 0.1, 0.1, 0.15, 0.05, 0.1, 0,0]
bins = array( 'd',[300,500,700,900,1100,1300,1500,1750,2000,2500,3000] )

Hists = []
HistsSysUp = []
HistsSysDown = []
HistsJecUp = []
HistsJecDown = []
Hists_copy =[]
HistsPdfUp=[]
HistsQscaleUp=[]
HistsPdfDown=[]
HistsQscaleDown=[]
for numyear, nameyear in enumerate(year):
    l0=[]
    copyl0=[]
    SysUpl0=[]
    SysDownl0=[]
    JecUpl0=[]
    JecDownl0=[]
    Files = []
    t0PdfUp=[]
    t0QscaleUp=[]
    t0PdfDown=[]
    t0QscaleDown=[]
    for f in range(len(Samples)):
        l1=[]
        copyl1=[]
        SysUpl1=[]
        SysDownl1=[]
        JecUpl1=[]
        JecDownl1=[]
        t1PdfUp=[]
        t1QscaleUp=[]
        t1PdfDown=[]
        t1QscaleDown=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        print Samples[f]
        SWscale, SWpdf =  SumofWeight(['/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL' + nameyear[2:]+ '/v1/UL' + nameyear[2:]+"_"+ Samples[f].split(".")[0]])
        for numch, namech in enumerate(channels):
            l2=[]
            copyl2=[]
            SysUpl2=[]
            SysDownl2=[]
            JecUpl2=[]
            JecDownl2=[]
            t2PdfUp=[]
            t2QscaleUp=[]
            t2PdfDown=[]
            t2QscaleDown=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                copyl3=[]
                SysUpl3=[]
                SysDownl3=[]
                JecUpl3=[]
                JecDownl3=[]
                t3PdfUp=[]
                t3QscaleUp=[]
                t3PdfDown=[]
                t3QscaleDown=[]
                for numvar, namevar in enumerate(variables):
                    SysUpl4=[]
                    SysDownl4=[]
                    JecUpl4=[]
                    JecDownl4=[]
                    t4Pdf=[]
                    t4Qscale=[]
                    print namech + '_' + namereg + '_' + namevar
                    h= Files[f].Get('promptG_'+namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                    h=h.Rebin(len(bins)-1,"",bins)
                    l3.append(h)
                    copyl3.append(h.Clone())
                    if namech=='aJets':
                        for numsys, namesys in enumerate(sys):
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            SysUpl4.append(h)
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            SysDownl4.append(h)
                        for numsys, namesys in enumerate(sysJec):
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            JecUpl4.append(h)
                            h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            JecDownl4.append(h)
                        for numsys in range(8):
                            h= Files[f].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_Qscale_'+str(numsys))
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            h.Scale(SWscale[numsys])
                            t4Qscale.append(h)
                        for numsys in range(100):
                            h= Files[f].Get('reweightingSys/' + namech +'_' + namereg + '_' + namevar+ '_PDF_'+str(numsys))
                            h.SetFillColor(colors[f])
                            h.SetLineColor(colors[f])
                            h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                            h=h.Rebin(len(bins)-1,"",bins)
                            h.Scale(SWpdf[numsys])
                            t4Pdf.append(h)
                    Pdf_hcUp = l3[0].Clone()
                    Pdf_hcDown = l3[0].Clone()
                    for b in range(l3[0].GetNbinsX()):
                        QS=np.zeros(8)
                        PDF=0
                        for numsys in range(8):
                            if numsys==2 or numsys==6:
                                QS[numsys] = l3[0].GetBinContent(b+1)
                                continue
                            QS[numsys] = t4Qscale[numsys].GetBinContent(b+1)
                        t4Qscale[0].SetBinContent(b+1,max(QS))
                        t4Qscale[1].SetBinContent(b+1,min(QS))
                        for numsys in range(100):
                            PDF = PDF + (t4Pdf[numsys].GetBinContent(b+1) - l3[0].GetBinContent(b+1))**2
                        #print str(math.sqrt(PDF))+":"+str(t4Qscale[4].GetBinContent(b+1))
                        Pdf_hcUp.SetBinContent(b+1,l3[0].GetBinContent(b+1)+math.sqrt(PDF))
                        Pdf_hcDown.SetBinContent(b+1,l3[0].GetBinContent(b+1)-math.sqrt(PDF))
                        #print str(Pdf_hcUp.GetBinContent(b+1)) +"<<"+str(t4Qscale[4].GetBinContent(b+1))+"<<"+str(Pdf_hcDown.GetBinContent(b+1))
                        #print str(l3[0].GetBinContent(b+1))
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                    JecUpl3.append(JecUpl4)
                    JecDownl3.append(JecDownl4)
                    t3QscaleUp.append(t4Qscale[0])
                    t3QscaleDown.append(t4Qscale[1])
                    t3PdfUp.append(Pdf_hcUp)
                    t3PdfDown.append(Pdf_hcDown)
                l2.append(l3)
                copyl2.append(copyl3)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
                JecUpl2.append(JecUpl3)
                JecDownl2.append(JecDownl3)
                t2PdfUp.append(t3PdfUp)
                t2PdfDown.append(t3PdfDown)
                t2QscaleUp.append(t3QscaleUp)
                t2QscaleDown.append(t3QscaleDown)
            l1.append(l2)
            copyl1.append(copyl2)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
            JecUpl1.append(JecUpl2)
            JecDownl1.append(JecDownl2)
            t1PdfUp.append(t2PdfUp)
            t1PdfDown.append(t2PdfDown)
            t1QscaleUp.append(t2QscaleUp)
            t1QscaleDown.append(t2QscaleDown)
        l0.append(l1)
        copyl0.append(copyl1)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
        JecUpl0.append(JecUpl1)
        JecDownl0.append(JecDownl1)
        t0PdfUp.append(t1PdfUp)
        t0PdfDown.append(t1PdfDown)
        t0QscaleUp.append(t1QscaleUp)
        t0QscaleDown.append(t1QscaleDown)

    Hists.append(l0)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)       
    HistsSysDown.append(SysDownl0)
    HistsJecUp.append(JecUpl0)
    HistsJecDown.append(JecDownl0)
    HistsPdfUp.append(t0PdfUp)
    HistsPdfDown.append(t0PdfDown)
    HistsQscaleUp.append(t0QscaleUp)
    HistsQscaleDown.append(t0QscaleDown)

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
for WS in range(len(Samples)):
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
                                cv = Hists[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)
                                rb = 0
                                if cv>0:
                                    rb = 100/cv
                                hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                                hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[numyear][WS][numch][numreg][numvar][numsys2].GetBinContent(b+1)-cv)*rb,0)))
                        glistup.append(hup)
                        glistdown.append(hdown)
                    hup = HistsPdfUp[numyear][WS][numch][numreg][numvar].Clone()
                    hdown = HistsPdfDown[numyear][WS][numch][numreg][numvar].Clone()
                    if hup.Integral()>0 or hdown.Integral()>0:
                        for b in range(hup.GetNbinsX()):
                            cv = Hists[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)
                            rb = 0
                            if cv>0:
                                rb = 100/cv
                            hup.SetBinContent(b+1, 0 + abs(max((HistsPdfUp[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsPdfDown[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                            hdown.SetBinContent(b+1, 0 - abs(min((HistsPdfUp[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsPdfDown[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                    sysModified=list(sys)
                    sysModified.append('PDF')
                    hup = HistsQscaleUp[numyear][WS][numch][numreg][numvar].Clone()
                    hdown = HistsQscaleDown[numyear][WS][numch][numreg][numvar].Clone()
                    if hup.Integral()>0 or hdown.Integral()>0:
                        for b in range(hup.GetNbinsX()):
                            print Samples[WS] + ' '+str(HistsQscaleUp[numyear][WS][numch][numreg][numvar].GetBinContent(b+1))+ ' '+str(HistsQscaleDown[numyear][WS][numch][numreg][numvar].GetBinContent(b+1))+ ' '+str(Hists_copy[numyear][WS][numch][numreg][numvar].GetBinContent(b+1))
                            cv = Hists[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)
                            rb = 0
                            if cv>0:
                                rb = 100/cv
                            hup.SetBinContent(b+1, 0 + abs(max((HistsQscaleUp[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsQscaleDown[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                            hdown.SetBinContent(b+1, 0 - abs(min((HistsQscaleUp[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb, (HistsQscaleDown[numyear][WS][numch][numreg][numvar].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                    sysModified.append('QScale')
                    compareError(glistup,glistdown, sysModified, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpWeight_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])

for WS in range(len(Samples)):
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
                    compareError(glistup,glistdown, sysJec, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpJec_'+Samples[WS].split('.')[0],Samples[WS].split('.')[0])

hfile = ROOT.TFile.Open( HistAddress +'2017_data.root')
print HistAddress + nameyear+ '_data.root'
H1=hfile.Get('promptG_aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1')
H1=H1.Rebin(len(bins)-1,"",bins)
Hup=hfile.Get('aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1_missTagRate_Up')
Hup=Hup.Rebin(len(bins)-1,"",bins)
Hdown=hfile.Get('aJets_nAk8G1nTtag0XtopMissTagRate_TsMass1_missTagRate_Down')
Hdown=Hdown.Rebin(len(bins)-1,"",bins)
glistup = []
glistdown = []
hup =Hup.Clone()
hdown =Hdown.Clone()
for b in range(H1.GetNbinsX()):
    cv = H1.GetBinContent(b+1)
    rb = 0
    if cv>0:
        rb = 100/cv
    hup.SetBinContent(b+1, 0 + abs(max((Hup.GetBinContent(b+1)-cv)*rb, (Hdown.GetBinContent(b+1)-cv)*rb,0)))
    hdown.SetBinContent(b+1, 0 - abs(min((Hup.GetBinContent(b+1)-cv)*rb, (Hdown.GetBinContent(b+1)-cv)*rb,0)))
glistup.append(hup)
glistdown.append(hdown)
compareError(glistup,glistdown, ['missTagRate'], 'aJets', 'aJets', '2017','TsMass1',"M(#gamma, highest mass AK8)", 'ExpGjet','Gjets')

