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

def stackPlots(hists, SignalHists, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    Blinded=False
    if reg=='nAk8G1nTtagG0':
        Blinded=True
    if not os.path.exists('DD' + year):
       os.makedirs('DD' + year)
    if not os.path.exists('DD' + year + '/' + ch):
       os.makedirs('DD' + year + '/' + ch)
    if not os.path.exists('DD' + year + '/' + ch +'/'+reg):
       os.makedirs('DD' + year + '/' + ch +'/'+reg)
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
    pad1.SetLogy(ROOT.kFALSE)

    y_min=0
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
    if Blinded:
        for b in range(dummy_ratio.GetNbinsX()):
            dummy_ratio.SetBinContent(b+1,100)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw()
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    canvas.Print("DD" + year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


#year=['2016','2017','2018','All']
year=['2017']


regions=[
"nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1TtagG0MTs2G300", "nAk8G1nTtag0","nAk8G1nTtag0MTs2G300", "nAk8G1nTtag0XtopMissTagRate", "nAk8G1Ttag0MTs2G300XtopMissTagRate", "nAk81nTtag0XtopMissTagRate"]

scaleSig = [1,1,1,1,1,0.5,40,1,1,1,1,1,1,1]
scaleSigRegion = [500,1,1,1,1,1,1,1,1,1,1,1]
channels=["aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers", "zJets"];
#channels=["aJets"]
variables=["GammaPt","GammaEta","GammaPhi","jet04Pt","jet04Eta","jet04Phi","njet04","nbjet04","jet08Pt","jet08Eta","jet08Phi","njet08","Met","nVtx", "nPh", "phoChargedIso", "dPhiGj08", "drGj08", "HT", "HoE", "softdropMass", "tau21", "tau31", "nbjet08","TvsQCD","njet08massG50","njet08massG120","TsMass1", "nTopTag","masstS2", "Sietaieta","Mll"]

variablesName=["p_{T}(#gamma)","#eta(#gamma)","#Phi(#gamma)","p_{T}(leading jet (AK4))","#eta(leading jet (AK4))","#Phi(leading jet (AK4))","Number of jets (AK4)","Number of b-jets (AK4)","p_{T}(leading jet (AK8))","#eta(leading jet (AK8))","#Phi(leading jet (AK8))","Number of jets (AK8)","MET","Number of vertices","Number of photons","phoChargedIso","#DeltaPhi(#gamma,jet08)", "#DeltaR(#gamma,jet08)", "HT", "H/E", "softdropMass (leading jet (AK8))", "tau21 (leading jet (AK8))", "tau32 (leading jet (AK8))", "num of AK8 jet b-tagged","TvsQCD (leading jet (AK8))", "Number of Ak8 jets with mass > 50","Number of Ak8 jets with mass > 120", "M(#gamma, highest mass AK8)", "N top-tagged ","mass of the second t*","#sigma_{i#eta i#eta}", "Mll"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/hists/'

#Samples = ['data.root','Fake.root', 'Gjets.root','ttG.root','other.root', 'TTga_M0800.root', 'TTga_M1600.root']
Samples = ['data.root','Fake.root', 'Gjets.root','ttG.root','misIDele.root', 'TTga_M0800.root', 'TTga_M1600.root']
SamplesName = ['Data','Non-prompt #gamma','#gamma+jets', 'ttG', 'misIDele', 't*t* (M=0.8TeV) #times 0.5', 't*t* (M=1.6TeV) #times 40']
SamplesNameLatex = ['Data','Non-prompt #gamma','Gjets', 'ttG', 'misIDele', 't*t* (M=0.8TeV)', 't*t* (M=1.6TeV)']

colors =  [ROOT.kBlack,ROOT.kYellow,ROOT.kGreen,ROOT.kRed-4, ROOT.kBlue+8,ROOT.kOrange-3, ROOT.kBlack, ROOT.kGreen+3,ROOT.kViolet, ROOT.kBlue-9, ROOT.kYellow-2]
bins = array( 'd',[0.0,100.0,200.0,300.0,400.0,500.0,700.0, 1000.0] )


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
                    print Samples[f] + namech + namereg + namevar
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    if 'jet08Pt' in namevar:
                        h=h.Rebin(len(bins)-1,"",bins)
                    if 'TTga' in Samples[f]:
                       h.Scale(scaleSig[f])
                       h.Scale(scaleSigRegion[numreg])
#                    if 'Gjets' in Samples[f]:
#                       h.Scale(1.84)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

#"nAk8G0", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1MLPG0p8", "nAk8G1MLPG0p8TtagG0", "nAk8G1MLPG0p8TtagG0MassTs2G300", "nAk81MLPG0p8TtagG0","nAk81","nAk8G1"
data1jet = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81")][variables.index("jet08Pt")].Clone()
data1jet1tag = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
Top1jet1tag = Hists[0][Samples.index("ttG.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
data1jet1tag.Add(Top1jet1tag,-1)
data1jet1tag.Add(Hists[0][Samples.index("misIDele.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")],-1)
data1jet1tag.Divide(data1jet)
draw1dHist(  data1jet1tag, 'topMistagRate','topMistagRate','topMistagRate' )
data1jet1tag.SetName('topMistagRate')

DYdata1jet = Hists[0][Samples.index("data.root")][channels.index("zJets")][regions.index("nAk81")][variables.index("jet08Pt")].Clone()
DYdata1jet1tag = Hists[0][Samples.index("data.root")][channels.index("zJets")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
DYTop1jet1tag = Hists[0][Samples.index("Fake.root")][channels.index("zJets")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
DYdata1jet1tag.Add(DYTop1jet1tag,-1)
DYdata1jet1tag.Divide(DYdata1jet)
draw1dHist(  DYdata1jet1tag, 'topMistagRateDY','topMistagRateDY','topMistagRateDY' )
DYdata1jet1tag.SetName('topMistagRateDY')

Fakedata1jet = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81")][variables.index("jet08Pt")].Clone()
Fakedata1jet.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81")][variables.index("jet08Pt")])
Fakedata1jet.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81")][variables.index("jet08Pt")])
Fakedata1jet1tag = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
Fakedata1jet1tag.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
Fakedata1jet1tag.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
Top1jet1tag =Hists[0][Samples.index("misIDele.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")].Clone()
Top1jet1tag.Add(Hists[0][Samples.index("misIDele.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
Top1jet1tag.Add(Hists[0][Samples.index("misIDele.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][variables.index("jet08Pt")])
Fakedata1jet1tag.Add(Top1jet1tag,-1)
Fakedata1jet1tag.Divide(Fakedata1jet)
draw1dHist(  Fakedata1jet1tag, 'topMistagRateFake','topMistagRateFake','topMistagRateFake' )
Fakedata1jet1tag.SetName('topMistagRateFake')
compareNeffHist([data1jet1tag, Fakedata1jet1tag], ['Gamma+1jet', 'FakeG+jet'], label_name="jet08Pt", can_name="MTRate")

hfile = ROOT.TFile( 'topMistagRate.root', 'RECREATE', 'mis top tag rate histogram' )
data1jet1tag.Write()
DYdata1jet1tag.Write()
Fakedata1jet1tag.Write()
hfile.Write()
hfile.Close()

#for numvar, namevar in enumerate(variables):
#    data1nAK4jet = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81")][variables.index(namevar)].Clone()
#    data1nAK4jet1tag = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index(namevar)].Clone()
#    Top1nAK4jet1tag = Hists[0][Samples.index("ttG.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][variables.index(namevar)].Clone()
#    data1nAK4jet1tag.Add(Top1nAK4jet1tag,-1)
#    data1nAK4jet1tag.Divide(data1nAK4jet)
#    draw1dHist(  data1nAK4jet1tag, 'topMistagRate' + namevar,'topMistagRatenAK4'+ namevar,'topMistagRatenAK4'+ namevar )

#Data Driven Gamma Jet
###for numvar, namevar in enumerate(variables):
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar] = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1nTtag0XtopMissTagRate")][numvar]
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar].SetFillColor(colors[Samples.index("Gjets.root")])
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar].SetLineColor(colors[Samples.index("Gjets.root")])
###
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar] = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk8G1Ttag0MTs2G300XtopMissTagRate")][numvar]
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].SetFillColor(colors[Samples.index("Gjets.root")])
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].SetLineColor(colors[Samples.index("Gjets.root")])
###
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar] = Hists[0][Samples.index("data.root")][channels.index("aJets")][regions.index("nAk81nTtag0XtopMissTagRate")][numvar]
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar].SetFillColor(colors[Samples.index("Gjets.root")])
###    Hists[0][Samples.index("Gjets.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar].SetLineColor(colors[Samples.index("Gjets.root")])
###
####Data Driven Fake photon
###    hDataCR1 = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1nTtagG0")][numvar].Clone()
###    hDataCR1.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1nTtagG0")][numvar])
###    hDataCR1.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1nTtagG0")][numvar])
###    hDataCR1.Scale(0.022/(1-0.022))
###    hGjetsCR1 = Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1nTtagG0")][numvar].Clone()
###    hGjetsCR1.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1nTtagG0")][numvar])
###    hGjetsCR1.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1nTtagG0")][numvar])
###    hGjetsCR1.Scale(0.022/(1-0.022))
###    hDataCR1.Add(hGjetsCR1,-1)
###    hDataCR1.SetFillColor(colors[Samples.index("Fake.root")])
###    hDataCR1.SetLineColor(colors[Samples.index("Fake.root")])
###    Hists[0][Samples.index("Fake.root")][channels.index("aJets")][regions.index("nAk8G1nTtagG0")][numvar] = hDataCR1
###
###    hDataCR2 = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].Clone()
###    hDataCR2.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
###    hDataCR2.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
###    hDataCR2.Scale(0.022/(1-0.022))
###    hGjetsCR2 = Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk8G1TtagG0MTs2G300")][numvar].Clone()
###    hGjetsCR2.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
###    hGjetsCR2.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk8G1TtagG0MTs2G300")][numvar])
###    hGjetsCR2.Scale(0.022/(1-0.022))
###    hDataCR2.Add(hGjetsCR2,-1)
###    hDataCR2.SetFillColor(colors[Samples.index("Fake.root")])
###    hDataCR2.SetLineColor(colors[Samples.index("Fake.root")])
###    Hists[0][Samples.index("Fake.root")][channels.index("aJets")][regions.index("nAk8G1TtagG0MTs2G300")][numvar] = hDataCR2
###
###    hDataCR3 = Hists[0][Samples.index("data.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][numvar].Clone()
###    hDataCR3.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][numvar])
###    hDataCR3.Add(Hists[0][Samples.index("data.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][numvar])
###    hDataCR3.Scale(0.022/(1-0.022))
###    hGjetsCR3 = Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsIso")][regions.index("nAk81nTtag1")][numvar].Clone()
###    hGjetsCR3.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsSiSi")][regions.index("nAk81nTtag1")][numvar])
###    hGjetsCR3.Add(Hists[0][Samples.index("Gjets.root")][channels.index("fakeAJetsOthers")][regions.index("nAk81nTtag1")][numvar])
###    hGjetsCR3.Scale(0.022/(1-0.022))
###    hDataCR3.Add(hGjetsCR3,-1)
###    hDataCR3.SetFillColor(colors[Samples.index("Fake.root")])
###    hDataCR3.SetLineColor(colors[Samples.index("Fake.root")])
###    Hists[0][Samples.index("Fake.root")][channels.index("aJets")][regions.index("nAk81nTtag1")][numvar] = hDataCR3

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


