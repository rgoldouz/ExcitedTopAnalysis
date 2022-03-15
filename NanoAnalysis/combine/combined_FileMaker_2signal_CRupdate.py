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
from ROOT import TFile
from ROOT import TGaxis
from ROOT import THStack
import gc
from operator import truediv
import copy
TGaxis.SetMaxDigits(2)

def EFTtoNormal(H, wc):
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    r=1
    for b in range(hpx.GetNbinsX()):
        if H.GetBinContent(b+1,ROOT.WCPoint("NONE"))>0:
            r = H.GetBinError(b+1)/H.GetBinContent(b+1,ROOT.WCPoint("NONE"))
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, r*H.GetBinContent(b+1,wc))
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
    if hpx.Integral()>0:
        hpx.Scale(1/hpx.Integral())
    return hpx

def TH1EFTtoTH1(H, wc):
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    r=1
    for b in range(hpx.GetNbinsX()):
 #       if H.GetBinContent(b+1,ROOT.WCPoint(wc))>0:
#            r = H.GetBinError(b+1)/H.GetBinContent(b+1,ROOT.WCPoint("NONE"))
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, H.GetBinError(b+1))
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
    return hpx

def SumofWeight(add):
    for root, dirs, files in os.walk(add):
        if len(files) == 0:
            continue
        for f in files:
            filename = root + '/' + f
            if 'fail' in f:
                continue
            fi = TFile.Open(filename)
            tree_meta = fi.Get('Runs')
            genEventSumw = 0
            genEventSumwScale = [0]*9
            genEventSumwPdf = [0]*100
            for i in range( tree_meta.GetEntries() ):
                tree_meta.GetEntry(i)
                genEventSumw += tree_meta.genEventSumw
                for pdf in range(100):
                    genEventSumwPdf[pdf] += tree_meta.LHEPdfSumw[pdf]*tree_meta.genEventSumw
                for Q in range(9):
                    genEventSumwScale[Q] += tree_meta.LHEScaleSumw[Q]*tree_meta.genEventSumw
            tree_meta.Reset()
            tree_meta.Delete()
            fi.Close()
    return [genEventSumw/x for x in genEventSumwScale] , [genEventSumw/x for x in genEventSumwPdf]

year=['2016preVFP', '2016postVFP', '2017','2018']
ULyear=['UL16preVFP', 'UL16postVFP', 'UL17','UL18']
#year=['2017']
#ULyear=['UL17']
LumiErr = [0.018, 0.018, 0.018, 0.018]
regions=["llB1"]
channels=["ee", "emu", "mumu"];
variables=["BDT"]
sys = ["eleRecoSf", "eleIDSf", "muIdSf", "muIsoSf", "bcTagSF", "udsgTagSF","pu", "prefiring", "trigSF", "jer", "muonScale","electronScale","muonRes","unclusMET"]
sysJecNames = ["AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]
sysJecNamesUnCorr = ["AbsoluteStat","RelativePtEC1","RelativePtEC2","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","TimePtEta"]
sysJecNamesCorr =["AbsoluteMPFBias","AbsoluteScale","FlavorQCD","Fragmentation","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtHF","RelativeBal","RelativeStatFSR","RelativeStatHF"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/hists/'

Samples = ['data.root','other.root', 'DY.root', 'ttbar.root', 'tW.root',
'STBNV_TBCE.root',
'STBNV_TBUE.root',
'STBNV_TDCE.root',
'STBNV_TDUE.root',
'STBNV_TSCE.root',
'STBNV_TSUE.root',
'TTBNV_TBCE.root',
'TTBNV_TBUE.root',
'TTBNV_TDCE.root',
'TTBNV_TDUE.root',
'TTBNV_TSCE.root',
'TTBNV_TSUE.root'
]

SamplesName = ['Data','Others', 'DY', 't#bar{t}', 'tW' , 'LFV-vec [c_{e#mutc}=5]', 'LFV-vec [c_{e#mutu}=2]']
SamplesNameCombined = ['data_obs','Others', 'DY', 'tt', 'tW', 
'STBNV_TBCE',
'STBNV_TBUE',
'STBNV_TDCE',
'STBNV_TDUE',
'STBNV_TSCE',
'STBNV_TSUE',
'TTBNV_TBCE',
'TTBNV_TBUE',
'TTBNV_TDCE',
'TTBNV_TDUE',
'TTBNV_TSCE',
'TTBNV_TSUE'
]
NormalizationErr = [0, 0.5, 0.5, 0.3, 0.05, 0.1, 0,0,0,0,0,0, 0,0,0,0,0,0]

SignalSamples=[
'STBNV_TBCE',
'STBNV_TBUE',
'STBNV_TDCE',
'STBNV_TDUE',
'STBNV_TSCE',
'STBNV_TSUE',
'TTBNV_TBCE',
'TTBNV_TBUE',
'TTBNV_TDCE',
'TTBNV_TDUE',
'TTBNV_TSCE',
'TTBNV_TSUE'
]


wc1 = ROOT.WCPoint("EFTrwgt1_cS_1_cT_1")

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, 
ROOT.kBlue, ROOT.kBlue-7, ROOT.kViolet, ROOT.kViolet-5,ROOT.kAzure-9, ROOT.kAzure+10,
ROOT.kGreen, ROOT.kGreen+2, ROOT.kTeal-9, ROOT.kTeal+10, ROOT.kSpring-7, ROOT.kSpring+9]

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
#                    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                    for b in range(h.GetNbinsX()):
                        if h.GetBinContent(b+1,wc1)<0:
                            h.SetBinContent(b+1,0)
                        if h.GetBinContent(b+1,wc1)==h.GetBinError(b+1):
                            h.SetBinContent(b+1,0)
                            h.SetBinError(b+1,0)               
                    if "BNV" in Samples[f]:
                        h.Scale(wc1)
                        for b in range(h.GetNbinsX()):
                            h.SetBinError(b+1,0)
                    hNormal = TH1EFTtoTH1(h,wc1)
                    l3.append(hNormal)
                    copyl3.append(h.Clone())
                    if 'data' in Samples[f]:
                        continue
                    for numsys, namesys in enumerate(sys):
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1,wc1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1,wc1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        if "BNV" in Samples[f]:
                            h.Scale(wc1)
                        hNormal = TH1EFTtoTH1(h,wc1)
                        SysUpl4.append(hNormal)
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1,wc1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1,wc1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        if "BNV" in Samples[f]:
                            h.Scale(wc1)
                        hNormal = TH1EFTtoTH1(h,wc1)
                        SysDownl4.append(hNormal)
                    for numsys, namesys in enumerate(sysJecNames):
                        h= Files[f].Get('JECSys/' +namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1,wc1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1,wc1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        if "BNV" in Samples[f]:
                            h.Scale(wc1)
                        hNormal = TH1EFTtoTH1(h,wc1)
                        JecUpl4.append(hNormal)
                        h= Files[f].Get('JECSys/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1,wc1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1,wc1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        if "BNV" in Samples[f]:
                            h.Scale(wc1)
                        hNormal = TH1EFTtoTH1(h,wc1)
                        JecDownl4.append(hNormal)
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
for f in range(len(SignalSamples)):
    SIGPdf=[]
    SIGQscale=[]
    for numyear, nameyear in enumerate(year):
        SIG1Pdf=[]
        SIG1Qscale=[]
        sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_'+ SignalSamples[f]+'.root')
        SWscale, SWpdf =  SumofWeight('/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL' + nameyear[2:]+ '/v2/UL' + nameyear[2:]+ '_' + SignalSamples[f])
        for numch, namech in enumerate(channels):
            SIGChPdf=[]
            SIGChQscale=[]
            SIGChISR=[]
            SIGChFSR=[]
            for numreg, namereg in enumerate(regions):
                SIG2Pdf=[]
                SIG2Qscale=[]
                for numvar, namevar in enumerate(variables):
                    if 'BDT' not in namevar:
                        continue
                    pdfHists=[]
                    QscaleHists=[]
                    for numsys in range(9):
                        hEFT=sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_Qscale_'+str(numsys))
                        h=TH1EFTtoTH1(hEFT,wc1)
                        h.Scale(SWscale[numsys])
                        QscaleHists.append(h)
                    for numsys in range(100):
                        hEFT=sysfile.Get('reweightingSys/' + namech +'_' + namereg + '_' + namevar+ '_PDF_'+str(numsys))
                        h=TH1EFTtoTH1(hEFT,wc1)
                        h.Scale(SWpdf[numsys])
                        pdfHists.append(h)
                    binwidth= array( 'd' )
                    bincenter= array( 'd' )
                    yvalue= array( 'd' )
                    yerrupQscale= array( 'd' )
                    yerrdownQscale= array( 'd' )
                    yerrupPDF= array( 'd' )
                    yerrdownPDF= array( 'd' )
                    for b in range(QscaleHists[0].GetNbinsX()):
                        QS=np.zeros(9)
                        PDF=0
                        binwidth.append(QscaleHists[0].GetBinWidth(b+1)/2)
                        bincenter.append(QscaleHists[0].GetBinCenter(b+1))
                        yvalue.append(0)
                        nomRatio = 1
                        for numsys in range(9):
                            if numsys==2 or numsys==6:
                                continue
                            QS[numsys] = QscaleHists[numsys].GetBinContent(b+1) - QscaleHists[4].GetBinContent(b+1)
                        yerrupQscale.append((abs(max(QS)))*nomRatio)
                        yerrdownQscale.append((abs(min(QS)))*nomRatio)
                        for numsys in range(100):
                            PDF = PDF + (pdfHists[numsys].GetBinContent(b+1) - QscaleHists[4].GetBinContent(b+1))**2
                        yerrupPDF.append((math.sqrt(PDF))*nomRatio)
                        yerrdownPDF.append((math.sqrt(PDF))*nomRatio)
                    SIG2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownQscale,yerrupQscale))
                    SIG2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownPDF,yerrupPDF))
                    del binwidth
                    del bincenter
                    del yvalue
                    del yerrupQscale
                    del yerrdownQscale
                    del yerrupPDF
                    del yerrdownPDF
                SIGChQscale.append(SIG2Qscale)
                SIGChPdf.append(SIG2Pdf)
            SIG1Qscale.append(SIGChQscale)
            SIG1Pdf.append(SIGChPdf)
        SIGQscale.append(SIG1Qscale)
        SIGPdf.append(SIG1Pdf)
        sysfile.Close()
        del sysfile
        gc.collect()
    SIGpdfGraph.append(SIGPdf)
    SIGqscaleGraph.append(SIGQscale)

GSIGsys = []
GSIGsys.append(SIGpdfGraph)
GSIGsys.append(SIGqscaleGraph)
SIGsys =  ['pdf','QS']

# find ttbar modeling uncertaintis
#os.system('cp ' + HistAddress +'2016preVFP_TTTo2L2Nu_sys_hdampDOWN.root ' + HistAddress +'2016preVFP_TTTo2L2Nu_sys_hdampUP.root' )
os.system('cp ' + HistAddress +'2016postVFP_TTTo2L2Nu_sys_CR1.root ' + HistAddress +'2016postVFP_TTTo2L2Nu_sys_erdON.root' )
pdfGraph=[]
qscaleGraph=[]

for numyear, nameyear in enumerate(year):
    t1Pdf=[]
    t1Qscale=[]
    sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu.root')
    SWscale, SWpdf =  SumofWeight('/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL' + nameyear[2:]+ '/v2/UL' + nameyear[2:]+ '_TTTo2L2Nu')
    for numch, namech in enumerate(channels):
        tChPdf=[]
        tChQscale=[]
        tChISR=[]
        tChFSR=[]
        for numreg, namereg in enumerate(regions):
            t2Pdf=[]
            t2Qscale=[]
            for numvar, namevar in enumerate(variables):
                if 'BDT' not in namevar:
                    continue
                pdfHists=[]
                QscaleHists=[]
                for numsys in range(9):
                    hEFT=sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_Qscale_'+str(numsys))
                    h=TH1EFTtoTH1(hEFT,wc1)
                    h.Scale(SWscale[numsys])
                    QscaleHists.append(h)
                for numsys in range(100):
                    hEFT=sysfile.Get('reweightingSys/' + namech +'_' + namereg + '_' + namevar+ '_PDF_'+str(numsys))
                    h=TH1EFTtoTH1(hEFT,wc1)
                    h.Scale(SWpdf[numsys])
                    pdfHists.append(h)
                binwidth= array( 'd' )
                bincenter= array( 'd' )
                yvalue= array( 'd' )
                yerrupQscale= array( 'd' )
                yerrdownQscale= array( 'd' )
                yerrupPDF= array( 'd' )
                yerrdownPDF= array( 'd' )
                for b in range(QscaleHists[0].GetNbinsX()):
                    QS=np.zeros(9)
                    PDF=0
                    binwidth.append(QscaleHists[0].GetBinWidth(b+1)/2)
                    bincenter.append(QscaleHists[0].GetBinCenter(b+1))
                    yvalue.append(0)
                    nomRatio = 1
                    for numsys in range(9):
                        if numsys==2 or numsys==6:
                            continue
                        QS[numsys] = QscaleHists[numsys].GetBinContent(b+1) - QscaleHists[4].GetBinContent(b+1)
                    yerrupQscale.append((abs(max(QS)))*nomRatio)
                    yerrdownQscale.append((abs(min(QS)))*nomRatio)
                    for numsys in range(100):
                        PDF = PDF + (pdfHists[numsys].GetBinContent(b+1) - QscaleHists[4].GetBinContent(b+1))**2
                    yerrupPDF.append((math.sqrt(PDF))*nomRatio)
                    yerrdownPDF.append((math.sqrt(PDF))*nomRatio)
                t2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownQscale,yerrupQscale))
                t2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrdownPDF,yerrupPDF))
                del binwidth
                del bincenter
                del yvalue
                del yerrupQscale
                del yerrdownQscale
                del yerrupPDF
                del yerrdownPDF
            tChQscale.append(t2Qscale)
            tChPdf.append(t2Pdf)
        t1Qscale.append(tChQscale)
        t1Pdf.append(tChPdf)
    pdfGraph.append(t1Pdf)
    qscaleGraph.append(t1Qscale)
    sysfile.Close()
    del sysfile
    gc.collect()

Gttsys = []
Gttsys.append(pdfGraph)
Gttsys.append(qscaleGraph)
ttSys = ['pdf','QS']
ttSysOther=['Tune','hdamp']
ttsysCR=['CRcr1','CRcr2','CRerd']
#statName={}

if not os.path.exists('CombinedFilesOriginal'):
    os.makedirs('CombinedFilesOriginal')

for numyear, nameyear in enumerate(year):
    sysfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu.root')
    CR1file = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_CR1.root')
    CR2file = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_CR2.root')
    erdfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_erdON.root')
    TuneCP5upfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_TuneCP5up.root')
    TuneCP5downfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_TuneCP5down.root')
    hdampupfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_hdampUP.root')
    hdampdownfile = ROOT.TFile.Open(HistAddress + nameyear+ '_TTTo2L2Nu_sys_hdampDOWN.root')
    SigInputFiles = []
    for f in range(5,len(Samples)):   
        sysfileSIG = ROOT.TFile.Open(HistAddress + nameyear+ '_'+ Samples[f])
        SigInputFiles.append(sysfileSIG)
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            hfile = ROOT.TFile( 'CombinedFilesOriginal/' + nameyear+'_'+namech+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
            for f in range(len(Samples)):
                Hists[numyear][f][numch][numreg][0].SetName(SamplesNameCombined[f])
                Hists[numyear][f][numch][numreg][0].Write()
                if f==0:
                    continue
                for numsys, namesys in enumerate(sys):
                    if 'jer' in namesys or 'unclusMET' in namesys or 'bcTagSF' in namesys:
                        HistsSysUp[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear +namesys + 'Up')
                        HistsSysDown[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + namesys + 'Down')
                    else:
                        HistsSysUp[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + 'Up')
                        HistsSysDown[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + 'Down')
                    HistsSysUp[numyear][f][numch][numreg][0][numsys].Write()
                    HistsSysDown[numyear][f][numch][numreg][0][numsys].Write()
    #JEC uncertainties
                for numsys, namesys in enumerate(sysJecNames):
                    if namesys in sysJecNamesCorr:
                        HistsJecUp[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_jes' + namesys + 'Up')
                        HistsJecDown[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_jes' + namesys + 'Down')
                        HistsJecUp[numyear][f][numch][numreg][0][numsys].Write()
                        HistsJecDown[numyear][f][numch][numreg][0][numsys].Write()
                    if namesys in sysJecNamesUnCorr:
                        HistsJecUp[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + 'jes' + namesys + 'Up')
                        HistsJecDown[numyear][f][numch][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + 'Y'+ nameyear + 'jes' + namesys + 'Down')
                        HistsJecUp[numyear][f][numch][numreg][0][numsys].Write()
                        HistsJecDown[numyear][f][numch][numreg][0][numsys].Write()
    #ttbar modeling uncertainties
            for g in range(len(Gttsys)):
                hup = Hists[numyear][3][numch][numreg][0].Clone()
                hdown = Hists[numyear][3][numch][numreg][0].Clone()
                for b in range(hup.GetNbinsX()):
    #                print nameyear + namereg + ttsys[g] + str(hup.GetBinContent(b+1)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYhigh(b)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
                    hup.SetBinContent(b+1,hup.GetBinContent(b+1) + Gttsys[g][numyear][numch][numreg][0].GetErrorYhigh(b))
                    hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - Gttsys[g][numyear][numch][numreg][0].GetErrorYlow(b))
                hup.SetName(SamplesNameCombined[3] + '_tt_' + ttSys[g] + 'Up')
                hdown.SetName(SamplesNameCombined[3] + '_tt_' + ttSys[g] + 'Down')
                hup.Write()
                hdown.Write()
            
            hTuneCP5upNormal = TuneCP5upfile.Get(namech + '_' + namereg + '_' + namevar)
            hTuneCP5up=TH1EFTtoTH1(hTuneCP5upNormal,wc1)
            hTuneCP5up.SetName(SamplesNameCombined[3] + '_tt_TuneUp') 
            hTuneCP5up.Write()
            hTuneCP5downNormal = TuneCP5downfile.Get(namech + '_' + namereg + '_' + namevar)
            hTuneCP5down =TH1EFTtoTH1(hTuneCP5downNormal,wc1)
            hTuneCP5down.SetName(SamplesNameCombined[3] + '_tt_TuneDown')
            hTuneCP5down.Write()
            hhdampupNormal = hdampupfile.Get(namech + '_' + namereg + '_' + namevar)
            hhdampup=TH1EFTtoTH1(hhdampupNormal,wc1)
            hhdampup.SetName(SamplesNameCombined[3] + '_tt_hdampUp')
            hhdampup.Write()
            hhdampdownNormal = hdampdownfile.Get(namech + '_' + namereg + '_' + namevar)
            hhdampdown = TH1EFTtoTH1(hhdampdownNormal,wc1)
            hhdampdown.SetName(SamplesNameCombined[3] + '_tt_hdampDown')
            hhdampdown.Write()
            hCR1Normal = CR1file.Get(namech + '_' + namereg + '_' + namevar)
            hCR1 = TH1EFTtoTH1(hCR1Normal,wc1)
            hCR1.SetName(SamplesNameCombined[3] + '_tt_CRcr1Up')
            hCR1.Write()
            hCR1.SetName(SamplesNameCombined[3] + '_tt_CRcr1Down')
            hCR1.Write()
            hCR2Normal = CR2file.Get(namech + '_' + namereg + '_' + namevar)
            hCR2 = TH1EFTtoTH1(hCR2Normal,wc1)
            hCR2.SetName(SamplesNameCombined[3] + '_tt_CRcr2Up')
            hCR2.Write()
            hCR2.SetName(SamplesNameCombined[3] + '_tt_CRcr2Down')
            hCR2.Write()
            hCRerdNormal = erdfile.Get(namech + '_' + namereg + '_' + namevar)
            hCRerd = TH1EFTtoTH1(hCRerdNormal,wc1)
            hCRerd.SetName(SamplesNameCombined[3] + '_tt_CRerdUp')
            hCRerd.Write()
            hCRerd.SetName(SamplesNameCombined[3] + '_tt_CRerdDown')
            hCRerd.Write()
            hISRupNormal = sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_0')
            hISRup = TH1EFTtoTH1(hISRupNormal,wc1)
            hISRup.SetName(SamplesNameCombined[3] + '_ISRUp')
            hISRup.Write()
            hISRdownNormal = sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_2')
            hISRdown= TH1EFTtoTH1(hISRdownNormal,wc1)
            hISRdown.SetName(SamplesNameCombined[3] + '_ISRDown')
            hISRdown.Write()
            hFSRupNormal = sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_1')
            hFSRup= TH1EFTtoTH1(hFSRupNormal,wc1)
            hFSRup.SetName(SamplesNameCombined[3] + '_FSRUp')
            hFSRup.Write()
            hFSRdownNormal = sysfile.Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_3')
            hFSRdown = TH1EFTtoTH1(hFSRdownNormal,wc1)
            hFSRdown.SetName(SamplesNameCombined[3] + '_FSRDown')
            hFSRdown.Write()
    #Signal Modeling
            for f in range(5,len(Samples)):
                for g in range(len(GSIGsys)):
                    hup = Hists[numyear][f][0][numreg][0].Clone()
                    hdown = Hists[numyear][f][0][numreg][0].Clone()
                    for b in range(hup.GetNbinsX()):
    #                print nameyear + namereg + ttsys[g] + str(hup.GetBinContent(b+1)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYhigh(b)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
                        hup.SetBinContent(b+1,hup.GetBinContent(b+1) + GSIGsys[g][f-5][numyear][numch][numreg][0].GetErrorYhigh(b))
                        hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - GSIGsys[g][f-5][numyear][numch][numreg][0].GetErrorYlow(b))
                    if 'TT' in SamplesNameCombined[f]:
                        hup.SetName(SamplesNameCombined[f] + '_tt_' + SIGsys[g] + 'Up')
                        hdown.SetName(SamplesNameCombined[f] + '_tt_' + SIGsys[g] + 'Down')
                    else:
                        hup.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Up')
                        hdown.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Down')
                    hup.Write()
                    hdown.Write()
            for f in range(5,len(Samples)):
                hISRupNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_0')
                hISRup = TH1EFTtoTH1(hISRupNormal,wc1)
                hISRup.SetName(SamplesNameCombined[f] + '_ISRUp')
                hISRup.Write()
                hISRdownNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_2')
                hISRdown= TH1EFTtoTH1(hISRdownNormal,wc1)
                hISRdown.SetName(SamplesNameCombined[f] + '_ISRDown')
                hISRdown.Write()
                hFSRupNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_1')
                hFSRup= TH1EFTtoTH1(hFSRupNormal,wc1)
                hFSRup.SetName(SamplesNameCombined[f] + '_FSRUp')
                hFSRup.Write()
                hFSRdownNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_3')
                hFSRdown = TH1EFTtoTH1(hFSRdownNormal,wc1)
                hFSRdown.SetName(SamplesNameCombined[f] + '_FSRDown')
                hFSRdown.Write()
    #add MC stat error
#            for f in range(len(Samples)):
#                if f==0:
#                    continue
#                stat=[]
#                for b in range(Hists[numyear][f][0][numreg][0].GetNbinsX()):
#                    if Hists[numyear][f][0][numreg][0].GetBinContent(b+1)==0:
#                        continue
#                    HstatUp = Hists[numyear][f][0][numreg][0].Clone()
#                    HstatUp.SetBinContent(b+1,HstatUp.GetBinContent(b+1) + HstatUp.GetBinError(b+1))
#                    HstatUp.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Up')
#    #                HstatUp.Write()
#                    HstatDown = Hists[numyear][f][0][numreg][0].Clone()
#                    HstatDown.SetBinContent(b+1,HstatDown.GetBinContent(b+1) - HstatDown.GetBinError(b+1))
#                    if HstatDown.GetBinContent(b+1) < 0.001:
#                        HstatDown.SetBinContent(b+1,0.001)
#                    HstatDown.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Down')
#    #                HstatDown.Write()
#                    stat.append('Y' + nameyear+namereg+SamplesNameCombined[f]+'StatBin' +str(b+1))
#                statName[ nameyear + namereg + SamplesNameCombined[f]]=stat
            hfile.Write()
            hfile.Close()

SignalSamplesD = {}
SignalSamplesD['TBCE']=['STBNV_TBCE','TTBNV_TBCE']
SignalSamplesD['TBUE']=['STBNV_TBUE','TTBNV_TBUE']
SignalSamplesD['TDCE']=['STBNV_TDCE','TTBNV_TDCE']
SignalSamplesD['TDUE']=['STBNV_TDUE','TTBNV_TDUE']
SignalSamplesD['TSCE']=['STBNV_TSCE','TTBNV_TSCE']
SignalSamplesD['TSUE']=['STBNV_TSUE','TTBNV_TSUE']

for namesig, valueD in SignalSamplesD.items():
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                cardName = namesig+'_'+namech+'_'+nameyear+'_' + namereg
                Sid0= Samples.index(valueD[0] + '.root')
                Sid1= Samples.index(valueD[1] + '.root')
                T1 = 'max 1 number of categories \n' +\
                     'jmax 5 number of samples minus one\n' +\
                     'kmax * number of nuisance parameters\n' +\
                     '------------\n'+\
                     'shapes * * '  + nameyear+'_'+namech+'_'+namereg+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n' +\
                     '------------\n'+\
                     'bin'.ljust(45) + cardName + '\n'+\
                     'observation'.ljust(45) + str(Hists[numyear][0][numch][numreg][0].Integral()) +'\n'+\
                     '------------\n'+\
                     'bin'.ljust(45) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) + cardName.ljust(25) +'\n'+\
                     'process'.ljust(45) +'-1'.ljust(25) +'0'.ljust(25) + '1'.ljust(25) + '2'.ljust(25) + '3'.ljust(25) + '4'.ljust(25) +'\n'+\
                     'process'.ljust(45) +valueD[0].ljust(25) +valueD[1].ljust(25)+ SamplesNameCombined[1].ljust(25) + SamplesNameCombined[2].ljust(25) +\
                     SamplesNameCombined[3].ljust(25) + SamplesNameCombined[4].ljust(25) +'\n'+\
                     'rate'.ljust(45) + str(Hists[numyear][Sid0][numch][numreg][0].Integral()).ljust(25) + str(Hists[numyear][Sid1][numch][numreg][0].Integral()).ljust(25) + str(Hists[numyear][1][numch][numreg][0].Integral()).ljust(25) + str(Hists[numyear][2][numch][numreg][0].Integral()).ljust(25)+\
                     str(Hists[numyear][3][numch][numreg][0].Integral()).ljust(25) + str(Hists[numyear][4][numch][numreg][0].Integral()).ljust(25) + '\n'+\
                     '------------\n'+\
                     'Other_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25)  + '1.5'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'+\
                     'DY_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.5'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'+\
                     'tt_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.05'.ljust(25) + '-'.ljust(25) +'\n'+\
                     'tW_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1.1'.ljust(25) +'\n'+\
                     'MuIDSF'.ljust(35)+'lnN'.ljust(10) + '1.01'.ljust(25) + '1.01'.ljust(25) + '1.01'.ljust(25) + '1.01'.ljust(25) + '1.01'.ljust(25) + '1.01'.ljust(25) +'\n'
                if '2016' in nameyear:
                    T1 = T1 + 'lumi2016'.ljust(35)+'lnN'.ljust(10) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) + '1.022'.ljust(25) +'\n'    
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) + '1.009'.ljust(25) +'\n'
                    T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25)  + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
                    T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(25) + '1.005'.ljust(25)+ '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) +'\n'
                    T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25)  + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
                if '2017' in nameyear:
                    T1 = T1 + 'lumi2017'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) +'\n'
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) + '1.008'.ljust(25) +'\n'
                    T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) + '1.004'.ljust(25) +'\n'
                    T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(25) + '1.005'.ljust(25)  + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) + '1.005'.ljust(25) +'\n'
                    T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) + '1.001'.ljust(25) +'\n'
                    T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) +'\n'
                    T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(25) + '1.003'.ljust(25)  + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) + '1.003'.ljust(25) +'\n'
                if '2018' in nameyear:
                    T1 = T1 + 'lumi2018'.ljust(35)+'lnN'.ljust(10) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) + '1.015'.ljust(25) +'\n'
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) + '1.02'.ljust(25) +'\n'
                    T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(25)  + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) +'\n'
                    T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) + '1.002'.ljust(25) +'\n'
                for numsys, namesys in enumerate(sysJecNamesCorr):
                    T1 = T1 +  'jes' + namesys.ljust(32)  +'shape'.ljust(10)  + '1'.ljust(25) +  '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                for numsys, namesys in enumerate(sysJecNamesUnCorr):
                    T1 = T1 + 'Y'+  nameyear + 'jes' + namesys.ljust(27)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                for b in sys:
                    if 'prefiring' in b or 'jer' in b or 'unclusMET' in b or 'bcTagSF' in b:
                        continue 
                    T1 = T1 +  b.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                T1 = T1 + 'Y'+ nameyear + 'jer'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(25)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                T1 = T1 + 'Y'+ nameyear + 'unclusMET'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                T1 = T1 + 'Y'+ nameyear + 'bcTagSF'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                T1 = T1 +  'prefiring'.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) + '1'.ljust(25) +'\n'
                for b in ttSys:
                    bpb= 'tt_' + b
                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'                    
                for b in ttSysOther:
                    bpb= 'tt_' + b
                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
                for b in ttsysCR:
                    bpb= 'tt_' + b
                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
                T1 = T1 + 'ISR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
                T1 = T1 + 'FSR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '1'.ljust(25) + '-'.ljust(25) +'\n'
                for b in SIGsys:
                    bpb= 'Signal_' + b
                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) + '-'.ljust(25) +'\n'
                T1 = T1 + '* autoMCStats 10' + '\n'
                open('CombinedFilesOriginal/' + cardName +'.txt', 'wt').write(T1)
    
    
    
    



