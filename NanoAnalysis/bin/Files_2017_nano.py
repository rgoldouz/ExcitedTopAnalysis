import sys 
import os 
import subprocess 
import readline 
import string 

mc2017_samples={'2017_QCDHT500to700': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT500to700/210922_094355/0000'], 'mc', 'none', '2017', 'none', '32100', '41.53', '56207744.0'], '2017_STtwchtop': [['rgoldouz/Etop_nanoAODv9_MC/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchtop/210922_095725/0000'], 'mc', 'none', '2017', 'none', '19.3', '41.53', '7945242.0'], '2017_GJetsHT100To200': [['rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT100To200/210922_094501/0000'], 'mc', 'none', '2017', 'none', '5383', '41.53', '15965137.0'], '2017_GJetsHT400To600': [['rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT400To600/210922_100157/0000'], 'mc', 'none', '2017', 'none', '132.1', '41.53', '13332751.0'], '2017_QCDHT300to500': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT300to500/210922_094609/0000'], 'mc', 'none', '2017', 'none', '347700', '41.53', '12412611.0'], '2017_QCDHT1000to1500': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT1000to1500/210922_095834/0000'], 'mc', 'none', '2017', 'none', '1207', '41.53', '16595628.0'], '2017_ttToSemiLeptonic': [['rgoldouz/Etop_nanoAODv9_MC/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_2017_ttToSemiLeptonic/210922_095941/0000'], 'mc', 'none', '2017', 'none', '364', '41.53', '41112723.0'], '2017_WJetsToLNu': [['rgoldouz/Etop_nanoAODv9_MC/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_WJetsToLNu/210922_094716/0000'], 'mc', 'none', '2017', 'none', '61526', '41.53', '33073306.0'], '2017_QCDHT200to300': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT200to300/210922_100846/0000'], 'mc', 'none', '2017', 'none', '1712000', '41.53', '59197363.0'], '2017_GJetsHT200To400': [['rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT200To400/210922_100304/0000'], 'mc', 'none', '2017', 'none', '1176', '41.53', '49870562.0'], '2017_STtchatop': [['rgoldouz/Etop_nanoAODv9_MC/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtchatop/210922_100627/0000'], 'mc', 'none', '2017', 'none', '81', '41.53', '64761200.0'], '2017_ttG': [['rgoldouz/Etop_nanoAODv9_MC/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017_ttG/210922_094823/0000'], 'mc', 'none', '2017', 'none', '3.697', '41.53', '7349100.0'], '2017_tptpM1000': [['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000'], 'mc', 'none', '2017', 'none', '1', '41.53', '100000'], '2017_QCDHT1500to2000': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT1500to2000/210922_095039/0000'], 'mc', 'none', '2017', 'none', '119.9', '41.53', '11634434.0'], '2017_GJetsHT600ToInf': [['rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_GJetsHT600ToInf/210922_094930/0000'], 'mc', 'none', '2017', 'none', '44.32', '41.53', '8392881.0'], '2017_QCDHT700to1000': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT700to1000/210922_100737/0000'], 'mc', 'none', '2017', 'none', '6831', '41.53', '47610552.0'], '2017_TTToHadronic': [['rgoldouz/Etop_nanoAODv9_MC/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_tt/210922_100412/0000'], 'mc', 'none', '2017', 'none', '380.1', '41.53', '121937676.0'], '2017_STtwchatop': [['rgoldouz/Etop_nanoAODv9_MC/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_STtwchatop/210922_100520/0000'], 'mc', 'none', '2017', 'none', '19.3', '41.53', '7374736.0'], '2017_QCDHT100to200': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT100to200/210922_095146/0000'], 'mc', 'none', '2017', 'none', '27990000', '41.53', '93231801.0'], '2017_tptpM2000': [['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M2000'], 'mc', 'none', '2017', 'none', '1', '41.53', '100000'], '2017_QCDHT2000toInf': [['rgoldouz/Etop_nanoAODv9_MC/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT2000toInf/210922_094249/0000'], 'mc', 'none', '2017', 'none', '25.24', '41.53', '11634434.0'], '2017_DYJetsToLLM10to50': [['rgoldouz/Etop_nanoAODv9_MC/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_DYJetsToLLM10to50/210922_095401/0000'], 'mc', 'none', '2017', 'none', '18610', '41.53', '39521230.0'], '2017_WGPtG130': [['rgoldouz/Etop_nanoAODv9_MC/WGJets_MonoPhoton_PtG-130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG130/210922_095508/0000'], 'mc', 'none', '2017', 'none', '0.88', '41.53', '4917580.0'], '2017_WGPtG40to130': [['rgoldouz/Etop_nanoAODv9_MC/WGJets_MonoPhoton_PtG-40to130_TuneCP5_13TeV-madgraph/crab_2017_WGPtG40to130/210922_095618/0000'], 'mc', 'none', '2017', 'none', '17.018', '41.53', '4903082.0'], '2017_DYJetsToLLM50': [['rgoldouz/Etop_nanoAODv9_MC/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_2017_DYJetsToLLM50/210922_100049/0000'], 'mc', 'none', '2017', 'none', '5765.4', '41.53', '178325599.0']}

data2017_samples={'2017_B_SingleMuon': [['rgoldouz/Etop_nanoAODv9_DATA/SingleMuon/crab_2017_B_SingleMuon/210922_154139/0000'], 'data', 'SingleMuon', '2017', 'B', '1', '1', '1'], '2017_F_SinglePhoton': [['rgoldouz/Etop_nanoAODv9_DATA/SinglePhoton/crab_2017_F_SinglePhoton/210922_154936/0000'], 'data', 'SinglePhoton', '2017', 'F', '1', '1', '1'], '2017_D_SinglePhoton': [['rgoldouz/Etop_nanoAODv9_DATA/SinglePhoton/crab_2017_D_SinglePhoton/210922_154404/0000'], 'data', 'SinglePhoton', '2017', 'D', '1', '1', '1'], '2017_E_SinglePhoton': [['rgoldouz/Etop_nanoAODv9_DATA/SinglePhoton/crab_2017_E_SinglePhoton/210922_154522/0000'], 'data', 'SinglePhoton', '2017', 'E', '1', '1', '1'], '2017_C_SingleMuon': [['rgoldouz/Etop_nanoAODv9_DATA/SingleMuon/crab_2017_C_SingleMuon/210922_154625/0000'], 'data', 'SingleMuon', '2017', 'C', '1', '1', '1'], '2017_C_SinglePhoton': [['rgoldouz/Etop_nanoAODv9_DATA/SinglePhoton/crab_2017_C_SinglePhoton/210922_154835/0000'], 'data', 'SinglePhoton', '2017', 'C', '1', '1', '1'], '2017_E_SingleMuon': [['rgoldouz/Etop_nanoAODv9_DATA/SingleMuon/crab_2017_E_SingleMuon/210922_154731/0000'], 'data', 'SingleMuon', '2017', 'E', '1', '1', '1'], '2017_B_SinglePhoton': [['rgoldouz/Etop_nanoAODv9_DATA/SinglePhoton/crab_2017_B_SinglePhoton/210922_155040/0000'], 'data', 'SinglePhoton', '2017', 'B', '1', '1', '1'], '2017_D_SingleMuon': [['rgoldouz/Etop_nanoAODv9_DATA/SingleMuon/crab_2017_D_SingleMuon/210922_155144/0000'], 'data', 'SingleMuon', '2017', 'D', '1', '1', '1'], '2017_F_SingleMuon': [['rgoldouz/Etop_nanoAODv9_DATA/SingleMuon/crab_2017_F_SingleMuon/210922_155248/0000'], 'data', 'SingleMuon', '2017', 'F', '1', '1', '1']}