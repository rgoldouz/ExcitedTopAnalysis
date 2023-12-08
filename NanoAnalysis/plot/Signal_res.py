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
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch +'/'+reg):
       os.makedirs(year + '/' + ch +'/'+reg)
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
    dummy.Draw("e")
    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
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
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw()
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    canvas.Print(year + '/' + ch +'/'+reg+'/'+var + ".png")
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
    A.GetYaxis().SetTitle('T* mass')
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

def compareNeffHist(A, textA, label_name="sample", can_name="can"):
    canvas = ROOT.TCanvas(can_name,can_name,10,10,1100,628)
    canvas.SetGrid();
    canvas.cd()
    for l in range(len(A)):
        A[l].SetLineColor( l+1 )
    if len(A)==2:
        A[0].SetLineColor(4)
    if len(A)==3:
        A[2].SetLineColor(4)

    A[0].SetMaximum(1.1)
    A[0].SetMinimum(0)
    A[0].SetTitle("")
    A[0].GetXaxis().SetTitle(i)
    A[0].GetYaxis().SetTitle('Stub eff ')
    A[0].GetXaxis().SetTitleSize(0.05)
    A[0].GetYaxis().SetTitleSize(0.05)
    for l in range(len(A)):
        A[l].Draw('esame')
    A[0].Draw("AXISSAMEY+")
    A[0].Draw("AXISSAMEX+")

    leg = ROOT.TLegend(0.78,0.7,1,0.98)
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
    canvas.Print("Compare"+ can_name +"_"+ label_name + ".png")
    del canvas
    gc.collect()

def compare2Hist(A, B, textA="A", textB="B", label_name="sample", can_name="can", axis_name="eta"):
    canvas = ROOT.TCanvas(can_name,can_name,50,50,865,780)
    canvas.cd()

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

    A.SetLineColor( 2 )
    B.SetLineColor( 4 )
    A.SetTitle("")
    A.GetXaxis().SetTitle(axis_name)
    A.GetXaxis().CenterTitle()
    A.GetXaxis().SetTitleSize(0.05)
    A.GetYaxis().SetTitleSize(0.05)
    A.GetXaxis().SetLabelSize(0)
    A.SetMaximum(1.4*max(A.GetMaximum(),B.GetMaximum()));
    A.SetMinimum(0.8*min(A.GetMinimum(),B.GetMinimum()));
    A.Draw()
    B.Draw('esame')
    A.Draw("AXISSAMEY+")
    A.Draw("AXISSAMEX+")

    legend = ROOT.TLegend(0.67,0.67,0.9,0.85)
    legend.AddEntry(A ,textA,'l')
    legend.AddEntry(B ,textB,'l')
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.Draw("same")

    label = ROOT.TLatex()
    label.SetTextAlign(12)
    label.SetTextFont(42)
    label.SetTextSize(0.06)
    label.SetNDC(ROOT.kTRUE)
    label.DrawLatex(0.25,0.95,"CMS Phase 2 Simulation Preliminary")

    pad2.cd()
    ratio = A.Clone()
    ratio.Divide(B)
    ratio.SetTitle("")
    ratio.SetMaximum(1.2)
    ratio.SetMinimum(0.8)
    ratio.GetXaxis().SetTitle(axis_name)
    ratio.GetYaxis().CenterTitle()
    ratio.GetXaxis().SetMoreLogLabels()
    ratio.GetXaxis().SetNoExponent()
    ratio.GetXaxis().SetTitleSize(0.04/0.3)
    ratio.GetYaxis().SetTitleSize(0.04/0.3)
    ratio.GetXaxis().SetTitleFont(42)
    ratio.GetYaxis().SetTitleFont(42)
    ratio.GetXaxis().SetTickLength(0.05)
    ratio.GetYaxis().SetTickLength(0.05)
    ratio.GetXaxis().SetLabelSize(0.115)
    ratio.GetYaxis().SetLabelSize(0.089)
    ratio.GetXaxis().SetLabelOffset(0.02)
    ratio.GetYaxis().SetLabelOffset(0.01)
    ratio.GetYaxis().SetTitleOffset(0.42)
    ratio.GetXaxis().SetTitleOffset(1.1)
    ratio.GetYaxis().SetNdivisions(504)
    ratio.SetStats(ROOT.kFALSE)
    ratio.GetYaxis().SetTitle('Ratio')

    ratio.Draw("e")
    ratio.Draw("AXISSAMEY+")
    ratio.Draw("AXISSAMEX+")
    canvas.Print("2H_" + can_name +"_"+ label_name + ".png")
    del canvas
    gc.collect()

Files = ROOT.TFile.Open("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/ANoutput.root")
H1= Files.Get('BestMass1vs2')
H1.SetMarkerColor(ROOT.kBlack)
H1.SetLineColor(ROOT.kBlack)
H1.SetLineWidth(2)
H1.SetMarkerStyle(20)
H1.SetMarkerSize(1.2)
H2 = Files.Get('M1vsM2')
H2.SetMarkerColor(ROOT.kRed-4)
H2.SetLineColor(ROOT.kRed-4)
H2.SetMarkerStyle(3)
H2.SetLineWidth(2)

H3 = Files.Get('BestMassV21vs2')
H3.SetMarkerColor(ROOT.kGreen)
H3.SetMarkerStyle(22)

canvas = ROOT.TCanvas('a','a',50,50,865,780)
canvas.SetGrid();
canvas.SetBottomMargin(0.17)
canvas.cd()

H1.Draw()
H2.Draw("same")
#H3.Draw("same")

canvas.Print("Signal_res"+ ".png")

canvas.Close()

canvas = ROOT.TCanvas('a','a',50,50,865,780)
canvas.SetGrid();
canvas.SetBottomMargin(0.17)
canvas.cd()

H1.ProjectionX().Draw("c");
H2.ProjectionX().Draw('Csame');
canvas.Print("Signal_res_1D"+ ".png")
