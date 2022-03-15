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

using namespace std;
using namespace correction;

int vInd(std::map<TString, std::vector<float>> V, TString name){
  return V.find(name)->second.at(0);
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset ,string year, TString run, float xs, float lumi, float Nevent, int iseft, int nRuns){
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

  std::vector<TString> sys{"phIDSf", "pu", "prefiring", "trigSF", "jes", "jer"};
  Dim4 HistsSysUp(channels.size(),Dim3(regions.size(),Dim2(vars.size(),Dim1(sys.size()))));
  Dim4 HistsSysDown(channels.size(),Dim3(regions.size(),Dim2(vars.size(),Dim1(sys.size()))));

  if(data == "mc"){
    for (int i=0;i<channels.size();++i){
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
  }



  typedef vector<TH2F*> TH2FDim1;
  typedef vector<TH2FDim1> TH2FDim2;
  typedef vector<TH2FDim2> TH2FDim3;
  typedef vector<TH2FDim3> TH2FDim4;
  TH2F *h_test2d;
  std::vector<TString> vars2d {"NtopTagvsNlepLHE", "NtopTagvsNak8", "t21vsJetPt", "t32vsJetPt", "topTagvsmass", "massJ1vsmassJ2","npvsJetPt","npvsmass", "npvstopTag","mergedvsTopPt", "nSubbvsPt", "nSubbvsmass","nSubbvstopTag", "nSubbvsBdis","subFlavorvsSubBTag"};
  TH2FDim3 Hists2d(channels.size(),TH2FDim2(regions.size(),TH2FDim1(vars2d.size())));
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[0];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),5,0,5,4,0,4);
        Hists2d[i][k][0] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[1];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),5,0,5,4,0,4);
        Hists2d[i][k][1] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[2];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),20,0,1,40,400,1000);
        Hists2d[i][k][2] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[3];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),20,0,1,40,400,1000);
        Hists2d[i][k][3] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[4];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),20,0,1,40,0,400);
        Hists2d[i][k][4] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[5];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),40,0,400,40,0,400);
        Hists2d[i][k][5] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[6];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),7,0,7,40,200,1000);
        Hists2d[i][k][6] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[7];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),7,0,7,40,0,400);
        Hists2d[i][k][7] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[8];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),7,0,7,20,0,1);
        Hists2d[i][k][8] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[9];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),4,0,4,20,0,1500);
        Hists2d[i][k][9] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[10];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),4,0,4,20,0,1500);
        Hists2d[i][k][10] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[11];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),4,0,4,20,0,500);
        Hists2d[i][k][11] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[12];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),4,0,4,20,0,1);
        Hists2d[i][k][12] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[13];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),4,0,4,20,0,1);
        Hists2d[i][k][13] = h_test2d;
        name.str("");
        name<<channels[i]<<"_"<<regions[k]<<"_"<<vars2d[14];
        h_test2d = new TH2F((name.str()).c_str(),(name.str()).c_str(),100,0,2000,100,0,2000);
        Hists2d[i][k][14] = h_test2d;
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
  std::vector<lepton_candidate*> *selectedLeptons;
  std::vector<int> *topIndex;
  std::vector<int> *wIndex;
  std::vector<int> *bsubIndex;
  std::vector<int> *topTagIndex;
  std::vector<int> *WTagIndex;

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
  float topPt;
  float tStarMass;
  bool topEvent=false;
  int NtopPartons;
  int NlepLHE;
  int Nmerged;
  double PX;
  double PY;
  double ptts;
  double MVAOutput;
  double fr=1;

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
    PX=0;
    PY=0;
    ptts=0;
    MVAOutput=-1;
    Ts2Candidate.SetPxPyPzE(0,0,0,0);

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
      Hists2d[0][0][6]->Fill(NtopPartons,FatJet_pt[l]);
      Hists2d[0][0][7]->Fill(NtopPartons,FatJet_msoftdrop[l]);
      Hists2d[0][0][8]->Fill(NtopPartons,FatJet_deepTagMD_TvsQCD[l]);
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

      Hists2d[0][0][10]->Fill(nsubB, FatJet_pt[l]);
      Hists2d[0][0][11]->Fill(nsubB, FatJet_msoftdrop[l]);
      Hists2d[0][0][12]->Fill(nsubB,FatJet_deepTagMD_TvsQCD[l]);
      Hists2d[0][0][13]->Fill(nsubB,FatJet_btagDeepB[l]);
    }
    sort(selectedJets08->begin(), selectedJets08->end(), CompareMassJet);
    for (int j=0; j<selectedJets08->size();j++){
        if(FatJet_msoftdrop[(*selectedJets08)[j]->indice_]>50) wIndex->push_back((*selectedJets08)[j]->indice_);
        if(FatJet_msoftdrop[(*selectedJets08)[j]->indice_]>120) topIndex->push_back((*selectedJets08)[j]->indice_);
        if((*selectedJets08)[j]->Nbsub_>0) bsubIndex->push_back((*selectedJets08)[j]->indice_);
        if((*selectedJets08)[j]->toptag_>0) topTagIndex->push_back(j);
        if((*selectedJets08)[j]->Wtag_>0) WTagIndex->push_back(j);
    }
    Hists2d[0][0][9]->Fill(Nmerged,topPt/2);

//select jets AK4

    selectedJets04 = new std::vector<jet_candidate*>();
    for (int l=0;l<nJet;l++){
      if(Jet_pt[l] <50 || abs(Jet_eta[l]) > 2.4 || Jet_jetId[l]<6) continue;
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



    int f=1;
    for (int l=0;l<selectedJets04->size();l++){
    PX += (*selectedJets04)[l]->pt_ * cos((*selectedJets04)[l]->phi_);
    PY += (*selectedJets04)[l]->pt_ * sin((*selectedJets04)[l]->phi_);
      ht = ht + (*selectedJets04)[0]->pt_;
      if((*selectedJets04)[l]->btag_) nbjet04++;
      if(selectedJets08->size()>0){
        if (deltaR((*selectedJets04)[l]->eta_, (*selectedJets04)[l]->phi_,(*selectedJets08)[0]->eta_, (*selectedJets08)[0]->phi_) > 0.8) Ts2Candidate += (*selectedJets04)[l]->p4_;
      }


      for (int j=0;j<selectedJets08->size();j++){
        if(deltaR((*selectedJets08)[j]->eta_, (*selectedJets08)[j]->phi_,Jet_eta[l],Jet_phi[l])<0.8) f=0 ;
      }
    }


    for (int l=0;l<selectedJets08->size();l++){
      ht = ht + (*selectedJets08)[0]->pt_;
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

    if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;
    if (data == "mc") finalWeight = weight_Lumi * signnum_typical(genWeight);
    if (data == "mc") finalWeightSF = weight_Lumi * signnum_typical(genWeight)*topTagSF;
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
//    if(selectedPhotons->size()>0) {
//        Hists[ch][0][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
//        Hists[ch][0][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
//        Hists[ch][0][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
//        Hists[ch][0][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
//        Hists[ch][0][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
//        Hists[ch][0][19]->Fill(drgj08,finalWeight);
//        Hists[ch][0][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
//        Hists[ch][0][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
//        Hists[ch][0][39]->Fill(Ts2Candidate.M(),finalWeight);
//        Hists[ch][0][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
//        Hists[ch][0][41]->Fill(MVAOutput,finalWeight);
//        Hists[ch][0][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
//        Hists[ch][0][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
//        Hists2d[ch][0][14]->Fill(Ts2Candidate.M(),Ts2Candidate.M());
//    }
//    if(selectedJets04->size()>0) Hists[ch][0][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
//    if(selectedJets04->size()>0) Hists[ch][0][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
//    if(selectedJets04->size()>0) Hists[ch][0][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
//    Hists[ch][0][6]->Fill(selectedJets04->size(),finalWeight);
//    Hists[ch][0][7]->Fill(nbjet04,finalWeight);
//    Hists[ch][0][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
//    Hists[ch][0][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
//    Hists[ch][0][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
//    Hists[ch][0][11]->Fill(selectedJets08->size(),finalWeight);
//    Hists[ch][0][12]->Fill(MET_pt,finalWeight);
//    Hists[ch][0][13]->Fill(PV_npvsGood,finalWeight);
//    Hists[ch][0][14]->Fill(selectedPhotons->size(),finalWeight);
//    if(selectedJets04->size()>0) Hists[ch][0][18]->Fill(drgj04,finalWeight);
//    Hists[ch][0][20]->Fill(ht,finalWeight);
//    Hists[ch][0][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
//    Hists[ch][0][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
//    Hists[ch][0][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
//    Hists[ch][0][25]->Fill(nbjet08,finalWeight);
//    Hists[ch][0][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
//    if(selectedLeptons->size()>0) {
//      Hists[ch][0][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
//      Hists[ch][0][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
//      Hists[ch][0][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
//    }
//    Hists[ch][0][30]->Fill(bsubIndex->size(),finalWeight);
//    if(bsubIndex->size()>0) {
//      Hists[ch][0][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
//      Hists[ch][0][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
//    }
//    Hists[ch][0][33]->Fill(wIndex->size(),finalWeight);
//    Hists[ch][0][34]->Fill(topIndex->size(),finalWeight);
//    Hists[ch][0][36]->Fill(ntopTag,finalWeight);
//    Hists[ch][0][37]->Fill(WTagIndex->size(),finalWeight);
//    if((*selectedJets08)[0]->btag_) {
//      Hists2d[ch][0][1]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],(*selectedJets08)[0]->pt_);
//      Hists2d[ch][0][2]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],(*selectedJets08)[0]->pt_);
//      Hists2d[ch][0][3]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],(*selectedJets08)[0]->pt_);
//      Hists2d[ch][0][4]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_], FatJet_msoftdrop[(*selectedJets08)[0]->indice_]);
//    }
//    Hists2d[ch][0][5]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],FatJet_msoftdrop[(*selectedJets08)[1]->indice_]);
/*
//top tag
    if(topTagIndex->size()==1 && selectedJets08->size()==1){
      if(selectedPhotons->size()>0) {
          Hists[ch][1][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
          Hists[ch][1][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
          Hists[ch][1][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
          Hists[ch][1][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][1][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][1][19]->Fill(drgj08,finalWeight);
          Hists[ch][1][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][1][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][1][39]->Fill(Ts2Candidate.M(),finalWeight);
          Hists[ch][1][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
          Hists[ch][1][41]->Fill(MVAOutput,finalWeight);
          Hists[ch][1][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][1][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][1][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
          Hists[ch][1][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
          Hists[ch][1][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
          Hists[ch][1][18]->Fill(drgj04,finalWeight);
      }
      Hists[ch][1][6]->Fill(selectedJets04->size(),finalWeight);
      Hists[ch][1][7]->Fill(nbjet04,finalWeight);
      Hists[ch][1][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
      Hists[ch][1][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
      Hists[ch][1][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
      Hists[ch][1][11]->Fill(selectedJets08->size(),finalWeight);
      Hists[ch][1][12]->Fill(MET_pt,finalWeight);
      Hists[ch][1][13]->Fill(PV_npvsGood,finalWeight);
      Hists[ch][1][14]->Fill(selectedPhotons->size(),finalWeight);
      Hists[ch][1][20]->Fill(ht,finalWeight);
      Hists[ch][1][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][1][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][1][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][1][25]->Fill(nbjet08,finalWeight);
      Hists[ch][1][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][1][33]->Fill(wIndex->size(),finalWeight);
      Hists[ch][1][34]->Fill(topIndex->size(),finalWeight);
      Hists[ch][1][36]->Fill(ntopTag,finalWeight);
      Hists[ch][1][37]->Fill(WTagIndex->size(),finalWeight);
      Hists[ch][1][30]->Fill(bsubIndex->size(),finalWeight);
      if(selectedLeptons->size()>0) {
        Hists[ch][1][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
        Hists[ch][1][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
        Hists[ch][1][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][1][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
        Hists[ch][1][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
      }
    }

    if(topTagIndex->size()>0 && selectedJets08->size()>1){
      if(selectedPhotons->size()>0) {
          Hists[ch][2][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
          Hists[ch][2][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
          Hists[ch][2][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
          Hists[ch][2][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][2][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][2][19]->Fill(drgj08,finalWeight);
          Hists[ch][2][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][2][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][2][39]->Fill(Ts2Candidate.M(),finalWeight);
          Hists[ch][2][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
          Hists[ch][2][41]->Fill(MVAOutput,finalWeight);
          Hists[ch][2][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][2][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][2][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
          Hists[ch][2][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
          Hists[ch][2][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
          Hists[ch][2][18]->Fill(drgj04,finalWeight);
      }
      Hists[ch][2][6]->Fill(selectedJets04->size(),finalWeight);
      Hists[ch][2][7]->Fill(nbjet04,finalWeight);
      Hists[ch][2][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
      Hists[ch][2][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
      Hists[ch][2][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
      Hists[ch][2][11]->Fill(selectedJets08->size(),finalWeight);
      Hists[ch][2][12]->Fill(MET_pt,finalWeight);
      Hists[ch][2][13]->Fill(PV_npvsGood,finalWeight);
      Hists[ch][2][14]->Fill(selectedPhotons->size(),finalWeight);
      Hists[ch][2][20]->Fill(ht,finalWeight);
      Hists[ch][2][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][2][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][2][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][2][25]->Fill(nbjet08,finalWeight);
      Hists[ch][2][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][2][33]->Fill(wIndex->size(),finalWeight);
      Hists[ch][2][34]->Fill(topIndex->size(),finalWeight);
      Hists[ch][2][36]->Fill(ntopTag,finalWeight);
      Hists[ch][2][37]->Fill(WTagIndex->size(),finalWeight);
      Hists[ch][2][30]->Fill(bsubIndex->size(),finalWeight);
      if(selectedLeptons->size()>0) {
        Hists[ch][2][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
        Hists[ch][2][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
        Hists[ch][2][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][2][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
        Hists[ch][2][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
      }
    }

    if(MVAOutput>0.8 && selectedJets08->size()>1){
      if(selectedPhotons->size()>0) {
          Hists[ch][3][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
          Hists[ch][3][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
          Hists[ch][3][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
          Hists[ch][3][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][3][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][3][19]->Fill(drgj08,finalWeight);
          Hists[ch][3][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][3][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][3][39]->Fill(Ts2Candidate.M(),finalWeight);
          Hists[ch][3][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
          Hists[ch][3][41]->Fill(MVAOutput,finalWeight);
          Hists[ch][3][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][3][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][3][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
          Hists[ch][3][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
          Hists[ch][3][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
          Hists[ch][3][18]->Fill(drgj04,finalWeight);
      }
      Hists[ch][3][6]->Fill(selectedJets04->size(),finalWeight);
      Hists[ch][3][7]->Fill(nbjet04,finalWeight);
      Hists[ch][3][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
      Hists[ch][3][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
      Hists[ch][3][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
      Hists[ch][3][11]->Fill(selectedJets08->size(),finalWeight);
      Hists[ch][3][12]->Fill(MET_pt,finalWeight);
      Hists[ch][3][13]->Fill(PV_npvsGood,finalWeight);
      Hists[ch][3][14]->Fill(selectedPhotons->size(),finalWeight);
      Hists[ch][3][20]->Fill(ht,finalWeight);
      Hists[ch][3][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][3][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][3][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][3][25]->Fill(nbjet08,finalWeight);
      Hists[ch][3][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][3][33]->Fill(wIndex->size(),finalWeight);
      Hists[ch][3][34]->Fill(topIndex->size(),finalWeight);
      Hists[ch][3][36]->Fill(ntopTag,finalWeight);
      Hists[ch][3][37]->Fill(WTagIndex->size(),finalWeight);
      Hists[ch][3][30]->Fill(bsubIndex->size(),finalWeight);
      if(selectedLeptons->size()>0) {
        Hists[ch][3][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
        Hists[ch][3][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
        Hists[ch][3][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][3][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
        Hists[ch][3][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
      }
    }

    if(MVAOutput>0.8 &&  topTagIndex->size()>0 && selectedJets08->size()>1){
      if(selectedPhotons->size()>0) {
          Hists[ch][4][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
          Hists[ch][4][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
          Hists[ch][4][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
          Hists[ch][4][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][4][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][4][19]->Fill(drgj08,finalWeight);
          Hists[ch][4][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][4][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][4][39]->Fill(Ts2Candidate.M(),finalWeight);
          Hists[ch][4][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
          Hists[ch][4][41]->Fill(MVAOutput,finalWeight);
          Hists[ch][4][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][4][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][4][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
          Hists[ch][4][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
          Hists[ch][4][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
          Hists[ch][4][18]->Fill(drgj04,finalWeight);
      }
      Hists[ch][4][6]->Fill(selectedJets04->size(),finalWeight);
      Hists[ch][4][7]->Fill(nbjet04,finalWeight);
      Hists[ch][4][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
      Hists[ch][4][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
      Hists[ch][4][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
      Hists[ch][4][11]->Fill(selectedJets08->size(),finalWeight);
      Hists[ch][4][12]->Fill(MET_pt,finalWeight);
      Hists[ch][4][13]->Fill(PV_npvsGood,finalWeight);
      Hists[ch][4][14]->Fill(selectedPhotons->size(),finalWeight);
      Hists[ch][4][20]->Fill(ht,finalWeight);
      Hists[ch][4][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][4][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][4][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][4][25]->Fill(nbjet08,finalWeight);
      Hists[ch][4][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][4][33]->Fill(wIndex->size(),finalWeight);
      Hists[ch][4][34]->Fill(topIndex->size(),finalWeight);
      Hists[ch][4][36]->Fill(ntopTag,finalWeight);
      Hists[ch][4][37]->Fill(WTagIndex->size(),finalWeight);
      Hists[ch][4][30]->Fill(bsubIndex->size(),finalWeight);
      if(selectedLeptons->size()>0) {
        Hists[ch][4][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
        Hists[ch][4][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
        Hists[ch][4][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][4][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
        Hists[ch][4][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
      }
    }

    if(Ts2Candidate.M()>300 && topTagIndex->size()>0 && selectedJets08->size()>1){
      if(selectedPhotons->size()>0) {
          Hists[ch][5][0]->Fill((*selectedPhotons)[0]->pt_,finalWeight);
          Hists[ch][5][1]->Fill((*selectedPhotons)[0]->eta_,finalWeight);
          Hists[ch][5][2]->Fill((*selectedPhotons)[0]->phi_,finalWeight);
          Hists[ch][5][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][5][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][5][19]->Fill(drgj08,finalWeight);
          Hists[ch][5][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][5][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][5][39]->Fill(Ts2Candidate.M(),finalWeight);
          Hists[ch][5][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeight);
          Hists[ch][5][41]->Fill(MVAOutput,finalWeight);
          Hists[ch][5][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeight);
          Hists[ch][5][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeight);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][5][3]->Fill((*selectedJets04)[0]->pt_,finalWeight);
          Hists[ch][5][4]->Fill((*selectedJets04)[0]->eta_,finalWeight);
          Hists[ch][5][5]->Fill((*selectedJets04)[0]->phi_,finalWeight);
          Hists[ch][5][18]->Fill(drgj04,finalWeight);
      }
      Hists[ch][5][6]->Fill(selectedJets04->size(),finalWeight);
      Hists[ch][5][7]->Fill(nbjet04,finalWeight);
      Hists[ch][5][8]->Fill((*selectedJets08)[0]->pt_,finalWeight);
      Hists[ch][5][9]->Fill((*selectedJets08)[0]->eta_,finalWeight);
      Hists[ch][5][10]->Fill((*selectedJets08)[0]->phi_,finalWeight);
      Hists[ch][5][11]->Fill(selectedJets08->size(),finalWeight);
      Hists[ch][5][12]->Fill(MET_pt,finalWeight);
      Hists[ch][5][13]->Fill(PV_npvsGood,finalWeight);
      Hists[ch][5][14]->Fill(selectedPhotons->size(),finalWeight);
      Hists[ch][5][20]->Fill(ht,finalWeight);
      Hists[ch][5][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][5][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][5][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][5][25]->Fill(nbjet08,finalWeight);
      Hists[ch][5][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeight);
      Hists[ch][5][33]->Fill(wIndex->size(),finalWeight);
      Hists[ch][5][34]->Fill(topIndex->size(),finalWeight);
      Hists[ch][5][36]->Fill(ntopTag,finalWeight);
      Hists[ch][5][37]->Fill(WTagIndex->size(),finalWeight);
      Hists[ch][5][30]->Fill(bsubIndex->size(),finalWeight);
      if(selectedLeptons->size()>0) {
        Hists[ch][5][27]->Fill((*selectedLeptons)[0]->pt_,finalWeight);
        Hists[ch][5][28]->Fill((*selectedLeptons)[0]->eta_,finalWeight);
        Hists[ch][5][29]->Fill((*selectedLeptons)[0]->phi_,finalWeight);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][5][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeight);
        Hists[ch][5][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeight);
      }
    }


    if(MVAOutput>0.8 &&  topTagIndex->size()==0 && selectedJets08->size()==1){
      if(selectedPhotons->size()>0) {
          Hists[ch][6][0]->Fill((*selectedPhotons)[0]->pt_,finalWeightSF);
          Hists[ch][6][1]->Fill((*selectedPhotons)[0]->eta_,finalWeightSF);
          Hists[ch][6][2]->Fill((*selectedPhotons)[0]->phi_,finalWeightSF);
          Hists[ch][6][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][6][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][6][19]->Fill(drgj08,finalWeightSF);
          Hists[ch][6][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][6][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][6][39]->Fill(Ts2Candidate.M(),finalWeightSF);
          Hists[ch][6][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeightSF);
          Hists[ch][6][41]->Fill(MVAOutput,finalWeightSF);
          Hists[ch][6][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][6][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeightSF);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][6][3]->Fill((*selectedJets04)[0]->pt_,finalWeightSF);
          Hists[ch][6][4]->Fill((*selectedJets04)[0]->eta_,finalWeightSF);
          Hists[ch][6][5]->Fill((*selectedJets04)[0]->phi_,finalWeightSF);
          Hists[ch][6][18]->Fill(drgj04,finalWeightSF);
      }
      Hists[ch][6][6]->Fill(selectedJets04->size(),finalWeightSF);
      Hists[ch][6][7]->Fill(nbjet04,finalWeightSF);
      Hists[ch][6][8]->Fill((*selectedJets08)[0]->pt_,finalWeightSF);
      Hists[ch][6][9]->Fill((*selectedJets08)[0]->eta_,finalWeightSF);
      Hists[ch][6][10]->Fill((*selectedJets08)[0]->phi_,finalWeightSF);
      Hists[ch][6][11]->Fill(selectedJets08->size(),finalWeightSF);
      Hists[ch][6][12]->Fill(MET_pt,finalWeightSF);
      Hists[ch][6][13]->Fill(PV_npvsGood,finalWeightSF);
      Hists[ch][6][14]->Fill(selectedPhotons->size(),finalWeightSF);
      Hists[ch][6][20]->Fill(ht,finalWeightSF);
      Hists[ch][6][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][6][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][6][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][6][25]->Fill(nbjet08,finalWeightSF);
      Hists[ch][6][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][6][33]->Fill(wIndex->size(),finalWeightSF);
      Hists[ch][6][34]->Fill(topIndex->size(),finalWeightSF);
      Hists[ch][6][36]->Fill(ntopTag,finalWeightSF);
      Hists[ch][6][37]->Fill(WTagIndex->size(),finalWeightSF);
      Hists[ch][6][30]->Fill(bsubIndex->size(),finalWeightSF);
      if(selectedLeptons->size()>0) {
        Hists[ch][6][27]->Fill((*selectedLeptons)[0]->pt_,finalWeightSF);
        Hists[ch][6][28]->Fill((*selectedLeptons)[0]->eta_,finalWeightSF);
        Hists[ch][6][29]->Fill((*selectedLeptons)[0]->phi_,finalWeightSF);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][6][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeightSF);
        Hists[ch][6][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeightSF);
      }
    }

    if( selectedJets08->size()==1 && (*selectedJets08)[0]->mass_>105 && (*selectedJets08)[0]->mass_<210){
      if(selectedPhotons->size()>0) {
          Hists[ch][7][0]->Fill((*selectedPhotons)[0]->pt_,finalWeightSF);
          Hists[ch][7][1]->Fill((*selectedPhotons)[0]->eta_,finalWeightSF);
          Hists[ch][7][2]->Fill((*selectedPhotons)[0]->phi_,finalWeightSF);
          Hists[ch][7][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][7][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][7][19]->Fill(drgj08,finalWeightSF);
          Hists[ch][7][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][7][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][7][39]->Fill(Ts2Candidate.M(),finalWeightSF);
          Hists[ch][7][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeightSF);
          Hists[ch][7][41]->Fill(MVAOutput,finalWeightSF);
          Hists[ch][7][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][7][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeightSF);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][7][3]->Fill((*selectedJets04)[0]->pt_,finalWeightSF);
          Hists[ch][7][4]->Fill((*selectedJets04)[0]->eta_,finalWeightSF);
          Hists[ch][7][5]->Fill((*selectedJets04)[0]->phi_,finalWeightSF);
          Hists[ch][7][18]->Fill(drgj04,finalWeightSF);
      }
      Hists[ch][7][6]->Fill(selectedJets04->size(),finalWeightSF);
      Hists[ch][7][7]->Fill(nbjet04,finalWeightSF);
      Hists[ch][7][8]->Fill((*selectedJets08)[0]->pt_,finalWeightSF);
      Hists[ch][7][9]->Fill((*selectedJets08)[0]->eta_,finalWeightSF);
      Hists[ch][7][10]->Fill((*selectedJets08)[0]->phi_,finalWeightSF);
      Hists[ch][7][11]->Fill(selectedJets08->size(),finalWeightSF);
      Hists[ch][7][12]->Fill(MET_pt,finalWeightSF);
      Hists[ch][7][13]->Fill(PV_npvsGood,finalWeightSF);
      Hists[ch][7][14]->Fill(selectedPhotons->size(),finalWeightSF);
      Hists[ch][7][20]->Fill(ht,finalWeightSF);
      Hists[ch][7][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][7][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][7][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][7][25]->Fill(nbjet08,finalWeightSF);
      Hists[ch][7][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][7][33]->Fill(wIndex->size(),finalWeightSF);
      Hists[ch][7][34]->Fill(topIndex->size(),finalWeightSF);
      Hists[ch][7][36]->Fill(ntopTag,finalWeightSF);
      Hists[ch][7][37]->Fill(WTagIndex->size(),finalWeightSF);
      Hists[ch][7][30]->Fill(bsubIndex->size(),finalWeightSF);
      if(selectedLeptons->size()>0) {
        Hists[ch][7][27]->Fill((*selectedLeptons)[0]->pt_,finalWeightSF);
        Hists[ch][7][28]->Fill((*selectedLeptons)[0]->eta_,finalWeightSF);
        Hists[ch][7][29]->Fill((*selectedLeptons)[0]->phi_,finalWeightSF);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][7][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeightSF);
        Hists[ch][7][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeightSF);
      }
    }

    for (int l=0;l<selectedJets08->size();l++){
      if((*selectedJets08)[l]->mass_>105 && (*selectedJets08)[l]->mass_<210){
        ntopTagRandom++;
        FR = FR * (1-rate(&h_topMistagRate,(*selectedJets08)[l]->pt_));
      }
    }
    finalWeightSF = finalWeightSF*((1-FR)/FR);

    if( selectedJets08->size()>1 && topTagIndex->size()==0 && ntopTagRandom>0){
      if(selectedPhotons->size()>0) {
          Hists[ch][8][0]->Fill((*selectedPhotons)[0]->pt_,finalWeightSF);
          Hists[ch][8][1]->Fill((*selectedPhotons)[0]->eta_,finalWeightSF);
          Hists[ch][8][2]->Fill((*selectedPhotons)[0]->phi_,finalWeightSF);
          Hists[ch][8][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][8][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][8][19]->Fill(drgj08,finalWeightSF);
          Hists[ch][8][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][8][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][8][39]->Fill(Ts2Candidate.M(),finalWeightSF);
          Hists[ch][8][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeightSF);
          Hists[ch][8][41]->Fill(MVAOutput,finalWeightSF);
          Hists[ch][8][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][8][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeightSF);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][8][3]->Fill((*selectedJets04)[0]->pt_,finalWeightSF);
          Hists[ch][8][4]->Fill((*selectedJets04)[0]->eta_,finalWeightSF);
          Hists[ch][8][5]->Fill((*selectedJets04)[0]->phi_,finalWeightSF);
          Hists[ch][8][18]->Fill(drgj04,finalWeightSF);
      }
      Hists[ch][8][6]->Fill(selectedJets04->size(),finalWeightSF);
      Hists[ch][8][7]->Fill(nbjet04,finalWeightSF);
      Hists[ch][8][8]->Fill((*selectedJets08)[0]->pt_,finalWeightSF);
      Hists[ch][8][9]->Fill((*selectedJets08)[0]->eta_,finalWeightSF);
      Hists[ch][8][10]->Fill((*selectedJets08)[0]->phi_,finalWeightSF);
      Hists[ch][8][11]->Fill(selectedJets08->size(),finalWeightSF);
      Hists[ch][8][12]->Fill(MET_pt,finalWeightSF);
      Hists[ch][8][13]->Fill(PV_npvsGood,finalWeightSF);
      Hists[ch][8][14]->Fill(selectedPhotons->size(),finalWeightSF);
      Hists[ch][8][20]->Fill(ht,finalWeightSF);
      Hists[ch][8][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][8][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][8][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][8][25]->Fill(nbjet08,finalWeightSF);
      Hists[ch][8][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][8][33]->Fill(wIndex->size(),finalWeightSF);
      Hists[ch][8][34]->Fill(topIndex->size(),finalWeightSF);
      Hists[ch][8][36]->Fill(ntopTagRandom,finalWeightSF);
      Hists[ch][8][37]->Fill(WTagIndex->size(),finalWeightSF);
      Hists[ch][8][30]->Fill(bsubIndex->size(),finalWeightSF);
      if(selectedLeptons->size()>0) {
        Hists[ch][8][27]->Fill((*selectedLeptons)[0]->pt_,finalWeightSF);
        Hists[ch][8][28]->Fill((*selectedLeptons)[0]->eta_,finalWeightSF);
        Hists[ch][8][29]->Fill((*selectedLeptons)[0]->phi_,finalWeightSF);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][8][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeightSF);
        Hists[ch][8][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeightSF);
      }
    }

    if( selectedJets08->size()>1 && topTagIndex->size()==0 && ntopTagRandom>0 &&  Ts2Candidate.M()>300){
      if(selectedPhotons->size()>0) {
          Hists[ch][9][0]->Fill((*selectedPhotons)[0]->pt_,finalWeightSF);
          Hists[ch][9][1]->Fill((*selectedPhotons)[0]->eta_,finalWeightSF);
          Hists[ch][9][2]->Fill((*selectedPhotons)[0]->phi_,finalWeightSF);
          Hists[ch][9][15]->Fill(Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][9][16]->Fill(Photon_pfRelIso03_all[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][9][19]->Fill(drgj08,finalWeightSF);
          Hists[ch][9][21]->Fill(Photon_hoe[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][9][38]->Fill(abs(deltaPhi((*selectedPhotons)[0]->phi_, atan(PY/PX))));
          Hists[ch][9][39]->Fill(Ts2Candidate.M(),finalWeightSF);
          Hists[ch][9][40]->Fill(abs(deltaPhi(Ts2Candidate.Phi(),((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Phi())),finalWeightSF);
          Hists[ch][9][41]->Fill(MVAOutput,finalWeightSF);
          Hists[ch][9][42]->Fill(Photon_sieie[(*selectedPhotons)[0]->indice_],finalWeightSF);
          Hists[ch][9][35]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),finalWeightSF);
      }
      if(selectedJets04->size()>0) {
          Hists[ch][9][3]->Fill((*selectedJets04)[0]->pt_,finalWeightSF);
          Hists[ch][9][4]->Fill((*selectedJets04)[0]->eta_,finalWeightSF);
          Hists[ch][9][5]->Fill((*selectedJets04)[0]->phi_,finalWeightSF);
          Hists[ch][9][18]->Fill(drgj04,finalWeightSF);
      }
      Hists[ch][9][6]->Fill(selectedJets04->size(),finalWeightSF);
      Hists[ch][9][7]->Fill(nbjet04,finalWeightSF);
      Hists[ch][9][8]->Fill((*selectedJets08)[0]->pt_,finalWeightSF);
      Hists[ch][9][9]->Fill((*selectedJets08)[0]->eta_,finalWeightSF);
      Hists[ch][9][10]->Fill((*selectedJets08)[0]->phi_,finalWeightSF);
      Hists[ch][9][11]->Fill(selectedJets08->size(),finalWeightSF);
      Hists[ch][9][12]->Fill(MET_pt,finalWeightSF);
      Hists[ch][9][13]->Fill(PV_npvsGood,finalWeightSF);
      Hists[ch][9][14]->Fill(selectedPhotons->size(),finalWeightSF);
      Hists[ch][9][20]->Fill(ht,finalWeightSF);
      Hists[ch][9][22]->Fill(FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][9][23]->Fill(FatJet_tau2[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][9][24]->Fill(FatJet_tau3[(*selectedJets08)[0]->indice_]/FatJet_tau1[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][9][25]->Fill(nbjet08,finalWeightSF);
      Hists[ch][9][26]->Fill(FatJet_deepTagMD_TvsQCD[(*selectedJets08)[0]->indice_],finalWeightSF);
      Hists[ch][9][33]->Fill(wIndex->size(),finalWeightSF);
      Hists[ch][9][34]->Fill(topIndex->size(),finalWeightSF);
      Hists[ch][9][36]->Fill(ntopTagRandom,finalWeightSF);
      Hists[ch][9][37]->Fill(WTagIndex->size(),finalWeightSF);
      Hists[ch][9][30]->Fill(bsubIndex->size(),finalWeightSF);
      if(selectedLeptons->size()>0) {
        Hists[ch][9][27]->Fill((*selectedLeptons)[0]->pt_,finalWeightSF);
        Hists[ch][9][28]->Fill((*selectedLeptons)[0]->eta_,finalWeightSF);
        Hists[ch][9][29]->Fill((*selectedLeptons)[0]->phi_,finalWeightSF);
      }
      if(bsubIndex->size()>0) {
        Hists[ch][9][31]->Fill(FatJet_msoftdrop[bsubIndex->at(0)],finalWeightSF);
        Hists[ch][9][32]->Fill(FatJet_deepTagMD_TvsQCD[bsubIndex->at(0)],finalWeightSF);
      }
    }
*/
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
   }
  cout<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;
  cout<<"from "<<ntr<<" events, "<<nOL<<" events are rejected by overlap removal requierment"<<endl;
  cout<<"fraction of events with both tops Merged = "<<float(nMerged)/float(nAccept)<<endl;
  cout<<"fraction of events with one top Merged = "<<float(nSemiMerged)/float(nAccept)<<endl;

  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<vars.size();++l){
        Hists[i][k][l]  ->Write("",TObject::kOverwrite);
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
  tree_out.Write() ;
  file_out.Close() ;
  Hists.clear();
  cout<<"Hists cleaned"<<endl;
  HistsSysUp.clear();
  cout<<"HistsSysUp cleaned"<<endl;
  HistsSysDown.clear();
  cout<<"HistsSysDown cleaned"<<endl;
  cout<<"Job is finished"<<endl;
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
