# This file skims the data and saves the output to ./tmp
# Do not combine files across runs, otherwise you may get inconsistent TTree structures!
# Doing things file by file is the safest way to avoid this problem, and comes at almost
# no extra cost.
# You can copy and paste json sources directly from https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/

import os
import ROOT
path = []

#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5_erdON_v15_v1/200311_155126/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5_erdON_v15_ext1_v1/200311_155018/0000/')
#path.append('/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_04_13/mc2017/gjets/GJets_HT_100To200_v1/')
#path.append('/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_04_13/mc2017/gjets/GJets_HT_400To600_v1/')
#path.append('/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_04_13/mc2017/gjets/GJets_HT_200To400_v1')
#path.append('/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_04_13/mc2017/gjets/GJets_HT_600ToInf_v2')

mc2017_samples = {}

#mc2017_samples["2017_GJetsHT100To200"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT100To200/200526_145843/0000'],    "mc",    "none",    "2017",    "none",    "5383",    "41.53",    ""]
#mc2017_samples["2017_GJetsHT200To400"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT200To400/200526_150140/0000'],    "mc",    "none",    "2017",    "none",    "1176",    "41.53",    ""]
#mc2017_samples["2017_GJetsHT400To600"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT400To600/200526_150102/0000'],    "mc",    "none",    "2017",    "none",    "132.1",    "41.53",    ""]
#mc2017_samples["2017_GJetsHT600ToInf"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_GJetsHT600ToInf/200526_145809/0000'],    "mc",    "none",    "2017",    "none",    "44.32",    "41.53",    ""]
#                                
#mc2017_samples["2017_QCDHT100to200"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT100to200_1/200526_145826/0000','rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT100to200_2/200526_145751/0000'],    "mc",    "none",    "2017",    "none",    "27990000",    "41.53",    ""]
#                                
#mc2017_samples["2017_QCDHT200to300"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT200to300/200526_150120/0000'],    "mc",    "none",    "2017",    "none",    "1712000",    "41.53",    ""]
#mc2017_samples["2017_QCDHT300to500"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT300to500/200526_145900/0000'],    "mc",    "none",    "2017",    "none",    "347700",    "41.53",    ""]
#mc2017_samples["2017_QCDHT500to700"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT500to700/200526_145641/0000','rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT500to700/200526_145641/0001'],    "mc",    "none",    "2017",    "none",    "32100",    "41.53",    ""]
#mc2017_samples["2017_QCDHT700to1000"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT700to1000/200526_150004/0000'],    "mc",    "none",    "2017",    "none",    "6831",    "41.53",    ""]
#mc2017_samples["2017_QCDHT1000to1500"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT1000to1500/200526_150200/0000'],    "mc",    "none",    "2017",    "none",    "1207",    "41.53",    ""]
#mc2017_samples["2017_QCDHT1500to2000"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT1500to2000/200526_145659/0000'],    "mc",    "none",    "2017",    "none",    "119.9",    "41.53",    ""]
#mc2017_samples["2017_QCDHT2000toInf"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT200to300/200526_150120/0000'],    "mc",    "none",    "2017",    "none",    "25.24",    "41.53",    ""]
#                                
#mc2017_samples["2017_DYJetsToLLM50"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2017_DYJetsToLLM50/200526_150041/0000'],    "mc",    "none",    "2017",    "none",    "5765.4",    "41.53",    "122037615"]
#mc2017_samples["2017_DYJetsToLLM10to50"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_DYJetsToLLM10to50/200526_145734/0000'],    "mc",    "none",    "2017",    "none",    "18610",    "41.53",    "122037615"]
#mc2017_samples["2017_WJetsToLNu"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_WJetsToLNu/200526_150238/0000'],    "mc",    "none",    "2017",    "none",    "61526",    "41.53",    "33043732"]                               
# 
#mc2017_samples["2017_WGPtG40to130"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WGJets_MonoPhoton_PtG-40to130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG40to130/200526_150219/0000'],    "mc",    "none",    "2017",    "none",    "17.018",    "41.53",    ""]
#mc2017_samples["2017_WGPtG130"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WGJets_MonoPhoton_PtG-130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG130/200526_145920/0000'],    "mc",    "none",    "2017",    "none",    "0.88",    "41.53",    ""]
#                                
#mc2017_samples["2017_ttHadronic"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_tt/200526_145717/0000'],    "mc",    "none",    "2017",    "none",    "380.1",        ""]
#mc2017_samples["2017_ttG"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017_ttG/200526_145939/0000'],    "mc",    "none",    "2017",    "none",    "3.697",        ""]
#mc2017_samples["2017_ttToSemiLeptonic"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2017_ttToSemiLeptonic/200527_080919/0000'],    "mc",    "none",    "2017",    "none",    "364",        ""]
#mc2017_samples["2017_STtchtop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_top_4f_InclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8/crab_2017_STtchtop/200527_080954/0000'],    "mc",    "none",    "2017",    "none",    "136",        ""]
#mc2017_samples["2017_STtchatop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtchatop/200527_080842/0000','rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtchatop/200527_080842/0001'],    "mc",    "none",    "2017",    "none",    "81",        ""]
#mc2017_samples["2017_STtwchtop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchtop/200527_080900/0000'],    "mc",    "none",    "2017",    "none",    "19.3"        ""]
#mc2017_samples["2017_STtwchatop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchatop/200527_080936/0000'],    "mc",    "none",    "2017",    "none",    "19.3"        ""]
#                                
#mc2017_samples["2017_tptpM1000"]=[    ['rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000'],    "mc",    "none",    "2017",    "none",    "30",    "41.53",    "100000"]
#mc2017_samples["2017_tptpM2000"]=[    ['rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M2000'],    "mc",    "none",    "2017",    "none",    "20",    "41.53",    "100000"]
mc2017_samples['2017_tptpM1000']= [['rgoldouz/FullProduction/IIHE_Ntuple_10215/ntuple_M1000_gaChannel'], 'mc', 'none', '2017', 'none', '1', '41.53', '100000']
add='/hadoop/store/user/'

SAMPLES = {}
SAMPLES.update(mc2017_samples)

for key, value in SAMPLES.items():
    print key
    nEventsraw = 0
    neventsweight = 0
    nEventsStored = 0
    nEventsiihe = 0
    for aa in value[0]:
#        print aa
        a = add + aa
        filenames = os.listdir(a)
        for fname in filenames:
            filename = a + '/' + fname
#            print fname 
            if 'fail' in fname:
                continue
            f = ROOT.TFile.Open(filename)
            
    #        if not f:
    #            print 'rm -rf '+fname
            tree_in = f.Get('IIHEAnalysis')
            tree_meta = f.Get('meta')
            nEventsiihe += tree_in.GetEntries()
            tree_meta.GetEntry(0)    
    #        print tree_meta.nEventsRaw
            nEventsraw += tree_meta.nEventsRaw
            nEventsStored += tree_meta.nEventsStored
            neventsweight += tree_meta.mc_nEventsWeighted
            f.Close()
    print 'neventsweight %d   '%(neventsweight)
#    print 'nEventsraw %d   '%(nEventsraw)
#    print 'nEventsStored %d   '%(nEventsStored)
#    print 'nEventsiihe %d   '%(nEventsiihe)
