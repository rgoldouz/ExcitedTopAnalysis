#include "../include/MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events") ;
////    ch ->Add("/hadoop/store/user/rgoldouz/FullProduction/IIHE_Ntuple_10215/ntuple_M1000_gaChannel/*10.root");
//    ch ->Add("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/outfile2.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/ExitedTopSamplesDataJan2021/SinglePhoton/crab_2017_F_SinglePhoton/210111_081219/0000/outfile_1-97.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/ExitedTopSamplesMC/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017_ttG/200526_145939/0000/outfile_1-11.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/FullProduction/IIHE_Ntuple_10215/ntuple_M1000_gaChannel/outfile_*5.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/ExitedTopSamplesMCJan2021/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_2017_GJetsHT600ToInf/210502_173452/0000/outfile_15*.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/Etop_nanoAODv9_MC/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/crab_2017_ttG/210922_094823/0000/tree_22.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/Etop_nanoAODv9_MC/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/crab_2017_NewQCDHT700to1000/210922_100737/0000/tree_9.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT400To600/210922_100157/0000/tree_1.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000/slim_14.*");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTG/tree_137.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_600ToInf/tree_444.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1000/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1000/220802_214616/0000/tree_7.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_WJetsToLNu/*");    
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTG/*");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTGamma_Hadronic_ptGamma200inf/TTGamma_Hadronic_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTGamma_Hadronic_ptGamma200inf/221027_121810/0000/tree_1.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_tWNoFullyHadronic/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/crab_UL17_tWNoFullyHadronic/220803_083332/0000/tree_1*");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M1000/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M1000/220802_214616/0000/*.root");
///    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/data_UL17_F_SinglePhoton/tree_530.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL18/v1/UL18_TTGamma_Hadronic_ptGamma100To200/TTGamma_Hadronic_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/crab_UL18_TTGamma_Hadronic_ptGamma100To200/231126_091745/0000/tree_1.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL18/v1/UL18_TTga_M2000/TstarTstarToTgluonTgamma_M-2000_TuneCP5_13TeV-madgraph-pythia8/crab_UL18_TTga_M2000/231126_000448/0000/tree_1.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL18/v1/data_UL18_C_EGamma/EGamma/crab_data_UL18_C_EGamma/231125_235619/0000/tree_22.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL16preVFP/v1/data_UL16preVFP_D_SingleElectron/SingleElectron/crab_data_UL16preVFP_D_SingleElectron/231126_092305/0000/tree_63.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL16preVFP/v1/UL16preVFP_TTgaSpin32_M1600/TstarTstarToTgluonTgamma_M-1600_TuneCP5_Spin32_13TeV-madgraph-pythia8/crab_UL16preVFP_TTgaSpin32_M1600/231127_115923/0000/tree_1.root");
    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_GJets_DR_0p4_HT_400To600/tree_3*");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M800/TstarTstarToTgluonTgamma_M-800_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M800/220802_213715/0000/tree_10.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTGamma_SingleLep_ptGamma200inf/TTGamma_SingleLept_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTGamma_SingleLep_ptGamma200inf/221027_122042/0000/tree_5.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000/slim_402.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_23.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_24.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_34.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_43.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_47.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_46.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_44.root");
//    ch ->Add("/hadoop/store/user/rbucci/ExcitedTops/Ntuples/2020_05_12/mc2017/tptp/tptp_tgta_M1000/ntuple_41.root");
//    ch ->Add("/hadoop/store/user/rgoldouz/ExitedTopSamplesMC/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/crab_2017_tt/200526_145717/0000/outfile_3-149.root");
//    rbucci/ExcitedTops/SlimNano/SlimNano_Feb2021/slim_TTga_M1000
    MyAnalysis t1(ch);
//    t1.Loop("test.root", "data",   "SinglePhoton",    "2016preVFP",    "E",   1,1,1,0,1);
//    t1.Loop("M1600", "mc", "none", "2017", "none", 0.18550148, 59.83, 2866000.0, 0, 1);
//    t1.Loop("UL17_TTga_M1000", "mc" , "SinglePhoton" , "2017" , "" , 2.06 , 41.53 , 494000,0,1);
    t1.Loop("UL17_Gjet", "mc" , "SinglePhoton" , "2017" , "" , 2.06 , 41.53 , 494000,0,1);
}
