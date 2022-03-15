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


year=['2016','2017','2018']
LumiErr = [0.025, 0.023, 0.025, 0.018]
regions=["llB1", "llBg1"]
channels=["emu"]
variables=["BDT"]
sys = ["eleRecoSf", "eleIDSf", "muIdSf", "muIsoSf", "bcTagSF", "udsgTagSF","pu", "prefiring", "trigSF", "jes", "jer", "unclusMET","muonScale","electronScale","muonRes"]
sysJecNames = ["AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativeJEREC1","RelativeJEREC2","RelativeJERHF","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]
sysJecNamesUnCorr = ["AbsoluteStat","RelativeJEREC1","RelativeJEREC2","RelativePtEC1","RelativePtEC2","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","TimePtEta"]
sysJecNamesCorr =["AbsoluteMPFBias","AbsoluteScale","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativeJERHF","RelativePtBB","RelativePtHF","RelativeBal","RelativeStatFSR","RelativeStatHF"]

HistAddress = '/user/rgoldouz/NewAnalysis2020/Analysis/hists/'

Samples = ['data.root','WJetsToLNu.root','others.root', 'DY.root', 'TTTo2L2Nu.root', 'ST_tW.root', 'LFVVecC.root', 'LFVVecU.root', 'LFVScalarC.root', 'LFVScalarU.root', 'LFVTensorC.root', 'LFVTensorU.root']
SamplesName = ['Data','Jets','Others', 'DY', 't#bar{t}', 'tW' , 'LFV-vec [c_{e#mutc}=5]', 'LFV-vec [c_{e#mutu}=2]']
SamplesNameCombined = ['data_obs','Jets','Others', 'DY', 'tt', 'tW',  'LfvVectorEmutc', 'LfvVectorEmutu', 'LfvScalarEmutc', 'LfvScalarEmutu', 'LfvTensorEmutc', 'LfvTensorEmutu']
NormalizationErr = [0, 0.5, 0.5, 0.3, 0.05, 0.1, 0,0,0,0,0,0]

SignalSamples = ['LFVVecC', 'LFVVecU', 'LFVScalarC', 'LFVScalarU', 'LFVTensorC', 'LFVTensorU']

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, ROOT.kCyan-6, ROOT.kOrange-6, ROOT.kCyan-6, ROOT.kOrange-6, ROOT.kCyan-6]

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
                    for numsys, namesys in enumerate(sysJecNames):
                        h= Files[f].Get('JECSys/' +namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        JecUpl4.append(h)
                        h= Files[f].Get('JECSys/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
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


#find signal uncertainties

SIGpdfGraph=[]
SIGqscaleGraph=[]
SIGISRGraph=[]
SIGFSRGraph=[]
for f in range(len(SignalSamples)):
    SIG1Pdf=[]
    SIG1Qscale=[]
    SIG1ISR=[]
    SIG1FSR=[]
    for numyear, nameyear in enumerate(year):
        sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_'+ SignalSamples[f]+'.root')
        SIG2Pdf=[]
        SIG2Qscale=[]
        SIG2ISR=[]
        SIG2FSR=[]
        for numreg, namereg in enumerate(regions):
            pdfHists=[]
            QscaleHists=[]
            for numsys in range(45):
                h=sysfile.Get('reweightingSys/emu' + '_' + namereg + '_BDT_QscalePDF_'+str(numsys))
                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                QscaleHists.append(h)
            for numsys in range(50,145):
                h=sysfile.Get('reweightingSys/emu' +'_' + namereg + '_BDT_QscalePDF_'+str(numsys))
                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                pdfHists.append(h)
            hISRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_8')
            hISRup.SetBinContent(hISRup.GetXaxis().GetNbins(), hISRup.GetBinContent(hISRup.GetXaxis().GetNbins()) + hISRup.GetBinContent(hISRup.GetXaxis().GetNbins()+1))
            hISRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_6')
            hISRdown .SetBinContent(hISRdown.GetXaxis().GetNbins(), hISRdown.GetBinContent(hISRdown.GetXaxis().GetNbins()) + hISRdown.GetBinContent(hISRdown.GetXaxis().GetNbins()+1))
            hFSRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_9')
            hFSRup.SetBinContent(hFSRup.GetXaxis().GetNbins(), hFSRup.GetBinContent(hFSRup.GetXaxis().GetNbins()) + hFSRup.GetBinContent(hFSRup.GetXaxis().GetNbins()+1))
            hFSRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_7')
            hFSRdown .SetBinContent(hFSRdown.GetXaxis().GetNbins(), hFSRdown.GetBinContent(hFSRdown.GetXaxis().GetNbins()) + hFSRdown.GetBinContent(hFSRdown.GetXaxis().GetNbins()+1))
            binwidth= array( 'd' )
            bincenter= array( 'd' )
            yvalue= array( 'd' )
            yerrupQscale= array( 'd' )
            yerrdownQscale= array( 'd' )
            yerrupPDF= array( 'd' )
            yerrdownPDF= array( 'd' )
            yerrupISR = array( 'd' )
            yerrdownISR = array( 'd' )
            yerrupFSR = array( 'd' )
            yerrdownFSR = array( 'd' )
            for b in range(QscaleHists[0].GetNbinsX()):
                QS=np.zeros(45)
                PDFup=0
                PDFdown=0
                binwidth.append(QscaleHists[0].GetBinWidth(b+1)/2)
                bincenter.append(QscaleHists[0].GetBinCenter(b+1))
                yvalue.append(0)
                nomRatio = 1
                for numsys in range(45):
                    if numsys==5 or numsys==10 or numsys==15 or numsys==20 or numsys==30 or numsys==40:
                        QS[numsys] = QscaleHists[numsys].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1)
                yerrupQscale.append((abs(max(QS)))*nomRatio)
                yerrdownQscale.append((abs(min(QS)))*nomRatio)
                for numsys in range(50,140):
                    if pdfHists[numsys-50].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1) >0:
                        PDFup = PDFup + (pdfHists[numsys-50].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1))**2
                    else:
                        PDFdown = PDFdown + (pdfHists[numsys-50].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1))**2
                yerrupPDF.append((math.sqrt(PDFup))*nomRatio)
                yerrdownPDF.append((math.sqrt(PDFdown))*nomRatio)
                yerrupISR.append((abs(max(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrdownISR.append((abs(min(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrupFSR.append((abs(max(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1,0),0)))*nomRatio)
                yerrdownFSR.append((abs(min(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
            SIG2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownQscale,yerrupQscale))
            SIG2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownPDF,yerrupPDF))
            SIG2ISR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownISR,yerrupISR))
            SIG2FSR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownFSR,yerrupFSR))
            del binwidth
            del bincenter
            del yvalue
            del yerrupQscale
            del yerrdownQscale
            del yerrupPDF
            del yerrdownPDF
            del yerrupISR
            del yerrdownISR
            del yerrupFSR
            del yerrdownFSR
            del pdfHists
            del QscaleHists
            gc.collect()
        SIG1Qscale.append(SIG2Qscale)
        SIG1Pdf.append(SIG2Pdf)
        SIG1ISR.append(SIG2ISR)
        SIG1FSR.append(SIG2FSR)
    SIGpdfGraph.append(SIG1Pdf)
    SIGqscaleGraph.append(SIG1Qscale)
    SIGISRGraph.append(SIG1ISR)
    SIGFSRGraph.append(SIG1FSR)
GSIGsys = []
GSIGsys.append(SIGpdfGraph)
GSIGsys.append(SIGqscaleGraph)
GSIGsys.append(SIGISRGraph)
GSIGsys.append(SIGFSRGraph)
SIGsys =  ['pdf','QS','ISR','FSR']


# find ttbar modeling uncertaintis
pdfGraph=[]
qscaleGraph=[]
ISRGraph=[]
FSRGraph=[]
CRGraph=[]
TuneGraph=[]
hdampGraph=[]

for numyear, nameyear in enumerate(year):
    t1Pdf=[]
    t1Qscale=[]
    t1ISR=[]
    t1FSR=[]
    t1CR=[]
    t1Tune=[]
    t1hdamp=[]
    sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu.root')
    CR1file = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_CR1QCDbased.root')
    CR2file = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_CR2QCDbased.root')
    erdfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_CRerdON.root')
    TuneCP5upfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5up.root')
    TuneCP5downfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5down.root')
    hdampupfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampUP.root')
    hdampdownfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampDOWN.root')
    for numreg, namereg in enumerate(regions):
        t2Pdf=[]
        t2Qscale=[]
        t2ISR=[]
        t2FSR=[]
        t2CR=[]
        t2Tune=[]
        t2hdamp=[]
        for numvar, namevar in enumerate(variables):
            pdfHists=[]
            QscaleHists=[]
            for numsys in range(9):
                h=sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_QscalePDF_'+str(numsys))
                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                QscaleHists.append(h)
#                del h
#                gc.collect()
            for numsys in range(9,110):
                h=sysfile.Get('reweightingSys/emu' +'_' + namereg + '_' + namevar+ '_QscalePDF_'+str(numsys))
                h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                pdfHists.append(h)
#                del h
#                gc.collect()
            hISRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_8')
            hISRup.SetBinContent(hISRup.GetXaxis().GetNbins(), hISRup.GetBinContent(hISRup.GetXaxis().GetNbins()) + hISRup.GetBinContent(hISRup.GetXaxis().GetNbins()+1))
            hISRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_6')
            hISRdown .SetBinContent(hISRdown.GetXaxis().GetNbins(), hISRdown.GetBinContent(hISRdown.GetXaxis().GetNbins()) + hISRdown.GetBinContent(hISRdown.GetXaxis().GetNbins()+1))
            hFSRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_9')
            hFSRup.SetBinContent(hFSRup.GetXaxis().GetNbins(), hFSRup.GetBinContent(hFSRup.GetXaxis().GetNbins()) + hFSRup.GetBinContent(hFSRup.GetXaxis().GetNbins()+1))
            hFSRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_7')
            hFSRdown .SetBinContent(hFSRdown.GetXaxis().GetNbins(), hFSRdown.GetBinContent(hFSRdown.GetXaxis().GetNbins()) + hFSRdown.GetBinContent(hFSRdown.GetXaxis().GetNbins()+1))
            hCR1 = CR1file.Get('emu' + '_' + namereg + '_' + namevar)
            hCR1.SetBinContent(hCR1.GetXaxis().GetNbins(), hCR1.GetBinContent(hCR1.GetXaxis().GetNbins()) + hCR1.GetBinContent(hCR1.GetXaxis().GetNbins()+1))
            hCR2 = CR2file.Get('emu' + '_' + namereg + '_' + namevar)
            hCR2.SetBinContent(hCR2.GetXaxis().GetNbins(), hCR2.GetBinContent(hCR2.GetXaxis().GetNbins()) + hCR2.GetBinContent(hCR2.GetXaxis().GetNbins()+1))
            herd = erdfile.Get('emu' + '_' + namereg + '_' + namevar)
            herd.SetBinContent(herd.GetXaxis().GetNbins(), herd.GetBinContent(herd.GetXaxis().GetNbins()) + herd.GetBinContent(herd.GetXaxis().GetNbins()+1))
            hTuneCP5up = TuneCP5upfile.Get('emu' + '_' + namereg + '_' + namevar)
            hTuneCP5up .SetBinContent(hTuneCP5up.GetXaxis().GetNbins(), hTuneCP5up.GetBinContent(hTuneCP5up.GetXaxis().GetNbins()) + hTuneCP5up.GetBinContent(hTuneCP5up.GetXaxis().GetNbins()+1))
            hTuneCP5down = TuneCP5downfile.Get('emu' + '_' + namereg + '_' + namevar)
            hTuneCP5down .SetBinContent(hTuneCP5down.GetXaxis().GetNbins(), hTuneCP5down.GetBinContent(hTuneCP5down.GetXaxis().GetNbins()) + hTuneCP5down.GetBinContent(hTuneCP5down.GetXaxis().GetNbins()+1))
            hhdampup = hdampupfile.Get('emu' + '_' + namereg + '_' + namevar)
            hhdampup .SetBinContent(hhdampup.GetXaxis().GetNbins(), hhdampup.GetBinContent(hhdampup.GetXaxis().GetNbins()) + hhdampup.GetBinContent(hhdampup.GetXaxis().GetNbins()+1))
            hhdampdown = hdampdownfile.Get('emu' + '_' + namereg + '_' + namevar)
            hhdampdown .SetBinContent(hhdampdown.GetXaxis().GetNbins(), hhdampdown.GetBinContent(hhdampdown.GetXaxis().GetNbins()) + hhdampdown.GetBinContent(hhdampdown.GetXaxis().GetNbins()+1))
            binwidth= array( 'd' )
            bincenter= array( 'd' )
            yvalue= array( 'd' )
            yerrupQscale= array( 'd' )
            yerrdownQscale= array( 'd' )
            yerrupPDF= array( 'd' )
            yerrdownPDF= array( 'd' )
            yerrupISR = array( 'd' )
            yerrdownISR = array( 'd' )
            yerrupFSR = array( 'd' )
            yerrdownFSR = array( 'd' )
            yerrupCR = array( 'd' )
            yerrdownCR = array( 'd' )
            yerrupTune= array( 'd' )
            yerrdownTune= array( 'd' )
            yerruphdamp= array( 'd' )
            yerrdownhdamp= array( 'd' )
            for b in range(QscaleHists[0].GetNbinsX()):
                QS=np.zeros(9)
                PDF=0
                binwidth.append(QscaleHists[0].GetBinWidth(b+1)/2)
                bincenter.append(QscaleHists[0].GetBinCenter(b+1))
                yvalue.append(0)
                nomRatio = 1
#                if QscaleHists[0].GetBinContent(b+1) > 0:
#                    nomRatio = 100/QscaleHists[0].GetBinContent(b+1)
                for numsys in range(9):
                    if numsys==0 or numsys==5 or numsys==7:
                        continue
                    QS[numsys] = QscaleHists[numsys].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1)
                yerrupQscale.append((abs(max(QS)))*nomRatio)
                yerrdownQscale.append((abs(min(QS)))*nomRatio)
                for numsys in range(9,110):
                    PDF = PDF + (pdfHists[numsys-9].GetBinContent(b+1) - QscaleHists[0].GetBinContent(b+1))**2
                yerrupPDF.append((math.sqrt(PDF))*nomRatio)
                yerrdownPDF.append((math.sqrt(PDF))*nomRatio)
                yerrupISR.append((abs(max(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrdownISR.append((abs(min(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrupFSR.append((abs(max(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1,0),0)))*nomRatio)
                yerrdownFSR.append((abs(min(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrupCR.append((abs(max(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1), hCR2.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrdownCR.append((abs(min(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1), hCR2.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrupTune.append((abs(max(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrdownTune.append((abs(min(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerruphdamp.append((abs(max(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
                yerrdownhdamp.append((abs(min(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1),0)))*nomRatio)
#                del QS
#                del PDF
#                del nomRatio
#                gc.collect()
            t2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownQscale,yerrupQscale))
            t2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownPDF,yerrupPDF))
            t2ISR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownISR,yerrupISR))
            t2FSR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownFSR,yerrupFSR))
            t2CR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownCR,yerrupCR))
            t2Tune.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownTune,yerrupTune))
            t2hdamp.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownhdamp,yerruphdamp))
            del binwidth
            del bincenter
            del yvalue
            del yerrupQscale
            del yerrdownQscale
            del yerrupPDF
            del yerrdownPDF
            del yerrupISR
            del yerrdownISR
            del yerrupFSR
            del yerrdownFSR
            del pdfHists
            del QscaleHists
            gc.collect()
        t1Qscale.append(t2Qscale)
        t1Pdf.append(t2Pdf)
        t1ISR.append(t2ISR)
        t1FSR.append(t2FSR)
        t1CR.append(t2CR)
        t1Tune.append(t2Tune)
        t1hdamp.append(t2hdamp)
    pdfGraph.append(t1Pdf)
    qscaleGraph.append(t1Qscale)
    ISRGraph.append(t1ISR)
    FSRGraph.append(t1FSR)
    CRGraph.append(t1CR)
    TuneGraph.append(t1Tune)
    hdampGraph.append(t1hdamp)
    sysfile.Close()
    CR1file.Close()
    erdfile.Close()
    TuneCP5upfile.Close()
    TuneCP5downfile.Close()
    hdampupfile.Close()
    hdampdownfile.Close()
    del sysfile
    del CR1file
    del erdfile
    del TuneCP5upfile
    del TuneCP5downfile
    del hdampupfile
    del hdampdownfile
    gc.collect()
Gttsys = []
Gttsys.append(pdfGraph)
Gttsys.append(qscaleGraph)
Gttsys.append(ISRGraph)
Gttsys.append(FSRGraph)
Gttsys.append(CRGraph)
Gttsys.append(TuneGraph)
Gttsys.append(hdampGraph)
ttsys =  ['pdf','QS','ISR','FSR','CR','Tune','hdamp']

statName={}

if not os.path.exists('CombinedFiles'):
    os.makedirs('CombinedFiles')

for numyear, nameyear in enumerate(year):
    TuneCP5upfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5up.root')
    TuneCP5downfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_TuneCP5down.root')
    hdampupfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampUP.root')
    hdampdownfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTsys_hdampDOWN.root')    
    for numreg, namereg in enumerate(regions):
        hfile = ROOT.TFile( 'CombinedFiles/' + nameyear+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
        for f in range(len(Samples)):
            Hists[numyear][f][0][numreg][0].SetName(SamplesNameCombined[f])
            Hists[numyear][f][0][numreg][0].Write()
            if f==0:
                continue
            for numsys, namesys in enumerate(sys):
                HistsSysUp[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + 'Up')
                HistsSysDown[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + 'Down')
                if 'jer' in namesys:
                    HistsSysUp[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear +namesys + 'Up')
                    HistsSysDown[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + namesys + 'Down')
                HistsSysUp[numyear][f][0][numreg][0][numsys].Write()
                HistsSysDown[numyear][f][0][numreg][0][numsys].Write()
#JEC uncertainties
            for numsys, namesys in enumerate(sysJecNames):
                if namesys in sysJecNamesCorr:
                    HistsJecUp[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_jes' + namesys + 'Up')
                    HistsJecDown[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_jes' + namesys + 'Down')
                    HistsJecUp[numyear][f][0][numreg][0][numsys].Write()
                    HistsJecDown[numyear][f][0][numreg][0][numsys].Write()
                if namesys in sysJecNamesUnCorr:
                    HistsJecUp[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + 'jes' + namesys + 'Up')
                    HistsJecDown[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + 'jes' + namesys + 'Down')
                    HistsJecUp[numyear][f][0][numreg][0][numsys].Write()
                    HistsJecDown[numyear][f][0][numreg][0][numsys].Write()
#ttbar modeling uncertainties
        for g in range(len(Gttsys)):
            if ttsys[g]=='Tune' or ttsys[g]=='hdamp':
                continue
            hup = Hists[numyear][4][0][numreg][0].Clone()
            hdown = Hists[numyear][4][0][numreg][0].Clone()
            for b in range(hup.GetNbinsX()):
#                print nameyear + namereg + ttsys[g] + str(hup.GetBinContent(b+1)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYhigh(b)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
                hup.SetBinContent(b+1,hup.GetBinContent(b+1) + Gttsys[g][numyear][numreg][0].GetErrorYhigh(b))
                hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
            hup.SetName(SamplesNameCombined[4] + '_tt_' + ttsys[g] + 'Up')
            hdown.SetName(SamplesNameCombined[4] + '_tt_' + ttsys[g] + 'Down')
            hup.Write()
            hdown.Write()
        hTuneCP5up = TuneCP5upfile.Get('emu' + '_' + namereg + '_' + namevar)
        hTuneCP5up.SetName(SamplesNameCombined[4] + '_tt_TuneUp') 
        hTuneCP5up.Write()
        hTuneCP5down = TuneCP5downfile.Get('emu' + '_' + namereg + '_' + namevar)
        hTuneCP5down.SetName(SamplesNameCombined[4] + '_tt_TuneDown')
        hTuneCP5down.Write()
        hhdampup = hdampupfile.Get('emu' + '_' + namereg + '_' + namevar)
        hhdampup.SetName(SamplesNameCombined[4] + '_tt_hdampUp')
        hhdampup.Write()
        hhdampdown = hdampdownfile.Get('emu' + '_' + namereg + '_' + namevar)
        hhdampdown.SetName(SamplesNameCombined[4] + '_tt_hdampDown')
        hhdampdown.Write()
#Signal Modeling
        for f in range(6,len(Samples)):
            for g in range(len(GSIGsys)):
                hup = Hists[numyear][f][0][numreg][0].Clone()
                hdown = Hists[numyear][f][0][numreg][0].Clone()
                for b in range(hup.GetNbinsX()):
#                print nameyear + namereg + ttsys[g] + str(hup.GetBinContent(b+1)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYhigh(b)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
                    hup.SetBinContent(b+1,hup.GetBinContent(b+1) + GSIGsys[g][f-6][numyear][numreg].GetErrorYhigh(b))
                    hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - GSIGsys[g][f-6][numyear][numreg].GetErrorYlow(b))
                hup.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Up')
                hdown.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Down')
                hup.Write()
                hdown.Write()
#add MC stat error
        for f in range(len(Samples)):
            if f==0:
                continue
            stat=[]
            for b in range(Hists[numyear][f][0][numreg][0].GetNbinsX()):
                if Hists[numyear][f][0][numreg][0].GetBinContent(b+1)==0:
                    continue
                HstatUp = Hists[numyear][f][0][numreg][0].Clone()
                HstatUp.SetBinContent(b+1,HstatUp.GetBinContent(b+1) + HstatUp.GetBinError(b+1))
                HstatUp.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Up')
                HstatUp.Write()
                HstatDown = Hists[numyear][f][0][numreg][0].Clone()
                HstatDown.SetBinContent(b+1,HstatDown.GetBinContent(b+1) - HstatDown.GetBinError(b+1))
                if HstatDown.GetBinContent(b+1) < 0.001:
                    HstatDown.SetBinContent(b+1,0.001)
                HstatDown.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Down')
                HstatDown.Write()
                stat.append('Y' + nameyear+namereg+SamplesNameCombined[f]+'StatBin' +str(b+1))
            statName[ nameyear + namereg + SamplesNameCombined[f]]=stat
        hfile.Write()
        hfile.Close()


for namesig in SignalSamples:
    for numyear, nameyear in enumerate(year):
        for numreg, namereg in enumerate(regions):
            cardName = namesig+'_'+nameyear+'_' + namereg
            Sid= Samples.index(namesig + '.root')
            T1 = 'max 1 number of categories \n' +\
                 'jmax 5 number of samples minus one\n' +\
                 'kmax * number of nuisance parameters\n' +\
                 '------------\n'+\
                 'shapes * * '  + nameyear+'_'+namereg+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n' +\
                 '------------\n'+\
                 'bin'.ljust(45) + cardName + '\n'+\
                 'observation'.ljust(45) + str(Hists[numyear][0][0][numreg][0].Integral()) +'\n'+\
                 '------------\n'+\
                 'bin'.ljust(45) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) +'\n'+\
                 'process'.ljust(45) +'0'.ljust(25) + '1'.ljust(25) + '2'.ljust(25) + '3'.ljust(25) + '4'.ljust(25) + '5'.ljust(25) +'\n'+\
                 'process'.ljust(45) +SamplesNameCombined[Sid].ljust(25) + SamplesNameCombined[1].ljust(25) + SamplesNameCombined[2].ljust(25) +\
                 SamplesNameCombined[3].ljust(25) + SamplesNameCombined[4].ljust(25) + SamplesNameCombined[5].ljust(25)+'\n'+\
                 'rate'.ljust(45)+ str(Hists[numyear][Sid][0][numreg][0].Integral()).ljust(25) + str(Hists[numyear][1][0][numreg][0].Integral()).ljust(25) + str(Hists[numyear][2][0][numreg][0].Integral()).ljust(25)+\
                 str(Hists[numyear][3][0][numreg][0].Integral()).ljust(25) + str(Hists[numyear][4][0][numreg][0].Integral()).ljust(25) + str(Hists[numyear][5][0][numreg][0].Integral()).ljust(25) + '\n'+\
                 '------------\n'+\
                 'lumi'.ljust(35)+'lnN'.ljust(10) + '1.025'.ljust(25) + '1.025'.ljust(25) + '1.025'.ljust(25) + '1.025'.ljust(25) + '1.025'.ljust(25) + '1.025'.ljust(25) +'\n'+\
                 'Jets_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '1.5'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'+\
                 'Other_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '1.5'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'+\
                 'DY_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.5'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'+\
                 'tt_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.05'.ljust(25) + '-'.ljust(25) +'\n'+\
                 'tW_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.1'.ljust(25) +'\n'
            if '2016' in nameyear:
                T1 = T1 + 'lumi2016'.ljust(35)+'lnN'.ljust(10) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) +'\n'    
                T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) +'\n'
                T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
                T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) +'\n'
                T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
            if '2017' in nameyear:
                T1 = T1 + 'lumi2017'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) +'\n'
                T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) +'\n'
                T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
                T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) +'\n'
                T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) +'\n'
                T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) +'\n'
                T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) +'\n'
            if '2018' in nameyear:
                T1 = T1 + 'lumi2018'.ljust(35)+'lnN'.ljust(10) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) +'\n'
                T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) +'\n'
                T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) +'\n'
                T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) +'\n'
            for numsys, namesys in enumerate(sysJecNamesCorr):
                T1 = T1 +  'jes' + namesys.ljust(32)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
            for numsys, namesys in enumerate(sysJecNamesUnCorr):
                T1 = T1 + 'Y'+  nameyear + 'jes' + namesys.ljust(27)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
            for b in sys:
                if 'prefiring' in b or 'jer' in b:
                    continue 
                T1 = T1 +  b.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
            T1 = T1 + 'Y'+ nameyear + 'jer'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
            if  '2018' not in nameyear:
                T1 = T1 +  'prefiring'.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
            for b in ttsys:
                bpb= 'tt_' + b
                T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
            for b in SIGsys:
                bpb= 'Signal_' + b
                T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
            for key, value in statName.items():
                if namereg in key and nameyear in key and namesig in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
                if namereg in key and nameyear in key and 'Jets' in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
                if namereg in key and nameyear in key and 'Other' in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
                if namereg in key and nameyear in key and 'DY' in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
                if namereg in key and nameyear in key and 'tt' in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
                if namereg in key and nameyear in key and 'tW' in key:
                    for e in value:
                        T1 = T1 +  e.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) +'\n'

            open('CombinedFiles/' + cardName +'.txt', 'wt').write(T1)







