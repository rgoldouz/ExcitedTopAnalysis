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

def Smoothing(AS, merge):
    x = array( 'd' )
    source =  array( 'd' )
    for i in range(AS.GetNbinsX()):
        x.append(AS.GetBinCenter(i + 1))
        source.append(AS.GetBinContent(i + 1))
    gs = ROOT.TGraphSmooth("normal")
    grin = ROOT.TGraph(AS.GetNbinsX(),x,source);
    grout = gs.SmoothKern(grin,"normal",merge);
    smooth = AS.Clone()
    for i in range(AS.GetNbinsX()):
        smooth.SetBinContent(i + 1,grout.GetY()[i])
    return smooth

def Rebin(AS, xbins):
    AB = AS.Rebin(len(xbins)-1,"AB",xbins)
    return AB

def correctHist(nominal,histRatio):
    for i in range(nominal.GetNbinsX()):
        histRatio.SetBinContent(i + 1,histRatio.GetBinContent(i + 1)*nominal.GetBinContent(i + 1))
    return histRatio
    
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


if not os.path.exists('CombinedFilesRebinned'):
    os.makedirs('CombinedFilesRebinned')
if not os.path.exists('CombinedFilesRebinnedSmooth'):
    os.makedirs('CombinedFilesRebinnedSmooth')

year=['2016preVFP', '2016postVFP', '2017','2018']
channels=["ee", "emu", "mumu"];
regions=["llB1"]

#nominalHists=['tt','LfvVectorEmutc', 'LfvVectorEmutu']
#nominalHists=['LFVStVecU', 'LFVTtVecU','LFVStVecC', 'LFVTtVecC']
nominalHists=['tt']

#bins = array( 'd',[-0.6,-0.4,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.2,0.25,0.6,0.8] )
#bins = array( 'd',[-0.6,-0.5,-0.3,-0.2,-0.1,0,0.1,0.20,0.3,0.4] )
bins = array( 'd',[-1,-0.5,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.20,0.25,0.4,1] )
couplings=['cS','cT']

for coup in couplings:
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                f1 = ROOT.TFile.Open('CombinedFilesOriginal/' + coup + '_' + nameyear + '_' + namech + '_' + namereg +'.root')
                hfile = ROOT.TFile( 'CombinedFilesRebinned/' + coup + '_' + nameyear+ '_' + namech+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
                my_list = f1.GetListOfKeys()
                Hists=[]
                HistsDraw=[]
                for obj in my_list: # obj is TKey
                    if obj.GetClassName() == "TH1F":
                        Hists.append(obj.GetName())
                        RF = Rebin(f1.Get(obj.GetName()),bins)
                        RF.SetName(obj.GetName())
                        for b in range(RF.GetNbinsX()):
                            if RF.GetBinContent(b+1)<0:
                                RF.SetBinContent(b+1,0)
                        if 'BNV' in obj.GetName():
                            RF.Scale(0.10)
                        RF.Write()
                hfile.Close()
                hfileS = ROOT.TFile( 'CombinedFilesRebinnedSmooth/' + coup + '_' + nameyear+'_'+namereg+'.root', 'RECREATE', 'combine smooth input histograms' )
                for H in Hists:
                    RF = Rebin(f1.Get(H),bins)
                    RF.SetName(H)
                    RF.Write()
                #    print H.split('_')[0]
                    if H.split('_')[0] not in nominalHists or ('CR' not in H and 'Tune' not in H and 'hdamp' not in H):
                        continue;
                #    print H[-2:]
                    if H[-2:]=='Up':
                        A1 = f1.Get(H.split('_')[0])
                        A2 = f1.Get(H)
                        A3 = f1.Get(H[:-2]+'Down')
                        RA1 = A1.Clone()
                        RA2 = A2.Clone()
                        RA3 = A3.Clone()
                        RA1.Divide(A1)
                        RA2.Divide(A1)
                        RA3.Divide(A1) 
                        SRA2 = Smoothing(RA2,0.1)
                        SRA3 = Smoothing(RA3,0.1)     
                        CSRA2 = correctHist(A1,SRA2)
                        CSRA3 = correctHist(A1,SRA3)         
                        SRA22 = Rebin(CSRA2,bins)
        #                SRA22.Divide(Rebin(RA1,bins))
                        SRA33 = Rebin(CSRA3,bins)
        #                SRA33.Divide(Rebin(RA1,bins))
        #                compare3Hist(A1,A2,A3,'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,nameyear + namereg+H[:-2])
        #                compare3Hist(RA1,RA2,RA3,'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,nameyear + namereg+H[:-2])
        #                compare3Hist(Rebin(RA1,bins),Rebin(Smoothing(RA2,0.05),bins),Rebin(Smoothing(RA3,0.05),bins),'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,'smooth'+nameyear + namereg+H[:-2])
        #                compare3Hist(RA1,RA2,Smoothing(RA2,1),'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,'RA'+nameyear + namereg+H[:-2])
        #                compare3Hist(RA2,Smoothing(RA2,0.1),Smoothing(RA2,0.2),'nominal', '0.1','0.2',nameyear + namereg+ H[:-2] ,'3'+nameyear + namereg+H[:-2])
        #                compare3Hist(Rebin(A1,bins),Rebin(A2,bins),Rebin(A3,bins),'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,'Rebin'+nameyear + namereg+H[:-2])
        #                compare3Hist(Rebin(A1,bins),correctHist(Rebin(A1,bins),SRA22),correctHist(Rebin(A1,bins),SRA33),'nominal', 'Up','Down',nameyear + namereg+ H[:-2] ,'Rebinsmooth'+nameyear + namereg+H[:-2])
        #                compare3Hist(Rebin(A1,bins),Rebin(A2,bins),SRA22,'nominal', 'Up','smoothUP',nameyear + namereg+ H[:-2] ,'RebinsmoothUP'+nameyear + namereg+H[:-2])
        #                compare3Hist(Rebin(A1,bins),Rebin(A3,bins),SRA33,'nominal', 'DOWN','smoothDOWN',nameyear + namereg+ H[:-2] ,'RebinsmoothDOWN'+nameyear + namereg+H[:-2])
#                        compare3Hist(Rebin(A1,bins),SRA22,SRA33,'nominal', 'smoothUP','smoothDOWN',nameyear + namereg+ H[:-2] ,'Rebinsmooth'+nameyear + namereg+H[:-2])
#                        compare3Hist(Rebin(A1,bins),Rebin(A2,bins),Rebin(A3,bins),'nominal', 'Up','DOWN',nameyear + namereg+ H[:-2] ,'Rebins'+nameyear + namereg+H[:-2])
        #                RFup = correctHist(Rebin(A1,bins),SRA22)
                        RFup = SRA22
                        RFup.SetName(H)
                        RFup.Write()
        #                RFdown = correctHist(Rebin(A1,bins),SRA33)
                        RFdown = SRA33
                        RFdown.SetName(H[:-2]+'Down')
                        RFdown.Write()

os.system("rm -rf CombinedFilesBNV")
os.system("mkdir CombinedFilesBNV")
os.system("cp -r CombinedFilesOriginal/* CombinedFilesBNV")
os.system("cp -r CombinedFilesRebinned/* CombinedFilesBNV")


