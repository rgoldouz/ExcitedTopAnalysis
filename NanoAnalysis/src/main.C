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
    ch ->Add("/hadoop/store/user/rgoldouz/Etop_nanoAODv9_MC/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_v2/crab_2017_GJetsHT400To600/210922_100157/0000/tree_1.root");
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
//    t1.Loop("test.root", "data",   "SinglePhoton",    "2017",    "E",   1,1,1);
    t1.Loop("lll.root", "mc" , "SinglePhoton" , "2017" , "" , 2.06 , 41.53 , 494000,0,1);
}