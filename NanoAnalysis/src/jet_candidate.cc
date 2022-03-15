#include "jet_candidate.h"

jet_candidate::jet_candidate(float pt_in, float eta_in, float phi_in, float E_in, float btag_in, TString year, int flavor_in, int ind_in, int NtopObj_in, int Nsub_in, int Nbsub_in, float mass_in, float toptag_in, float Wtag_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  btag_ = isb(btag_in,year);
  toptag_ = istop(toptag_in,year, mass_in);
  Wtag_ = isW(Wtag_in,year);
  p4_.SetPtEtaPhiM(pt_, eta_, phi_, E_in) ;
  flavor_ = flavor_in;
  indice_ = ind_in;
  NtopObj_ = NtopObj_in;
  Nsub_ = Nsub_in;
  Nbsub_ = Nbsub_in;
  mass_ = mass_in;
}


int jet_candidate::isb(float btag_in , TString year){
  int R = 0;
  if (year == "2016" && btag_in > 0.6321) R=1;
  if (year == "2017" && btag_in > 0.4941) R=1;
  if (year == "2018" && btag_in > 0.4184) R=1;
  return R;
}
 
int jet_candidate::istop(float toptag_in , TString year, float mSD){
  int R = 0;
  if (year == "2016" && toptag_in > 0.863 && mSD>105 && mSD<210) R=1;
  if (year == "2017" && toptag_in > 0.863 && mSD>105 && mSD<210) R=1;
  if (year == "2018" && toptag_in > 0.863 && mSD>105 && mSD<210) R=1;
  return R;
}
 
int jet_candidate::isW(float Wtag_in , TString year){
  int R = 0;
  if (year == "2016" && Wtag_in > 0.918) R=1;
  if (year == "2017" && Wtag_in > 0.475) R=1;
  if (year == "2018" && Wtag_in > 0.918) R=1;
  return R;
}

jet_candidate::~jet_candidate(){}


