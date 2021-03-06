#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "PU_reWeighting.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
#include "ScaleFactors.h"
#include "RoccoR.h"
#include "BTagCalibrationStandalone.h"
#include "Utils.h"
#include "correction.h"
#include "CondFormats/Serialization/interface/Archive.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

using namespace std;
using namespace correction;

int vInd(std::map<TString, std::vector<float>> V, TString name){
  return V.find(name)->second.at(0);
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset ,string year, TString run, float xs, float lumi, float Nevent, int iseft, int nRuns){
// Get starting timepoint
   auto start = high_resolution_clock::now();

   string deepAk8TopTagSF="";
   string photonSF="";

   if(year == "2016"){
     deepAk8TopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2017_EOY/2017_jmar.json";
     photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2017_UL/photon.json";
   }

   if(year == "2017"){
     deepAk8TopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2017_EOY/2017_jmar.json";
     photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2017_UL/photon.json";
   }

   if(year == "2018"){
     deepAk8TopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2017_EOY/2017_jmar.json";
     photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2017_UL/photon.json";
   }


   auto csetFileDeepAk8TopTagSF = CorrectionSet::from_file(deepAk8TopTagSF);
   auto csetDeepAk8TopTagSF = csetFileDeepAk8TopTagSF->at("DeepAK8_Top_MassDecorr");
   cout<<"Scale factor is: "<<csetDeepAk8TopTagSF->evaluate({2.1, 390.0, "nom", "1p0"})<<endl;
   auto csetFilePhotonSF = CorrectionSet::from_file(photonSF);
   auto csetPhotonCsevSF = csetFilePhotonSF->at("UL-Photon-CSEV-SF");
   auto csetPhotonIdSF = csetFilePhotonSF->at("UL-Photon-ID-SF");
   cout<<"ID Scale factor is: "<<csetPhotonCsevSF->evaluate({"2017", "sf", "Medium", "EBInc"})<<endl;
   cout<<"CSEV Scale factor is: "<<csetPhotonIdSF->evaluate({"2017", "sf", "Medium", 1.1,100.1})<<endl;


  TRandom3 Tr;
  TFile *f_topMistagRate = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/topMistagRate.root");
  TH1F h_topMistagRate = *(TH1F*)f_topMistagRate->Get("topMistagRate");
  f_topMistagRate->Close();
  ULong64_t Event;
  int Lumi;
  int Run;
  int Ch;
  std::vector<float> Ph_pt;
  std::vector<float> Ph_eta;
  std::vector<float> Ph_phi;
  std::vector<float> Ak8_pt;
  std::vector<float> Ak8_eta;
  std::vector<float> Ak8_phi;
  TFile file_out ("ANoutput.root","RECREATE");
  TTree tree_out("TStar","Excited top analysis") ;
  tree_out.Branch("Event"      , &Event      ) ;
  tree_out.Branch("Lumi"      , &Lumi      , "Lumi/I"      ) ;
  tree_out.Branch("Run"      , &Run      , "Run/I"      ) ;
  tree_out.Branch("Ch"      , &Ch      , "Ch/I"      ) ;
  tree_out.Branch("Ph_pt"      , &Ph_pt  ) ;
  tree_out.Branch("Ph_eta"      , &Ph_eta  ) ;
  tree_out.Branch("Ph_phi"      , &Ph_phi  ) ;
  tree_out.Branch("Ak8_pt"      , &Ak8_pt  ) ;
  tree_out.Branch("Ak8_eta"      , &Ak8_eta  ) ;
  tree_out.Branch("Ak8_phi"      , &Ak8_phi  ) ;


  float MVA_Ph_pt, MVA_Ph_eta, MVA_Ak8_pt, MVA_Ak8_eta, MVA_Ak8_Mass, MVA_Ak8_TvsQCD, MVA_Ak8_N, MVA_Ak8_Nbsub, MVA_Ak8_NtopTag, MVA_Ak4_pt, MVA_Ak4_eta, MVA_Ak4_HT, MVA_Ak4_N;
  tree_out.Branch("MVA_Ph_pt"      , &MVA_Ph_pt) ;
  tree_out.Branch("MVA_Ph_eta"     , &MVA_Ph_eta) ;
  tree_out.Branch("MVA_Ak8_eta"    , &MVA_Ak8_eta) ;
  tree_out.Branch("MVA_Ak8_pt"     , &MVA_Ak8_pt) ;
  tree_out.Branch("MVA_Ak8_Mass"   , &MVA_Ak8_Mass) ;
  tree_out.Branch("MVA_Ak8_TvsQCD"      , &MVA_Ak8_TvsQCD) ;
  tree_out.Branch("MVA_Ak8_N"      , &MVA_Ak8_N) ;
  tree_out.Branch("MVA_Ak8_Nbsub"      , &MVA_Ak8_Nbsub) ;
  tree_out.Branch("MVA_Ak8_NtopTag"      , &MVA_Ak8_NtopTag) ;
  tree_out.Branch("MVA_Ak4_pt"      , &MVA_Ak4_pt) ;
  tree_out.Branch("MVA_Ak4_eta"      , &MVA_Ak4_eta) ;
  tree_out.Branch("MVA_Ak4_HT"      , &MVA_Ak4_HT) ;
  tree_out.Branch("MVA_Ak4_N"      , &MVA_Ak4_N) ;

//MVA setting
   TMVA::Tools::Instance();
   TMVA::Reader *readerMVA = new TMVA::Reader( "!Color:!Silent" );
   Float_t MVA_Input_Ph_pt, MVA_Input_Ph_eta, MVA_Input_Ak8_pt, MVA_Input_Ak8_eta, MVA_Input_Ak8_Mass, MVA_Input_Ak8_TvsQCD, MVA_Input_Ak8_N, MVA_Input_Ak8_Nbsub, MVA_Input_Ak8_NtopTag, MVA_Input_Ak4_pt, MVA_Input_Ak4_eta, MVA_Input_Ak4_HT, MVA_Input_Ak4_N;


  readerMVA->AddVariable ("MVA_Input_Ph_pt"      , &MVA_Input_Ph_pt) ;
  readerMVA->AddVariable ("MVA_Input_Ph_eta"     , &MVA_Input_Ph_eta) ;
  readerMVA->AddVariable ("MVA_Input_Ak8_pt"     , &MVA_Input_Ak8_pt) ;
  readerMVA->AddVariable ("MVA_Input_Ak8_eta"    , &MVA_Input_Ak8_eta) ;
  readerMVA->AddVariable ("MVA_Input_Ak8_Mass"   , &MVA_Input_Ak8_Mass) ;
//  readerMVA->AddVariable ("MVA_Input_Ak8_TvsQCD"      , &MVA_Input_Ak8_TvsQCD) ;
  readerMVA->AddVariable ("MVA_Input_Ak8_Nbsub"      , &MVA_Input_Ak8_Nbsub) ;
  readerMVA->AddVariable ("MVA_Input_Ak8_N"      , &MVA_Input_Ak8_N) ;
  readerMVA->AddVariable ("MVA_Input_Ak4_N"      , &MVA_Input_Ak4_N) ;
  readerMVA->AddVariable ("MVA_Input_Ak4_pt"      , &MVA_Input_Ak4_pt) ;
  readerMVA->AddVariable ("MVA_Input_Ak4_eta"      , &MVA_Input_Ak4_eta) ;
  readerMVA->AddVariable ("MVA_Input_Ak4_HT"      , &MVA_Input_Ak4_HT) ;

  readerMVA->BookMVA( "MLP", "/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/MVA/dataset/weights/TMVAClassification_MLP.weights.xml");

//  typedef vector<TH1F*> Dim1;
//  typedef vector<Dim1> Dim2;
//  typedef vector<Dim2> Dim3;
//  typedef vector<Dim3> Dim4;


  const std::map<TString, std::vector<float>> vars =
  {
    {"GammaPt",                        {0,      40,   0,  1000}},
    {"GammaEta",                       {1,      20,   -3, 3   }},
    {"GammaPhi",                       {2,      25,   -4, 4   }},
    {"jet04Pt",                        {3,      40,   0,  1000}},
    {"jet04Eta",                       {4,      20,   -3, 3   }},
    {"jet04Phi",                       {5,      25,   -4, 4   }},
    {"njet04",                         {6,      10,    0, 10  }},
    {"nbjet04",                        {7,      4 ,    0, 4   }},
    {"jet08Pt",                        {8,      10,    0, 1000}},
    {"jet08Eta",                       {9,      20,   -3, 3   }},
    {"jet08Phi",                       {10,     25,   -4, 4   }},
    {"njet08",                         {11,     7,     0, 7   }},
    {"Met",                            {12,     20,    0, 200 }},
    {"nVtx",                           {13,     70,    0, 70  }},
    {"nPh",                            {14,     3,     0, 3   }},
    {"phoChargedIso",                  {15,     200,    0, 20  }},
    {"drGj04",                         {16,     14,    0, 7   }},
    {"dPhiGj08",                       {17,     14,    0, 7  }},
    {"HT",                             {18,     35,    0, 7000}},
    {"HoE",                            {19,     20,    0, 0.05}},
    {"softdropMass",                   {20,     40,    0, 800 }},
    {"tau21",                          {21,     20,    0, 1   }},
    {"tau31",                          {22,     20,    0, 1   }},
    {"nbjet08",                        {23,     4,     0, 4   }},
    {"TvsQCD",                         {24,     20,    0, 1   }},
    {"nBsub",                          {25,     4,     0, 4   }},
    {"njet08massG50",                  {26,     5,     0, 5   }},
    {"njet08massG120",                 {27,     5,     0, 5   }},
    {"TsMass1",                        {28,     40,    0, 4000}},
    {"nTopTag",                        {29,     4,     0, 4   }},
    {"nWTag",                          {30,     4,     0, 4   }},
    {"masstS2",                        {31,     40,    0, 2000}},
    {"Sietaieta",                      {32,     40,    0, 0.02}}
  };

  std::vector<TString> regions{"nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1TtagG0MTs2G300", "nAk8G1nTtag0","nAk8G1nTtag0MTs2G300", "nAk8G1nTtag0XtopMissTagRate", "nAk8G1Ttag0MTs2G300XtopMissTagRate"};
  std::vector<TString> channels{"aJets", "fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsOthers"};

//  D3HistsContainer Hists;
  Hists.resize(channels.size());
  for (int i=0;i<channels.size();++i){
    Hists[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      Hists[i][k].resize(vars.size());
    }
  }

//  Dim3 Hists(channels.size(),Dim2(regions.size(),Dim1(vars.size())));
  std::stringstream name;
  TH1F *h_test;

  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
        name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first;
        h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
        h_test->StatOverflows(kTRUE);
        h_test->Sumw2(kTRUE);
        Hists[i][k][it->second.at(0)] = h_test;
        name.str("");
      }
    }
  }

  std::vector<TString> sys{"phIDSf", "pu", "prefiring", "trigSF"};
  HistsSysUp.resize(1);
  for (int i=0;i<1;++i){
    HistsSysUp[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsSysUp[i][k].resize(vars.size());
      for (int n=0;n<vars.size();++n){
        HistsSysUp[i][k][n].resize(sys.size());
      }
    }
  }

  HistsSysDown.resize(1);
  for (int i=0;i<1;++i){
    HistsSysDown[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsSysDown[i][k].resize(vars.size());
      for (int n=0;n<vars.size();++n){
        HistsSysDown[i][k][n].resize(sys.size());
      }
    }
  }

  for (int i=0;i<1;++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
        for (int n=0;n<sys.size();++n){
          name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sys[n]<<"_Up";
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          HistsSysUp[i][k][it->second.at(0)][n] = h_test;
          name.str("");
          name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sys[n]<<"_Down";
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          HistsSysDown[i][k][it->second.at(0)][n] = h_test;
          name.str("");
        }
      }
    }
  }

  std::string JECFile04;
  if(year == "2016preVFP")    JECFile04 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16APV_V7_MC/Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.txt";
  if(year == "2016postVFP")   JECFile04 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16_V7_MC/Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.txt";
  if(year == "2017")          JECFile04 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL17_V5_MC/Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.txt";
  if(year == "2018")          JECFile04 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL18_V5_MC/Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt";

  std::vector<TString> sysJecNames{"AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta", "Total"};
  const int nsrc = 25;
  const char* srcnames[nsrc] = {"AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtHF","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativePtHF","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","RelativeStatHF","SinglePionECAL","SinglePionHCAL","TimePtEta", "Total"};
  std::vector<JetCorrectionUncertainty*> vsrc04(nsrc);
  for (int isrc = 0; isrc < nsrc; isrc++) {
    JetCorrectorParameters *p = new JetCorrectorParameters(JECFile04, srcnames[isrc]);
    JetCorrectionUncertainty *unc = new JetCorrectionUncertainty(*p);
    vsrc04[isrc] = unc;
  }

  std::string JECFile08;
  if(year == "2016preVFP")    JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16APV_V7_MC/Summer19UL16APV_V7_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2016postVFP")   JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16_V7_MC/Summer19UL16_V7_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2017")          JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL17_V5_MC/Summer19UL17_V5_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2018")          JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL18_V5_MC/Summer19UL18_V5_MC_UncertaintySources_AK8PFPuppi.txt";

  std::vector<JetCorrectionUncertainty*> vsrc08(nsrc);
  for (int isrc = 0; isrc < nsrc; isrc++) {
    JetCorrectorParameters *p = new JetCorrectorParameters(JECFile08, srcnames[isrc]);
    JetCorrectionUncertainty *unc = new JetCorrectionUncertainty(*p);
    vsrc08[isrc] = unc;
  }


  HistsJecUp.resize(1);
  for (int i=0;i<1;++i){
    HistsJecUp[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsJecUp[i][k].resize(vars.size());
      for (int n=0;n<vars.size();++n){
        HistsJecUp[i][k][n].resize(sysJecNames.size());
      }
    }
  }

  HistsJecDown.resize(1);
  for (int i=0;i<1;++i){
    HistsJecDown[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsJecDown[i][k].resize(vars.size());
      for (int n=0;n<vars.size();++n){
        HistsJecDown[i][k][n].resize(sysJecNames.size());
      }
    }
  }

  for (int i=0;i<1;++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
        for (int n=0;n<sysJecNames.size();++n){
          name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysJecNames[n]<<"_Up";
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          HistsJecUp[i][k][it->second.at(0)][n] = h_test;
          name.str("");
          name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysJecNames[n]<<"_Down";
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          HistsJecDown[i][k][it->second.at(0)][n] = h_test;
          name.str("");
        }
      }
    }
  }

  typedef vector<TH2F*> TH2FDim1;
  typedef vector<TH2FDim1> TH2FDim2;
  typedef vector<TH2FDim2> TH2FDim3;
  typedef vector<TH2FDim3> TH2FDim4;
  TH2F *h_test2d;
  std::vector<TString> vars2d {"M1vsM2"};
  TH2FDim3 Hists2d(channels.size(),TH2FDim2(regions.size(),TH2FDim1(vars2d.size())));
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[0];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),100,0,2000,100,0,2000);
        Hists2d[i][k][0] = h_test2d;
        name.str("");
    }
  }

// scale factors
  FatJetScaleFactor fatjetscalefactors = FatJetScaleFactor();
  cout<<fatjetscalefactors.ak8SF(false, 2017, 6, true, 0, 1, 330,  0)<<endl;

  std::vector<lepton_candidate*> *PhotonsMedium;
  std::vector<lepton_candidate*> *fakePhotons;
  std::vector<lepton_candidate*> *fakePhotonsIso;
  std::vector<lepton_candidate*> *fakePhotonsSiSi;
  std::vector<lepton_candidate*> *fakePhotonsOther;
  std::vector<lepton_candidate*> *selectedPhotons;
  std::vector<jet_candidate*> *selectedJets08;
  std::vector<jet_candidate*> *selectedJets04;
  std::vector<std::vector<jet_candidate*>> *JEC08sysUp;
  std::vector<std::vector<jet_candidate*>> *JEC08sysDown;
  std::vector<std::vector<jet_candidate*>> *JEC04sysUp;
  std::vector<std::vector<jet_candidate*>> *JEC04sysDown;
  std::vector<jet_candidate*> *JECJetsUp;
  std::vector<jet_candidate*> *JECJetsDown;
  std::vector<lepton_candidate*> *selectedLeptons;
  std::vector<int> *topIndex;
  std::vector<int> *wIndex;
  std::vector<int> *bsubIndex;
  std::vector<int> *topTagIndex;
  std::vector<int> *WTagIndex;

  PU wPU;
  int nAccept=0;
  int nMerged=0;
  int nOL=0;
  int nSemiMerged=0;
  bool triggerPassA;
  bool triggerPassMu;
  float weight_Lumi;
  float finalWeight;
  float finalWeightSF;
  float topTagSF;
  int nbjet04;
  int nbjet08;
  int ntop;
  int ntopTag;
  int ntopTagRandom;
  int nWTag;
  int nW;
  float FR;
  float drgj04;
  float drgj08;
  float drtA;
  float ht;
  bool jetlepfail;
  int ch;
  std::vector<int> reg;
  std::vector<float> wgt;
  std::vector<float> wgtUp;
  std::vector<float> wgtDown;
  float topPt;
  float tStarMass;
  bool topEvent=false;
  bool topLeptonicEvent=false;
  int NtopPartons;
  int NlepLHE;
  int Nmerged;
  double ptts;
  double MVAOutput;
  double fr=1;
  double sup = 0;
  double sdw = 0;

  std::vector<float> nominalWeights;
  nominalWeights.assign(sys.size(), 1);
  std::vector<float> sysUpWeights;
  sysUpWeights.assign(sys.size(), 1);
  std::vector<float> sysDownWeights;
  sysDownWeights.assign(sys.size(), 1);

  std::vector<long int> EVENT = {14113658};
  std::vector<TLorentzVector*> *topObjects;
  TLorentzVector *topObj;
  TLorentzVector BoostCandidate;
  TLorentzVector GluonCandidate;
  TLorentzVector TopCandidate;
  TLorentzVector GammaCandidate;
  TLorentzVector Ts2Candidate;

  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries ();


  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Ph_pt.clear();
    Ph_eta.clear();
    Ph_phi.clear();
    Ak8_pt.clear();
    Ak8_eta.clear();
    Ak8_phi.clear();
    reg.clear();
    wgt.clear();

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;

    triggerPassA = false;
    triggerPassMu = false;
    weight_Lumi =1;
    finalWeight =1;
    finalWeightSF =1;
    topTagSF =1;
    nbjet04=0;
    nbjet08=0;
    ntop = 0;
    ntopTag = 0;
    ntopTagRandom=0;
    nWTag = 0;
    nW = 0;
    FR= 1;
    drgj04 = 10;
    drgj08 = 10;
    ht=0;
    jetlepfail = false;
    ch=999;
    NtopPartons=0;
    topPt=0;
    Nmerged=0;
    NlepLHE=0;
    ptts=0;
    MVAOutput=-1;
    topLeptonicEvent=false;
    Ts2Candidate.SetPxPyPzE(0,0,0,0);

    for (int n=0;n<sys.size();++n){
      nominalWeights[n] =1;
      sysUpWeights[n] =1;
      sysDownWeights[n] =1;
    }

    if(data == "mc"){
      for (int l=0;l<nGenPart;l++){
        if(abs(GenPart_pdgId[l])==6){
          topEvent=true;
           break;
        }
      }
    }
    topObjects = new std::vector<TLorentzVector*>();
    if(topEvent){
      for (int l=0;l<nGenPart;l++){
       if(abs(GenPart_pdgId[l])==11 || GenPart_pdgId[l]==13 ||GenPart_pdgId[l]==15){
         if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) topLeptonicEvent=true;
       }

       if(abs(GenPart_pdgId[l])==600) ptts=GenPart_pt[l];
        if(abs(GenPart_pdgId[l])>0 && abs(GenPart_pdgId[l])<5 && abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) {
            topObj = new TLorentzVector ();
            topObj->SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]) ;
            topObjects->push_back(topObj);
        }
        if(abs(GenPart_pdgId[l])==5 && abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==6) {
            topObj = new TLorentzVector ();
            topObj->SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]) ;
            topObjects->push_back(topObj);
        }
        if(abs(GenPart_pdgId[l])==6){
          topPt = topPt + GenPart_pt[l];
        }
      }
    if(topObjects->size()!=6) topEvent=false;
          for (int l=0;l<nLHEPart;l++){
            if(abs(LHEPart_pdgId[l]) ==11 || abs(LHEPart_pdgId[l]) ==13 || abs(LHEPart_pdgId[l]) ==15 ) NlepLHE++;
          }
    }

//overlap removal of the qcd-gammaJets and ttbar-ttbarGamma
   if(data == "mc" &&     fname.Contains("QCD")){
     if (overlapRemoval(25., 2.5, 0.4, false)) {
       nOL++;
       continue;
     }
   }

   if(data == "mc" &&     fname.Contains("TTJets")){
     if (overlapRemoval(10.0, 5.0, 0.1, false)) {
       nOL++;
       continue;
     }
   }
//trigger
   if(data == "mc"){
       if(HLT_Photon200) triggerPassA = true;
//       if(HLT_IsoMu27) triggerPassMu = true;
     }
     if(data == "data"){
       if(dataset=="SinglePhoton"){
         if(HLT_Photon200) triggerPassA = true;
       }
//       if(dataset=="SingleMuon"){
//         if(!HLT_Photon200 && HLT_IsoMu27) triggerPassMu = true;
//       }
     }

     if(!(triggerPassA || triggerPassMu)) continue;
     if (std::find(EVENT.begin(), EVENT.end(), event) != EVENT.end()) cout<<"triggerPassA="<<triggerPassA<<"triggerPassMu"<<triggerPassMu<<endl;


    PhotonsMedium = new std::vector<lepton_candidate*>();
    fakePhotons = new std::vector<lepton_candidate*>();
    fakePhotonsIso = new std::vector<lepton_candidate*>();
    fakePhotonsSiSi = new std::vector<lepton_candidate*>();
    fakePhotonsOther = new std::vector<lepton_candidate*>();
    for (int l=0;l<nPhoton;l++){
//      bitset<16> myBitSet(Photon_vidNestedWPBitmap[l]);
//      cout << myBitSet.to_string() << " (" << myBitSet.to_ulong() << ") " << endl;
      if(Photon_pt[l] <250.0 || abs(Photon_eta[l])>1.444) continue;
      if(!Photon_electronVeto[l]) continue;
      std::vector<bool> cuts_loose = parsePhotonVIDCuts(Photon_vidNestedWPBitmap[l],1);
      if(!cuts_loose[1] ||  Photon_sieie[l] > 0.02 || Photon_pfRelIso03_chg[l]*Photon_pt[l] > 20.0) continue;
//      
//      if(Photon_hoe[l] <  0.02197  &&  Photon_sieie[l] <  0.01015  && Photon_pfRelIso03_chg[l] <  1.1 ) PhotonsMedium->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
//      else if(Photon_hoe[l] <  0.02197  &&  Photon_sieie[l] <  0.01015  && Photon_pfRelIso03_chg[l] > 10 ) fakePhotonsIso->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
//      else if(Photon_hoe[l] <  0.02197  &&  Photon_sieie[l] >  0.011 ) fakePhotonsSiSi->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
//      else fakePhotonsOther->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
//
      std::vector<bool> cuts_medium = parsePhotonVIDCuts(Photon_vidNestedWPBitmap[l],2);
      
      nominalWeights[0] = nominalWeights[0] * csetPhotonIdSF->evaluate({"2017", "sf", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({"2017", "sf", "Medium", "EBInc"});
      sysUpWeights[0] = sysUpWeights[0] * csetPhotonIdSF->evaluate({"2017", "sfup", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({"2017", "sfup", "Medium", "EBInc"});
      sysDownWeights[0] = sysDownWeights[0] * csetPhotonIdSF->evaluate({"2017", "sfdown", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({"2017", "sfdown", "Medium", "EBInc"});


      if(Photon_cutBased[l]>=2) PhotonsMedium->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      else if(cuts_medium[1] && cuts_medium[2] &&  cuts_medium[4] && cuts_medium[5] && Photon_pfRelIso03_chg[l]*Photon_pt[l] > 10) fakePhotonsIso->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      else if(cuts_medium[1] && !cuts_medium[2] && cuts_medium[4] && cuts_medium[5] && Photon_sieie[l] > 0.011) fakePhotonsSiSi->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      else fakePhotonsOther->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      Ph_pt.emplace_back(Photon_pt[l]);
      Ph_eta.emplace_back(Photon_eta[l]);
      Ph_phi.emplace_back(Photon_phi[l]);
    }

    sort(PhotonsMedium->begin(), PhotonsMedium->end(), ComparePtLep);
    sort(fakePhotonsIso->begin(), fakePhotonsIso->end(), ComparePtLep);
    sort(fakePhotonsSiSi->begin(), fakePhotonsSiSi->end(), ComparePtLep);
    sort(fakePhotonsOther->begin(), fakePhotonsOther->end(), ComparePtLep);


//select Muon
    selectedLeptons = new std::vector<lepton_candidate*>();
    for (int l=0;l<nMuon;l++){
      if(Muon_pt[l] <35 || abs(Muon_eta[l]) > 2.4) continue;
      if(!Muon_tightId[l]) continue;
      if(Muon_tkIsoId[l] < 2) continue;
      selectedLeptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10));
    }
    sort(selectedLeptons->begin(),selectedLeptons->end(), ComparePtLep);

//select jets AK8
    selectedJets08 = new std::vector<jet_candidate*>();
    topIndex = new std::vector<int>();
    wIndex = new std::vector<int>();
    bsubIndex = new std::vector<int>();
    topTagIndex = new std::vector<int>();
    WTagIndex = new std::vector<int>();
    int nsubB = 0;
    for (int l=0;l<nFatJet;l++){
      if(FatJet_pt[l] <225 || abs(FatJet_eta[l]) > 2.4) continue;
      jetlepfail = false;
      for (int i=0;i<PhotonsMedium->size();i++){
        if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      for (int i=0;i<fakePhotonsIso->size();i++){
        if(deltaR((*fakePhotonsIso)[i]->eta_,(*fakePhotonsIso)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      for (int i=0;i<fakePhotonsSiSi->size();i++){
        if(deltaR((*fakePhotonsSiSi)[i]->eta_,(*fakePhotonsSiSi)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      for (int i=0;i<fakePhotonsOther->size();i++){
        if(deltaR((*fakePhotonsOther)[i]->eta_,(*fakePhotonsOther)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      if(jetlepfail) continue;
      NtopPartons=0;
      if(topEvent){
        for (int i=0;i<topObjects->size();i++){
          if(deltaR((*topObjects)[i]->Eta(),(*topObjects)[i]->Phi(),FatJet_eta[l],FatJet_phi[l]) < 0.8 ) NtopPartons++;
         }
      }
      if(NtopPartons==3) Nmerged++;
      nsubB = 0;
      if (SubJet_btagCSVV2[FatJet_subJetIdx1[l]] > 0.580) nsubB = nsubB +1;
      if (SubJet_btagCSVV2[FatJet_subJetIdx2[l]] > 0.580) nsubB = nsubB +1;
     
      selectedJets08->push_back(new jet_candidate(FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_deepTagMD_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));

      Ak8_pt.emplace_back(FatJet_pt[l]);
      Ak8_eta.emplace_back(FatJet_eta[l]);
      Ak8_phi.emplace_back(FatJet_phi[l]);

      for (int j=0; j<PhotonsMedium->size();j++){
        if (deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_, FatJet_eta[l],FatJet_phi[l])< drgj08) drgj08 = deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,FatJet_eta[l],FatJet_phi[l]);
      }
    }
    sort(selectedJets08->begin(), selectedJets08->end(), CompareMassJet);

    JEC08sysUp = new std::vector<std::vector<jet_candidate*>>();
    JEC08sysDown = new std::vector<std::vector<jet_candidate*>>();
    if(data == "mc"){
      for (int n=0;n<sysJecNames.size();++n){
        JECJetsUp= new std::vector<jet_candidate*>();
        JECJetsDown= new std::vector<jet_candidate*>();
        for (int l=0;l<nFatJet;l++){
          if(abs(FatJet_eta[l]) > 2.4) continue;
          jetlepfail = false;
          for (int i=0;i<PhotonsMedium->size();i++){
            if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
          }
          if(jetlepfail) continue;
          JetCorrectionUncertainty *unc = vsrc08[n];
          unc->setJetPt(FatJet_pt[l]);
          unc->setJetEta(FatJet_eta[l]);
          sup = unc->getUncertainty(true);
          if ((1+sup)*FatJet_pt[l]>225) {
            JECJetsUp->push_back(new jet_candidate((1+sup)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_deepTagMD_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
          }
          unc->setJetPt(FatJet_pt[l]);
          unc->setJetEta(FatJet_eta[l]);
          sdw = unc->getUncertainty(false);
          if ((1-sdw)*FatJet_pt[l]>225){
            JECJetsDown->push_back(new jet_candidate((1-sdw)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_deepTagMD_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
          }
        }
        sort(JECJetsUp->begin(), JECJetsUp->end(), CompareMassJet);
        sort(JECJetsDown->begin(), JECJetsDown->end(), CompareMassJet);
        JEC08sysUp->push_back(*JECJetsUp);
        JEC08sysDown->push_back(*JECJetsDown);
      }
    }

    for (int j=0; j<selectedJets08->size();j++){
        if(FatJet_msoftdrop[(*selectedJets08)[j]->indice_]>50) wIndex->push_back((*selectedJets08)[j]->indice_);
        if(FatJet_msoftdrop[(*selectedJets08)[j]->indice_]>120) topIndex->push_back((*selectedJets08)[j]->indice_);
        if((*selectedJets08)[j]->Nbsub_>0) bsubIndex->push_back((*selectedJets08)[j]->indice_);
        if((*selectedJets08)[j]->toptag_>0) topTagIndex->push_back(j);
        if((*selectedJets08)[j]->Wtag_>0) WTagIndex->push_back(j);
    }

//select jets AK4

    selectedJets04 = new std::vector<jet_candidate*>();
    for (int l=0;l<nJet;l++){
      if(Jet_pt[l] <30 || abs(Jet_eta[l]) > 5 || Jet_jetId[l]<6) continue;
      jetlepfail = false;
      for (int i=0;i<PhotonsMedium->size();i++){
        if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }
      for (int i=0;i<fakePhotonsIso->size();i++){
        if(deltaR((*fakePhotonsIso)[i]->eta_,(*fakePhotonsIso)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }
      for (int i=0;i<fakePhotonsSiSi->size();i++){
        if(deltaR((*fakePhotonsSiSi)[i]->eta_,(*fakePhotonsSiSi)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }

      for (int i=0;i<fakePhotonsOther->size();i++){
        if(deltaR((*fakePhotonsOther)[i]->eta_,(*fakePhotonsOther)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }
      if(jetlepfail) continue;
      selectedJets04->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepB[l], year,Jet_partonFlavour[l],l,0,0,0,0,0,0));
      for (int j=0; j<PhotonsMedium->size();j++){
        if (deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,Jet_eta[l],Jet_phi[l])< drgj04)  drgj04 = deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,Jet_eta[l],Jet_phi[l]);
      }
    }
    sort(selectedJets04->begin(), selectedJets04->end(), ComparePtJet);
    JEC04sysUp = new std::vector<std::vector<jet_candidate*>>();
    JEC04sysDown = new std::vector<std::vector<jet_candidate*>>();
    if(data == "mc"){
      for (int n=0;n<sysJecNames.size();++n){
        JECJetsUp= new std::vector<jet_candidate*>();
        JECJetsDown= new std::vector<jet_candidate*>();
        for (int l=0;l<nJet;l++){
          if(abs(Jet_eta[l]) > 5 || Jet_jetId[l]<6) continue;
          jetlepfail = false;
          for (int i=0;i<PhotonsMedium->size();i++){
            if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
          }
          if(jetlepfail) continue;
          JetCorrectionUncertainty *unc = vsrc04[n];
          unc->setJetPt(Jet_pt[l]);
          unc->setJetEta(Jet_eta[l]);
          sup = unc->getUncertainty(true);
          if ((1+sup)*FatJet_pt[l]>30) {
            JECJetsUp->push_back(new jet_candidate((1+sup)*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepB[l], year,Jet_partonFlavour[l],l,0,0,0,0,0,0));
          }
          unc->setJetPt(Jet_pt[l]);
          unc->setJetEta(Jet_eta[l]);
          sdw = unc->getUncertainty(false);
          if ((1-sdw)*FatJet_pt[l]>30){
            JECJetsDown->push_back(new jet_candidate((1-sdw)*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepB[l], year,Jet_partonFlavour[l],l,0,0,0,0,0,0));
          }
        }
        sort(JECJetsUp->begin(), JECJetsUp->end(), ComparePtJet);
        sort(JECJetsDown->begin(), JECJetsDown->end(), ComparePtJet);
        JEC04sysUp->push_back(*JECJetsUp);
        JEC04sysDown->push_back(*JECJetsDown);
      }
    }

    for (int l=0;l<selectedJets04->size();l++){
      ht = ht + (*selectedJets04)[l]->pt_;
      if((*selectedJets04)[l]->btag_) nbjet04++;
      if(selectedJets08->size()>0){
        if (deltaR((*selectedJets04)[l]->eta_, (*selectedJets04)[l]->phi_,(*selectedJets08)[0]->eta_, (*selectedJets08)[0]->phi_) > 0.8) Ts2Candidate += (*selectedJets04)[l]->p4_;
      }
    }


    for (int l=0;l<selectedJets08->size();l++){
      if((*selectedJets08)[l]->btag_) nbjet08++;
      if((*selectedJets08)[l]->toptag_) ntopTag++;
      if((*selectedJets08)[l]->toptag_) topTagSF= topTagSF*fatjetscalefactors.ak8SF(false, 2017, 6, false, 1, (*selectedJets08)[l]->eta_, (*selectedJets08)[l]->pt_,  0);
    }
    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()>0) ch=0;
//    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()==0&& selectedLeptons->size()==1) ch=1;
//    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()>0 && selectedLeptons->size()==1) ch=2;
    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()==0&& fakePhotonsIso->size()>0) ch=1;
    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()==0&& fakePhotonsSiSi->size()>0) ch=2;
    if(selectedJets04->size()>1 && selectedJets08->size()>0 && PhotonsMedium->size()==0&& fakePhotonsOther->size()>0) ch=3;
    if(ch>10) continue;

    if(ch==0){
      MVA_Ph_pt= (*PhotonsMedium)[0]->pt_;
      MVA_Ph_eta= (*PhotonsMedium)[0]->eta_;
      MVA_Ak8_eta= (*selectedJets08)[0]->eta_;
      MVA_Ak8_pt= (*selectedJets08)[0]->pt_;
      MVA_Ak8_Mass= FatJet_msoftdrop[(*selectedJets08)[0]->indice_];
      MVA_Ak8_TvsQCD= FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_];
      MVA_Ak8_N = selectedJets08->size();
      MVA_Ak8_Nbsub = bsubIndex->size();
      MVA_Ak8_NtopTag = topTagIndex->size();
      MVA_Ak4_pt= (*selectedJets04)[0]->pt_;
      MVA_Ak4_eta=(*selectedJets04)[0]->eta_;
      MVA_Ak4_HT= ht;
      MVA_Ak4_N=selectedJets04->size();
      tree_out.Fill() ;
     }
    selectedPhotons = PhotonsMedium;
    if (ch==1) selectedPhotons = fakePhotonsIso;
    if (ch==2) selectedPhotons = fakePhotonsSiSi;
    if (ch==3) selectedPhotons = fakePhotonsOther;
    MVA_Input_Ph_pt= (*selectedPhotons)[0]->pt_;
    MVA_Input_Ph_eta= (*selectedPhotons)[0]->eta_;
    MVA_Input_Ak8_eta= (*selectedJets08)[0]->eta_;
    MVA_Input_Ak8_pt= (*selectedJets08)[0]->pt_;
    MVA_Input_Ak8_Mass= FatJet_msoftdrop[(*selectedJets08)[0]->indice_];
    MVA_Input_Ak8_N = selectedJets08->size();
    MVA_Input_Ak8_Nbsub = bsubIndex->size();
    MVA_Input_Ak4_pt= (*selectedJets04)[0]->pt_;
    MVA_Input_Ak4_eta=(*selectedJets04)[0]->eta_;
    MVA_Input_Ak4_HT= ht;
    MVA_Input_Ak4_N=selectedJets04->size();
    MVAOutput = readerMVA->EvaluateMVA( "MLP");

    for (int l=0;l<selectedJets08->size();l++){
      if((*selectedJets08)[l]->mass_>105 && (*selectedJets08)[l]->mass_<210){
        ntopTagRandom++;
        FR = FR * (1-rate(&h_topMistagRate,(*selectedJets08)[l]->pt_));
      }
    }

    if (data == "mc" && year == "2016preVFP") {
      nominalWeights[1] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[1] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"up");
      sysDownWeights[1] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2016postVFP") {
      nominalWeights[1] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[1] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"up");
      sysDownWeights[1] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2017") {
      nominalWeights[1] = wPU.PU_2017(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[1] = wPU.PU_2017(int(Pileup_nTrueInt),"up");
      sysDownWeights[1] = wPU.PU_2017(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2018") {
      nominalWeights[1] = wPU.PU_2018(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[1] = wPU.PU_2018(int(Pileup_nTrueInt),"up");
      sysDownWeights[1] = wPU.PU_2018(int(Pileup_nTrueInt),"down");
    }

    if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;
    if (data == "mc") finalWeight = weight_Lumi * signnum_typical(genWeight) * nominalWeights[0]*nominalWeights[1]*nominalWeights[2]*nominalWeights[3];
    if (data == "mc") finalWeightSF = weight_Lumi * signnum_typical(genWeight)*topTagSF * nominalWeights[0]*nominalWeights[1]*nominalWeights[2]*nominalWeights[3];

//regions{"nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0", "nAk8G1TtagG0MTs2G300", "nAk8G1nTtag0","nAk8G1nTtag0MTs2G300", "nAk8G1nTtag0XtopMissTagRate", "nAk8G1Ttag0MTs2G300XtopMissTagRate"};
    reg.push_back(0);
    wgt.push_back(finalWeight);
    if(selectedJets08->size()==1 && (*selectedJets08)[0]->mass_>105 && (*selectedJets08)[0]->mass_<210){
      reg.push_back(1);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()==1 && ntopTag==1){
      reg.push_back(2);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()>1 && ntopTag>0){
      reg.push_back(3);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()>1 && ntopTag>0 && Ts2Candidate.M()>300){
      reg.push_back(4);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()>1 && ntopTag==0) {
      reg.push_back(5);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()>1 && ntopTag==0 && Ts2Candidate.M()>300){
      reg.push_back(6);
      wgt.push_back(finalWeight);
    }
    if(selectedJets08->size()>1 && ntopTag==0 && ntopTagRandom>0) {
      reg.push_back(7);
      wgt.push_back(finalWeight*((1-FR)/FR));
    }
    if(selectedJets08->size()>1 && ntopTag==0 && ntopTagRandom>0 &&  Ts2Candidate.M()>300){
      reg.push_back(8);
      wgt.push_back(finalWeight*((1-FR)/FR));
    }

//Fill histograms
    FillD3Hists(Hists, ch, reg, vInd(vars,"GammaPt"),          (*selectedPhotons)[0]->pt_       ,wgt);
    FillD3Hists(Hists, ch, reg, vInd(vars,"GammaEta"),         (*selectedPhotons)[0]->eta_      ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"GammaPhi"),         (*selectedPhotons)[0]->phi_      ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet04Pt"),          (*selectedJets04)[0]->pt_        ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet04Eta"),         (*selectedJets04)[0]->eta_       ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet04Phi"),         (*selectedJets04)[0]->phi_       ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"njet04"),           selectedJets04->size()           ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nbjet04"),          nbjet04                          ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet08Pt"),          (*selectedJets08)[0]->pt_        ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet08Eta"),         (*selectedJets08)[0]->eta_        ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"jet08Phi"),         (*selectedJets08)[0]->phi_        ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"njet08"),           selectedJets08->size()           ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"Met"),              MET_pt                           ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nVtx"),             PV_npvsGood                      ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nPh"),              selectedPhotons->size()          ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"phoChargedIso"),    Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"drGj04"),           drgj04                           ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"dPhiGj08"),         drgj08                           ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"HT"),               ht                               ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"HoE"),              Photon_hoe[(*selectedPhotons)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"softdropMass"),     FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"tau21"),            FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"tau31"),            FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nbjet08"),          nbjet08                          ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"TvsQCD"),           FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nBsub"),            bsubIndex->size()                ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"njet08massG50"),    wIndex->size()                   ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"njet08massG120"),   topIndex->size()                 ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"TsMass1"),          ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nTopTag"),          ntopTag                          ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"nWTag"),            WTagIndex->size()                ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"masstS2"),          Ts2Candidate.M()                 ,wgt); 
    FillD3Hists(Hists, ch, reg, vInd(vars,"Sietaieta"),        Photon_sieie[(*selectedPhotons)[0]->indice_],wgt); 

    if (data == "mc"){
//Wieght dependent sys
      for(int n=0;n<sys.size();++n){
        if(ch>0) continue;
        wgtUp.clear();
        wgtDown.clear();
        for(int l=0;l<wgt.size();++l){
          wgtUp.push_back( wgt[l]*(sysUpWeights[n]/nominalWeights[n]));
          wgtDown.push_back( wgt[l]*(sysDownWeights[n]/nominalWeights[n]));
        }
  //Up
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPt"),         n, (*selectedPhotons)[0]->pt_       ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaEta"),        n, (*selectedPhotons)[0]->eta_      ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPhi"),        n, (*selectedPhotons)[0]->phi_      ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nVtx"),            n, PV_npvsGood                      ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"drGj04"),          n, drgj04                           ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"dPhiGj08"),        n, drgj08                           ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"softdropMass"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"tau21"),           n, FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"tau31"),           n, FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet08"),         n, nbjet08                          ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nBsub"),           n, bsubIndex->size()                ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08massG50"),   n, wIndex->size()                   ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08massG120"),  n, topIndex->size()                 ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nWTag"),           n, WTagIndex->size()                ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtUp);
        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtUp);
  //Down
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPt"),         n, (*selectedPhotons)[0]->pt_       ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaEta"),        n, (*selectedPhotons)[0]->eta_      ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPhi"),        n, (*selectedPhotons)[0]->phi_      ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nVtx"),            n, PV_npvsGood                      ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"drGj04"),          n, drgj04                           ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"dPhiGj08"),        n, drgj08                           ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"softdropMass"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"tau21"),           n, FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"tau31"),           n, FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet08"),         n, nbjet08                          ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nBsub"),           n, bsubIndex->size()                ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08massG50"),   n, wIndex->size()                   ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08massG120"),  n, topIndex->size()                 ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nWTag"),           n, WTagIndex->size()                ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtDown);
        FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtDown);
      } 
//JES UP sys
      for (int n=0;n<sysJecNames.size();++n){
        ch=999;
        if((*JEC04sysUp)[n].size()>1 && (*JEC08sysUp)[n].size()>0 && PhotonsMedium->size()>0) ch=0;
        if(ch>0) continue;
        ntopTag=0;
        ntopTagRandom=0;
        ht=0;
        FR=1;
        Ts2Candidate.SetPxPyPzE(0,0,0,0);
        for (int l=0;l<(*JEC04sysUp)[n].size();l++){
          ht = ht + (*JEC04sysUp)[n][l]->pt_;
          if((*JEC08sysUp)[n].size()>0){
            if (deltaR((*JEC04sysUp)[n][l]->eta_, (*JEC04sysUp)[n][l]->phi_,(*JEC08sysUp)[n][0]->eta_, (*JEC08sysUp)[n][0]->phi_) > 0.8) Ts2Candidate += (*JEC04sysUp)[n][l]->p4_;
          }
        }

        for (int l=0;l<(*JEC08sysUp)[n].size();l++){
          if((*JEC08sysUp)[n][l]->toptag_) ntopTag++;
          if((*JEC08sysUp)[n][l]->mass_>105 && (*JEC08sysUp)[n][l]->mass_<210){
            ntopTagRandom++;
            FR = FR * (1-rate(&h_topMistagRate,(*JEC08sysUp)[n][l]->pt_));
          }
        }
  
        reg.clear();
        wgt.clear();
        reg.push_back(0);
        wgt.push_back(finalWeight);
        if((*JEC08sysUp)[n].size()==1 && (*JEC08sysUp)[n][0]->mass_>105 && (*JEC08sysUp)[n][0]->mass_<210){
          reg.push_back(1);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size()==1 && ntopTag==1){
          reg.push_back(2);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size() && ntopTag>0){
          reg.push_back(3);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size()>1 && ntopTag>0 && Ts2Candidate.M()>300){
          reg.push_back(4);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size()>1 && ntopTag==0) {
          reg.push_back(5);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size()>1 && ntopTag==0 && Ts2Candidate.M()>300){
          reg.push_back(6);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysUp)[n].size()>1 && ntopTag==0 && ntopTagRandom>0) {
          reg.push_back(7);
          wgt.push_back(finalWeight*((1-FR)/FR));
        }
        if((*JEC08sysUp)[n].size()>1 && ntopTag==0 && ntopTagRandom>0 &&  Ts2Candidate.M()>300){
          reg.push_back(8);
          wgt.push_back(finalWeight*((1-FR)/FR));
        }
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"GammaPt"),          n, (*selectedPhotons)[0]->pt_       ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"GammaEta"),         n, (*selectedPhotons)[0]->eta_      ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"GammaPhi"),         n, (*selectedPhotons)[0]->phi_      ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet04Pt"),          n, (*JEC04sysUp)[n][0]->pt_        ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet04Eta"),         n, (*JEC04sysUp)[n][0]->eta_       ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet04Phi"),         n, (*JEC04sysUp)[n][0]->phi_       ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"njet04"),           n, (*JEC04sysUp)[n].size()           ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nbjet04"),          n, nbjet04                          ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet08Pt"),          n, (*JEC08sysUp)[n][0]->pt_        ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet08Eta"),         n, (*JEC08sysUp)[n][0]->eta_        ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"jet08Phi"),         n, (*JEC08sysUp)[n][0]->phi_        ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"njet08"),           n, (*JEC08sysUp)[n].size()           ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"Met"),              n, MET_pt                           ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nVtx"),             n, PV_npvsGood                      ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nPh"),              n, selectedPhotons->size()          ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"phoChargedIso"),    n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"drGj04"),           n, drgj04                           ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"dPhiGj08"),         n, drgj08                           ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"HT"),               n, ht                               ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"HoE"),              n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"softdropMass"),     n, FatJet_msoftdrop[(*JEC08sysUp)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"tau21"),            n, FatJet_tau2[(*JEC08sysUp)[n][0]->indice_]/FatJet_tau1[(*JEC08sysUp)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"tau31"),            n, FatJet_tau3[(*JEC08sysUp)[n][0]->indice_]/FatJet_tau1[(*JEC08sysUp)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nbjet08"),          n, nbjet08                          ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"TvsQCD"),           n, FatJet_deepTagMD_TvsQCD[(*JEC08sysUp)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nBsub"),            n, bsubIndex->size()                ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"njet08massG50"),    n, wIndex->size()                   ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"njet08massG120"),   n, topIndex->size()                 ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"TsMass1"),          n, ((*selectedPhotons)[0]->p4_+(*JEC08sysUp)[n][0]->p4_).M(),wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nTopTag"),          n, ntopTag                          ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"nWTag"),            n, WTagIndex->size()                ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"masstS2"),          n, Ts2Candidate.M()                 ,wgt);
        FillD4Hists(HistsJecUp, ch, reg, vInd(vars,"Sietaieta"),        n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
      }
  //JES Down sys
      for (int n=0;n<sysJecNames.size();++n){
        ch=999;
        if((*JEC04sysDown)[n].size()>1 && (*JEC08sysDown)[n].size()>0 && PhotonsMedium->size()>0) ch=0;
        if(ch>0) continue;
        ntopTag=0;
        ntopTagRandom=0;
        ht=0;
        FR=1;
        Ts2Candidate.SetPxPyPzE(0,0,0,0);
        for (int l=0;l<(*JEC04sysDown)[n].size();l++){
          ht = ht + (*JEC04sysDown)[n][l]->pt_;
          if((*JEC08sysDown)[n].size()>0){
            if (deltaR((*JEC04sysDown)[n][l]->eta_, (*JEC04sysDown)[n][l]->phi_,(*JEC08sysDown)[n][0]->eta_, (*JEC08sysDown)[n][0]->phi_) > 0.8) Ts2Candidate += (*JEC04sysDown)[n][l]->p4_;
          }
        }
        for (int l=0;l<(*JEC08sysDown)[n].size();l++){
          if((*JEC08sysDown)[n][l]->toptag_) ntopTag++;
          if((*JEC08sysDown)[n][l]->mass_>105 && (*JEC08sysDown)[n][l]->mass_<210){
            ntopTagRandom++;
            FR = FR * (1-rate(&h_topMistagRate,(*JEC08sysDown)[n][l]->pt_));
          }
        }
  
        reg.clear();
        wgt.clear();
        reg.push_back(0);
        wgt.push_back(finalWeight);
        if((*JEC08sysDown)[n].size()==1 && (*JEC08sysDown)[n][0]->mass_>105 && (*JEC08sysDown)[n][0]->mass_<210){
          reg.push_back(1);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size()==1 && ntopTag==1){
          reg.push_back(2);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size() && ntopTag>0){
          reg.push_back(3);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size()>1 && ntopTag>0 && Ts2Candidate.M()>300){
          reg.push_back(4);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size()>1 && ntopTag==0) {
          reg.push_back(5);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size()>1 && ntopTag==0 && Ts2Candidate.M()>300){
          reg.push_back(6);
          wgt.push_back(finalWeight);
        }
        if((*JEC08sysDown)[n].size()>1 && ntopTag==0 && ntopTagRandom>0) {
          reg.push_back(7);
          wgt.push_back(finalWeight*((1-FR)/FR));
        }
        if((*JEC08sysDown)[n].size()>1 && ntopTag==0 && ntopTagRandom>0 &&  Ts2Candidate.M()>300){
          reg.push_back(8);
          wgt.push_back(finalWeight*((1-FR)/FR));
        }
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"GammaPt"),          n, (*selectedPhotons)[0]->pt_       ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"GammaEta"),         n, (*selectedPhotons)[0]->eta_      ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"GammaPhi"),         n, (*selectedPhotons)[0]->phi_      ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet04Pt"),          n, (*JEC04sysDown)[n][0]->pt_        ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet04Eta"),         n, (*JEC04sysDown)[n][0]->eta_       ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet04Phi"),         n, (*JEC04sysDown)[n][0]->phi_       ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"njet04"),           n, (*JEC04sysUp)[n].size()           ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nbjet04"),          n, nbjet04                          ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet08Pt"),          n, (*JEC08sysDown)[n][0]->pt_        ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet08Eta"),         n, (*JEC08sysDown)[n][0]->eta_        ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"jet08Phi"),         n, (*JEC08sysDown)[n][0]->phi_        ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"njet08"),           n, (*JEC08sysUp)[n].size()           ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"Met"),              n, MET_pt                           ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nVtx"),             n, PV_npvsGood                      ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nPh"),              n, selectedPhotons->size()          ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"phoChargedIso"),    n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"drGj04"),           n, drgj04                           ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"dPhiGj08"),         n, drgj08                           ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"HT"),               n, ht                               ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"HoE"),              n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"softdropMass"),     n, FatJet_msoftdrop[(*JEC08sysDown)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"tau21"),            n, FatJet_tau2[(*JEC08sysDown)[n][0]->indice_]/FatJet_tau1[(*JEC08sysDown)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"tau31"),            n, FatJet_tau3[(*JEC08sysDown)[n][0]->indice_]/FatJet_tau1[(*JEC08sysDown)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nbjet08"),          n, nbjet08                          ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"TvsQCD"),           n, FatJet_deepTagMD_TvsQCD[(*JEC08sysDown)[n][0]->indice_],wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nBsub"),            n, bsubIndex->size()                ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"njet08massG50"),    n, wIndex->size()                   ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"njet08massG120"),   n, topIndex->size()                 ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"TsMass1"),          n, ((*selectedPhotons)[0]->p4_+(*JEC08sysDown)[n][0]->p4_).M(),wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nTopTag"),          n, ntopTag                          ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"nWTag"),            n, WTagIndex->size()                ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"masstS2"),          n, Ts2Candidate.M()                 ,wgt);
        FillD4Hists(HistsJecDown, ch, reg, vInd(vars,"Sietaieta"),        n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
      }
    }

    nAccept++;
    if(Nmerged==2)nMerged++;
    if(Nmerged==1)nSemiMerged++;

    for (int l=0;l<selectedJets04->size();l++){
      delete (*selectedJets04)[l];
      (*selectedJets04)[l] = NULL;
    }
    for (int l=0;l<selectedJets08->size();l++){
      delete (*selectedJets08)[l];
      (*selectedJets08)[l] = NULL;
    }
    for (int l=0;l<PhotonsMedium->size();l++){
      delete (*PhotonsMedium)[l];
    }
    for (int l=0;l<fakePhotons->size();l++){
      delete (*fakePhotons)[l];
    }
    selectedJets04->clear();
    selectedJets04->shrink_to_fit();
    delete selectedJets04;
    selectedJets08->clear();
    selectedJets08->shrink_to_fit();
    delete selectedJets08;
    PhotonsMedium->clear();
    PhotonsMedium->shrink_to_fit();
    delete PhotonsMedium;
    fakePhotons->clear();
    fakePhotons->shrink_to_fit();
    delete fakePhotons;
    fakePhotonsIso->clear();
    fakePhotonsIso->shrink_to_fit();
    delete fakePhotonsIso;
    fakePhotonsOther->clear();
    fakePhotonsOther->shrink_to_fit();
    delete fakePhotonsOther;
    fakePhotonsSiSi->clear();
    fakePhotonsSiSi->shrink_to_fit();
    delete fakePhotonsSiSi;

    for (int l=0;l<JEC04sysUp->size();l++){
      for (int n=0;n<(*JEC04sysUp)[l].size();n++){
        delete (*JEC04sysUp)[l][n];
      }
    }
    for (int l=0;l<JEC04sysDown->size();l++){
      for (int n=0;n<(*JEC04sysDown)[l].size();n++){
        delete (*JEC04sysDown)[l][n];
      }
    }
    JEC04sysUp->clear();
    JEC04sysUp->shrink_to_fit();
    JEC04sysDown->clear();
    JEC04sysDown->shrink_to_fit();
    delete JEC04sysUp;
    delete JEC04sysDown;

    for (int l=0;l<JEC08sysUp->size();l++){
      for (int n=0;n<(*JEC08sysUp)[l].size();n++){
        delete (*JEC08sysUp)[l][n];
      }
    }
    for (int l=0;l<JEC08sysDown->size();l++){
      for (int n=0;n<(*JEC08sysDown)[l].size();n++){
        delete (*JEC08sysDown)[l][n];
      }
    }
    JEC08sysUp->clear();
    JEC08sysUp->shrink_to_fit();
    JEC08sysDown->clear();
    JEC08sysDown->shrink_to_fit();
    delete JEC08sysUp;
    delete JEC08sysDown;

   }
  cout<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;
  cout<<"from "<<ntr<<" events, "<<nOL<<" events are rejected by overlap removal requierment"<<endl;
  cout<<"fraction of events with both tops Merged = "<<float(nMerged)/float(nAccept)<<endl;
  cout<<"fraction of events with one top Merged = "<<float(nSemiMerged)/float(nAccept)<<endl;

  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<vars.size();++l){
        Hists[i][k][l]  ->Write("",TObject::kOverwrite);
        if(i==0){
          for (int n=0;n<sys.size();++n){
            HistsSysUp[i][k][l][n]->Write("",TObject::kOverwrite);
            HistsSysDown[i][k][l][n]->Write("",TObject::kOverwrite);
          }
        }
      }
    }
  }

  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<vars2d.size();++l){
        Hists2d[i][k][l]  ->Write("",TObject::kOverwrite);
      }
    }
  }


  file_out.mkdir("JECSys");
  for (int i=0;i<1;++i){
    for (int k=0;k<regions.size();++k){
      file_out.mkdir("JECSys/"+regions[k]);
      file_out.cd("JECSys/"+regions[k]);
      for (int l=0;l<vars.size();++l){
        for (int n=0;n<sysJecNames.size();++n){
          HistsJecUp[i][k][l][n]->Write("",TObject::kOverwrite);
          HistsJecDown[i][k][l][n]->Write("",TObject::kOverwrite);
        }
      }
    }
  }
  file_out.cd("");

  tree_out.Write() ;
  file_out.Close() ;
  Hists.clear();
  cout<<"Hists cleaned"<<endl;
  HistsSysUp.clear();
  cout<<"HistsSysUp cleaned"<<endl;
  HistsSysDown.clear();
  cout<<"HistsSysDown cleaned"<<endl;
  cout<<"Job is finished"<<endl;

  auto stop = high_resolution_clock::now();
  auto duration = duration_cast<seconds>(stop - start);
  cout << "Time taken: " << duration.count() << " seconds" << endl;
}


////////////////
//Other functions
std::vector<double> MyAnalysis::minGenDr(int myInd, std::vector<int> ignorePID){
    double myEta = GenPart_eta[myInd];
    double myPhi = GenPart_phi[myInd];
    int myPID = GenPart_pdgId[myInd];

    double mindr = 999.0;
    double dr;
    int bestInd = -1;
    for( int oind = 0; oind < nGenPart; oind++){
        if(oind == myInd) continue;
        if(GenPart_status[oind] != 1) continue; // check if it's final state
        if(GenPart_pt[oind] < 5)  continue;
        if(abs(GenPart_pt[oind] - GenPart_pt[myInd]) < 0.01 && (GenPart_pdgId[oind] == GenPart_pdgId[myInd]) && abs(GenPart_eta[oind] - GenPart_eta[myInd]) < 0.01)  continue; // skip if same particle
        int opid = abs(GenPart_pdgId[oind]);
        if(opid == 12 || opid == 14 || opid == 16) continue;
        if(std::find(ignorePID.begin(),ignorePID.end(),opid) != ignorePID.end()) continue;
        dr = dR(myEta, myPhi, GenPart_eta[oind], GenPart_phi[oind]);
        if( mindr > dr ) {
            int genParentIdx = GenPart_genPartIdxMother[oind];
            bool isDecay = false;
            while (genParentIdx>=myInd){
                if (genParentIdx==myInd) isDecay = true;
                genParentIdx = GenPart_genPartIdxMother[genParentIdx];
            }
            if (isDecay) continue;

            mindr = dr;
            bestInd = oind;
        }
    }
    vector<double> v;
    v.push_back(mindr);
    v.push_back((double)bestInd);
    return v;
}



bool MyAnalysis::overlapRemoval(double Et_cut, double Eta_cut, double dR_cut, bool verbose){
    bool haveOverlap = false;
    vector<int> extraPIDIgnore={22};
    for(int mcInd=0; mcInd<nGenPart; ++mcInd){
        if(GenPart_pdgId[mcInd]==22){

            bool parentagePass=false;
            vector<double> minDR_Result = {-1.,0.};
            bool Overlaps = false;
            int maxPDGID = 0;
            if (GenPart_pt[mcInd] >= Et_cut &&
                fabs(GenPart_eta[mcInd]) <= Eta_cut){

                Int_t parentIdx = mcInd;
                int motherPDGID = 0;
                bool fromTopDecay = false;
                while (parentIdx != -1){
                    motherPDGID = std::abs(GenPart_pdgId[parentIdx]);
                    maxPDGID = std::max(maxPDGID,motherPDGID);
                    parentIdx = GenPart_genPartIdxMother[parentIdx];
                }

                bool parentagePass = maxPDGID < 37;
                if (parentagePass) {
                    minDR_Result= minGenDr(mcInd, extraPIDIgnore);
                    if(minDR_Result.at(0) > dR_cut) {
                        haveOverlap = true;
                        Overlaps = true;
                    }
                }
            }
            if (verbose){
                cout << " gen particle idx="<<mcInd << " pdgID="<<GenPart_pdgId[mcInd] << " status="<<GenPart_status[mcInd] << " pt="<<GenPart_pt[mcInd] << " eta=" << GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
            }
        }
    }
    return haveOverlap;
}


void MyAnalysis::FillD3Hists(D3HistsContainer H3, int v1, std::vector<int> v2, int v3, float value, std::vector<float> weight){
  for (int i = 0; i < v2.size(); ++i) {
    H3[v1][v2[i]][v3]->Fill(value, weight[i]);
  }
}

void MyAnalysis::FillD4Hists(D4HistsContainer H4, int v1, std::vector<int> v2, int v3, int v4, float value, std::vector<float> weight){
  for (int i = 0; i < v2.size(); ++i) {
    H4[v1][v2[i]][v3][v4]->Fill(value, weight[i]);
  }
}
