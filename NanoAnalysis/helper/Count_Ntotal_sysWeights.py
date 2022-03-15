# This file skims the data and saves the output to ./tmp
# Do not combine files across runs, otherwise you may get inconsistent TTree structures!
# Doing things file by file is the safest way to avoid this problem, and comes at almost
# no extra cost.
# You can copy and paste json sources directly from https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/

import os
import ROOT
path = []

#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-10to50_v3/191130_081246/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-10to50_v3_ext1/191130_081323/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M50_v3_ext1/191130_075804/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_v3_ext2/191130_081130/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/crab_TTTo2L2Nu/191130_081559/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WWTo2L2Nu_13TeV-powheg/crab_WWTo2L2Nu/191130_090952/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/ZZTo2L2Nu_13TeV_powheg_pythia8/crab_ZZTo2L2Nu/191130_091725/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_antitop_v3_ext1/191130_092526/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/crab_ST_tW_top_v3_ext1/191130_093520/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/ZZTo4L_13TeV_powheg_pythia8/crab_ZZTo4L/191130_092020/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/crab_WZTo2L2Q/191130_091455/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/crab_WZTo3LNu_v3_ext1_v1/191201_062001/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu_v3_ext2_v2/191130_113603/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu_v3_v2/191130_115257/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToQQ/191130_110848/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToLLNuN/191130_110706/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_v3_ext1_v2/191201_071154/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_v3_ext3_v1/191201_071416/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_v3_ext1_v2/191201_070704/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu/191130_110349/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToQQ/191130_110154/0000/')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TOPptSamples/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_Mtt_1000toInf/200226_084805/0000')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TOPptSamples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT/200226_084823/0000')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TOPptSamples/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_Mtt_700to1000/200226_084843/0000')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_amc_v3_v1/191130_144027/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_amc_v3_ext2_v1/191130_144155/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_amc_v3_ext2_v1/191130_144155/0001/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50-amcFXFX/200310_182844/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2016/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5_PSweights_2016/200311_140933/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5_PSweights_erdON_13TeV-powheg-pythia8/crab_TTTo2L2Nu_erdON/200311_145319/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_QCDbased/200311_145409/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5down_v3_v1/200311_145235/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5down_v3_ext1/200311_145122/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5up_v3_v1/200311_145034/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5up_v3_ext1/200311_144936/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampDOWN_v3_v1/200311_144843/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampDOWN_v3_ext1/200311_144755/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampUP_v3_v1/200311_144425/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2016/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampUP_v3_ext1/200311_144331/0000/')

#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-10to50_v14-v1/191201_123859/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-10to50_v14_ext1_v2/191201_123656/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_v14_ext1-v1/191201_122119/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_v14_ext1-v1/191201_122119/0001/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_v14_ext1-v1/191201_122119/0002/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_v14_v1/191201_124029/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_top/191201_124931/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_antitop/191201_125119/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/crab_WWTo2L2Nu/191201_124202/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ZZTo2L2Nu_13TeV_powheg_pythia8/crab_ZZTo2L2Nu/191201_124641/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ZZTo4L_13TeV_powheg_pythia8/crab_ZZTo4L/191201_124808/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/crab_WZTo2L2Q/191201_124509/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_WZTo3LNu/191201_124341/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu/191201_132144/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToQQ_v14_v1/191201_131707/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_v14_v1/191201_125315/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_v14_v1/191201_131835/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToQQ_v14_v1/191201_132958/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_top/191201_124931/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_antitop/191201_125119/0000/')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutc/')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_vector_emutu/')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutc/')
#path.append('/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_TT_vector_emutu/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5_PSweights_v14_v2/200311_161044/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2017/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5_PSweights_v14_v2/200311_161044/0001/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2017/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampUP_v14_v1/200311_161214/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2017/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_TTo2L2Nu_hdampDOWN_v14_v1/200311_161259/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2017/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5up_v14_v1/200311_161406/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2017/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5down_v14_v1/200311_161500/0000/')


#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_v1/200311_151257/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0001/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_amcatnlo_v15_ext2_v1/200311_150842/0002/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_top_v15_ext1-v2/191201_151723/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_antitop_v15_ext1-v2/191201_152039/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-10to50_v15_v2/191201_145133/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50/191201_144729/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50/191201_144729/0001/')
path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_3/191215_182557/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_antitop_v15_ext1-v2/191201_152039/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_ST_tW_top_v15_ext1-v2/191201_151723/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/crab_WWTo2L2Nu/191201_145426/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/crab_ZZTo2L2Nu_v15_ext2-v2/191201_151518/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/crab_ZZTo4L_v15_ext1-v2/191201_151326/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/crab_WZTo2L2Q_v15_v1/191201_150857/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/crab_WZTo3LNu_v15-v1/191201_145614/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/crab_WJetsToLNu/191201_153344/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToQQ_v15_v1/191201_152701/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_TTWJetsToLNu_v15_ext1-v2/191201_152347/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToLLNuNu_v15_ext1-v2/191201_152847/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/MC_RunII_2018/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/crab_TTZToQQ_v15_ext1-v1/191201_153157/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampUP_v15_ext1_v1/200311_154046/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampUP_v15_v1/200311_154149/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampDOWN_v15_ext1_v1/200311_154237/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8/crab_TTTo2L2Nu_hdampDOWN_v15_v1/200311_154323/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5up_v15_ext1_v1/200311_154416/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5up_v15_v1/200311_154516/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5down_v15_ext1_v1/200311_154727/0000/')
#path.append('/pnfs/iihe/cms/store/user/schenara/SYS_RunII_2018/TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8/crab_TTTo2L2Nu_TuneCP5down_v15_v1/200311_154910/0000/')
nEventsraw = 0
neventsweight = 0
nEventsStored = 0
nEventsiihe = 0
LHEWeightID=[]
sumOfLHEWeight=[]
sumOfMcWeight=[]

for n,a in enumerate(path):
    filenames = os.listdir(a)
    for fnum, fname in enumerate(filenames):
        filename = a + '/' + fname
        print fname 
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
        if fnum==0 and n==0:
            for j in range(tree_meta.mc_LHEweightsId.size()):
                LHEWeightID.append(float(tree_meta.mc_LHEweightsId[j]))
                sumOfLHEWeight.append(tree_meta.mc_sumofLHEWeights[j])
            for j in range(tree_meta.mc_sumofgenWeights.size()):
                sumOfMcWeight.append(tree_meta.mc_sumofgenWeights[j])
        else:
            for j in range(tree_meta.mc_LHEweightsId.size()):
                sumOfLHEWeight[j]+=tree_meta.mc_sumofLHEWeights[j]
            for j in range(tree_meta.mc_sumofgenWeights.size()):
                sumOfMcWeight[j]+=tree_meta.mc_sumofgenWeights[j]
        f.Close()

round_sumOfLHEWeight = [round(num, 2) for num in sumOfLHEWeight]
round_sumOfMcWeight = [round(num, 2) for num in sumOfMcWeight]
print 'LHEWeightID='
print LHEWeightID
print 'sumOfLHEWeight='
print round_sumOfLHEWeight
print 'sumOfMcWeight='
print round_sumOfMcWeight
print 'nEventsraw %d   '%(nEventsraw)
print 'neventsweight %d   '%(neventsweight)
print 'nEventsStored %d   '%(nEventsStored)
print 'nEventsiihe %d   '%(nEventsiihe)
