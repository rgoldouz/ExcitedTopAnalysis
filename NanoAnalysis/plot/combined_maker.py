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


year=['2016','2017','2018','All']
LumiErr = [0.025, 0.023, 0.025, 0.018]
regions=["llB1", "llBg1"]
channels=["emu"]
variables=["llM"]
sys = ["eleRecoSf", "eleIDSf", "muIdSf", "muIsoSf", "bcTagSF", "udsgTagSF","pu", "prefiring", "jes", "jer"]
HistAddress = '/user/rgoldouz/NewAnalysis2020/Analysis/hists/'

Samples = ['data.root','WJetsToLNu.root','others.root', 'DY.root', 'TTTo2L2Nu.root', 'ST_tW.root', 'LFVVecC.root', 'LFVVecU.root']
SamplesName = ['Data','Jets','Others', 'DY', 't#bar{t}', 'tW' , 'LFV-vec [c_{e#mutc}=5]', 'LFV-vec [c_{e#mutu}=2]']
SamplesNameCombined = ['data_obs','Jets','Others', 'DY', 'tt', 'tW',  'LfvVectorEmutc', 'LfvVectorEmutu']
NormalizationErr = [0, 0.5, 0.5, 0.3, 0.05, 0.1, 0,0]

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kBlue-3,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kOrange-6, ROOT.kCyan-6]

Hists = []
HistsSysUp = []
HistsSysDown = []
Hists_copy =[]
for numyear, nameyear in enumerate(year):
    l0=[]
    copyl0=[]
    SysUpl0=[]
    SysDownl0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        copyl1=[]
        SysUpl1=[]
        SysDownl1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            copyl2=[]
            SysUpl2=[]
            SysDownl2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                copyl3=[]
                SysUpl3=[]
                SysDownl3=[]
                for numvar, namevar in enumerate(variables):
                    SysUpl4=[]
                    SysDownl4=[]
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
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                l2.append(l3)
                copyl2.append(copyl3)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
            l1.append(l2)
            copyl1.append(copyl2)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
        l0.append(l1)
        copyl0.append(copyl1)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
    Hists.append(l0)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)       
    HistsSysDown.append(SysDownl0)


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
                QscaleHists.append(h)
                del h
                gc.collect()
            for numsys in range(9,110):
                h=sysfile.Get('reweightingSys/emu' +'_' + namereg + '_' + namevar+ '_QscalePDF_'+str(numsys))
                pdfHists.append(h)
                del h
                gc.collect()
            hISRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_8')
            hISRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_6')
            hFSRup = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_9')
            hFSRdown = sysfile.Get('reweightingSys/emu' + '_' + namereg + '_' + namevar+ '_PS_7')
            hCR1 = CR1file.Get('emu' + '_' + namereg + '_' + namevar)
            herd = erdfile.Get('emu' + '_' + namereg + '_' + namevar)
            hTuneCP5up = TuneCP5upfile.Get('emu' + '_' + namereg + '_' + namevar)
            hTuneCP5down = TuneCP5downfile.Get('emu' + '_' + namereg + '_' + namevar)
            hhdampup = hdampupfile.Get('emu' + '_' + namereg + '_' + namevar)
            hhdampdown = hdampdownfile.Get('emu' + '_' + namereg + '_' + namevar)
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
                yvalue.append(QscaleHists[0].GetBinContent(b+1))
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
                yerrupISR.append((abs(max(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrdownISR.append((abs(min(hISRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hISRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrupFSR.append((abs(max(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrdownFSR.append((abs(min(hFSRup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hFSRdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)        
                yerrupCR.append((abs(max(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrdownCR.append((abs(min(herd.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hCR1.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrupTune.append((abs(max(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrdownTune.append((abs(min(hTuneCP5up.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hTuneCP5down.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerruphdamp.append((abs(max(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                yerrdownhdamp.append((abs(min(hhdampup.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1) , hhdampdown.GetBinContent(b+1)- QscaleHists[0].GetBinContent(b+1))))*nomRatio)
                del QS
                del PDF
                del nomRatio
                gc.collect()
            t2Qscale.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupQscale,yerrdownQscale))
            t2Pdf.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupPDF,yerrdownPDF))
            t2ISR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupISR,yerrdownISR))
            t2FSR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupFSR,yerrdownFSR))
            t2CR.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupCR,yerrdownCR))
            t2Tune.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerrupTune,yerrdownTune))
            t2hdamp.append(ROOT.TGraphAsymmErrors(len(bincenter),bincenter,yvalue,binwidth,binwidth,yerruphdamp,yerrdownhdamp))
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
#for numyear, nameyear in enumerate(year):
#    for numreg, namereg in enumerate(regions):
#        if numreg<2:
#            continue
#        for numvar, namevar in enumerate(variables):
#            print nameyear+namereg+namevar
##            draw(pdfGraph[numyear][numreg-2][numvar], 'pdf', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(qscaleGraph[numyear][numreg-2][numvar], 'qs', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(ISRGraph[numyear][numreg-2][numvar], 'isr', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(FSRGraph[numyear][numreg-2][numvar], 'fsr', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(CRGraph[numyear][numreg-2][numvar], 'cr', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(TuneGraph[numyear][numreg-2][numvar], 'tune', 'emu', namereg, nameyear,namevar,variablesName[numvar])
##            draw(hdampGraph[numyear][numreg-2][numvar], 'hdamp', 'emu', namereg, nameyear,namevar,variablesName[numvar])
#            glist = []    
#            glist.append(pdfGraph[numyear][numreg-2][numvar])           
#            glist.append(qscaleGraph[numyear][numreg-2][numvar])
#            glist.append(ISRGraph[numyear][numreg-2][numvar])
#            glist.append(FSRGraph[numyear][numreg-2][numvar])
#            glist.append(CRGraph[numyear][numreg-2][numvar])
#            glist.append(TuneGraph[numyear][numreg-2][numvar])
#            glist.append(hdampGraph[numyear][numreg-2][numvar])
#            compareError(glist, ttSys, 'emu', namereg, nameyear,namevar,variablesName[numvar])        
#            del glist
#            gc.collect()


if not os.path.exists('CombinedFiles'):
    os.makedirs('CombinedFiles')

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        hfile = ROOT.TFile( 'CombinedFiles/' + nameyear+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
        for f in range(len(Samples)):
            Hists[numyear][f][0][numreg][0].SetName(SamplesNameCombined[f])
            Hists[numyear][f][0][numreg][0].Write()
            if f==0:
                continue
            for numsys, namesys in enumerate(sys):
                HistsSysUp[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + '_' + 'Up')
                HistsSysDown[numyear][f][0][numreg][0][numsys].SetName(SamplesNameCombined[f] + '_' + namesys + '_' + 'Down')
                HistsSysUp[numyear][f][0][numreg][0][numsys].Write()
                HistsSysDown[numyear][f][0][numreg][0][numsys].Write()
        for g in range(len(Gttsys)):
            hup = Hists[numyear][4][0][numreg][0].Clone()
            hdown = Hists[numyear][4][0][numreg][0].Clone()
            for b in range(hup.GetNbinsX()):
                hup.SetBinContent(b+1,hup.GetBinContent(b+1) + Gttsys[g][numyear][numreg][0].GetErrorYhigh(b))
                hdown.SetBinContent(b+1,hdown.GetBinContent(b+1) - Gttsys[g][numyear][numreg][0].GetErrorYlow(b))
            hup.SetName(SamplesNameCombined[4] + '_' + ttsys[g] + '_' + 'Up')
            hdown.SetName(SamplesNameCombined[4] + '_' + ttsys[g] + '_' + 'Down')
            hup.Write()
            hdown.Write()
        hfile.Write()
        hfile.Close()
