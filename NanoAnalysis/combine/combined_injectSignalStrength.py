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

def compare3Hist(A, B, C, textA="A", textB="B", textC="C",label_name="sample", can_name="can"):

    canvas = ROOT.TCanvas(can_name,can_name,10,10,1100,628)
    canvas.SetRightMargin(0.15)
    canvas.cd()

    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0.05, 0.3, 1, 0.99 , 0)
    pad1.Draw()
    pad1.SetLogy()
    pad2=ROOT.TPad(pad_name, pad_name, 0.05, 0.05, 1, 0.3 , 0)
    pad2.SetGridy();
    pad2.Draw()
    pad1.cd()

    A.SetLineColor( 1 )
    B.SetLineColor( 2 )
    C.SetLineColor( 4 )

    A.SetTitle(can_name)
    A.GetXaxis().SetTitle('BDT output')
    A.GetYaxis().SetTitle('Event ')
    A.GetXaxis().SetTitleSize(0.05)
    A.GetYaxis().SetTitleSize(0.05)
    A.SetMaximum(1.2*max(A.GetMaximum(),B.GetMaximum(),C.GetMaximum()));
    A.SetMinimum(0.1);
    A.GetYaxis().SetTitleOffset(0.7)
    A.Draw()
    B.Draw('esame')
    C.Draw('esame')

    legend = ROOT.TLegend(0.7,0.75,1,1)
    legend.AddEntry(A ,textA,'l')
    legend.AddEntry(B ,textB,'l')
    legend.AddEntry(C ,textC,'l')
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend.Draw("same")

    pad2.cd()
    ratioB = A.Clone()
    ratioB.Divide(B)
    ratioB.SetLineColor( 2 )
    ratioB.SetMaximum(1.2)
    ratioB.SetMinimum(0.98)
    r = ratioB.Clone()
    fontScale = 2
    nbin = ratioB.GetNbinsX()
    x_min= ratioB.GetBinLowEdge(1)
    x_max= ratioB.GetBinLowEdge(nbin)+ratioB.GetBinWidth(nbin)
#    ratio_y_min=0.95*r.GetBinContent(r.FindFirstBinAbove(0))
#    ratio_y_max=1.05*r.GetBinContent(r.GetMaximumBin())
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,0.8,1.2)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Ratio')
    dummy_ratio.GetXaxis().SetTitle("")
    dummy_ratio.GetXaxis().SetTitleSize(0.05*fontScale)
    dummy_ratio.GetXaxis().SetLabelSize(0.05*fontScale)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetYaxis().SetNdivisions(505)
    dummy_ratio.GetYaxis().SetTitleSize(0.07*fontScale)
    dummy_ratio.GetYaxis().SetLabelSize(0.05 *fontScale)
    dummy_ratio.GetYaxis().SetTitleOffset(0.3)
    dummy_ratio.Draw()
    ratioB.Draw("esame")

    ratioC = A.Clone()
    ratioC.Divide(C)
    ratioC.SetLineColor( 4 )
    ratioC.Draw("esame")

    canvas.Print("3H_" + can_name + ".png")
    del canvas
    gc.collect()

#year=['2016','2017','2018']
year=['2016']
regions=["llB1", "llBg1"]

#f1 = ROOT.TFile.Open('CombinedFiles/2018_llB1.root')
#f1.cd()
##my_list = ROOT.gDirectory.GetList()
#my_list = f1.GetListOfKeys()
#
#Hists=[]
#HistsDraw=[]
#nominalHists=['tt','LfvVectorEmutc', 'LfvVectorEmutu']
nominalHists=['tW']
#for obj in my_list: # obj is TKey
#    if obj.GetClassName() == "TH1F":
#        Hists.append(obj.GetName())
##        print obj.GetName()

injectStrength=0.5
SamplesNameBG = ['Jets','Others', 'DY', 'tt', 'tW']
#SamplesNameSig = ['LfvVectorEmutc', 'LfvVectorEmutu', 'LfvScalarEmutc', 'LfvScalarEmutu', 'LfvTensorEmutc', 'LfvTensorEmutu']
#SignalSamples = ['LFVVecC', 'LFVVecU', 'LFVScalarC', 'LFVScalarU', 'LFVTensorC', 'LFVTensorU']
SamplesNameSig = [ 'LfvVectorEmutu']
SSN = 'LFVVecU'
Asimov = ROOT.TH1F()
data = ROOT.TH1F()

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        f1 = ROOT.TFile.Open('CombinedFiles/' + nameyear + '_' + namereg +'.root')
        fOut = ROOT.TFile( 'CombinedFilesAsimov/' + nameyear+'_'+namereg+ 'mu'+ str(injectStrength) +'.root', 'RECREATE', 'injectStrength' )
        my_list = f1.GetListOfKeys()
        Hists=[]
        HistsDraw=[]
        for obj in my_list: # obj is TKey
            if obj.GetClassName() == "TH1F":
                Hists.append(obj.GetName())
        for n,H in enumerate(Hists):
            HH = f1.Get(H)
            if n==0:
                Asimov=HH.Clone()
                for b in range(Asimov.GetNbinsX()):
                    Asimov.SetBinContent(b+1,0)
            if H.split('_')[0] in SamplesNameBG:
                HH.Write()
            if H.split('_')[0] in SamplesNameSig:
#                HH.Scale(injectStrength)
                HH.Write()
            if len(H.split('_'))==1 and 'data' not in H and 'Lfv' not in H:
                print H
                Asimov.Add(HH)
            if 'data' in  H:
                data = HH
            if len(H.split('_'))==1 and H.split('_')[0] in SamplesNameSig:
                Hscale = HH.Clone()
                Hscale.Scale(injectStrength)
                Asimov.Add(Hscale)
        for b in range(Asimov.GetNbinsX()):
            if(data.GetBinContent(b+1)==0):
                Asimov.SetBinContent(b+1,0)
        Asimov.SetName('data_obs')
        Asimov.Write()
        f1.Close()
        fOut.Close()

        fileR = open('CombinedFiles/' + SSN +'_'+nameyear+'_' + namereg + '.txt',"r") 
        Read = fileR.readlines()
        fileW = open('CombinedFilesAsimov/' + SSN+'_'+nameyear+'_' + namereg + 'mu'+ str(injectStrength)+ '.txt',"w+")
        for x in Read:
            if 'observation' in x:
                SS = 'observation'.ljust(45) + str(Asimov.Integral()) + '\n'
                fileW.write(SS)
            elif '.root' in x:
                fileW.write('shapes * * '  + nameyear+'_'+namereg+'mu'+ str(injectStrength)+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n')
            else:
                fileW.write(x)
        fileR.close()
        fileW.close()
  
             
