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
from ROOT import TFile
import gc
import sys
import os
import subprocess
import readline
import string
import glob
from joblib import Parallel, delayed
MCSAMPLES = {}

def f(name):
    print name
    neventsweight = 0
    neventsweightSumw = 0
    nRuns = 0
    nWeight = []
    for fname in os.listdir(name):
        filename = name + '/' + fname
        print filename 
        if 'fail' in fname:
            continue
        fi = TFile.Open(filename)
        tree_meta = fi.Get('Runs')
        genEventCount = 0
        genEventSumw = 0
        evtTree = fi.Get('Events')
        evtTree.SetBranchStatus("*", 0)
        evtTree.SetBranchStatus("genWeight", 1)
        evtTree.SetBranchStatus("LHEWeight_originalXWGTUP", 1)
        if 'BNV' in name:
            for i in range( evtTree.GetEntries() ):
                evtTree.GetEntry(i)
                if evtTree.LHEWeight_originalXWGTUP not in nWeight:
                    nWeight.append(evtTree.LHEWeight_originalXWGTUP)
        evtTree.GetEntry(0)
        for i in range( tree_meta.GetEntries() ):
            tree_meta.GetEntry(i)
            genEventCount += tree_meta.genEventCount
            genEventSumw += tree_meta.genEventSumw
            nRuns +=1
        neventsweight += genEventCount
        print '.genWeight ' + str(evtTree.genWeight) 
        if abs(evtTree.genWeight)>0:
            neventsweightSumw += genEventSumw/abs(evtTree.genWeight)
        else:
            neventsweightSumw += genEventSumw
        if tree_meta.GetEntries()>1:
            print 'Warning number of MC Runs is more than 1, be careful about sum of the weights'
        tree_meta.Reset()
        tree_meta.Delete()
        evtTree.Reset()
        evtTree.Delete()
        fi.Close()
    return name[19:],str(neventsweightSumw), str(len(nWeight)) 
#    for key, value in MCSAMPLES.items():
#        if key == name.split('/')[8]:
#            value[0].append(name[19:])
#            value[7] = str( float(value[8]) + neventsweightSumw)
#            value[9] = str(len(nWeight))


if __name__ == '__main__':
#    MCSAMPLES = {}
   
    bTyTg = 0.03*0.97*2 
    crossSection = {
    'tWNoFullyHadronic': '19.47',
    'antitWNoFullyHadronic': '19.47',
    'ST_t-channel_top': '136.02',
    'ST_t-channel_antitop': '80.95',
    'TTTo2L2Nu': '87.31',
    'TTToSemiLeptonic': '365.34',
    'TTToHadronic': '379.11',
    'TTJets': '831.76',
    'DY10to50': '18610',
    'DY50': '6077.22',
    'WZTo2L2Q':'5.595',
    'ZZTo2L2Nu':'0.564',
    'TTZToLLNuNu_M_10':'0.2529',
    'WJetsToLNu':'61526.7',
    'TTW':'0.2043',
    'WZTo3LNu':'4.43',
    'WWZ_4F':'0.1651',
    'ZZTo4L':'1.256 ',
    'WWW_4F':'0.2086',
    'ZZZ':'0.01398',
    'WWTo2L2Nu': '12.178',
    'WWpythia': '118.7',
    'WZpythia': '47.13',
    'ZZpythia': '16.523',
    'GJets_DR_0p4_HT_100To200': '5383',
    'GJets_DR_0p4_HT_200To400':'1176',
    'GJets_DR_0p4_HT_400To600':'132.1',
    'GJets_DR_0p4_HT_600ToInf':'44.32',
    'QCD_HT100to200':'27990000',
    'QCD_HT200to300':'1712000',
    'QCD_HT300to500':'347700',
    'QCD_HT500to700':'32100',
    'QCD_HT700to1000':'6831',
    'QCD_HT1000to1500':'1207',
    'QCD_HT1500to2000':'119.9',
    'QCD_HT2000toInf':'25.24',
    'WGJets_MonoPhoton_PtG_40to130':'17.018',
    'WGJets_MonoPhoton_PtG_130':'0.88',
    'TTga_M700':str(bTyTg*4.92),
    'TTga_M800':str(bTyTg*1.68),
    'TTga_M900':str(bTyTg*0.636),
    'TTga_M1000':str(bTyTg*0.262),
    'TTga_M1100':str(bTyTg*0.116),
    'TTga_M1200':str(bTyTg*0.0537),
    'TTga_M1300':str(bTyTg*0.0261),
    'TTga_M1400':str(bTyTg*0.0131),
    'TTga_M1500':str(bTyTg*0.00677),
    'TTga_M1600':str(bTyTg*0.00359),
    }
    
#    blackList = ['ST_antitop_tchannel','ST_top_tchannel', 'ST_top_schannel', 'TTJets','fcnc', 'tbarW_Inclusive', 'tW_Inclusive', 'FCNC', 'WZTo', 'WWTo', 'ZZTo', 'TTG','pythia']
    blackList = ['TTJets','TTga_M1600','TTga_M1700','TTga_M1800','TTga_M1900','TTga_M2000']   
    text = ''
    text += 'import sys \n'
    text += 'import os \n'
    text += 'import subprocess \n'
    text += 'import readline \n'
    text += 'import string \n'
    text += '\n'
    
    dirSamples = {
#    'UL16preVFP': ['2016preVFP','/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL16preVFP/v2','19.52'],
#    'UL16postVFP': ['2016postVFP','/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL16postVFP/v2','16.81'],
    '2017': ['2017' , '/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1',"41.48"],
#    '2017S': ['2017' , '/hadoop/store/user/rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021',"41.48"],
#    '2018': ['2018' , '/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL18/v2',"59.83"],
    }
    
    Slist=[]
    for key, value in dirSamples.items():
        dir_list = os.listdir(value[1])
        for key in dir_list:
            accept = True
            for S in blackList:
                if S in key:
                    accept = False
            if accept:
                if 'data' in key:
                    a,b,c,d = key.split("_")   
                    MCSAMPLES[key] = [    [],    "data",    d,    value[0],    c,    "1",    value[2],    "1",  "0", "1"]
                else:
                    MCSAMPLES[key] = [    [],    "mc",    "none",    value[0],    "none",    "1",    value[2],    "0",  "0", "1"]
    
        for root, dirs, files in os.walk(value[1]):
            if len(files) > 0:
                if 'data' in root:
                    for key, value in MCSAMPLES.items():
                        if key in root:
                            value[0].append(root[19:])
                else:
                    Slist.append(root)
    res = Parallel(n_jobs=40)(delayed(f)(i) for i in Slist)
    Address = [item[0] for item in res]
    Sumw = [item[1] for item in res]
    SumRuns = [item[2] for item in res]

    for a in range(len(Address)):
        print Address[a] + ' ' + Sumw[a] +" " +SumRuns[a]
        for key, value in MCSAMPLES.items():
            if key == Address[a].split('/')[4]:
                value[0].append(Address[a])
                value[7] = Sumw[a]
                value[9] = SumRuns[a]

    for key, value in MCSAMPLES.items():
        for S, xs in crossSection.items():
            if S in key:
                value[5]=xs
    
    for key, value in MCSAMPLES.items():
        if not ('BNV' in key or 'FCNC' in key):
            value[9] = "1"
            continue
        neventsweight = 0
        neventsweightSumw = 0
        value[8] = "1"
        print key
        print value
        if len(value[0])==0:
            del MCSAMPLES[key]
            continue
        files = os.listdir('/hadoop/store/user/'+value[0][0])
        for fname in files:
            filename = '/hadoop/store/user/'+value[0][0] + '/' + fname
            f = ROOT.TFile.Open(filename)
            tree_meta = f.Get('Events')
            neventsweight +=  tree_meta.GetEntries()
            neventsweightSumw +=  tree_meta.GetEntries()
            tree_meta.Reset()
            tree_meta.Delete()
            f.Close()    
        value[7] = str(neventsweight)
    
    
    text += 'UL17={'                
    #text += str(MCSAMPLES)
    text += '\n'
    
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' not in key:
            continue
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
        print(key, ' : ', value)
    text += '}'
    #
    print text
    open('Files_ULall_nano.py', 'wt').write(text)
