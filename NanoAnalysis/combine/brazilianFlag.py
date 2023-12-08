import gc
import sys
import ROOT
import numpy as np
import copy
import os
from array import array
import gc
import math
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

year=['2017']

bTyTg = 0.03*0.97*2
crossSection = {
'TTga_M800':[800,bTyTg*1.68],
'TTga_M1200':[1200,bTyTg*0.0537],
'TTga_M1400':[1400,bTyTg*0.0131],
'TTga_M1000':[1000,bTyTg*0.262],
'TTga_M1600':[1600,bTyTg*0.00359],
'TTga_M1300':[1300,bTyTg*0.0261],
#'TTga_M1700':[1700,bTyTg*4.92],
}



Obs=0.777
mu=0.777
muM2=0.777
muM1=0.777
muP1=0.777
muP2=0.777

for numyear, nameyear in enumerate(year):
    upperBoundObs = {}
    upperBoundExp = {}
    upperBoundExpP1 = {}
    upperBoundExpP2 = {}
    upperBoundExpM1 = {}
    upperBoundExpM2 = {}
    theoryBound = {}
    for fname in os.listdir('/hadoop/store/user/rgoldouz/FullProduction/LimitsExcitedTop'):
        os.system('cp /hadoop/store/user/rgoldouz/FullProduction/LimitsExcitedTop/' + fname + '/* ' + './impacts')
    for fname in os.listdir('impacts'):
        if 'impacts' not in fname:
            continue
        os.system('mv impacts/' + fname +' impacts/' + '_'.join(fname.split('_')[:-1]) + '.pdf')
    os.system('combineTool.py -M CollectLimits  impacts/*Limits.* -o limits.json')
   # Style and pads
    ModTDRStyle()
    canv = ROOT.TCanvas('limit', 'limit')
    pads = OnePad()
    
    # Get limit TGraphs as a dictionary
    graphs = StandardLimitsFromJSONFile('limits.json', draw=['exp0', 'exp1', 'exp2'])
    yval=1
    spline = ROOT.TSpline3("spline3", graphs['exp0'])
    func = ROOT.TF1(
        "splinefn",
        partial(Eval, spline),
        graphs.GetX()[0],
        graphs.GetX()[graphs['exp0'].GetN() - 1],
        1,
    )
    for i in range(graphs['exp0'].GetN() - 1):
        if (graphs['exp0'].GetY()[i] - yval) * (graphs['exp0'].GetY()[i + 1] - yval) < 0.0:
            cross = func.GetX(yval, graphs['exp0'].GetX()[i], graphs['exp0'].GetX()[i + 1]) 
            print "excluded mass is:"+str(cross) 
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    axis = CreateAxisHist(graphs.values()[0])
    axis.GetXaxis().SetTitle('m_{T*} (GeV)')
    axis.GetYaxis().SetTitle('95% CL limit on #mu')
    pads[0].cd()
    axis.Draw('axis')
    
    # Create a legend in the top left
    legend = PositionedLegend(0.3, 0.2, 3, 0.015)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend)
    legend.Draw()
    
    # Re-draw the frame and tick marks
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()
    pads[0].SetLogy(ROOT.kTRUE)
    pads[0].SetGridy()
    pads[0].SetTickx()
    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0.1, 0, GetPadYMax(pads[0]), 0.25)
    
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)
    
    line = ROOT.TLine(800,1,1600,1);
    line.SetLineColor(1)
    line.SetLineWidth(2)
    line.SetLineStyle(5)
    line.Draw("same")

    canv.Print('.pdf')
    canv.Print('.png')
#            if 'results' not in fname:
#                file1 = open('/hadoop/store/user/rgoldouz/FullProduction/LimitsExcitedTop/' + fname + '/' + mass , 'r') 
#                Lines = file1.readlines()
#                Obs= 0.0
#                mu=  0.0
#                muM2=0.0
#                muM1=0.0
#                muP1=0.0
#                muP2=0.0 
#                for line in Lines: 
#                    if 'Observed Limit' in line:
#                        Obs = float(line.split()[-1])
#                    if 'Expected 50.0' in line:
#                        mu = float(line.split()[-1])
#                    if 'Expected  2.5' in line:
#                        muM2 = float(line.split()[-1])
#                    if 'Expected 16.0' in line:
#                        muM1 = float(line.split()[-1])
#                    if 'Expected 84.0' in line:
#                        muP1 = float(line.split()[-1])
#                    if 'Expected 97.5' in line:
#                        muP2 = float(line.split()[-1])
#            for S, xs in crossSection.items():
#                if S in mass:
#                    upperBoundExp[xs[0]]=xs[1]*mu
#                    upperBoundExpP1[xs[0]]=xs[1]*muP1
#                    upperBoundExpP2[xs[0]]=xs[1]*muP2
#                    upperBoundExpM1[xs[0]]=xs[1]*muM1
#                    upperBoundExpM2[xs[0]]=xs[1]*muM2
#                    upperBoundObs[xs[0]]=xs[1]*mu
#                    theoryBound[xs[0]]=xs[1]
#
#print upperBoundExp
#print theoryBound
