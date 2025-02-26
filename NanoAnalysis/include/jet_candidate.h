#ifndef MY_jet_candidate
#define MY_jet_candidate

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>
#include "TString.h"

using namespace std;
//using namespace math;
class jet_candidate {
  
public:
  jet_candidate(float, float, float, float, float, TString, int ,int,int,int,int,float,float,float);
  ~jet_candidate();
  float pt_;
  float eta_;
  float phi_;
  int flavor_;
  int indice_;
  int btag_;
  int toptag_;
  int Wtag_;
  int NtopObj_;
  int Nsub_;
  int Nbsub_;
  int isb(float, TString);
  int istop(float, TString, float);
  int isW(float, TString);
  TLorentzVector p4_;
  float mass_;


private:
  
};

#endif

