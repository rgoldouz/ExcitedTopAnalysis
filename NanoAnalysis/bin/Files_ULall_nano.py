import sys 
import os 
import subprocess 
import readline 
import string 

UL17={
"slim_TTga_M1200":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1200'], 'mc', 'none', '2017', 'none', '0.00312534', '41.48', '500000.0', '0', '1'],
"UL17_QCD_HT700to1000":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT700to1000'], 'mc', 'none', '2017', 'none', '6831', '41.48', '32934816.0', '0', '1'],
"UL17_DY50":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_DY50'], 'mc', 'none', '2017', 'none', '6077.22', '41.48', '130529214.888', '0', '1'],
"UL17_GJets_DR_0p4_HT_400To600":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_400To600'], 'mc', 'none', '2017', 'none', '132.1', '41.48', '9022800.0', '0', '1'],
"UL17_QCD_HT300to500":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT300to500'], 'mc', 'none', '2017', 'none', '347700', '41.48', '43429979.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_100To200":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_100To200'], 'mc', 'none', '2017', 'none', '5383', '41.48', '10034997.0', '0', '1'],
"UL17_QCD_HT2000toInf":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT2000toInf'], 'mc', 'none', '2017', 'none', '25.24', '41.48', '4112573.0', '0', '1'],
"UL17_QCD_HT200to300":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT200to300'], 'mc', 'none', '2017', 'none', '1712000', '41.48', '42714435.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_600ToInf":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_600ToInf'], 'mc', 'none', '2017', 'none', '44.32', '41.48', '8330226.0', '0', '1'],
"slim_TTga_M0800":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M0800'], 'mc', 'none', '2017', 'none', '0.097776', '41.48', '500000.0', '0', '1'],
"slim_TTga_M1300":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1300'], 'mc', 'none', '2017', 'none', '0.00151902', '41.48', '500000.0', '0', '1'],
"UL17_DY10to50_v9":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_DY10to50_v9'], 'mc', 'none', '2017', 'none', '18610', '41.48', '68101524.0', '0', '1'],
"UL17_TTG":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTG'], 'mc', 'none', '2017', 'none', '1', '41.48', '1261451.94994', '0', '1'],
"UL17_WJetsToLNu":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WJetsToLNu'], 'mc', 'none', '2017', 'none', '61526.7', '41.48', '105947254.894', '0', '1'],
"slim_TTga_M1000":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000'], 'mc', 'none', '2017', 'none', '0.0152484', '41.48', '500000.0', '0', '1'],
"UL17_QCD_HT1000to1500":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT1000to1500'], 'mc', 'none', '2017', 'none', '1207', '41.48', '10186734.0', '0', '1'],
"UL17_WGJets_MonoPhoton_PtG_40to130":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WGJets_MonoPhoton_PtG_40to130'], 'mc', 'none', '2017', 'none', '17.018', '41.48', '3598774.0', '0', '1'],
"UL17_QCD_HT100to200":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT100to200'], 'mc', 'none', '2017', 'none', '27990000', '41.48', '54381393.0', '0', '1'],
"UL17_QCD_HT500to700":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT500to700'], 'mc', 'none', '2017', 'none', '32100', '41.48', '36194860.0', '0', '1'],
"UL17_WGJets_MonoPhoton_PtG_130":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WGJets_MonoPhoton_PtG_130'], 'mc', 'none', '2017', 'none', '0.88', '41.48', '2049282.0', '0', '1'],
"slim_TTga_M1600":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1600'], 'mc', 'none', '2017', 'none', '0.000208938', '41.48', '500000.0', '0', '1'],
"UL17_QCD_HT1500to2000":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT1500to2000'], 'mc', 'none', '2017', 'none', '119.9', '41.48', '7701876.0', '0', '1'],
"UL17_TTJets":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTJets'], 'mc', 'none', '2017', 'none', '831.76', '41.48', '90030688.4968', '0', '1'],
"slim_TTga_M1700":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1700'], 'mc', 'none', '2017', 'none', '0.286344', '41.48', '500000.0', '0', '1'],
"UL17_GJets_DR_0p4_HT_200To400":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_200To400'], 'mc', 'none', '2017', 'none', '1176', '41.48', '33884844.0', '0', '1'],
"slim_TTga_M1400":[['rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1400'], 'mc', 'none', '2017', 'none', '0.00076242', '41.48', '500000.0', '0', '1'],

 
"data_UL17_B_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_B_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'B', '1', '41.48', '1', '0', '1'],
"data_UL17_E_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_E_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'E', '1', '41.48', '1', '0', '1'],
"data_UL17_F_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_F_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'F', '1', '41.48', '1', '0', '1'],
"data_UL17_C_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_C_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'C', '1', '41.48', '1', '0', '1'],
"data_UL17_D_SinglePhoton":[['rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_D_SinglePhoton'], 'data', 'SinglePhoton', '2017', 'D', '1', '41.48', '1', '0', '1'],
}