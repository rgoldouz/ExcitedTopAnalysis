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
#include <typeinfo>

using namespace std;
using namespace correction;

template <class T>
void cleanVec( std::vector<T*> *vec )
{
    for( typename std::vector<T*>::iterator iter = vec->begin();  iter != vec->end(); ++iter )
    {
        delete *iter;
//        iter = vec.erase(iter);
    }
    vec->clear();
    vec->shrink_to_fit();
    delete vec;
}


int vInd(std::map<TString, std::vector<float>> V, TString name){
  return V.find(name)->second.at(0);
}

int getVecPos(std::vector<TString> vec, string element){
    int i;
    for(i = 0; i < vec.size(); i++){
      if(vec[i] == element) break;
    }
    if(i == vec.size()){
        std::cout<<"No such element as "<<element<<" found. Please enter again: ";
        std::cin>>element;
        i = getVecPos(vec, element);
    }
    return i;
}

void bestMass(TLorentzVector top, std::vector<TLorentzVector*> *others , float* mT1, float* mT2){
   float dm=100000.0;
   TLorentzVector T1,T2;
   if(others->size()>2){
     for(int i = 0; i < others->size(); i++){
  //     cout<<i<<" pairing with top:"<<(*others)[i]->Pt()<<":"<<(*others)[i]->Eta()<<":"<<(*others)[i]->Phi()<<":"<<(*others)[i]->M()<<endl;
  //     if ((*others)[i]->M()>10 || (*others)[i]->Pt()<100) continue;
       T1.SetPtEtaPhiM(0,0,0,0);
       T2.SetPtEtaPhiM(0,0,0,0);
       T1=top+*((*others)[i]);
       for(int j = 0; j < others->size(); j++){
         if (i==j) continue;
  //       cout<<"Object"<<j<<":"<<(*others)[j]->Pt()<<":"<<(*others)[j]->Eta()<<":"<<(*others)[j]->Phi()<<endl;
         T2 = T2 + *((*others)[j]);
       }
      
  //        cout<<"BestMAss:"<<T1.M()<<","<<T2.M()<<"-"<<abs(T1.M()-T2.M())/(T1.M()+T2.M())<<endl;
  //        cout<<"T1:"<<T1.Pt()<<","<<T1.Eta()<<","<<T1.Phi()<<endl;
  //        cout<<"T2:"<<T2.Pt()<<","<<T2.Eta()<<","<<T2.Phi()<<endl;
  //     if(abs(T1.M()-T2.M())/(T1.M()+T2.M()) < dm){
  //        dm = abs(T1.M()-T2.M())/(T1.M()+T2.M());
       if(abs(T1.M()-T2.M()) < dm){
          dm = abs(T1.M()-T2.M());
          *mT1=T1.M();
          *mT2=T2.M();
       }
     }
   }
   else{
     *mT1=(top+*((*others)[others->size()-1])).M();
     T2.SetPtEtaPhiM(0,0,0,0);
     for(int j = 0; j < others->size()-1; j++){
       T2 = T2 + *((*others)[j]);
     }
     *mT2=T2.M();;
   }

}

void bestMassV2(TLorentzVector top1, TLorentzVector ph , std::vector<TLorentzVector*> *others , float* mT1, float* mT2){
   float tm=100000;
   int g=-1;
   TLorentzVector T1,T2;
   TLorentzVector top2,top2candidate;
   for(int i = 0; i < others->size(); i++){
     if((*others)[i]->Pt()<200) continue;
     top2candidate.SetPtEtaPhiM(0,0,0,0);
     for(int j = 0; j < others->size(); j++){
       if (i==j) continue;
       top2candidate= top2candidate + *((*others)[j]);
     }
   if(abs(top2candidate.M()-172.5)<tm){
     tm = top2candidate.M();
     top2=top2candidate;
     g=i;
   }
  }
  if(g<0 || abs(top2.M()-172.5)>100){
    *mT1 =(top1+ph).M();
    *mT2 = 0;}
  else if(abs((top1+ph).M()-(top2+*((*others)[g])).M()) < abs((top2+ph).M()-(top1+*((*others)[g])).M())){
    *mT1 =(top1+ph).M();
    *mT2 = (top2+*((*others)[g])).M();
  }else{
    *mT1 =(top2+ph).M();
    *mT2 = (top1+*((*others)[g])).M();
  }
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset ,string year, TString run, float xs, float lumi, float Nevent, int iseft, int nRuns){
// Get starting timepoint
  double memoryInit=getValue();
  cout<<"initiated mamory:"<<memoryInit/1000.0<<" MB"<<endl;
  bool ifSys=false;
  auto start = high_resolution_clock::now();

  TH1F  *trigEffNum = new TH1F("trigEffNum","trigEffNum",50,0,500);
  TH1F  *trigEffDen = new TH1F("trigEffDen","trigEffDen",50,0,500);

  string particleNetTopTagSF="";
  string photonSF="";
  string photonES="";
  string MTR="";
  string JAFr="";

  if(year == "2016preVFP"){
    particleNetTopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2016preVFP_UL/jmar.json.gz";
    photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2016preVFP_UL/photon.json.gz";
//see https://twiki.cern.ch/twiki/bin/view/CMS/EgammaSFJSON
    photonES="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/EGammaScaleFactorsJSON-master/2016preVFP_UL/EGM_ScaleUnc.json.gz";
    MTR="2016preVFP_2DMistagRatejetPtvsMass";
    JAFr="2016preVFP_FakeRateVsEta";
  }
  if(year == "2016postVFP"){
    particleNetTopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2016postVFP_UL/jmar.json.gz";
    photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2016postVFP_UL/photon.json.gz";
    photonES="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/EGammaScaleFactorsJSON-master/2016postVFP_UL/EGM_ScaleUnc.json.gz";
    MTR="2016postVFP_2DMistagRatejetPtvsMass";
    JAFr="2016postVFP_FakeRateVsEta";
  }
  if(year == "2017"){
    particleNetTopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2017_UL/jmar.json.gz";
    photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2017_UL/photon.json.gz";
    photonES="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/EGammaScaleFactorsJSON-master/2017_UL/EGM_ScaleUnc.json";
    MTR="2017_2DMistagRatejetPtvsMass";
    JAFr="2017_FakeRateVsEta";
  }
  if(year == "2018"){
    particleNetTopTagSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/JME/2018_UL/jmar.json.gz";
    photonSF="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/data/POG/EGM/2018_UL/photon.json.gz";
    photonES="/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/EGammaScaleFactorsJSON-master/2018_UL/EGM_ScaleUnc.json.gz";
    MTR="2018_2DMistagRatejetPtvsMass";
    JAFr="2018_FakeRateVsEta";
  }

  auto csetFileParticleNetTopTagSF = CorrectionSet::from_file(particleNetTopTagSF);
  auto csetParticleNetTopTagSF = csetFileParticleNetTopTagSF->at("ParticleNet_Top_Nominal");
  auto csetFilePhotonSF = CorrectionSet::from_file(photonSF);
  auto csetPhotonCsevSF = csetFilePhotonSF->at("UL-Photon-CSEV-SF");
  auto csetPhotonIdSF = csetFilePhotonSF->at("UL-Photon-ID-SF");
  auto csetFilePhotonES = CorrectionSet::from_file(photonES);
  auto csetPhotonES = csetFilePhotonES->at("UL-EGM_ScaleUnc");
  cout<<"Scale factor is: "<<csetParticleNetTopTagSF->evaluate({2.1, 390.0, "nom", "0p1"})<<":"<<csetParticleNetTopTagSF->evaluate({2.1, 390.0, "up", "0p1"})<<":"<<csetParticleNetTopTagSF->evaluate({2.1, 390.0, "down", "0p1"})<<endl;
//  cout<<"ID Scale factor is: "<<csetPhotonCsevSF->evaluate({"2017", "sf", "Medium", "EBInc"})<<endl;
//  cout<<"CSEV Scale factor is: "<<csetPhotonIdSF->evaluate({"2017", "sf", "Medium", 1.1,100.1})<<endl;
//  cout<<"photon ES is: "<<csetPhotonES->evaluate({"2017", "scaledown", 1.2, 1})<<endl;

  TRandom3 Tr;
  TFile *f_topMistagRate = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/topMistagRate2D.root");
  TH2F h_topMistagRate = *(TH2F*)f_topMistagRate->Get(MTR.c_str());
  f_topMistagRate->Close();
  TFile *f_fakeRate = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/input/JetFakeRate.root");
  TH1F h_fakeRate = *(TH1F*)f_fakeRate->Get(JAFr.c_str());
  f_fakeRate->Close();
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

  const std::map<TString, std::vector<float>> vars =
  {
    {"GammaPt",                        {0,      40,   0,  1000}},
    {"GammaEta",                       {1,      20,   -3, 3   }},
    {"GammaPhi",                       {2,      25,   -4, 4   }},
    {"jet04Pt",                        {3,      40,   0,  1000}},
    {"jet04Eta",                       {4,      20,   -3, 3   }},
    {"njet04",                         {5,      10,    0, 10  }},
    {"nbjet04",                        {6,      4 ,    0, 4   }},
    {"jet08Pt",                        {7,      10,    0, 1000}},
    {"jet08Eta",                       {8,      20,   -3, 3   }},
    {"jet08Phi",                       {9,     25,   -4, 4   }},
    {"njet08",                         {10,     7,     0, 7   }},
    {"Met",                            {11,     20,    0, 200 }},
    {"nPh",                            {12,     3,     0, 3   }},
    {"phoChargedIso",                  {13,     200,    0, 20 }},
    {"HT",                             {14,     35,    0, 7000}},
    {"HoE",                            {15,     20,    0, 0.05}},
    {"softdropMassLeadingJet08",       {16,     40,    0, 800 }},
    {"TvsQCD",                         {17,     20,    0, 1   }},
    {"TsMass1",                        {18,     40,    0, 4000}},
    {"nTopTag",                        {19,     4,     0, 4   }},
    {"masstS2",                        {20,     40,    0, 2000}},
    {"Sietaieta",                      {21,     40,    0, 0.02}},
    {"MtGMet",                         {22,     50,    0, 1000}},
    {"subLeadingJet08Pt",              {23,      10,    0, 1000}},
    {"nVtxApu",                        {24,     70,    0, 70 }},
    {"nVtxBpu",                        {25,     70,    0, 70 }},
    {"subLeadingJet08Eta",             {26,      20,   -3, 3   }},
    {"subLeadingJet08Phi",             {27,     25,   -4, 4   }},
    {"softdropMassSubLeadingJet08",    {28,     40,    0, 800 }},
  };

  std::vector<TString> categories{"promptG", "fakeGEle","fakeGJet"};
  std::vector<TString> channels{"aJets"};
  std::vector<TString> regions{"nAk8G0", "nAk81", "nAk81nTtag1", "nAk8G1nTtagG0",  "nAk8G1nTtag0", "nAk8G1nTtag0XtopMissTagRate",  "nAk81nTtag0XtopMissTagRate", "nAk8G1nTtagG0LepG0", "nAk81nTtagOffMt","nAk81nTtagOffMtXtopMissTagRate"};

  std::vector<TString> sys{"phIDSf", "pu", "prefiring","photonEScale","photonESmear", "topTagSF","JesTotal"};
  std::vector<TString> sysNotWeight{"photonEScale","photonESmear","JesTotal"};
  std::vector<TString> sysData{"missTagRate"};
  std::vector<TString> sysJecNames{"AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","SinglePionECAL","SinglePionHCAL","TimePtEta", "Total"};
  const int nsrc = 22;
  const char* srcnames[nsrc] = {"AbsoluteMPFBias","AbsoluteScale","AbsoluteStat","FlavorQCD","Fragmentation","PileUpDataMC","PileUpPtBB","PileUpPtEC1","PileUpPtEC2","PileUpPtRef","RelativeFSR","RelativePtBB","RelativePtEC1","RelativePtEC2","RelativeBal","RelativeSample","RelativeStatEC","RelativeStatFSR","SinglePionECAL","SinglePionHCAL","TimePtEta", "Total"};
    std::vector<JetCorrectionUncertainty*> vsrc08(nsrc);
    std::vector<int> JecRegions = {getVecPos(regions,"nAk8G1nTtagG0")};
  std::string JECFile08;
  if(year == "2016preVFP")    JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16APV_V7_MC/Summer19UL16APV_V7_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2016postVFP")   JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL16_V7_MC/Summer19UL16_V7_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2017")          JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL17_V5_MC/Summer19UL17_V5_MC_UncertaintySources_AK8PFPuppi.txt";
  if(year == "2018")          JECFile08 = "/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/input/Summer19UL18_V5_MC/Summer19UL18_V5_MC_UncertaintySources_AK8PFPuppi.txt";

    for (int isrc = 0; isrc < nsrc; isrc++) {
      JetCorrectorParameters *p = new JetCorrectorParameters(JECFile08, srcnames[isrc]);
      JetCorrectionUncertainty *unc = new JetCorrectionUncertainty(*p);
      vsrc08[isrc] = unc;
    }

//  D3HistsContainer Hists;
  Hists.resize(categories.size());
  for (int l=0;l<categories.size();++l){
    Hists[l].resize(channels.size());
    for (int i=0;i<channels.size();++i){
      Hists[l][i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        Hists[l][i][k].resize(vars.size());
      }
    }
  }

  std::vector<TString> categoriesFA{"promptG", "fakeGEle","fakeGJet"};
  std::vector<TString> channelsFA{"fakeAJetsIso", "fakeAJetsSiSi","fakeAJetsIsoSiSi","fakeAJetsOthers"};
  std::vector<TString> regionsFA{"nAk8G0","nAk81nTtag1", "nAk8G1nTtagG0","nAk81nTtagOffMt"};
  const std::map<TString, std::vector<float>> varsFA =
  {
    {"GammaPt",                        {0,      40,   0,  1000}},
    {"GammaEta",                       {1,      20,   -3, 3   }},
    {"GammaPhi",                       {2,      25,   -4, 4   }},
    {"jet08Pt",                        {3,      10,    0, 1000}},
    {"jet08Eta",                       {4,      20,   -3, 3   }},
    {"nPh",                            {5,     3,     0, 3   }},
    {"phoChargedIso",                  {6,     200,    0, 20 }},
    {"HoE",                            {7,     20,    0, 0.05}},
    {"Sietaieta",                      {8,     40,    0, 0.02}},
    {"TsMass1",                        {9,     40,    0, 4000}},
    {"HT",                             {10,     35,    0, 7000}},
    {"Met",                            {11,     20,    0, 200 }},
    {"njet08",                         {12,     7,     0, 7   }},
    {"jet08Phi",                       {13,     25,   -4, 4   }},
    {"softdropMassLeadingJet08",       {14,     40,    0, 800 }},
    {"subLeadingJet08Eta",             {15,      20,   -3, 3   }},
    {"subLeadingJet08Phi",             {16,     25,   -4, 4   }},
    {"softdropMassSubLeadingJet08",    {17,     40,    0, 800 }},
  };

  HistsFA.resize(categoriesFA.size());
  for (int l=0;l<categoriesFA.size();++l){
    HistsFA[l].resize(channelsFA.size());
    for (int i=0;i<channelsFA.size();++i){
      HistsFA[l][i].resize(regionsFA.size());
      for (int k=0;k<regionsFA.size();++k){
        HistsFA[l][i][k].resize(varsFA.size());
      }
    }
  }

// [0] is renscfact=0.5d0 facscfact=0.5d0 ; [1] is renscfact=0.5d0 facscfact=1d0 ; [2] is renscfact=0.5d0 facscfact=2d0 ; [3] is renscfact=1d0 facscfact=0.5d0 ; [4] is renscfact=1d0 facscfact=1d0 ; [5] is renscfact=1d0 facscfact=2d0 ; [6] is renscfact=2d0 facscfact=0.5d0 ; [7] is renscfact=2d0 facscfact=1d0 ; [8] is renscfact=2d0 facscfact=2d0 *
  int nScale = 9;
//  Dim3 Hists(channels.size(),Dim2(regions.size(),Dim1(vars.size())));
// LHA IDs NNPDF31_nnlo_hessian_pdfas 306000 - 306102*
  int nPdf = 100;
  std::stringstream name;
  TH1F *h_test;
  for (int l=0;l<categories.size();++l){
    for (int i=0;i<channels.size();++i){
      for (int k=0;k<regionsFR.size();++k){
        for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
          name<<categories[l]<<"_"<<channels[i]<<"_"<<regionsFR[k]<<"_"<<it->first;
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          Hists[l][i][k][it->second.at(0)] = h_test;
          name.str("");
        }
      }
    }
  }

  for (int l=0;l<categoriesFA.size();++l){
    for (int i=0;i<channelsFA.size();++i){
      for (int k=0;k<regionsFA.size();++k){
        for( auto it = varsFA.cbegin() ; it != varsFA.cend() ; ++it ){
          name<<categoriesFA[l]<<"_"<<channelsFA[i]<<"_"<<regionsFA[k]<<"_"<<it->first;
          h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
          h_test->StatOverflows(kTRUE);
          h_test->Sumw2(kTRUE);
          HistsFA[l][i][k][it->second.at(0)] = h_test;
          name.str("");
        }
      }
    }
  }

  if(data == "data" && ifSys){
    HistsSysDataUp.resize(1);
    for (int i=0;i<1;++i){
      HistsSysDataUp[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysDataUp[i][k].resize(vars.size());
        for (int n=0;n<vars.size();++n){
          HistsSysDataUp[i][k][n].resize(sysData.size());
        }
      }
    }
    HistsSysDataDown.resize(1);
    for (int i=0;i<1;++i){
      HistsSysDataDown[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysDataDown[i][k].resize(vars.size());
        for (int n=0;n<vars.size();++n){
          HistsSysDataDown[i][k][n].resize(sysData.size());
        }
      }
    }
    for (int i=0;i<1;++i){
      for (int k=0;k<regions.size();++k){
        for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
          for (int n=0;n<sysData.size();++n){
            name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysData[n]<<"_Up";
            h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
            h_test->StatOverflows(kTRUE);
            h_test->Sumw2(kTRUE);
            HistsSysDataUp[i][k][it->second.at(0)][n] = h_test;
            name.str("");
            name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysData[n]<<"_Down";
            h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
            h_test->StatOverflows(kTRUE);
            h_test->Sumw2(kTRUE);
            HistsSysDataDown[i][k][it->second.at(0)][n] = h_test;
            name.str("");
          }
        }
      }
    }
  }
  if(data == "mc" && ifSys){
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
  
    HistsJecUp.resize(1);
    for (int i=0;i<1;++i){
      HistsJecUp[i].resize(1);
      for (int k=0;k<1;++k){
        HistsJecUp[i][k].resize(1);
        for (int n=0;n<1;++n){
          HistsJecUp[i][k][n].resize(sysJecNames.size());
        }
      }
    }
  
    HistsJecDown.resize(1);
    for (int i=0;i<1;++i){
      HistsJecDown[i].resize(1);
      for (int k=0;k<1;++k){
        HistsJecDown[i][k].resize(1);
        for (int n=0;n<1;++n){
          HistsJecDown[i][k][n].resize(sysJecNames.size());
        }
      }
    }
  
    for (int i=0;i<1;++i){
      for (int k=0;k<regions.size();++k){
        if (!(std::count(JecRegions.begin(), JecRegions.end(), k))) continue;
        for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
          if(it->first !="TsMass1") continue;
          for (int n=0;n<sysJecNames.size();++n){
            name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysJecNames[n]<<"_Up";
            h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
            h_test->StatOverflows(kTRUE);
            h_test->Sumw2(kTRUE);
            HistsJecUp[0][0][0][n] = h_test;
            name.str("");
            name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysJecNames[n]<<"_Down";
            h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
            h_test->StatOverflows(kTRUE);
            h_test->Sumw2(kTRUE);
            HistsJecDown[0][0][0][n] = h_test;
            name.str("");
          }
        }
      }
    }

    if (fname.Contains("TTga") || fname.Contains("TTGamma")){
      HistsSysReweightsPDF.resize(1);
      for (int i=0;i<1;++i){
        HistsSysReweightsPDF[i].resize(1);
        for (int k=0;k<1;++k){
          HistsSysReweightsPDF[i][k].resize(1);
          for (int n=0;n<1;++n){
            HistsSysReweightsPDF[i][k][n].resize(nPdf);
          }
        }
      }
  
      HistsSysReweightsQscale.resize(1);
      for (int i=0;i<1;++i){
        HistsSysReweightsQscale[i].resize(1);
        for (int k=0;k<1;++k){
          HistsSysReweightsQscale[i][k].resize(1);
          for (int n=0;n<1;++n){
            HistsSysReweightsQscale[i][k][n].resize(nScale);
          }
        }
      }
  
      for (int i=0;i<1;++i){
        for (int k=0;k<regions.size();++k){
          if (!(std::count(JecRegions.begin(), JecRegions.end(), k))) continue;
          for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
            if(it->first !="TsMass1") continue;
            for (int n=0;n<nScale;++n){
              name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_Qscale_"<<n;
              h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
              h_test->StatOverflows(kTRUE);
              h_test->Sumw2(kTRUE);
              HistsSysReweightsQscale[0][0][0][n] = h_test;
              name.str("");
            }
            for (int n=0;n<nPdf;++n){
              name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first<<"_PDF_"<<n;
              h_test = new TH1F((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
              h_test->StatOverflows(kTRUE);
              h_test->Sumw2(kTRUE);
              HistsSysReweightsPDF[0][0][0][n] = h_test;
              name.str("");
            }
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
  std::vector<TString> vars2d {"M1vsM2", "M1vsDPhi","M1vsDr","pt1vspt2","BestMass1vs2","BestMassV21vs2", "GammaPvsTmass", "nAK8vsnAK4"};
//  TH2FDim3 Hists2d(channels.size(),TH2FDim2(regions.size(),TH2FDim1(vars2d.size())));
  TH2FDim3 Hists2d(1,TH2FDim2(1,TH2FDim1(vars2d.size())));

 Double_t edgesPt[4] = {225.0, 350.0, 500.0, 800};
 Double_t edgesMass[8] = {90,110,125,150,175,200,225,400};
 h_test2d = new TH2F("M1vsM2","M1vsM2",100,0,2000,100,0,2000);
        Hists2d[0][0][0] = h_test2d;
 h_test2d = new TH2F("M1vsDPhi","M1vsDPhi",100,0,2000,100,0,7);
        Hists2d[0][0][1] = h_test2d;
 h_test2d = new TH2F("M1vsDr","M1vsDr",100,0,2000,100,0,7);
        Hists2d[0][0][2] = h_test2d;
 h_test2d = new TH2F("pt1vspt2","pt1vspt2",100,0,2000,100,0,2000);
        Hists2d[0][0][3] = h_test2d;
 h_test2d = new TH2F("jetPtvsTmass1jetFakePh","jetPtvsTmass1jetFakePh",3,edgesPt,7,edgesMass);
        Hists2d[0][0][4] = h_test2d;
 h_test2d = new TH2F("jetPtvsTmass1jet1tagFakePh","jetPtvsTmass1jet1tagFakePh",3,edgesPt,7,edgesMass);
        Hists2d[0][0][5] = h_test2d;
 h_test2d = new TH2F("jetPtvsTmass1jetPromptPh","jetPtvsTmass1jetPromptPh",3,edgesPt,7,edgesMass);
        Hists2d[0][0][6] = h_test2d;
 h_test2d = new TH2F("jetPtvsTmass1jet1tagPromptPh","jetPtvsTmass1jet1tagPromptPh",3,edgesPt,7,edgesMass);
        Hists2d[0][0][7] = h_test2d;

  TH2F *h_2dSieieVsChiso=new TH2F("h_2dSieieVsChiso","h_2dSieieVsChiso",40,0,0.02,40,0,20);


  const std::map<TString, std::vector<float>> vars1dSignal =
  {
    {"excitedTop_genPt",          {0,      40,   0,  2000}},
    {"excitedTop_genEta",         {1,      20,   -5, 5   }},
    {"top_genPt",                 {2,      40,   0, 1000 }},
    {"top_genEta",                {3,      20,   -5,5    }},
    {"gamma_genPt",               {4,      40,   0, 1000 }},
    {"gamma_genEta",              {5,      20,   -5,5    }},
    {"gluon_genPt",               {6,      40,   0, 1000 }},
    {"gluon_genEta",              {7,      20,   -5, 5 }},
    {"excitedTop_mass",           {8,      100,    0, 2000}},
    {"genMassPhtop",              {9,      40,   0,  2000}},
    {"genMassGluontop",           {10,      40,   0,  2000}},
    {"geDrPhtop",                 {11,      10,   0, 7 }},
    {"geDrPGluontop",             {12,      10,   0, 7 }},
    {"genMassTTbar",              {13,      100,   0,  10000}},
  };
  vector<TH1F*> Hists1dSignal(vars1dSignal.size());
  for( auto it = vars1dSignal.cbegin() ; it != vars1dSignal.cend() ; ++it ){
    h_test = new TH1F(it->first ,it->first ,it->second.at(1), it->second.at(2), it->second.at(3)); 
    h_test->StatOverflows(kTRUE);
    h_test->Sumw2(kTRUE);
    Hists1dSignal[it->second.at(0)] = h_test;
  }

  int sizeHists2dSignal=4;
  vector<TH2F*> Hists2dSignal(sizeHists2dSignal);
  Hists2dSignal[0] = new TH2F("GenMassTop-gammaVsGenMassTop-gluon","GenMassTop-gammaVsGenMassTop-gluon",100,0,2000,100,0,2000);
  Hists2dSignal[1] = new TH2F("GenMassTop-gammaVsGenMassAntiTop-gamma","GenMassTop-gammaVsGenMassAntiTop-gamma",100,0,2000,100,0,2000);
  Hists2dSignal[2] = new TH2F("GengammaPtVsTopGammaMass","GengammaPtVsTopGammaMass",100,0,2000,100,0,2000);
  Hists2dSignal[3] = new TH2F("TopPtVsAntiTopPt","TopPtVsAntiTopPt",100,0,2000,100,0,2000);

// scale factors
  FatJetScaleFactor fatjetscalefactors = FatJetScaleFactor();
//  cout<<fatjetscalefactors.ak8SF(false, 2017, 6, true, 0, 1, 330,  0)<<endl;

  std::vector<lepton_candidate*> *PhotonsMedium;
  std::vector<lepton_candidate*> *PhotonsMediumScaleUp;
  std::vector<lepton_candidate*> *PhotonsMediumScaleDown;
  std::vector<lepton_candidate*> *PhotonsMediumSmearUp;
  std::vector<lepton_candidate*> *PhotonsMediumSmearDown;
  std::vector<lepton_candidate*> *fakePhotonsIso;
  std::vector<lepton_candidate*> *fakePhotonsSiSi;
  std::vector<lepton_candidate*> *fakePhotonsIsoSiSi;
  std::vector<lepton_candidate*> *fakePhotonsOther;
  std::vector<lepton_candidate*> *selectedPhotons;
  std::vector<jet_candidate*> *selectedJets08;
  std::vector<jet_candidate*> *selectedJets08JesUp;
  std::vector<jet_candidate*> *selectedJets08JesDown;
  std::vector<jet_candidate*> *selectedJets04;
  std::vector<std::vector<jet_candidate*>> *JEC08sysUp;
  std::vector<std::vector<jet_candidate*>> *JEC08sysDown;
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
  int nAcceptPassTrigger=0;
  int nAcceptPassPhoton=0;
  int nAcceptLeptonicTop=0;
  int ntopTag0=0;
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
  int nbq;
  int ntop;
  int ntopTag;
  int ntopTagSB;
  int ntopTagNM;
  int ntopTagRandom;
  int ntopTagRandomSB;
  int nWTag;
  int nW;

  float topMTRSB;
  float topMTR;
  float topMTRup;
  float topMTRdown;
  float FR;
  float drgj04;
  float drgj08;
  float drtA;
  float ht;
  bool jetlepfail;
  bool jetAk8fail;
  int cat;
  int ch;
  std::vector<int> reg;
  std::vector<int> regUp;
  std::vector<float> wgt;
  std::vector<float> wgtFA;
  std::vector<float> wgtUp;
  std::vector<float> wgtDown;
  std::vector<float> wgtnoPU;
  int chFA;
  std::vector<int> regFA;
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
  bool metFilterPass;
  float mT1, mT2;
  float mT1V2, mT2V2;
  int toptagIndex;
  float phESunc;  
  float phEnergy;

  std::vector<float> nominalWeights;
  nominalWeights.assign(sys.size(), 1);
  std::vector<float> sysUpWeights;
  sysUpWeights.assign(sys.size(), 1);
  std::vector<float> sysDownWeights;
  sysDownWeights.assign(sys.size(), 1);

  std::vector<float> nominalWeightsData;
  nominalWeightsData.assign(sysData.size(), 1);
  std::vector<float> sysUpWeightsData;
  sysUpWeightsData.assign(sysData.size(), 1);
  std::vector<float> sysDownWeightsData;
  sysDownWeightsData.assign(sysData.size(), 1);

  std::vector<long int> EVENT = {14113658};
  std::vector<TLorentzVector*> *topObjects;
  std::vector<TLorentzVector*> *otherObjects;
  std::vector<TLorentzVector*> *otherObjectsV2;
  TLorentzVector *topObj;
  TLorentzVector BoostCandidate;
  TLorentzVector GluonCandidate;
  TLorentzVector TopCandidate, TopBarCandidate;
  TLorentzVector GammaCandidate;
  TLorentzVector TsCandidate, TsBarCandidate, Ts2Candidate;
  TLorentzVector Wnu, Wele, gLHE;//, WnuLHE, WeleLHE;
  bool gammaFromT;


  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries ();


  for (Long64_t jentry=0; jentry<nentries;jentry++) {
//  for (Long64_t jentry=0; jentry<5000;jentry++) {
cout<<jentry<<endl;
    Ph_pt.clear();
    Ph_eta.clear();
    Ph_phi.clear();
    Ak8_pt.clear();
    Ak8_eta.clear();
    Ak8_phi.clear();
    reg.clear();
    regFA.clear();
    wgt.clear();
    wgtFA.clear();
    wgtnoPU.clear();

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;

    triggerPassA = false;
    triggerPassMu = false;
    metFilterPass = false;
    weight_Lumi =1;
    finalWeight =1;
    finalWeightSF =1;
    topTagSF =1;
    nbjet04=0;
    nbjet08=0;
    nbq=0;
    ntop = 0;
    ntopTag = 0;
    ntopTagSB = 0;
    ntopTagNM = 0;
    ntopTagRandom=0;
    ntopTagRandomSB=0;
    nWTag = 0;
    nW = 0;
    topMTRSB= 1;
    topMTR= 1;
    topMTRup= 1;
    topMTRdown= 1;
    FR=1;
    drgj04 = 10;
    drgj08 = 10;
    ht=0;
    jetlepfail = false;
    ch=999;
    chFA=999;
    cat=0;
    NtopPartons=0;
    topPt=0;
    Nmerged=0;
    NlepLHE=0;
    ptts=0;
    MVAOutput=-1;
    topLeptonicEvent=false;
    Ts2Candidate.SetPxPyPzE(0,0,0,0);
    toptagIndex=0;

    for (int n=0;n<sys.size();++n){
      nominalWeights[n] =1;
      sysUpWeights[n] =1;
      sysDownWeights[n] =1;
    }

    for (int n=0;n<sysData.size();++n){
      nominalWeightsData[n] =1;
      sysUpWeightsData[n] =1;
      sysDownWeightsData[n] =1;
    }
    if(data == "mc"){
      for (int l=0;l<nGenPart;l++){
        if(abs(GenPart_pdgId[l])==6){
          topEvent=true;
           break;
        }
      }
      for (int l=0;l<nLHEPart;l++){
        if(abs(LHEPart_pdgId[l]) ==22) gLHE.SetPtEtaPhiM(LHEPart_pt[l], LHEPart_eta[l], LHEPart_phi[l], LHEPart_mass[l]);
      }
      if(fname.Contains("pt0toinf") && gLHE.Pt()>100) continue;
    }

    

    topObjects = new std::vector<TLorentzVector*>();

//     for (int l=0;l<nLHEPart;l++){
//       if(abs(LHEPart_pdgId[l]) ==11 || abs(LHEPart_pdgId[l]) ==13 || abs(LHEPart_pdgId[l]) ==15 ) WeleLHE.SetPtEtaPhiM(LHEPart_pt[l], LHEPart_eta[l], LHEPart_phi[l], LHEPart_mass[l]);;
//       if(abs(LHEPart_pdgId[l]) ==12 || abs(LHEPart_pdgId[l]) ==14 || abs(LHEPart_pdgId[l]) ==16 ) WnuLHE.SetPtEtaPhiM(LHEPart_pt[l], LHEPart_eta[l], LHEPart_phi[l], LHEPart_mass[l]);;
//     }
    if(topEvent){
      gammaFromT=false;
      for (int l=0;l<nGenPart;l++){
        if(isnan(GenPart_pt[l]) || isinf(GenPart_pt[l]) || GenPart_pt[l]==0) continue;
        if(abs(GenPart_pdgId[l])==11 || GenPart_pdgId[l]==13 ||GenPart_pdgId[l]==15){
          if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) topLeptonicEvent=true;
        }
       if(abs(GenPart_pdgId[l])==600 || abs(GenPart_pdgId[l])==9000005) ptts=GenPart_pt[l];
       if(GenPart_pdgId[l]==600 || abs(GenPart_pdgId[l])==9000005) TsCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
       if(GenPart_pdgId[l]==-600 || abs(GenPart_pdgId[l])==-9000005) TsBarCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
       if(GenPart_genPartIdxMother[l]<0) continue;
       if(abs(GenPart_pdgId[l])>0 && abs(GenPart_pdgId[l])<5 && abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24){
         topObj = new TLorentzVector ();
         topObj->SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]) ;
         topObjects->push_back(topObj);
       }
       if(abs(GenPart_pdgId[l])==5 && abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==6){
         topObj = new TLorentzVector ();
         topObj->SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]) ;
         topObjects->push_back(topObj);
       }
       if(abs(GenPart_pdgId[l])==6){
         topPt = topPt + GenPart_pt[l];
         if(GenPart_pdgId[GenPart_genPartIdxMother[l]]==600 || GenPart_pdgId[GenPart_genPartIdxMother[l]]==9000005) TopCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
       }
       if(GenPart_pdgId[l]==-6 && (abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==600 || abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==9000005)) TopBarCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
       if(abs(GenPart_pdgId[l])==22 && (abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==600 || abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==9000005)) GammaCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
       if(abs(GenPart_pdgId[l])==22 && (GenPart_pdgId[GenPart_genPartIdxMother[l]]==600|| GenPart_pdgId[GenPart_genPartIdxMother[l]]==9000005)) gammaFromT=true;
       if(abs(GenPart_pdgId[l])==21 && (abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==600|| abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==9000005)) GluonCandidate.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
      }

      if(topObjects->size()!=6) topEvent=false;
      for (int l=0;l<nLHEPart;l++){
        if(abs(LHEPart_pdgId[l]) ==11 || abs(LHEPart_pdgId[l]) ==13 || abs(LHEPart_pdgId[l]) ==15 ) NlepLHE++;
      }
      Hists1dSignal[vInd(vars1dSignal,"excitedTop_genPt")]->Fill(TsCandidate.Pt());
      Hists1dSignal[vInd(vars1dSignal,"excitedTop_genEta")]->Fill(TsCandidate.Eta());
      Hists1dSignal[vInd(vars1dSignal,"top_genPt")]->Fill(TopCandidate.Pt());
      Hists1dSignal[vInd(vars1dSignal,"top_genEta")]->Fill(TopCandidate.Eta());
      Hists1dSignal[vInd(vars1dSignal,"gamma_genPt")]->Fill(GammaCandidate.Pt());
      Hists1dSignal[vInd(vars1dSignal,"gamma_genEta")]->Fill(GammaCandidate.Eta());
      Hists1dSignal[vInd(vars1dSignal,"gluon_genPt")]->Fill(GluonCandidate.Pt());
      Hists1dSignal[vInd(vars1dSignal,"gluon_genEta")]->Fill(GluonCandidate.Eta());
      Hists1dSignal[vInd(vars1dSignal,"excitedTop_mass")]->Fill(TsCandidate.M());
      Hists1dSignal[vInd(vars1dSignal,"genMassPhtop")]->Fill((TopCandidate+GammaCandidate).M());
      Hists1dSignal[vInd(vars1dSignal,"genMassGluontop")]->Fill((TopCandidate+GluonCandidate).M());
      Hists1dSignal[vInd(vars1dSignal,"geDrPhtop")]->Fill(deltaR(TopCandidate.Eta(), TopCandidate.Phi(), GammaCandidate.Eta(),GammaCandidate.Phi()));
      Hists1dSignal[vInd(vars1dSignal,"geDrPGluontop")]->Fill(deltaR(TopCandidate.Eta(), TopCandidate.Phi(), GluonCandidate.Eta(),GluonCandidate.Phi()));
      Hists1dSignal[vInd(vars1dSignal,"genMassTTbar")]->Fill((TsCandidate+TsBarCandidate).M());
      Hists2dSignal[0]->Fill((TopCandidate+GammaCandidate).M(),(TopCandidate+GluonCandidate).M());
      Hists2dSignal[1]->Fill((TopCandidate+GammaCandidate).M(),(TopBarCandidate+GammaCandidate).M());
      Hists2dSignal[2]->Fill(GammaCandidate.Pt(),(TopCandidate+GammaCandidate).M());
      Hists2dSignal[3]->Fill(TopCandidate.P(), TopBarCandidate.P());
    }
//overlap removal of the qcd-gammaJets and ttbar-ttbarGamma
   if(data == "mc" &&     fname.Contains("QCD")){
     if (overlapRemoval(25., 2.5, 0.4, false)) {
       nOL++;
       continue;
     }
   }

   if(fname.Contains("TTTo")){
     if (overlapRemoval(10.0, 5.0, 0.1, false)) {
       nOL++;
       continue;
     }
   }

//MET filters
    if(year == "2017" || year == "2018"){
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }
    else{
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }
//trigger
   if(data == "mc") {
     if(year == "2017" || year == "2018"){
       if(HLT_Photon200) triggerPassA = true;
     }
     else{
       if(HLT_Photon175) triggerPassA = true;
     }
   }
   if(data == "data"){
     if(year == "2017" || year == "2018"){
       if(HLT_Photon200) triggerPassA = true;
     }
     else{
       if(HLT_Photon175) triggerPassA = true;
     }
   }


   for (int l=0;l<nPhoton;l++){
     if(abs(Photon_eta[l])>1.444 || Photon_pt[l]<150) continue;
     if(Photon_pixelSeed[l]) continue;
     if(Photon_cutBased[l]<2) continue;
     trigEffDen->Fill(Photon_pt[l]);
     if(triggerPassA) trigEffNum->Fill(Photon_pt[l]);
   }
   if(!metFilterPass || !triggerPassA) continue;
   nAcceptPassTrigger++;
//Photon Selection
    PhotonsMedium = new std::vector<lepton_candidate*>();
    PhotonsMediumScaleUp = new std::vector<lepton_candidate*>();
    PhotonsMediumScaleDown = new std::vector<lepton_candidate*>();
    PhotonsMediumSmearUp = new std::vector<lepton_candidate*>();
    PhotonsMediumSmearDown = new std::vector<lepton_candidate*>();
    fakePhotonsIso = new std::vector<lepton_candidate*>();
    fakePhotonsSiSi = new std::vector<lepton_candidate*>();
    fakePhotonsIsoSiSi = new std::vector<lepton_candidate*>();
    fakePhotonsOther = new std::vector<lepton_candidate*>();
    for (int l=0;l<nPhoton;l++){
      if(abs(Photon_eta[l])>1.444) continue;
      if(Photon_pixelSeed[l]) continue;
//      bitset<16> myBitSet(Photon_vidNestedWPBitmap[l]);
//      cout << myBitSet.to_string() << " (" << myBitSet.to_ulong() << ") " << endl;
      if(Photon_pt[l] >240.0){
//      if(!Photon_electronVeto[l]) continue;
        std::vector<bool> cuts_loose = parsePhotonVIDCuts(Photon_vidNestedWPBitmap[l],1);
        std::vector<bool> cuts_medium = parsePhotonVIDCuts(Photon_vidNestedWPBitmap[l],2);
        if( cuts_medium[1] &&  cuts_medium[4] && cuts_medium[5]) h_2dSieieVsChiso->Fill(Photon_sieie[l],Photon_pfRelIso03_chg[l]*Photon_pt[l]);
        if(!cuts_loose[1] ||  Photon_sieie[l] > 0.02 || Photon_pfRelIso03_chg[l]*Photon_pt[l] > 20.0) continue;
        nominalWeights[getVecPos(sys,"phIDSf")] = nominalWeights[getVecPos(sys,"phIDSf")] * csetPhotonIdSF->evaluate({year, "sf", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({year, "sf", "Medium", "EBInc"});
        sysUpWeights[getVecPos(sys,"phIDSf")] = sysUpWeights[getVecPos(sys,"phIDSf")] * csetPhotonIdSF->evaluate({year, "sfup", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({year, "sfup", "Medium", "EBInc"});
        sysDownWeights[getVecPos(sys,"phIDSf")] = sysDownWeights[getVecPos(sys,"phIDSf")] * csetPhotonIdSF->evaluate({year, "sfdown", "Medium", Photon_eta[l], Photon_pt[l]}) * csetPhotonCsevSF->evaluate({year, "sfdown", "Medium", "EBInc"});
        if(Photon_cutBased[l]>=2) PhotonsMedium->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
        else if(cuts_medium[1] && cuts_medium[2] && !cuts_medium[3] &&  cuts_medium[4] && cuts_medium[5] && Photon_pfRelIso03_chg[l]*Photon_pt[l] > 10 && Photon_pfRelIso03_chg[l]*Photon_pt[l] <20) fakePhotonsIso->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
        else if(cuts_medium[1] && !cuts_medium[2] && cuts_medium[3] && cuts_medium[4] && cuts_medium[5] && Photon_sieie[l] > 0.011) fakePhotonsSiSi->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
        else if(cuts_medium[1] && !cuts_medium[2] && !cuts_medium[3] && cuts_medium[4] && cuts_medium[5] && Photon_sieie[l] > 0.011 && Photon_pfRelIso03_chg[l]*Photon_pt[l] > 10 && Photon_pfRelIso03_chg[l]*Photon_pt[l] <20) fakePhotonsIsoSiSi->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
        else fakePhotonsOther->push_back(new lepton_candidate(Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
        Ph_pt.emplace_back(Photon_pt[l]);
        Ph_eta.emplace_back(Photon_eta[l]);
        Ph_phi.emplace_back(Photon_phi[l]);
      }
      phESunc= csetPhotonES->evaluate({year, "scaleup", Photon_eta[l], static_cast<int>(Photon_seedGain[l])});
      if(phESunc*Photon_pt[l] >240.0 && Photon_cutBased[l]>=2) PhotonsMediumScaleUp->push_back(new lepton_candidate((1+phESunc)*Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      phESunc= csetPhotonES->evaluate({year, "scaledown", Photon_eta[l], static_cast<int>(Photon_seedGain[l])});
      if(phESunc*Photon_pt[l] >240.0 && Photon_cutBased[l]>=2) PhotonsMediumScaleDown->push_back(new lepton_candidate((1-phESunc)*Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      phEnergy=Photon_pt[l]*cosh(Photon_eta[l]);
      if((1-(Photon_dEsigmaUp[l]/phEnergy))*Photon_pt[l] >240.0  && Photon_cutBased[l]>=2) PhotonsMediumSmearUp->push_back(new lepton_candidate((1-(Photon_dEsigmaUp[l]/phEnergy))*Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
      if((1-(Photon_dEsigmaDown[l]/phEnergy))*Photon_pt[l] >240.0 && Photon_cutBased[l]>=2) PhotonsMediumSmearDown->push_back(new lepton_candidate((1-(Photon_dEsigmaDown[l]/phEnergy))*Photon_pt[l],Photon_eta[l],Photon_phi[l],0,l,1));
    }

    sort(PhotonsMedium->begin(), PhotonsMedium->end(), ComparePtLep);
    sort(PhotonsMediumScaleUp->begin(), PhotonsMediumScaleUp->end(), ComparePtLep);
    sort(PhotonsMediumScaleDown->begin(), PhotonsMediumScaleDown->end(), ComparePtLep);
    sort(PhotonsMediumSmearUp->begin(), PhotonsMediumSmearUp->end(), ComparePtLep);
    sort(PhotonsMediumSmearDown->begin(), PhotonsMediumSmearDown->end(), ComparePtLep);
    sort(fakePhotonsIso->begin(), fakePhotonsIso->end(), ComparePtLep);
    sort(fakePhotonsSiSi->begin(), fakePhotonsSiSi->end(), ComparePtLep);
    sort(fakePhotonsIsoSiSi->begin(), fakePhotonsIsoSiSi->end(), ComparePtLep);
    sort(fakePhotonsOther->begin(), fakePhotonsOther->end(), ComparePtLep);
//select Muon
    selectedLeptons = new std::vector<lepton_candidate*>();
    for (int l=0;l<nMuon;l++){
      if(abs(Muon_eta[l]) > 2.4) continue;
      if(Muon_highPtId[l]<2) continue;
      if(Muon_tkIsoId[l]<1) continue;
      if(Muon_tunepRelPt[l]*Muon_pt[l]>30) selectedLeptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10));
    }
//select electron
    for (int l=0;l<nElectron;l++){
      if(abs(Electron_eta[l]) > 2.4 || (abs(Electron_eta[l])> 1.4442 && (abs(Electron_eta[l])< 1.566))) continue;
      if(Electron_pt[l] <30) continue;
      if(!Electron_cutBased_HEEP[l]) continue;
      selectedLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1));
    }
    sort(selectedLeptons->begin(),selectedLeptons->end(), ComparePtLep);
//select jets AK8
    selectedJets08 = new std::vector<jet_candidate*>();
    selectedJets08JesUp = new std::vector<jet_candidate*>();
    selectedJets08JesDown = new std::vector<jet_candidate*>();
    topIndex = new std::vector<int>();
    wIndex = new std::vector<int>();
    bsubIndex = new std::vector<int>();
    topTagIndex = new std::vector<int>();
    WTagIndex = new std::vector<int>();
    int nsubB = 0;
    for (int l=0;l<nFatJet;l++){
      if(abs(FatJet_eta[l]) > 2.4) continue;
      jetlepfail = false;
      for (int i=0;i<PhotonsMedium->size();i++){
        if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      if(PhotonsMedium->size()==0){
        for (int i=0;i<fakePhotonsIso->size();i++){
          if(deltaR((*fakePhotonsIso)[i]->eta_,(*fakePhotonsIso)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
        }
        for (int i=0;i<fakePhotonsSiSi->size();i++){
          if(deltaR((*fakePhotonsSiSi)[i]->eta_,(*fakePhotonsSiSi)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
        }
        for (int i=0;i<fakePhotonsOther->size();i++){
          if(deltaR((*fakePhotonsOther)[i]->eta_,(*fakePhotonsOther)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
        }
      }
      if(jetlepfail) continue;
      if(FatJet_pt[l]>225){
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
        selectedJets08->push_back(new jet_candidate(FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_particleNet_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
        Ak8_pt.emplace_back(FatJet_pt[l]);
        Ak8_eta.emplace_back(FatJet_eta[l]);
        Ak8_phi.emplace_back(FatJet_phi[l]);

        for (int j=0; j<PhotonsMedium->size();j++){
          if (deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_, FatJet_eta[l],FatJet_phi[l])< drgj08) drgj08 = deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,FatJet_eta[l],FatJet_phi[l]);
        }
      }
      vsrc08[21]->setJetPt(FatJet_pt[l]);
      vsrc08[21]->setJetEta(FatJet_eta[l]);
      sup =  vsrc08[21]->getUncertainty(true);
      if ((1+sup)*FatJet_pt[l]>225) selectedJets08JesUp->push_back(new jet_candidate((1+sup)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_particleNet_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
      if ((1-sup)*FatJet_pt[l]>225) selectedJets08JesDown->push_back(new jet_candidate((1-sup)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_particleNet_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
    }
    sort(selectedJets08->begin(), selectedJets08->end(), CompareMassJet);
    sort(selectedJets08JesUp->begin(), selectedJets08JesUp->end(), CompareMassJet);
    sort(selectedJets08JesDown->begin(), selectedJets08JesDown->end(), CompareMassJet);

    if(data == "mc" && ifSys){
      JEC08sysUp = new std::vector<std::vector<jet_candidate*>>();
      JEC08sysDown = new std::vector<std::vector<jet_candidate*>>();
      for (int n=0;n<sysJecNames.size();++n){
        JECJetsUp= new std::vector<jet_candidate*>();
        JECJetsDown= new std::vector<jet_candidate*>();
        for (int l=0;l<nFatJet;l++){
          if(abs(FatJet_eta[l]) > 2.4) continue;
          jetlepfail = false;
          for (int i=0;i<PhotonsMedium->size();i++){
            if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
          }
          if(PhotonsMedium->size()==0){
            for (int i=0;i<fakePhotonsIso->size();i++){
              if(deltaR((*fakePhotonsIso)[i]->eta_,(*fakePhotonsIso)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
            }
            for (int i=0;i<fakePhotonsSiSi->size();i++){
              if(deltaR((*fakePhotonsSiSi)[i]->eta_,(*fakePhotonsSiSi)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
            }
            for (int i=0;i<fakePhotonsIsoSiSi->size();i++){
              if(deltaR((*fakePhotonsIsoSiSi)[i]->eta_,(*fakePhotonsIsoSiSi)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
            }
            for (int i=0;i<fakePhotonsOther->size();i++){
              if(deltaR((*fakePhotonsOther)[i]->eta_,(*fakePhotonsOther)[i]->phi_,FatJet_eta[l],FatJet_phi[l]) < 0.8 ) jetlepfail=true;
            }
          }
          if(jetlepfail) continue;
          vsrc08[n]->setJetPt(FatJet_pt[l]);
          vsrc08[n]->setJetEta(FatJet_eta[l]);
          sup = vsrc08[n]->getUncertainty(true);
          if ((1+sup)*FatJet_pt[l]>225) {
            JECJetsUp->push_back(new jet_candidate((1+sup)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_particleNet_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
          }
          if ((1-sup)*FatJet_pt[l]>225){
            JECJetsDown->push_back(new jet_candidate((1-sup)*FatJet_pt[l],FatJet_eta[l],FatJet_phi[l],FatJet_mass[l],FatJet_btagDeepB[l], year,0,l,NtopPartons,2,nsubB, FatJet_msoftdrop[l], FatJet_particleNet_TvsQCD[l],FatJet_deepTagMD_WvsQCD[l]));
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
      if(Jet_pt[l] <50.0 || abs(Jet_eta[l]) > 2.5 || Jet_jetId[l]<6) continue;
      jetlepfail = false;
      jetAk8fail = false;
      for (int i=0;i<PhotonsMedium->size();i++){
        if(deltaR((*PhotonsMedium)[i]->eta_,(*PhotonsMedium)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetlepfail=true;
      }
      if(PhotonsMedium->size()==0){
        for (int i=0;i<fakePhotonsIso->size();i++){
          if(deltaR((*fakePhotonsIso)[i]->eta_,(*fakePhotonsIso)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetlepfail=true;
        }
        for (int i=0;i<fakePhotonsSiSi->size();i++){
          if(deltaR((*fakePhotonsSiSi)[i]->eta_,(*fakePhotonsSiSi)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetlepfail=true;
        }
        for (int i=0;i<fakePhotonsIsoSiSi->size();i++){
          if(deltaR((*fakePhotonsIsoSiSi)[i]->eta_,(*fakePhotonsIsoSiSi)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetlepfail=true;
        }
        for (int i=0;i<fakePhotonsOther->size();i++){
          if(deltaR((*fakePhotonsOther)[i]->eta_,(*fakePhotonsOther)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetlepfail=true;
        }
      }
      if(jetlepfail) continue;
      for (int i=0;i<selectedJets08->size();i++){
//        if(i>0) continue;
        if(deltaR((*selectedJets08)[i]->eta_,(*selectedJets08)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.8 ) jetAk8fail=true;
      }
      if(jetAk8fail) continue;
      selectedJets04->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],0,Jet_btagDeepB[l], year,Jet_partonFlavour[l],l,0,0,0,0,0,0));
      for (int j=0; j<PhotonsMedium->size();j++){
        if (deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,Jet_eta[l],Jet_phi[l])< drgj04)  drgj04 = deltaR((*PhotonsMedium)[j]->eta_, (*PhotonsMedium)[j]->phi_,Jet_eta[l],Jet_phi[l]);
      }
    }
    sort(selectedJets04->begin(), selectedJets04->end(), ComparePtJet);

    for (int l=0;l<selectedJets04->size();l++){
      ht = ht + (*selectedJets04)[l]->pt_;
      if((*selectedJets04)[l]->btag_ && abs((*selectedJets04)[l]->eta_)<2.4) nbq++;
      if(selectedJets08->size()>0){
//        if (deltaR((*selectedJets04)[l]->eta_, (*selectedJets04)[l]->phi_,(*selectedJets08)[0]->eta_, (*selectedJets08)[0]->phi_) > 0.8) Ts2Candidate += (*selectedJets04)[l]->p4_;
        if(deltaR((*selectedJets04)[l]->eta_, (*selectedJets04)[l]->phi_,(*selectedJets08)[0]->eta_, (*selectedJets08)[0]->phi_) > 1.2 && abs((*selectedJets04)[l]->eta_)<2.4 && (*selectedJets04)[l]->btag_) nbjet04++;
      }
    }

    for (int l=0;l<selectedJets08->size();l++){
      if ((*selectedJets08)[l]->toptag_){
        toptagIndex=l;
        break;
      }
    }
    for (int l=0;l<selectedJets08->size();l++){
      ht = ht + (*selectedJets08)[l]->pt_;
      if((*selectedJets08)[l]->btag_) nbjet08++;
      if((*selectedJets08)[l]->toptag_) ntopTagNM++;
      if((*selectedJets08)[l]->toptag_ && (*selectedJets08)[l]->mass_>125 && (*selectedJets08)[l]->mass_<225) ntopTag++;
      if((*selectedJets08)[l]->toptag_ && ((*selectedJets08)[l]->mass_<125 || (*selectedJets08)[l]->mass_>225)) ntopTagSB++;
      if((*selectedJets08)[l]->toptag_ && (*selectedJets08)[l]->pt_>300 && (*selectedJets08)[l]->pt_<1200){
        nominalWeights[getVecPos(sys,"topTagSF")] = nominalWeights[getVecPos(sys,"topTagSF")] * csetParticleNetTopTagSF->evaluate({(*selectedJets08)[l]->eta_, (*selectedJets08)[l]->pt_,"nom", "0p1"});
        sysUpWeights[getVecPos(sys,"topTagSF")] = sysUpWeights[getVecPos(sys,"topTagSF")] * csetParticleNetTopTagSF->evaluate({(*selectedJets08)[l]->eta_, (*selectedJets08)[l]->pt_,"up", "0p1"});
        sysDownWeights[getVecPos(sys,"topTagSF")] = sysDownWeights[getVecPos(sys,"topTagSF")] * csetParticleNetTopTagSF->evaluate({(*selectedJets08)[l]->eta_, (*selectedJets08)[l]->pt_,"down", "0p1"});
      }
//      if((*selectedJets08)[l]->toptag_ && (*selectedJets08)[l]->pt_>300) topTagSF= topTagSF*fatjetscalefactors.ak8SF(false, 2017, 6, true, 4, (*selectedJets08)[l]->eta_, (*selectedJets08)[l]->pt_,  0);
    }
    if(selectedJets08->size()>0 && (PhotonsMedium->size()>0 || PhotonsMediumScaleUp->size()>0 || PhotonsMediumScaleDown->size()>0 ||  PhotonsMediumSmearUp->size()>0 || PhotonsMediumSmearDown->size()>0)) ch=0;
    if(selectedJets08->size()>0 && PhotonsMedium->size()==0 && fakePhotonsIso->size()>0) chFA=0;
    if(selectedJets08->size()>0 && PhotonsMedium->size()==0 && fakePhotonsSiSi->size()>0) chFA=1;
    if(selectedJets08->size()>0 && PhotonsMedium->size()==0 && fakePhotonsIsoSiSi->size()>0) chFA=2;
    if(selectedJets08->size()>0 && PhotonsMedium->size()==0 && fakePhotonsOther->size()>0) chFA=3;
    if(ch==0) nAcceptPassPhoton++;

    if(ch>10 && chFA>10) {
      for (int l=0;l<selectedJets04->size();l++){
        delete (*selectedJets04)[l];
      }
      for (int l=0;l<selectedJets08->size();l++){
        delete (*selectedJets08)[l];
      }
      for (int l=0;l<PhotonsMedium->size();l++){
        delete (*PhotonsMedium)[l];
      }
      for (int l=0;l<fakePhotonsIso->size();l++){
        delete (*fakePhotonsIso)[l];
      }
      for (int l=0;l<fakePhotonsSiSi->size();l++){
        delete (*fakePhotonsSiSi)[l];
      }
      for (int l=0;l<fakePhotonsIsoSiSi->size();l++){
        delete (*fakePhotonsIsoSiSi)[l];
      }
      for (int l=0;l<fakePhotonsOther->size();l++){
        delete (*fakePhotonsOther)[l];
      }
      if(data == "mc" && ifSys){
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
        delete JEC08sysUp;
        JEC08sysDown->clear();
        JEC08sysDown->shrink_to_fit();
        delete JEC08sysDown;
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
      cleanVec (PhotonsMediumScaleUp);
      cleanVec (PhotonsMediumScaleDown);
      cleanVec (PhotonsMediumSmearUp);
      cleanVec (PhotonsMediumSmearDown);
      cleanVec (selectedJets08JesUp);
      cleanVec (selectedJets08JesDown);
      fakePhotonsIsoSiSi->clear();
      fakePhotonsIsoSiSi->shrink_to_fit();
      delete fakePhotonsIsoSiSi;
      fakePhotonsIso->clear();
      fakePhotonsIso->shrink_to_fit();
      delete fakePhotonsIso;
      fakePhotonsOther->clear();
      fakePhotonsOther->shrink_to_fit();
      delete fakePhotonsOther;
      fakePhotonsSiSi->clear();
      fakePhotonsSiSi->shrink_to_fit();
      delete fakePhotonsSiSi;
      topIndex->clear();
      topIndex->shrink_to_fit();
      delete topIndex;
      wIndex->clear();
      wIndex->shrink_to_fit();
      delete wIndex;
      bsubIndex->clear();
      bsubIndex->shrink_to_fit();
      delete bsubIndex;
      topTagIndex->clear();
      topTagIndex->shrink_to_fit();
      delete topTagIndex;
      WTagIndex->clear(); 
      WTagIndex->shrink_to_fit();
      delete WTagIndex;
      continue;
    }
    if (data == "mc"){
      if (year == "2016preVFP") {
        nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"nominal");
        sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"up");
        sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"down");
      }
      if (year == "2016postVFP") {
        nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"nominal");
        sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"up");
        sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"down");
      }
      if (year == "2017") {
        nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"nominal");
        sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"up");
        sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"down");
      }
      if (year == "2018") {
        nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"nominal");
        sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"up");
        sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"down");
      }

      nominalWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Nom;
      sysUpWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Up;
      sysDownWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Dn;

      weight_Lumi = (1000*xs*lumi)/Nevent;
      finalWeight = weight_Lumi * signnum_typical(genWeight) * nominalWeights[getVecPos(sys,"phIDSf")]*nominalWeights[getVecPos(sys,"pu")]*nominalWeights[getVecPos(sys,"prefiring")];
      finalWeightSF = finalWeight*nominalWeights[getVecPos(sys,"topTagSF")];
    }
    //calculate the mistag rate
    for (int l=0;l<selectedJets08->size();l++){
      if((*selectedJets08)[l]->mass_>125 && (*selectedJets08)[l]->mass_<225){
        ntopTagRandom++;
        topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*selectedJets08)[l]->pt_,FatJet_msoftdrop[(*selectedJets08)[l]->indice_],"central"));
        topMTRup = topMTRup * (1-scale_factor(&h_topMistagRate,(*selectedJets08)[l]->pt_,FatJet_msoftdrop[(*selectedJets08)[l]->indice_],"up"));
        topMTRdown = topMTRdown * (1-scale_factor(&h_topMistagRate,(*selectedJets08)[l]->pt_,FatJet_msoftdrop[(*selectedJets08)[l]->indice_],"down"));
      }
      if(((*selectedJets08)[l]->mass_<125 && (*selectedJets08)[l]->mass_>100) || (*selectedJets08)[l]->mass_>225){
        ntopTagRandomSB++;
        topMTRSB = topMTRSB * (1-scale_factor(&h_topMistagRate,(*selectedJets08)[l]->pt_,FatJet_msoftdrop[(*selectedJets08)[l]->indice_],"central"));
      }
    }
      nominalWeightsData[getVecPos(sysData,"missTagRate")] = topMTR;
      sysUpWeightsData[getVecPos(sysData,"missTagRate")] = topMTRup;
      sysDownWeightsData[getVecPos(sysData,"missTagRate")] = topMTRdown;
//Fill the nominal histograms
    if(PhotonsMedium->size()>0 || fakePhotonsIso->size()>0 || fakePhotonsSiSi->size()>0 || fakePhotonsIsoSiSi->size()>0 || fakePhotonsOther->size()>0){
      if (ch==0) selectedPhotons = PhotonsMedium;
      if (chFA==0) selectedPhotons = fakePhotonsIso;
      if (chFA==1) selectedPhotons = fakePhotonsSiSi;
      if (chFA==2) selectedPhotons = fakePhotonsIsoSiSi;
      if (chFA==3) selectedPhotons = fakePhotonsOther;
      if(data == "mc"){
        if (Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1) cat=0;
        else if (Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==11) cat=1;
        else cat=2;
      }
      FR=rate(&h_fakeRate,(*selectedPhotons)[0]->eta_);
      FR=FR/(1-FR);
      //Find the best T* mass
      mT1=0;
      mT2=0;
      mT1V2=0;
      mT2V2=0;
      otherObjects = new std::vector<TLorentzVector*>();
      otherObjectsV2 = new std::vector<TLorentzVector*>();
      for (int l=0;l<selectedJets08->size();l++){
        if(l==toptagIndex) continue;
        topObj = new TLorentzVector ();
        topObj->SetPtEtaPhiM((*selectedJets08)[l]->p4_.Pt(), (*selectedJets08)[l]->p4_.Eta(),(*selectedJets08)[l]->p4_.Phi(),(*selectedJets08)[l]->p4_.M()) ;
        otherObjects->push_back(topObj);
        Ts2Candidate+= (*selectedJets08)[l]->p4_;
      }
  
      topObj = new TLorentzVector ();
      topObj->SetPtEtaPhiM((*selectedPhotons)[0]->p4_.Pt(), (*selectedPhotons)[0]->p4_.Eta(),(*selectedPhotons)[0]->p4_.Phi(),(*selectedPhotons)[0]->p4_.M()) ;
      otherObjects->push_back(topObj);
  
      bestMass((*selectedJets08)[toptagIndex]->p4_, otherObjects, &mT1, &mT2);
      bestMassV2((*selectedJets08)[toptagIndex]->p4_, (*selectedPhotons)[0]->p4_, otherObjectsV2, &mT1V2, &mT2V2);
  
      for (int n=0;n<otherObjects->size();n++){
            delete (*otherObjects)[n];
      }
      otherObjects->clear();
      otherObjects->shrink_to_fit();
      delete otherObjects;
  
      Wnu.SetPtEtaPhiM(MET_pt,0,MET_phi,0);
      Wele.SetPtEtaPhiM((*selectedPhotons)[0]->pt_,0,(*selectedPhotons)[0]->phi_,0);

      reg.push_back(getVecPos(regions,"nAk8G0"));
      wgt.push_back(finalWeight);
      regFA.push_back(getVecPos(regionsFA,"nAk8G0"));
      wgtFA.push_back(finalWeight);
      if(selectedJets08->size()==1 && (*selectedJets08)[0]->mass_>90){
        if(chFA<10) {
          Hists2d[0][0][4]->Fill((*selectedJets08)[0]->pt_,FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
          if(ntopTagNM>0) Hists2d[0][0][5]->Fill((*selectedJets08)[0]->pt_,FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
        }
        if(ch==0) {
          Hists2d[0][0][6]->Fill((*selectedJets08)[0]->pt_,FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
          if(ntopTagNM>0) Hists2d[0][0][7]->Fill((*selectedJets08)[0]->pt_,FatJet_msoftdrop[(*selectedJets08)[0]->indice_],finalWeightSF);
        }
        reg.push_back(getVecPos(regions,"nAk81"));
        wgt.push_back(finalWeight);
      }
      if(selectedJets08->size()==1 && ntopTag==1){
        reg.push_back(getVecPos(regions,"nAk81nTtag1"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
        regFA.push_back(getVecPos(regionsFA,"nAk81nTtag1"));
        wgtFA.push_back(finalWeight*FR);
      }
      if(selectedJets08->size()>1 &&  ntopTag>0){
        reg.push_back(getVecPos(regions,"nAk8G1nTtagG0"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
        if(ch==0) nAccept++;
        if(ch==0 && NlepLHE>0) nAcceptLeptonicTop++;
        regFA.push_back(getVecPos(regionsFA,"nAk8G1nTtagG0"));
        wgtFA.push_back(finalWeight*FR);
  //if(mT1<600){
  //   cout<<"################################################################################################"<<endl;
  //   cout<<"GluonCandidate:"<<GluonCandidate.Pt()<<","<<GluonCandidate.Eta()<<","<<GluonCandidate.Phi()<<endl; 
  //   cout<<"TopCandidate:"<<TopCandidate.Pt()<<","<<TopCandidate.Eta()<<","<<TopCandidate.Phi()<<endl;
  //   cout<<"TopBarCandidate:"<<TopBarCandidate.Pt()<<","<<TopBarCandidate.Eta()<<","<<TopBarCandidate.Phi()<<endl;
  //   cout<<"GammaCandidate:"<<GammaCandidate.Pt()<<","<<GammaCandidate.Eta()<<","<<GammaCandidate.Phi();
  //   if(gammaFromT) cout<<"  Gamma from T*" <<endl;
  //   else cout<<"  Gamma from Anti-T*" <<endl;
  //for (int l=0;l<selectedJets08->size();l++){
  //   if(l==toptagIndex) continue;
  //cout<<"Ak8 Jet "<<l<<":"<<(*selectedJets08)[l]->p4_.Pt()<<","<<(*selectedJets08)[l]->p4_.Eta()<<","<<(*selectedJets08)[l]->p4_.Phi()<<" - Top tagged: "<<(*selectedJets08)[l]->toptag_<<endl;
  //   }
  //for (int l=0;l<selectedJets04->size();l++){
  //cout<<"Ak4 Jet "<<l<<":"<<(*selectedJets04)[l]->p4_.Pt()<<","<<(*selectedJets04)[l]->p4_.Eta()<<","<<(*selectedJets04)[l]->p4_.Phi()<<endl;
  //   }
  
  //   cout<<"TOP tagged:"<<(*selectedJets08)[toptagIndex]->p4_.Pt()<<","<<(*selectedJets08)[toptagIndex]->p4_.Eta()<<","<<(*selectedJets08)[toptagIndex]->p4_.Phi()<<endl;
  //   cout<<"selectedPhotons:"<<(*selectedPhotons)[0]->p4_.Pt()<<","<<(*selectedPhotons)[0]->p4_.Eta()<<","<<(*selectedPhotons)[0]->p4_.Phi()<<endl;
  //
  //   cout<<"NEW Mass:"<<mT1<<","<<mT2<<endl;
  ////   cout<<"NEW MassV2:"<<mT1V2<<","<<mT2V2<<endl;
  //   cout<<"OLD Mass:"<<((*selectedPhotons)[0]->p4_+(*selectedJets08)[toptagIndex]->p4_).M()<<","<<Ts2Candidate.M()<<endl;
  //}
        Hists2d[0][0][0]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),Ts2Candidate.M());
        Hists2d[0][0][1]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),abs(deltaPhi((*selectedPhotons)[0]->phi_, (*selectedJets08)[0]->phi_)));
        Hists2d[0][0][2]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),deltaR((*selectedPhotons)[0]->eta_, (*selectedPhotons)[0]->phi_,(*selectedJets08)[0]->eta_, (*selectedJets08)[0]->phi_));
        Hists2d[0][0][3]->Fill(((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).Pt(),Ts2Candidate.Pt());
      }

      if(selectedJets08->size()>1 && ntopTag>0 && selectedLeptons->size()>0){
        reg.push_back(getVecPos(regions,"nAk8G1nTtagG0LepG0"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
//cout<<NlepLHE<<":"<<selectedLeptons->size()<<endl;
//for (int l=0;l<selectedLeptons->size();l++){
//cout<<(*selectedLeptons)[l]->lep_<<" dr="<<deltaR((*selectedLeptons)[l]->eta_,(*selectedLeptons)[l]->phi_,(*selectedPhotons)[0]->eta_,(*selectedPhotons)[0]->phi_)<<":"<<endl;
//if((*selectedLeptons)[l]->lep_==1) cout<<"status"<<Electron_genPartFlav[(*selectedLeptons)[l]->indice_]<<endl;
//}
      }

      if(selectedJets08->size()==1 &&  ntopTagSB>0 && ntopTag==0){
        reg.push_back(getVecPos(regions,"nAk81nTtagOffMt"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
        regFA.push_back(getVecPos(regionsFA,"nAk81nTtagOffMt"));
        wgtFA.push_back(finalWeight*FR);
      }

      if(selectedJets08->size()>1 && ntopTag==0) {
        reg.push_back(getVecPos(regions,"nAk8G1nTtag0"));
        wgt.push_back(finalWeight);
        if(ch==0) ntopTag0++;
      }
      if(selectedJets08->size()>1 &&  ntopTag==0 && ntopTagRandom>0) {
        reg.push_back(getVecPos(regions,"nAk8G1nTtag0XtopMissTagRate"));
        wgt.push_back(finalWeight*((1-topMTR)/topMTR));
      }
      if(selectedJets08->size()==1 && ntopTag==0 && ntopTagRandom>0){
        reg.push_back(getVecPos(regions,"nAk81nTtag0XtopMissTagRate"));
        wgt.push_back(finalWeight*((1-topMTR)/topMTR));
      }
      if(selectedJets08->size()==1 && ntopTag==0 && ntopTagSB==0 && ntopTagRandomSB>0){
        reg.push_back(getVecPos(regions,"nAk81nTtagOffMtXtopMissTagRate"));
        wgt.push_back(finalWeight*((1-topMTRSB)/topMTRSB));
      }
      for(int n=0;n<wgt.size();++n){
        wgtnoPU.push_back(wgt[n]/nominalWeights[getVecPos(sys,"pu")]);
      }
  //Fill histograms
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"GammaPt"),          (*selectedPhotons)[0]->pt_       ,wgt);
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"GammaEta"),         (*selectedPhotons)[0]->eta_      ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"GammaPhi"),         (*selectedPhotons)[0]->phi_      ,wgt);
      if(selectedJets04->size()>0){
        FillD3Hists(Hists, cat, ch, reg, vInd(vars,"jet04Pt"),          (*selectedJets04)[0]->pt_        ,wgt); 
        FillD3Hists(Hists, cat, ch, reg, vInd(vars,"jet04Eta"),         (*selectedJets04)[0]->eta_       ,wgt); 
      }
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"njet04"),           selectedJets04->size()+selectedJets08->size()           ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"nbjet04"),          nbjet04                          ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"jet08Pt"),          (*selectedJets08)[0]->pt_        ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"jet08Eta"),         (*selectedJets08)[0]->eta_        ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"jet08Phi"),         (*selectedJets08)[0]->phi_        ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"njet08"),           selectedJets08->size()           ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"Met"),              MET_pt                           ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"nPh"),              selectedPhotons->size()          ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"phoChargedIso"),    Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"HT"),               ht                               ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"HoE"),              Photon_hoe[(*selectedPhotons)[0]->indice_],wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"TvsQCD"),           FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"TsMass1"),          ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"nTopTag"),          ntopTag                          ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"masstS2"),          Ts2Candidate.M()                 ,wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"Sietaieta"),        Photon_sieie[(*selectedPhotons)[0]->indice_],wgt); 
      FillD3Hists(Hists, cat, ch, reg, vInd(vars ,"MtGMet"),TransverseMass(Wele,Wnu,0,0)        ,wgt);
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"nVtxApu"), PV_npvs ,wgt);
      FillD3Hists(Hists, cat, ch, reg, vInd(vars,"nVtxBpu"), PV_npvs ,wgtnoPU);
      if(selectedJets08->size()>1) FillD3Hists(Hists, cat, ch, reg, vInd(vars,"subLeadingJet08Pt"),          (*selectedJets08)[1]->pt_        ,wgt);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"GammaPt"),          (*selectedPhotons)[0]->pt_       ,wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"GammaEta"),         (*selectedPhotons)[0]->eta_      ,wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"nPh"),              selectedPhotons->size()          ,wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"phoChargedIso"),    Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"HoE"),              Photon_hoe[(*selectedPhotons)[0]->indice_],wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"Sietaieta"),        Photon_sieie[(*selectedPhotons)[0]->indice_],wgtFA);
      FillD3Hists(HistsFA, cat, chFA, regFA, vInd(varsFA,"TsMass1"),          ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtFA);

      if (data == "mc" && ifSys && Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1){
  //Wieght dependent sys
        for(int n=0;n<sys.size();++n){
          if (std::find(sysNotWeight.begin(), sysNotWeight.end(), sys[n]) != sysNotWeight.end()) continue;
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
    //      FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtUp);
   //       FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtUp);
  //        FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"softdropMassLeadingJet08"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtUp);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtUp);
    //Down
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPt"),         n, (*selectedPhotons)[0]->pt_       ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaEta"),        n, (*selectedPhotons)[0]->eta_      ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPhi"),        n, (*selectedPhotons)[0]->phi_      ,wgtDown);
    //      FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtDown);
    //      FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtDown);
    //      FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"softdropMassLeadingJet08"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtDown);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtDown);
        }
  //PDF, QS, PS
        if ((fname.Contains("TTga")  || fname.Contains("TTGamma")) && ch==0){
          for (int k=0;k<reg.size();++k){
            if(reg[k]!=getVecPos(regions,"nAk8G1nTtagG0")) continue;
            regUp.clear();
            regUp.push_back(0);
            for (int n=0;n<nScale;++n){
              if(isnan(LHEScaleWeight[n]) || isinf(LHEScaleWeight[n])) continue;
              wgtUp.clear();
              wgtUp.push_back(wgt[k]*LHEScaleWeight[n]);
              FillD4Hists(HistsSysReweightsQscale, ch, regUp, 0, n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(), wgtUp);
            }
          for (int i=0;i<nPdf;++i){
              if(isnan(LHEPdfWeight[i]) || isinf(LHEPdfWeight[i])) continue;
              wgtUp.clear();
              wgtUp.push_back( wgt[k]*LHEPdfWeight[i]);
              FillD4Hists(HistsSysReweightsPDF, ch, regUp, 0, i, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(), wgtUp);
            }
          }
        }

//total JES unc
 
        ch=999;
        if(selectedJets08JesUp->size()>0 && PhotonsMedium->size()>0) ch=0;
        if(ch==0){
          ntopTag=0;
          ntopTagRandom=0;
          ht=0;
          topMTR=1;
          Ts2Candidate.SetPxPyPzE(0,0,0,0);
  
          for (int l=0;l<selectedJets08JesUp->size();l++){
            if((*selectedJets08JesUp)[l]->toptag_) ntopTag++;
            if((*selectedJets08JesUp)[l]->mass_>120 && (*selectedJets08JesUp)[l]->mass_<210){
              ntopTagRandom++;
              topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*selectedJets08JesUp)[l]->pt_,FatJet_msoftdrop[(*selectedJets08JesUp)[l]->indice_],"central"));
            }
          }
          reg.clear();
          wgt.clear();
          reg.push_back(getVecPos(regions,"nAk8G0"));
          wgt.push_back(finalWeight);
          if(selectedJets08JesUp->size()==1 && (*selectedJets08JesUp)[0]->mass_>120 && (*selectedJets08JesUp)[0]->mass_<210){
            reg.push_back(getVecPos(regions,"nAk81"));
            wgt.push_back(finalWeight);
          }
          if(selectedJets08JesUp->size()==1 && ntopTag==1){
            reg.push_back(getVecPos(regions,"nAk81nTtag1"));
            if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
            else  wgt.push_back(finalWeight);
          }
          if(selectedJets08JesUp->size()>1 && ntopTag>0){
            reg.push_back(getVecPos(regions,"nAk8G1nTtagG0"));
            if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
            else  wgt.push_back(finalWeight);
          }
          if(selectedJets08JesUp->size()>1 && ntopTag==0) {
            reg.push_back(getVecPos(regions,"nAk8G1nTtag0"));
            wgt.push_back(finalWeight);
            if(ch==0) ntopTag0++;
          }
          if(selectedJets08JesUp->size()>1 && ntopTag==0 && ntopTagRandom>0) {
            reg.push_back(getVecPos(regions,"nAk8G1nTtag0XtopMissTagRate"));
            wgt.push_back(finalWeight*((1-topMTR)/topMTR));
          }
          if(selectedJets08JesUp->size()==1 && ntopTag==0 && ntopTagRandom>0){
            reg.push_back(getVecPos(regions,"nAk81nTtag0XtopMissTagRate"));
            wgt.push_back(finalWeight*((1-topMTR)/topMTR));
          }

          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"JesTotal"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"JesTotal"), (*selectedJets08JesUp)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"JesTotal"), (*selectedJets08JesUp)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"JesTotal"), (*selectedJets08JesUp)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"JesTotal"), selectedJets08JesUp->size()           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"JesTotal"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"JesTotal"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"JesTotal"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"JesTotal"), ht                               ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"JesTotal"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"JesTotal"), FatJet_msoftdrop[(*selectedJets08JesUp)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"JesTotal"), FatJet_particleNet_TvsQCD[(*selectedJets08JesUp)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"JesTotal"), ((*selectedPhotons)[0]->p4_+(*selectedJets08JesUp)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"JesTotal"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"JesTotal"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"JesTotal"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }
//Total JES down

        ch=999;
        if(selectedJets08JesDown->size()>0 && PhotonsMedium->size()>0) ch=0;
        if(ch==0){
          ntopTag=0;
          ntopTagRandom=0;
          ht=0;
          topMTR=1;
          Ts2Candidate.SetPxPyPzE(0,0,0,0);

          for (int l=0;l<selectedJets08JesDown->size();l++){
            if((*selectedJets08JesDown)[l]->toptag_) ntopTag++;
            if((*selectedJets08JesDown)[l]->mass_>120 && (*selectedJets08JesDown)[l]->mass_<210){
              ntopTagRandom++;
              topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*selectedJets08JesDown)[l]->pt_,FatJet_msoftdrop[(*selectedJets08JesDown)[l]->indice_],"central"));
            }
          }
          reg.clear();
          wgt.clear();
          reg.push_back(getVecPos(regions,"nAk8G0"));
          wgt.push_back(finalWeight);
          if(selectedJets08JesDown->size()==1 && (*selectedJets08JesDown)[0]->mass_>120 && (*selectedJets08JesDown)[0]->mass_<210){
            reg.push_back(getVecPos(regions,"nAk81"));
            wgt.push_back(finalWeight);
          }
          if(selectedJets08JesDown->size()==1 && ntopTag==1){
            reg.push_back(getVecPos(regions,"nAk81nTtag1"));
            if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
            else  wgt.push_back(finalWeight);
          }
          if(selectedJets08JesDown->size()>1 && ntopTag>0){
            reg.push_back(getVecPos(regions,"nAk8G1nTtagG0"));
            if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
            else  wgt.push_back(finalWeight);
          }
          if(selectedJets08JesDown->size()>1 && ntopTag==0) {
            reg.push_back(getVecPos(regions,"nAk8G1nTtag0"));
            wgt.push_back(finalWeight);
            if(ch==0) ntopTag0++;
          }
          if(selectedJets08JesDown->size()>1 && ntopTag==0 && ntopTagRandom>0) {
            reg.push_back(getVecPos(regions,"nAk8G1nTtag0XtopMissTagRate"));
            wgt.push_back(finalWeight*((1-topMTR)/topMTR));
          }
          if(selectedJets08JesDown->size()==1 && ntopTag==0 && ntopTagRandom>0){
            reg.push_back(getVecPos(regions,"nAk81nTtag0XtopMissTagRate"));
            wgt.push_back(finalWeight*((1-topMTR)/topMTR));
          }
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"JesTotal"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"JesTotal"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"JesTotal"), (*selectedJets08JesDown)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"JesTotal"), (*selectedJets08JesDown)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"JesTotal"), (*selectedJets08JesDown)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"JesTotal"), selectedJets08JesDown->size()           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"JesTotal"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"JesTotal"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"JesTotal"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"JesTotal"), ht                               ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"JesTotal"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"JesTotal"), FatJet_msoftdrop[(*selectedJets08JesDown)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"JesTotal"), FatJet_particleNet_TvsQCD[(*selectedJets08JesDown)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"JesTotal"), ((*selectedPhotons)[0]->p4_+(*selectedJets08JesDown)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"JesTotal"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"JesTotal"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"JesTotal"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }

  //JES UP sys
        for (int n=0;n<sysJecNames.size();++n){
          ch=999;
          if((*JEC08sysUp)[n].size()>0 && PhotonsMedium->size()>0) ch=0;
          if(ch>0) continue;
          ntopTag=0;
          ntopTagRandom=0;
          ht=0;
          topMTR=1;
          Ts2Candidate.SetPxPyPzE(0,0,0,0);
  
          for (int l=0;l<(*JEC08sysUp)[n].size();l++){
            if((*JEC08sysUp)[n][l]->toptag_) ntopTag++;
            if((*JEC08sysUp)[n][l]->mass_>120 && (*JEC08sysUp)[n][l]->mass_<210){
              ntopTagRandom++;
              topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*JEC08sysUp)[n][l]->pt_,FatJet_msoftdrop[(*JEC08sysUp)[n][l]->indice_],"central"));
            }
          }
    
          regUp.clear();
          wgtUp.clear();
          if((*JEC08sysUp)[n].size()>1 && ntopTag>0){
            regUp.push_back(0);
            if(fname.Contains("TTG")) wgtUp.push_back(finalWeightSF);
            else  wgtUp.push_back(finalWeight);
          }
          FillD4Hists(HistsJecUp, ch, regUp, 0,          n, ((*selectedPhotons)[0]->p4_+(*JEC08sysUp)[n][0]->p4_).M(),wgtUp);
        }
    //JES Down sys
        for (int n=0;n<sysJecNames.size();++n){
          ch=999;
          if((*JEC08sysDown)[n].size()>0 && PhotonsMedium->size()>0) ch=0;
          if(ch>0) continue;
          ntopTag=0;
          ntopTagRandom=0;
          ht=0;
          topMTR=1;
          Ts2Candidate.SetPxPyPzE(0,0,0,0);
          for (int l=0;l<(*JEC08sysDown)[n].size();l++){
            if((*JEC08sysDown)[n][l]->toptag_) ntopTag++;
            if((*JEC08sysDown)[n][l]->mass_>120 && (*JEC08sysDown)[n][l]->mass_<210){
              ntopTagRandom++;
              topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*JEC08sysDown)[n][l]->pt_,FatJet_msoftdrop[(*JEC08sysDown)[n][l]->indice_],"central"));
            }
          }
    
          regUp.clear();
          wgtUp.clear();
          if((*JEC08sysDown)[n].size()>1 && ntopTag>0){
            regUp.push_back(0);
            if(fname.Contains("TTG")) wgtUp.push_back(finalWeightSF);
            else  wgtUp.push_back(finalWeight);
          }
          FillD4Hists(HistsJecDown, ch, regUp, 0,          n, ((*selectedPhotons)[0]->p4_+(*JEC08sysDown)[n][0]->p4_).M(),wgtUp);
        }
      }
//  Add data driven errors
      if (data == "data" && ifSys){
  //Wieght dependent sys
        for(int n=0;n<sysData.size();++n){
          if(ch>0) continue;
          wgtUp.clear();
          wgtDown.clear();
          for(int l=0;l<wgt.size();++l){
            wgtUp.push_back( wgt[l]*(sysUpWeightsData[n]/nominalWeightsData[n]));
            wgtDown.push_back( wgt[l]*(sysDownWeightsData[n]/nominalWeightsData[n]));
          }
    //Up
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"GammaPt"),         n, (*selectedPhotons)[0]->pt_       ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"GammaEta"),        n, (*selectedPhotons)[0]->eta_      ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"GammaPhi"),        n, (*selectedPhotons)[0]->phi_      ,wgtUp);
    //      FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtUp);
   //       FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtUp);
  //        FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"softdropMassLeadingJet08"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtUp);
          FillD4Hists(HistsSysDataUp, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtUp);
   //Down
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"GammaPt"),         n, (*selectedPhotons)[0]->pt_       ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"GammaEta"),        n, (*selectedPhotons)[0]->eta_      ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"GammaPhi"),        n, (*selectedPhotons)[0]->phi_      ,wgtDown);
    //      FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet04Pt"),         n, (*selectedJets04)[0]->pt_        ,wgtDown);
    //      FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet04Eta"),        n, (*selectedJets04)[0]->eta_       ,wgtDown);
    //      FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet04Phi"),        n, (*selectedJets04)[0]->phi_       ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"njet04"),          n, selectedJets04->size()           ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"nbjet04"),         n, nbjet04                          ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet08Pt"),         n, (*selectedJets08)[0]->pt_        ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet08Eta"),        n, (*selectedJets08)[0]->eta_        ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"jet08Phi"),        n, (*selectedJets08)[0]->phi_        ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"njet08"),          n, selectedJets08->size()           ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"Met"),             n, MET_pt                           ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"nPh"),             n, selectedPhotons->size()          ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"phoChargedIso"),   n, Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"HT"),              n, ht                               ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"HoE"),             n, Photon_hoe[(*selectedPhotons)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"softdropMassLeadingJet08"),    n, FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"TvsQCD"),          n, FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"TsMass1"),         n, ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"nTopTag"),         n, ntopTag                          ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"masstS2"),         n, Ts2Candidate.M()                 ,wgtDown);
          FillD4Hists(HistsSysDataDown, ch, reg, vInd(vars,"Sietaieta"),       n, Photon_sieie[(*selectedPhotons)[0]->indice_],wgtDown);
        }
      }
    }
    if (data == "mc" && ifSys){
//photon Scale/Smearing unc
      ntopTag=0;
      ntopTagRandom=0;
      ht=0;
      topMTR=1;
      Ts2Candidate.SetPxPyPzE(0,0,0,0);
      for (int l=0;l<selectedJets08->size();l++){
        if((*selectedJets08)[l]->toptag_) ntopTag++;
        if((*selectedJets08)[l]->mass_>120 && (*selectedJets08)[l]->mass_<210){
          ntopTagRandom++;
          topMTR = topMTR * (1-scale_factor(&h_topMistagRate,(*selectedJets08)[l]->pt_,FatJet_msoftdrop[(*selectedJets08)[l]->indice_],"central"));
        }
      }
      reg.clear();
      wgt.clear();
      if(selectedJets08->size()>0){
        reg.push_back(getVecPos(regions,"nAk8G0"));
        wgt.push_back(finalWeight);
      }
      if(selectedJets08->size()==1 && (*selectedJets08)[0]->mass_>120 && (*selectedJets08)[0]->mass_<210){
        reg.push_back(getVecPos(regions,"nAk81"));
        wgt.push_back(finalWeight);
      }
      if(selectedJets08->size()==1 && ntopTag==1){
        reg.push_back(getVecPos(regions,"nAk81nTtag1"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
      }
      if(selectedJets08->size()>1 && ntopTag>0){
        reg.push_back(getVecPos(regions,"nAk8G1nTtagG0"));
        if(fname.Contains("TTG")) wgt.push_back(finalWeightSF);
        else  wgt.push_back(finalWeight);
      }
      if(selectedJets08->size()>1 && ntopTag==0) {
        reg.push_back(getVecPos(regions,"nAk8G1nTtag0"));
        wgt.push_back(finalWeight);
        if(ch==0) ntopTag0++;
      }
      if(selectedJets08->size()>1 && ntopTag==0 && ntopTagRandom>0) {
        reg.push_back(getVecPos(regions,"nAk8G1nTtag0XtopMissTagRate"));
        wgt.push_back(finalWeight*((1-topMTR)/topMTR));
      }
      if(selectedJets08->size()==1 && ntopTag==0 && ntopTagRandom>0){
        reg.push_back(getVecPos(regions,"nAk81nTtag0XtopMissTagRate"));
        wgt.push_back(finalWeight*((1-topMTR)/topMTR));
      }

//Photon scale UP
      if(PhotonsMediumScaleUp->size()>0 && selectedJets08->size()>0){
        selectedPhotons = PhotonsMediumScaleUp;
        if(Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1){
          ch=0;
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"photonEScale"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"photonEScale"), selectedJets08->size()           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"photonEScale"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"photonEScale"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"photonEScale"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"photonEScale"), ht                               ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"photonEScale"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"photonEScale"), FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"photonEScale"), FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"photonEScale"), ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"photonEScale"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"photonEScale"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"photonEScale"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }
      }
//Photon scale Down
      if(PhotonsMediumScaleDown->size()>0){
        selectedPhotons = PhotonsMediumScaleDown;
        if(Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1){
          ch=0;
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"photonEScale"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"photonEScale"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"photonEScale"), (*selectedJets08)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"photonEScale"), selectedJets08->size()           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"photonEScale"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"photonEScale"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"photonEScale"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"photonEScale"), ht                               ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"photonEScale"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"photonEScale"), FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"photonEScale"), FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"photonEScale"), ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"photonEScale"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"photonEScale"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"photonEScale"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }
      }
//Photon smear UP
      if(PhotonsMediumSmearUp->size()>0){
        selectedPhotons = PhotonsMediumSmearUp;
        if(Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1){
          ch=0;
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"photonESmear"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"photonESmear"), selectedJets08->size()           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"photonESmear"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"photonESmear"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"photonESmear"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"photonESmear"), ht                               ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"photonESmear"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"photonESmear"), FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"photonESmear"), FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"photonESmear"), ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"photonESmear"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"photonESmear"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysUp, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"photonESmear"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }
      }
//Photon smear DOWN
      if(PhotonsMediumSmearDown->size()>0){
        selectedPhotons = PhotonsMediumSmearDown;
        if(Photon_genPartFlav[(*selectedPhotons)[0]->indice_]==1){
          ch=0;
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPt"),          getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->pt_       ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaEta"),         getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->eta_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"GammaPhi"),         getVecPos(sys,"photonESmear"), (*selectedPhotons)[0]->phi_      ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nbjet04"),          getVecPos(sys,"photonESmear"), nbjet04                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Pt"),          getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->pt_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Eta"),         getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->eta_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"jet08Phi"),         getVecPos(sys,"photonESmear"), (*selectedJets08)[0]->phi_        ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"njet08"),           getVecPos(sys,"photonESmear"), selectedJets08->size()           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Met"),              getVecPos(sys,"photonESmear"), MET_pt                           ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nPh"),              getVecPos(sys,"photonESmear"), selectedPhotons->size()          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"phoChargedIso"),    getVecPos(sys,"photonESmear"), Photon_pfRelIso03_chg[(*selectedPhotons)[0]->indice_]*Photon_pt[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HT"),               getVecPos(sys,"photonESmear"), ht                               ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"HoE"),              getVecPos(sys,"photonESmear"), Photon_hoe[(*selectedPhotons)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"softdropMassLeadingJet08"),     getVecPos(sys,"photonESmear"), FatJet_msoftdrop[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TvsQCD"),           getVecPos(sys,"photonESmear"), FatJet_particleNet_TvsQCD[(*selectedJets08)[0]->indice_],wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"TsMass1"),          getVecPos(sys,"photonESmear"), ((*selectedPhotons)[0]->p4_+(*selectedJets08)[0]->p4_).M(),wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"nTopTag"),          getVecPos(sys,"photonESmear"), ntopTag                          ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"masstS2"),          getVecPos(sys,"photonESmear"), Ts2Candidate.M()                 ,wgt);
          FillD4Hists(HistsSysDown, ch, reg, vInd(vars,"Sietaieta"),        getVecPos(sys,"photonESmear"), Photon_sieie[(*selectedPhotons)[0]->indice_],wgt);
        }
      }
    }

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
    for (int l=0;l<fakePhotonsIso->size();l++){
      delete (*fakePhotonsIso)[l];
    }
    for (int l=0;l<fakePhotonsSiSi->size();l++){
      delete (*fakePhotonsSiSi)[l];
    }
    for (int l=0;l<fakePhotonsIsoSiSi->size();l++){
      delete (*fakePhotonsIsoSiSi)[l];
    }
    for (int l=0;l<fakePhotonsOther->size();l++){
      delete (*fakePhotonsOther)[l];
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
    fakePhotonsIsoSiSi->clear();
    fakePhotonsIsoSiSi->shrink_to_fit();
    delete fakePhotonsIsoSiSi;
    fakePhotonsIso->clear();
    fakePhotonsIso->shrink_to_fit();
    delete fakePhotonsIso;
    fakePhotonsOther->clear();
    fakePhotonsOther->shrink_to_fit();
    delete fakePhotonsOther;
    fakePhotonsSiSi->clear();
    fakePhotonsSiSi->shrink_to_fit();
    delete fakePhotonsSiSi;
    cleanVec (PhotonsMediumScaleUp);
    cleanVec (PhotonsMediumScaleDown);
    cleanVec (PhotonsMediumSmearUp);
    cleanVec (PhotonsMediumSmearDown);
    cleanVec (selectedJets08JesUp);
    cleanVec (selectedJets08JesDown);

    if(data == "mc" && ifSys){
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
      delete JEC08sysUp;
      JEC08sysDown->clear();
      JEC08sysDown->shrink_to_fit();
      delete JEC08sysDown;
    }
    topIndex->clear();
    topIndex->shrink_to_fit();
    delete topIndex;
    wIndex->clear();
    wIndex->shrink_to_fit();
    delete wIndex;
    bsubIndex->clear();
    bsubIndex->shrink_to_fit();
    delete bsubIndex;
    topTagIndex->clear();
    topTagIndex->shrink_to_fit();
    delete topTagIndex;
    WTagIndex->clear();
    WTagIndex->shrink_to_fit();
    delete WTagIndex;

   }

  cout<<float(nAcceptPassTrigger*100)/float(ntr)<<"% of events pass trigger"<<endl;
  cout<<float(nAcceptPassPhoton*100)/float(ntr)<<"% of events pass trigger+pre-selection"<<endl;
  cout<<float(ntopTag0*100)/float(ntr)<<"% of events pass preselection but fail full-selection and "<<endl;
  cout<<float(nAccept*100)/float(ntr)<<"% of events pass full-selection and "<<endl;
  cout<<"------------------------------------------------------------------"<<endl;
  cout<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;
  cout<<"from "<<nAccept<<" Accepted events, "<<nAcceptLeptonicTop<<" events are from leptonic decays"<<endl;
  cout<<"from "<<ntr<<" events, "<<ntopTag0<<" events are failed because there is no top tagged jet"<<endl;
  cout<<"from "<<ntr<<" events, "<<nOL<<" events are rejected by overlap removal requierment"<<endl;
  cout<<"fraction of events with both tops Merged = "<<float(nMerged)/float(nAccept)<<endl;
  cout<<"fraction of events with one top Merged = "<<float(nSemiMerged)/float(nAccept)<<endl;
  
cout<<"Total Virtual Memory: "<<(getValue()-memoryInit)/1000.0<<" MB"<<endl;

  for (int j=0;j<categories.size();++j){
    for (int i=0;i<channels.size();++i){
      for (int k=0;k<regions.size();++k){
        for (int l=0;l<vars.size();++l){
          Hists[j][i][k][l]  ->Write("",TObject::kOverwrite);
          delete Hists[j][i][k][l];  
        }
      }
    }
  }

  for (int j=0;j<categories.size();++j){
    for (int i=0;i<channelsFA.size();++i){
      for (int k=0;k<regionsFA.size();++k){
        for (int l=0;l<varsFA.size();++l){
          HistsFA[j][i][k][l]  ->Write("",TObject::kOverwrite);
          delete HistsFA[j][i][k][l];
        }
      }
    }
  }

  for (int i=0;i<1;++i){
    for (int k=0;k<1;++k){
      for (int l=0;l<vars2d.size();++l){
        Hists2d[i][k][l]  ->Write("",TObject::kOverwrite);
      }
    }
  }


  for (int l=0;l<vars1dSignal.size();++l){
    Hists1dSignal[l]  ->Write("",TObject::kOverwrite);
  }

  for (int l=0;l<sizeHists2dSignal;++l){
    Hists2dSignal[l]  ->Write("",TObject::kOverwrite);
  }

  if (data == "mc" && ifSys){
    for (int i=0;i<channels.size();++i){
      for (int k=0;k<regions.size();++k){
        for (int l=0;l<vars.size();++l){
          if(i==0){
            for (int n=0;n<sys.size();++n){
              HistsSysUp[i][k][l][n]->Write("",TObject::kOverwrite);
              HistsSysDown[i][k][l][n]->Write("",TObject::kOverwrite);
              delete HistsSysUp[i][k][l][n];
              delete HistsSysDown[i][k][l][n];
            }
          }
        }
      }
    }

    if (fname.Contains("TTga") || fname.Contains("TTGamma")){
      file_out.mkdir("reweightingSys");
      file_out.cd("reweightingSys/");
      for (int i=0;i<1;++i){
        for (int k=0;k<1;++k){
          for (int n=0;n<nScale;++n){
            HistsSysReweightsQscale[i][k][0][n]->Write("",TObject::kOverwrite);
            delete HistsSysReweightsQscale[i][k][0][n];
          }
          for (int n=0;n<nPdf;++n){
            HistsSysReweightsPDF[i][k][0][n]->Write("",TObject::kOverwrite);
            delete HistsSysReweightsPDF[i][k][0][n];
          }
        }
      }
    }
    file_out.cd("");
    file_out.mkdir("JECSys");
    for (int i=0;i<1;++i){
      for (int k=0;k<regions.size();++k){
        if (!(std::count(JecRegions.begin(), JecRegions.end(), k))) continue;
        file_out.mkdir("JECSys/"+regions[k]);
        file_out.cd("JECSys/"+regions[k]);
        for (int l=0;l<1;++l){
          for (int n=0;n<sysJecNames.size();++n){
            HistsJecUp[i][0][l][n]->Write("",TObject::kOverwrite);
            HistsJecDown[i][0][l][n]->Write("",TObject::kOverwrite);
            delete HistsJecUp[i][0][l][n];
            delete HistsJecDown[i][0][l][n];
          }
        }
      }
    }
  }

  file_out.cd("");
  if (data == "data" && ifSys){
    for (int i=0;i<channels.size();++i){
      for (int k=0;k<regions.size();++k){
        for (int l=0;l<vars.size();++l){
          if(i==0){
            for (int n=0;n<sysData.size();++n){
              HistsSysDataUp[i][k][l][n]->Write("",TObject::kOverwrite);
              HistsSysDataDown[i][k][l][n]->Write("",TObject::kOverwrite);
              delete HistsSysDataUp[i][k][l][n];
              delete HistsSysDataDown[i][k][l][n];
            }
          }
        }
      }
    }
  }

  trigEffDen->Write("",TObject::kOverwrite);
  trigEffNum->Write("",TObject::kOverwrite);
  h_2dSieieVsChiso->Write("",TObject::kOverwrite);

  tree_out.Write() ;
  file_out.Close() ;
  Hists.clear();
  cout<<"Hists cleaned"<<endl;
  HistsSysUp.clear();
  cout<<"HistsSysUp cleaned"<<endl;
  HistsSysDown.clear();
  cout<<"HistsSysDown cleaned"<<endl;
  if(ifSys){
    HistsSysUp.clear();
    HistsSysUp.shrink_to_fit();
    cout<<"HistsSysUp cleaned"<<endl;
    HistsSysDown.clear();
    HistsSysDown.shrink_to_fit();
    cout<<"HistsSysDown cleaned"<<endl;
    HistsJecUp.clear();
    HistsJecUp.shrink_to_fit();
    cout<<"HistsJecUp cleaned"<<endl;
    HistsJecDown.clear();
    HistsJecDown.shrink_to_fit();
    cout<<"HistsJecDown cleaned"<<endl;
    HistsSysReweightsPDF.clear();
    HistsSysReweightsPDF.shrink_to_fit();
    cout<<"HistsSysReweightPDF cleaned"<<endl;
    HistsSysReweightsQscale.clear();
    HistsSysReweightsQscale.shrink_to_fit();
    cout<<"HistsSysReweightsQscale cleaned"<<endl;
    HistsSysReweightsPS.clear();
    HistsSysReweightsPS.shrink_to_fit();
    cout<<"HistsSysReweightPS cleaned"<<endl;
    HistsSysDataUp.clear();
    HistsSysDataUp.shrink_to_fit();
    cout<<"HistsSysUp cleaned"<<endl;
    HistsSysDataDown.clear();
    HistsSysDataDown.shrink_to_fit();
    cout<<"HistsSysDown cleaned"<<endl;
    cout<<"Job is finished"<<endl;
  }
  auto stop = high_resolution_clock::now();
  auto duration = duration_cast<seconds>(stop - start);
  cout<<"final Memory:"<<getValue()/1000.0<<" MB"<<endl;
  cout<<"Total Virtual Memory: "<<(getValue()-memoryInit)/1000.0<<" MB"<<endl;
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


void MyAnalysis::FillD3Hists(D4HistsContainer H3, int ca, int v1, std::vector<int> v2, int v3, float value, std::vector<float> weight){
  if (v1<10){
    for (int i = 0; i < v2.size(); ++i) {
      H3[ca][v1][v2[i]][v3]->Fill(value, weight[i]);
    }
  }
}

void MyAnalysis::FillD4Hists(D4HistsContainer H4, int v1, std::vector<int> v2, int v3, int v4, float value, std::vector<float> weight){
  for (int i = 0; i < v2.size(); ++i) {
//cout<<v1<<":"<<v2[i]<<":"<<v3<<":"<<v4<<endl;
    H4[v1][v2[i]][v3][v4]->Fill(value, weight[i]);
  }
}
