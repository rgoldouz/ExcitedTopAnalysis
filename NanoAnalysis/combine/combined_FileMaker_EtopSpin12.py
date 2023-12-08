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

def SumofWeight(add):
    genEventSumw = 0
    genEventSumwScale = [0]*9
    genEventSumwPdf = [0]*100
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

bins = array( 'd',[300,500,700,900,1100,1300,1500,1750,2000,2500,3000] )
year=['2016preVFP', '2016postVFP', '2017','2018']
ULyear=['UL16preVFP', 'UL16postVFP', 'UL17','UL18']
year=['2017']
#ULyear=['UL17']
LumiErr = [0.018, 0.018, 0.018, 0.018]
regions=["nAk8G1nTtagG0","nAk8G1nTtag0XtopMissTagRate"]
scaleSig = [1,1,1,1,1,0.5,40,1,1,1,1,1,1,1]
channels=["aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"];
regionsCombined = ['SR']
variables=["TsMass1"]
sys = ["phIDSf", "pu", "prefiring","photonEScale","photonESmear"]
sysJec= ["AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]
sysJecNames=[
"AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta"]
sysJecNamesUnCorr = ["AbsoluteStat","RelativePtEC1","RelativePtEC2","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","TimePtEta"]
sysJecNamesCorr =["AbsoluteMPFBias","AbsoluteScale","FlavorQCD","Fragmentation","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtHF","RelativeBal","RelativeStatFSR","RelativeStatHF"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

Samples = ['data.root','ttG.root','Other.root',
'TTga_M700.root',
'TTga_M800.root',
'TTga_M1000.root',
'TTga_M1200.root',
'TTga_M1300.root',
'TTga_M1400.root',
'TTga_M1500.root',
'TTga_M1600.root',
]

SamplesNameCombined = ['data_obs','ttG','Other_prompt_Ph',
'TTga_M700',
'TTga_M800',
'TTga_M1000',
'TTga_M1200',
'TTga_M1300',
'TTga_M1400',
'TTga_M1500',
'TTga_M1600',
]
NormalizationErr = [0, 0.5, 0.5, 0.3, 0.05, 0.1, 0,0,0,0,0,0, 0,0,0,0,0,0]

SignalSamples=[
'TTga_M700',
'TTga_M800',
'TTga_M1000',
'TTga_M1200',
'TTga_M1300',
'TTga_M1400',
'TTga_M1500',
'TTga_M1600',
]

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, 
ROOT.kBlue, ROOT.kBlue-7, ROOT.kViolet, ROOT.kViolet-5,ROOT.kAzure-9, ROOT.kAzure+10,
ROOT.kGreen, ROOT.kGreen+2, ROOT.kTeal-9, ROOT.kTeal+10, ROOT.kSpring-7, ROOT.kSpring+9,
ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6,
ROOT.kBlue, ROOT.kBlue-7, ROOT.kViolet, ROOT.kViolet-5,ROOT.kAzure-9, ROOT.kAzure+10,
ROOT.kGreen, ROOT.kGreen+2, ROOT.kTeal-9, ROOT.kTeal+10, ROOT.kSpring-7, ROOT.kSpring+9
]

Hists = []
HistsDataUp=[]
HistsDataDown=[]
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
    l0DataUp=[]
    l0DataDown=[]
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
        l1DataUp=[]
        l1DataDown=[]
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
        for numch, namech in enumerate(channels):
            l2=[]
            l2DataUp=[]
            l2DataDown=[]
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
                l3DataUp=[]
                l3DataDown=[]
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
                    h= Files[f].Get('promptG_'+namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
#                    h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                    for b in range(h.GetNbinsX()):
                        if h.GetBinContent(b+1)<0:
                            h.SetBinContent(b+1,0)
                        if h.GetBinContent(b+1)==h.GetBinError(b+1):
                            h.SetBinContent(b+1,0)
                            h.SetBinError(b+1,0)               
                    h=h.Rebin(len(bins)-1,"",bins)
                    l3.append(h)
                    copyl3.append(h.Clone())
                    if namech!="aJets":
                        continue
                    if 'data' in Samples[f]:
                        print namech + '_' + namereg + '_' + namevar+ '_missTagRate_Up'
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_missTagRate_Up')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
                        h=h.Rebin(len(bins)-1,"",bins)
                        l3DataUp.append(h)
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_missTagRate_Down')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
                        h=h.Rebin(len(bins)-1,"",bins)
                        l3DataDown.append(h)
                        continue
                    for numsys, namesys in enumerate(sys):
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        h=h.Rebin(len(bins)-1,"",bins)
                        SysUpl4.append(h)
                        h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                        h.SetFillColor(colors[f])
                        h.SetLineColor(colors[f])
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        h=h.Rebin(len(bins)-1,"",bins)
                        SysDownl4.append(h)
                    for numsys, namesys in enumerate(sysJecNames):
                        if namereg!="nAk8G1nTtagG0":
                            continue
                        h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        h=h.Rebin(len(bins)-1,"",bins)
                        JecUpl4.append(h)
                        h= Files[f].Get("JECSys/"+ namereg + '/' + namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
#                        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
                        for b in range(h.GetNbinsX()):
                            if h.GetBinContent(b+1)<0:
                                h.SetBinContent(b+1,0)
                            if h.GetBinContent(b+1)==h.GetBinError(b+1):
                                h.SetBinContent(b+1,0)
                                h.SetBinError(b+1,0)
                        h=h.Rebin(len(bins)-1,"",bins)
                        JecDownl4.append(h)
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                    JecUpl3.append(JecUpl4)
                    JecDownl3.append(JecDownl4)
                    if 'TTga' not in Samples[f] or namereg!="nAk8G1nTtagG0":
                        continue
                    #print '/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL' + nameyear[2:]+ '/v1/UL' + nameyear[2:]+"_"+ Samples[f].split(".")[0]
                    SWscale, SWpdf =  SumofWeight('/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL' + nameyear[2:]+ '/v1/UL' + nameyear[2:]+"_"+ Samples[f].split(".")[0])
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
                    t3QscaleUp.append(t4Qscale[0])
                    t3QscaleDown.append(t4Qscale[1])
                    t3PdfUp.append(Pdf_hcUp)
                    t3PdfDown.append(Pdf_hcDown)
                l2.append(l3)
                l2DataUp.append(l3DataUp)
                l2DataDown.append(l3DataDown)
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
            l1DataUp.append(l2DataUp)
            l1DataDown.append(l2DataDown)
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
        l0DataUp.append(l1DataUp)
        l0DataDown.append(l1DataDown)
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
    HistsDataUp.append(l0DataUp)
    HistsDataDown.append(l0DataDown)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)       
    HistsSysDown.append(SysDownl0)
    HistsJecUp.append(JecUpl0)
    HistsJecDown.append(JecDownl0)
    HistsPdfUp.append(t0PdfUp)
    HistsPdfDown.append(t0PdfDown)
    HistsQscaleUp.append(t0QscaleUp)
    HistsQscaleDown.append(t0QscaleDown)


fakeEleHists=[]
for numyear, nameyear in enumerate(year):
    FF=ROOT.TFile.Open(HistAddress + nameyear+ '_Other.root')
    h= FF.Get('fakeGEle_aJets_nAk8G1nTtagG0_TsMass1')
    for b in range(h.GetNbinsX()):
        if h.GetBinContent(b+1)<0:
            h.SetBinContent(b+1,0)
        if h.GetBinContent(b+1)==h.GetBinError(b+1):
            h.SetBinContent(b+1,0)
            h.SetBinError(b+1,0)
    h=h.Rebin(len(bins)-1,"",bins)
    fakeEleHists.append(h)

#Data Driven Gamma Jet
for numvar, namevar in enumerate(variables):
#    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar] = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1Ttag0MTs2G300XtopMissTagRate")][numvar]
#    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].SetFillColor(colors[Samples.index("Gjets.root")])
#    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].SetLineColor(colors[Samples.index("Gjets.root")])
#Data Driven Fake photon
#    hDataCR2 = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].Clone()
#    hDataCR2.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
#    hDataCR2.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
#    hDataCR2.Scale(0.022/(1-0.022))
#    hGjetsCR2 = Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].Clone()
#    hGjetsCR2.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
#    hGjetsCR2.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
#    hGjetsCR2.Scale(0.022/(1-0.022))
#    hDataCR2.Add(hGjetsCR2,-1)
#    hDataCR2.SetFillColor(colors[Samples.index("Fake.root")])
#    hDataCR2.SetLineColor(colors[Samples.index("Fake.root")])
#    Hists[0][Samples.index("Fake.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar] = hDataCR2

    hDataCR1 = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1nTtagG0")][numvar].Clone()
    hDataCR1.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1nTtagG0")][numvar])
    hDataCR1.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1nTtagG0")][numvar])
    hDataCR1.Scale(0.022/(1-0.022))
    print str(hDataCR1.Integral())
    FF=ROOT.TFile.Open(HistAddress + '2017_Gjets.root')
    hGjetsCR1 =  FF.Get("promptG_fakeAJetsIso_nAk8G1nTtagG0_"+namevar)
    hGjetsCR1.Add(FF.Get("promptG_fakeAJetsSiSi_nAk8G1nTtagG0_"+namevar))
    hGjetsCR1.Add(FF.Get("promptG_fakeAJetsOthers_nAk8G1nTtagG0_"+namevar))
    hGjetsCR1.Scale(0.022/(1-0.022))
    hDataCR1.Add(hGjetsCR1,-1)

if not os.path.exists('CombinedFilesETop'):
    os.makedirs('CombinedFilesETop')
#else:
#    os.system('rm -rf CombinedFilesETop/'+ wcName +'_*')

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regionsCombined):
            if namereg!="nAk8G1nTtagG0" and namech!="aJets":
                continue
            hfile = ROOT.TFile( 'CombinedFilesETop/' + nameyear+'_'+namech+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
            hDataCR1.SetName('Fake_jet')
            hDataCR1.Write()
            Hists[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].SetName('Gjets')
            Hists[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].Write()
            HistsDataUp[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].SetName('Gjets_' + 'Y'+ nameyear + 'missTagRateUp')
            HistsDataUp[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].Write()
            HistsDataDown[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].SetName('Gjets_' + 'Y'+ nameyear + 'missTagRateDown')
            HistsDataDown[numyear][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].Write()
            fakeEleHists[numyear].SetName('Fake_ele')
            fakeEleHists[numyear].Write()
            for f in range(len(Samples)):
                Hists[numyear][f][numch][numreg][0].SetName(SamplesNameCombined[f])
                Hists[numyear][f][numch][numreg][0].Write()
                if f<1:
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
                    print namesys
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
#    #Signal Modeling
                if 'TTga' not in Samples[f]:
                        continue
                print  Samples[f]
                HistsPdfUp[numyear][f][numch][numreg][numvar].SetName(SamplesNameCombined[f] + '_PDFUp')
                HistsPdfDown[numyear][f][numch][numreg][numvar].SetName(SamplesNameCombined[f] + '_PDFDown')
                HistsQscaleUp[numyear][f][numch][numreg][numvar].SetName(SamplesNameCombined[f] + '_QScaleUp')
                HistsQscaleDown[numyear][f][numch][numreg][numvar].SetName(SamplesNameCombined[f] + '_QScaleDown')
                HistsPdfUp[numyear][f][numch][numreg][numvar].Write()
                HistsPdfDown[numyear][f][numch][numreg][numvar].Write()
                HistsQscaleUp[numyear][f][numch][numreg][numvar].Write()
                HistsQscaleDown[numyear][f][numch][numreg][numvar].Write()
#            for f in range(5,len(Samples)):
#                for g in range(len(GSIGsys)):
#                    hup = Hists[numyear][f][numch][numreg][0].Clone()
#                    hdown = Hists[numyear][f][numch][numreg][0].Clone()
#                    for b in range(hup.GetNbinsX()):
#    #                print nameyear + namereg + ttsys[g] + str(hup.GetBinContent(b+1)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYhigh(b)) + '  ' + str(Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
#                        hup.SetBinContent(b+1,hup.GetBinContent(b+1) + GSIGsys[g][f-5][numyear][numch][numreg][0].GetErrorYhigh(b))
#                        hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - GSIGsys[g][f-5][numyear][numch][numreg][0].GetErrorYlow(b))
#                    if 'TT' in SamplesNameCombined[f]:
#                        hup.SetName(SamplesNameCombined[f] + '_tt_' + SIGsys[g] + 'Up')
#                        hdown.SetName(SamplesNameCombined[f] + '_tt_' + SIGsys[g] + 'Down')
#                    else:
#                        hup.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Up')
#                        hdown.SetName(SamplesNameCombined[f] + '_Signal_' + SIGsys[g] + 'Down')
#                    hup.Write()
#                    hdown.Write()
#            for f in range(5,len(Samples)):
#                hISRupNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_0')
#                hISRup = TH1EFTtoTH1(hISRupNormal,wc1)
#                hISRup.SetName(SamplesNameCombined[f] + '_ISRUp')
#                hISRup.Write()
#                hISRdownNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_2')
#                hISRdown= TH1EFTtoTH1(hISRdownNormal,wc1)
#                hISRdown.SetName(SamplesNameCombined[f] + '_ISRDown')
#                hISRdown.Write()
#                hFSRupNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_1')
#                hFSRup= TH1EFTtoTH1(hFSRupNormal,wc1)
#                hFSRup.SetName(SamplesNameCombined[f] + '_FSRUp')
#                hFSRup.Write()
#                hFSRdownNormal = SigInputFiles[f-5].Get('reweightingSys/' + namech + '_' + namereg + '_' + namevar+ '_PS_3')
#                hFSRdown = TH1EFTtoTH1(hFSRdownNormal,wc1)
#                hFSRdown.SetName(SamplesNameCombined[f] + '_FSRDown')
#                hFSRdown.Write()
#    #add MC stat error
##            for f in range(len(Samples)):
##                if f==0:
##                    continue
##                stat=[]
##                for b in range(Hists[numyear][f][0][numreg][0].GetNbinsX()):
##                    if Hists[numyear][f][0][numreg][0].GetBinContent(b+1)==0:
##                        continue
##                    HstatUp = Hists[numyear][f][0][numreg][0].Clone()
##                    HstatUp.SetBinContent(b+1,HstatUp.GetBinContent(b+1) + HstatUp.GetBinError(b+1))
##                    HstatUp.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Up')
##    #                HstatUp.Write()
##                    HstatDown = Hists[numyear][f][0][numreg][0].Clone()
##                    HstatDown.SetBinContent(b+1,HstatDown.GetBinContent(b+1) - HstatDown.GetBinError(b+1))
##                    if HstatDown.GetBinContent(b+1) < 0.001:
##                        HstatDown.SetBinContent(b+1,0.001)
##                    HstatDown.SetName(SamplesNameCombined[f]+ '_' + 'Y'+ nameyear + namereg + SamplesNameCombined[f]+'StatBin' +str(b+1)+ 'Down')
##    #                HstatDown.Write()
##                    stat.append('Y' + nameyear+namereg+SamplesNameCombined[f]+'StatBin' +str(b+1))
##                statName[ nameyear + namereg + SamplesNameCombined[f]]=stat
            hfile.Write()
            hfile.Close()

#'data_obs','Fake','Gjets','ttG','Others'
for valueD, namesig  in enumerate(SignalSamples):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regionsCombined):
                if namereg!="nAk8G1TtagG0" and namech!="aJets":
                    continue
                cardName = namesig+'_'+namech+'_'+nameyear+'_' + namereg
                Sid0= Samples.index(namesig + '.root')
#                Sid1= Samples.index(valueD[1] + '.root')
                T1 = 'max 1 number of categories \n' +\
                     'jmax 5 number of samples minus one\n' +\
                     'kmax * number of nuisance parameters\n' +\
                     '------------\n'+\
                     'shapes * * '  + nameyear+'_'+namech+'_'+namereg+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n' +\
                     '------------\n'+\
                     'bin'.ljust(45) + cardName + '\n'+\
                     'observation'.ljust(45) + str(Hists[numyear][0][numch][numreg][0].Integral()) +'\n'+\
                     '------------\n'+\
                     'bin'.ljust(45) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40)+ cardName.ljust(40) +'\n'+\
                     'process'.ljust(45) + '0'.ljust(40) + '1'.ljust(40) + '2'.ljust(40) + '3'.ljust(40) + '4'.ljust(40) + '5'.ljust(40) +'\n'+\
                     'process'.ljust(45) + namesig.ljust(40)+ SamplesNameCombined[1].ljust(40) + SamplesNameCombined[2].ljust(40) +\
                     'Gjets'.ljust(40) + 'Fake_jet'.ljust(40) + 'Fake_ele'.ljust(40) +'\n'+\
                     'rate'.ljust(45) + str(Hists[numyear][Sid0][numch][numreg][0].Integral()).ljust(40) + str(Hists[numyear][1][numch][numreg][0].Integral()).ljust(40) + str(Hists[numyear][2][numch][numreg][0].Integral()).ljust(40)+\
                     str(Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar].Integral()).ljust(40)+\
                     str(hDataCR1.Integral()).ljust(40) + str(fakeEleHists[numyear].Integral()).ljust(40) + '\n'+\
                     '------------\n'+\
                     'Fake_jet_norm'.ljust(35)+'lnN'.ljust(10)  + '-'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.5'.ljust(40) + '-'.ljust(40) + '\n'+\
                     'Fake_ele_norm'.ljust(35)+'lnN'.ljust(10)  + '-'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.3'.ljust(40) + '\n'+\
                     'Gjets_norm'.ljust(35)+'lnN'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.3'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'+\
                     'ttG_norm'.ljust(35)+'lnN'.ljust(10)  + '-'.ljust(40) + '1.15'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40)+ '\n'+\
                     'trigg'.ljust(35)+'lnN'.ljust(10)  + '1.05'.ljust(40) + '1.05'.ljust(40) +  '1.05'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.05'.ljust(40)+'\n' 
                if '2016' in nameyear:
                    T1 = T1 + 'lumi2016'.ljust(35)+'lnN'.ljust(10) + '1.022'.ljust(40) + '1.022'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.022'.ljust(40)  +'\n'    
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.009'.ljust(40) + '1.009'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.009'.ljust(40)  + '\n'
                    T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(40) + '1.004'.ljust(40) + '-'.ljust(40)  + '-'.ljust(40) + '1.004'.ljust(40)  + '\n'
                    T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(40) + '1.005'.ljust(40) + '-'.ljust(40)+ '-'.ljust(40) + '1.005'.ljust(40) +'\n'
                    T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(40) + '1.004'.ljust(40) + '-'.ljust(40)  + '-'.ljust(40) + '1.004'.ljust(40)  +'\n'
                if '2017' in nameyear:
                    T1 = T1 + 'lumi2017'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.02'.ljust(40)  +'\n'
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.008'.ljust(40) + '1.008'.ljust(40) + '1.008'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.008'.ljust(40)  +'\n'
                    T1 = T1 + 'lumiBBDef'.ljust(35)+'lnN'.ljust(10) + '1.004'.ljust(40) + '1.004'.ljust(40) + '1.004'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.004'.ljust(40) + '\n'
                    T1 = T1 + 'lumiDynamicB'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(40)+ '1.005'.ljust(40)+ '1.005'.ljust(40) + '-'.ljust(40)  + '-'.ljust(40) + '1.005'.ljust(40)  +'\n'
                    T1 = T1 + 'lumiGhostS'.ljust(35)+'lnN'.ljust(10) + '1.001'.ljust(40) + '1.001'.ljust(40)+ '1.001'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '1.001'.ljust(40)  +'\n'
                    T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(40)+ '1.003'.ljust(40)+ '1.003'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '1.003'.ljust(40)  + '\n'
                    T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.003'.ljust(40)+ '1.003'.ljust(40)+ '1.003'.ljust(40) + '-'.ljust(40)  + '-'.ljust(40) + '1.003'.ljust(40)  + '\n'
                if '2018' in nameyear:
                    T1 = T1 + 'lumi2018'.ljust(35)+'lnN'.ljust(10) + '1.015'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.015'.ljust(40)  + '\n'
                    T1 = T1 + 'lumiXY'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.02'.ljust(40) + '\n'
                    T1 = T1 + 'lumiLengthS'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '1.002'.ljust(40)  + '\n'
                    T1 = T1 + 'lumiBeamCC'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.002'.ljust(40)  + '\n'
                for numsys, namesys in enumerate(sysJecNamesCorr):
                    T1 = T1 +  'jes' + namesys.ljust(32)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) +  '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '\n'
                for numsys, namesys in enumerate(sysJecNamesUnCorr):
                    T1 = T1 + 'Y'+  nameyear + 'jes' + namesys.ljust(27)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) +  '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '\n'
                for b in sys:
                    if 'jer' in b or 'unclusMET' in b or 'bcTagSF' in b:
                        continue 
                    T1 = T1 +  b.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) +  '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
                T1 = T1 + 'Y'+ nameyear + 'missTagRate'.ljust(30)+'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
                T1 = T1 + 'PDF'.ljust(30)+'shape'.ljust(10)  + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
                T1 = T1 + 'QScale'.ljust(30)+'shape'.ljust(10)  + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
#                T1 = T1 + 'Y'+ nameyear + 'jer'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#                T1 = T1 + 'Y'+ nameyear + 'unclusMET'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#                T1 = T1 + 'Y'+ nameyear + 'bcTagSF'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#                T1 = T1 +  'prefiring'.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#                for b in ttSys:
#                    bpb= 'tt_' + b
#                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'                    
#                for b in ttSysOther:
#                    bpb= 'tt_' + b
#                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#                for b in ttsysCR:
#                    bpb= 'tt_' + b
#                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#                T1 = T1 + 'ISR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#                T1 = T1 + 'FSR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#                for b in SIGsys:
#                    bpb= 'Signal_' + b
#                    T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
                T1 = T1 + '* autoMCStats 10' + '\n'
                open('CombinedFilesETop/' + cardName +'.txt', 'wt').write(T1)
    
    
    
    



