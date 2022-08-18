import sys 
import os 
import subprocess 
import readline 
import string 

UL17={
"UL17_QCD_HT700to1000":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT700to1000'], 'mc', 'none', '2017', 'none', '6831', '41.48', '32934816.0', '0', '1'],
"UL17_DY50":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_DY50'], 'mc', 'none', '2017', 'none', '6077.22', '41.48', '130529214.888', '0', '1'],
"UL17_GJets_DR_0p4_HT_400To600":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_400To600'], 'mc', 'none', '2017', 'none', '132.1', '41.48', '9022800.0', '0', '1'],
"UL17_QCD_HT300to500":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT300to500'], 'mc', 'none', '2017', 'none', '347700', '41.48', '43429979.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_100To200":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_100To200'], 'mc', 'none', '2017', 'none', '5383', '41.48', '10034997.0', '0', '1'],
"UL17_TTTo2L2Nu":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTTo2L2Nu/TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8/crab_UL17_TTTo2L2Nu/220802_213058/0000'], 'mc', 'none', '2017', 'none', '87.31', '41.48', '38967608.2726', '0', '1'],
"UL17_QCD_HT2000toInf":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT2000toInf'], 'mc', 'none', '2017', 'none', '25.24', '41.48', '4112573.0', '0', '1'],
"UL17_QCD_HT200to300":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT200to300'], 'mc', 'none', '2017', 'none', '1712000', '41.48', '42714435.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_600ToInf":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_600ToInf'], 'mc', 'none', '2017', 'none', '44.32', '41.48', '8330226.0', '0', '1'],
"UL17_DY10to50_v9":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_DY10to50_v9'], 'mc', 'none', '2017', 'none', '18610', '41.48', '68101524.0', '0', '1'],
"UL17_TTG":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTG'], 'mc', 'none', '2017', 'none', '1', '41.48', '1261451.94994', '0', '1'],
#"UL17_TTga_M1400":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1400/TstarTstarToTgluonTgamma_M-1400_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1400/220802_213444/0000'], 'mc', 'none', '2017', 'none', '0.00076242', '41.48', '195000.0', '0', '1'],
"UL17_QCD_HT1000to1500":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT1000to1500'], 'mc', 'none', '2017', 'none', '1207', '41.48', '10186734.0', '0', '1'],
#"UL17_TTga_M1500":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1500/TstarTstarToTgluonTgamma_M-1500_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1500/220802_213600/0000'], 'mc', 'none', '2017', 'none', '0.000394014', '41.48', '200000.0', '0', '1'],
#"UL17_TTga_M800":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M800/TstarTstarToTgluonTgamma_M-800_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M800/220802_213715/0000'], 'mc', 'none', '2017', 'none', '0.097776', '41.48', '200000.0', '0', '1'],
"UL17_ST_t_channel_antitop":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_ST_t_channel_antitop/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5up_13TeV-powheg-madspin-pythia8/crab_UL17_ST_t-channel_antitop/220803_083447/0000'], 'mc', 'none', '2017', 'none', '1', '41.48', '24935049.1161', '0', '1'],
#"UL17_TTga_M1200":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1200/TstarTstarToTgluonTgamma_M-1200_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1200/220802_213831/0000'], 'mc', 'none', '2017', 'none', '0.00312534', '41.48', '200000.0', '0', '1'],
"UL17_WGJets_MonoPhoton_PtG_40to130":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WGJets_MonoPhoton_PtG_40to130'], 'mc', 'none', '2017', 'none', '17.018', '41.48', '3598774.0', '0', '1'],
#"UL17_TTga_M700":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M700/TstarTstarToTgluonTgamma_M-700_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M700/220802_213947/0000'], 'mc', 'none', '2017', 'none', '0.286344', '41.48', '200000.0', '0', '1'],
"UL17_QCD_HT100to200":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT100to200'], 'mc', 'none', '2017', 'none', '27990000', '41.48', '54381393.0', '0', '1'],
"UL17_QCD_HT500to700":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT500to700'], 'mc', 'none', '2017', 'none', '32100', '41.48', '36194860.0', '0', '1'],
"UL17_WJetsToLNu":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WJetsToLNu'], 'mc', 'none', '2017', 'none', '61526.7', '41.48', '105947254.894', '0', '1'],
"UL17_WGJets_MonoPhoton_PtG_130":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WGJets_MonoPhoton_PtG_130'], 'mc', 'none', '2017', 'none', '0.88', '41.48', '2049282.0', '0', '1'],
"UL17_TTToHadronic":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTToHadronic/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/crab_UL17_TTToHadronic/220802_214103/0000'], 'mc', 'none', '2017', 'none', '379.11', '41.48', '213188606.697', '0', '1'],
"UL17_antitWNoFullyHadronic":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_antitWNoFullyHadronic/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_UL17_antitWNoFullyHadronic/220803_092657/0000'], 'mc', 'none', '2017', 'none', '19.47', '41.48', '6994364.77413', '0', '1'],
"UL17_QCD_HT1500to2000":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT1500to2000'], 'mc', 'none', '2017', 'none', '119.9', '41.48', '7701876.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_200To400":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_200To400'], 'mc', 'none', '2017', 'none', '1176', '41.48', '33884844.0', '0', '1'],
#"UL17_TTga_M1300":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1300/TstarTstarToTgluonTgamma_M-1300_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1300/220802_214334/0000'], 'mc', 'none', '2017', 'none', '0.00151902', '41.48', '200000.0', '0', '1'],
"UL17_ST_t_channel_top":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_ST_t_channel_top/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/crab_UL17_ST_t-channel_top/220803_083216/0000'], 'mc', 'none', '2017', 'none', '1', '41.48', '110989397.314', '0', '1'],
"UL17_TTToSemiLeptonic":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTToSemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/crab_UL17_TTToSemiLeptonic/220802_214450/0000'], 'mc', 'none', '2017', 'none', '365.34', '41.48', '329449244.144', '0', '1'],
"UL17_tWNoFullyHadronic":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_tWNoFullyHadronic/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_UL17_tWNoFullyHadronic/220803_083332/0000'], 'mc', 'none', '2017', 'none', '19.47', '41.48', '8506765.0112', '0', '1'],
#"UL17_TTga_M1000":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1000/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1000/220802_214616/0000'], 'mc', 'none', '2017', 'none', '0.0152484', '41.48', '200000.0', '0', '1'],

 
"data_UL17_F_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_F_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL17_E_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_E_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL17_B_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_B_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL17_C_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_C_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL17_D_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_D_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'D', '1', '41.48', '1', '0', '1'],
}
