import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}

mc2017_samples["2017_GJetsHT100To200"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT100To200/200526_145843/0000'],    "mc",    "none",    "2017",    "none",    "5383",    "41.53",    "15961733"]
mc2017_samples["2017_GJetsHT200To400"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT200To400/200526_150140/0000'],    "mc",    "none",    "2017",    "none",    "1176",    "41.53",    "50520606"]
mc2017_samples["2017_GJetsHT400To600"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT400To600/200526_150102/0000'],    "mc",    "none",    "2017",    "none",    "132.1",    "41.53",    "13606648"]
mc2017_samples["2017_GJetsHT600ToInf"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_GJetsHT600ToInf/200526_145809/0000'],    "mc",    "none",    "2017",    "none",    "44.32",    "41.53",    "8454929"]
                                
mc2017_samples["2017_QCDHT100to200"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT100to200_1/200526_145826/0000','rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT100to200_2/200526_145751/0000'],    "mc",    "none",    "2017",    "none",    "27990000",    "41.53",    "124185627"]
                                
mc2017_samples["2017_QCDHT200to300"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT200to300/200526_150120/0000'],    "mc",    "none",    "2017",    "none",    "1712000",    "41.53",    "9076637"]
mc2017_samples["2017_QCDHT300to500"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT300to500/200526_145900/0000'],    "mc",    "none",    "2017",    "none",    "347700",    "41.53",    "59502402"]
mc2017_samples["2017_QCDHT500to700"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT500to700/200526_145641/0000','rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT500to700/200526_145641/0001'],    "mc",    "none",    "2017",    "none",    "32100",    "41.53",    "51887885"]
mc2017_samples["2017_QCDHT700to1000"]=[    ['/rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT700to1000/200526_150004/0000'],    "mc",    "none",    "2017",    "none",    "6831",    "41.53",    "47667223"]
mc2017_samples["2017_QCDHT1000to1500"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT1000to1500/200526_150200/0000'],    "mc",    "none",    "2017",    "none",    "1207",    "41.53",    "15777446"]
mc2017_samples["2017_QCDHT1500to2000"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT1500to2000/200526_145659/0000'],    "mc",    "none",    "2017",    "none",    "119.9",    "41.53",    "11659607"]
mc2017_samples["2017_QCDHT2000toInf"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/crab_2017_QCDHT200to300/200526_150120/0000'],    "mc",    "none",    "2017",    "none",    "25.24",    "41.53",    "9076637"]
                                
mc2017_samples["2017_DYJetsToLLM50"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2017_DYJetsToLLM50/200526_150041/0000'],    "mc",    "none",    "2017",    "none",    "5765.4",    "41.53",    "126049003"]
mc2017_samples["2017_DYJetsToLLM10to50"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_DYJetsToLLM10to50/200526_145734/0000'],    "mc",    "none",    "2017",    "none",    "18610",    "41.53",    "39407363"]
mc2017_samples["2017_WJetsToLNu"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_WJetsToLNu/200526_150238/0000'],    "mc",    "none",    "2017",    "none",    "61526",    "41.53",    "33043732"]
                                
mc2017_samples["2017_WGPtG40to130"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WGJets_MonoPhoton_PtG-40to130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG40to130/200526_150219/0000'],    "mc",    "none",    "2017",    "none",    "17.018",    "41.53",    "4899842"]
mc2017_samples["2017_WGPtG130"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/WGJets_MonoPhoton_PtG-130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG130/200526_145920/0000'],    "mc",    "none",    "2017",    "none",    "0.88",    "41.53",    "4903944"]
                                
mc2017_samples["2017_TTToHadronic"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_tt/200526_145717/0000'],    "mc",    "none",    "2017",    "none",    "380.1",    "41.53",    "59292050"]
mc2017_samples["2017_ttG"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017_ttG/200526_145939/0000'],    "mc",    "none",    "2017",    "none",    "3.697",    "41.53",    "2843791"]
mc2017_samples["2017_ttToSemiLeptonic"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2017_ttToSemiLeptonic/200527_080919/0000'],    "mc",    "none",    "2017",    "none",    "364",    "41.53",    "30784149"]
#mc2017_samples["2017_STtchtop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_top_4f_InclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8/crab_2017_STtchtop/200527_080954/0000'],    "mc",    "none",    "2017",    "none",    "136",    "41.53",    "30593400"]
mc2017_samples["2017_STtchatop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtchatop/200527_080842/0000','rgoldouz/ExitedTopSamplesMCJan2021/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtchatop/200527_080842/0001'],    "mc",    "none",    "2017",    "none",    "81",    "41.53",    "61772400"]
mc2017_samples["2017_STtwchtop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchtop/200527_080900/0000'],    "mc",    "none",    "2017",    "none",    "19.3",    "41.53",    "6004512"]
mc2017_samples["2017_STtwchatop"]=[    ['rgoldouz/ExitedTopSamplesMCJan2021/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchatop/200527_080936/0000'],    "mc",    "none",    "2017",    "none",    "19.3",    "41.53",    "2837802"]
                                
mc2017_samples["2017_tptpM1000"]=[    ['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000'],    "mc",    "none",    "2017",    "none",    "1",    "41.53",    "100000"]
mc2017_samples["2017_tptpM2000"]=[    ['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M2000'],    "mc",    "none",    "2017",    "none",    "1",    "41.53",    "100000"]
                                
data2017_samples["2017_B_SinglePhoton"]=[    ['rgoldouz/ExitedTopSamplesData/SinglePhoton/crab_2017_B_SinglePhoton/200430_120739/0000'],    "data",    "SinglePhoton",    "2017",    "B",    "1",    "1",    "1"]
data2017_samples["2017_C_SinglePhoton"]=[    ['rgoldouz/ExitedTopSamplesData/SinglePhoton/crab_2017_C_SinglePhoton/200430_120757/0000'],    "data",    "SinglePhoton",    "2017",    "C",    "1",    "1",    "1"]
data2017_samples["2017_D_SinglePhoton"]=[    ['rgoldouz/ExitedTopSamplesData/SinglePhoton/crab_2017_D_SinglePhoton/200430_120816/0000'],    "data",    "SinglePhoton",    "2017",    "D",    "1",    "1",    "1"]
data2017_samples["2017_E_SinglePhoton"]=[    ['rgoldouz/ExitedTopSamplesData/SinglePhoton/crab_2017_E_SinglePhoton/200430_120705/0000'],    "data",    "SinglePhoton",    "2017",    "E",    "1",    "1",    "1"]
data2017_samples["2017_F_SinglePhoton"]=[    ['rgoldouz/ExitedTopSamplesData/SinglePhoton/crab_2017_F_SinglePhoton/200430_120722/0000'],    "data",    "SinglePhoton",    "2017",    "F",    "1",    "1",    "1"]
                                
data2017_samples["2017_B_SingleMuon"]=[    ['rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_B_SingleMuon/200526_145404/0000'],    "data",    "SingleMuon",    "2017",    "B",    "1",    "1",    "1"]
data2017_samples["2017_C_SingleMuon"]=[    ['rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_C_SingleMuon/200526_145520/0000'],    "data",    "SingleMuon",    "2017",    "C",    "1",    "1",    "1"]
data2017_samples["2017_D_SingleMuon"]=[    ['rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_D_SingleMuon/200526_145442/0000'],    "data",    "SingleMuon",    "2017",    "D",    "1",    "1",    "1"]
data2017_samples["2017_E_SingleMuon"]=[    ['rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_E_SingleMuon/200526_145424/0000'],    "data",    "SingleMuon",    "2017",    "E",    "1",    "1",    "1"]
data2017_samples["2017_F_SingleMuon"]=[    ['rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_F_SingleMuon/200526_145501/0000','rgoldouz/ExitedTopSamplesData/SingleMuon/crab_2017_F_SingleMuon/200526_145501/0001'],    "data",    "SingleMuon",    "2017",    "F",    "1",    "1",    "1"]
