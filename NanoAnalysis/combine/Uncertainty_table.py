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

    A.SetTitle("")
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

    Label_channel = ROOT.TLatex(0.15,0.8,can_name.split('_')[0])
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")
    Label_channel2 = ROOT.TLatex(0.15,0.65,'#color[2]{'+can_name.split('_')[-1]+'}')
    Label_channel2.SetNDC()
    Label_channel2.SetTextFont(42)
    Label_channel2.SetTextSize(0.085)
    Label_channel2.Draw("same")

    pad2.cd()
    ratioB = B.Clone()
    ratioB.Divide(A)
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
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,0.5,1.5)
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

    ratioC = C.Clone()
    ratioC.Divide(A)
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
nominalHists=['tt','LFVTtVecU','LFVStVecU']
#nominalHists=['tt']
#for obj in my_list: # obj is TKey
#    if obj.GetClassName() == "TH1F":
#        Hists.append(obj.GetName())
##        print obj.GetName()

#f1 = ROOT.TFile.Open('CombinedFiles/AllHistsAdded_sysTable.root')

StatError = True
f1 = ROOT.TFile.Open('CombinedFiles/AllHistsAdded_sysTable2018.root')
my_list = f1.GetListOfKeys()
Hists=[]
HistsDraw=[]
for obj in my_list: # obj is TKey
    if obj.GetClassName() == "TH1F":
        Hists.append(obj.GetName())
for N in nominalHists:
    for H in Hists:
        if N not in H:
            continue
        if H[-2:]=='Up':
            A1 = f1.Get(H.split('_')[0])
            A2 = f1.Get(H)
            A3 = f1.Get(H[:-2]+'Down')
            if StatError:
                print '********************************************stat Error: ' +str(math.sqrt(A1.GetSumw2().GetSum())/A1.Integral())
            print H
            print str(abs(1-A2.Integral()/A1.Integral())*100) +' , ' + str(abs(1-A3.Integral()/A1.Integral())*100) 
