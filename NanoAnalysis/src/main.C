#include "../include/MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events") ;
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL16preVFP/v1/data_UL16preVFP_D_SinglePhoton/SinglePhoton/crab_data_UL16preVFP_D_SinglePhoton/231127_141914/0000/tree_11.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTga_M800/TstarTstarToTgluonTgamma_M-800_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTga_M800/220802_213715/0000/tree_10.root");
    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL18/v1/UL18_TTga_M1000/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/crab_UL18_TTga_M1000/231125_231711/0000/tree_1.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_TTGamma_Hadronic_ptGamma200inf/TTGamma_Hadronic_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/crab_UL17_TTGamma_Hadronic_ptGamma200inf/221027_121810/0000/tree_1.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/NanoAodPostProcessingULGammaJets/UL17/v1/UL17_QCD_HT500to700/tree_33*");
    MyAnalysis t1(ch);
//    t1.Loop("test.root", "data",   "SinglePhoton",    "2016preVFP",    "E",   1,1,1,0,1);
    t1.Loop("M1000", "mc", "none", "2018", "none", 0.18550148, 59.83, 2866000.0, 0, 1);
}
