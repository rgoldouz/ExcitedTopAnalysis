#include "Utils.h"
#include "sys/types.h"
#include "sys/sysinfo.h"

int parseLine(char* line){
    // This assumes that a digit will be found and the line ends in " Kb".
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}

int getValue(){ //Note: this value is in KB!
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];

    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmRSS:", 6) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}

double dR(double eta1, double phi1, double eta2, double phi2){
    double dphi = phi2 - phi1;
    double deta = eta2 - eta1;
    static const double pi = TMath::Pi();
    dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
    return TMath::Sqrt( dphi*dphi + deta*deta );
}

void displayProgress(long current, long max){
  using std::cerr;
  if (max<5000) return;
  if (current%(max/500)!=0 && current<max-1) return;

  int width = 52; // Hope the terminal is at least that wide.
  int barWidth = width - 2;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  for(int i=0 ; i<barWidth ; ++i){ if(i<barWidth*current/max){ cerr << '=' ; }else{ cerr << ' ' ; } }
  cerr << ']';
  cerr << " " << Form("%8d/%8d (%5.2f%%)", (int)current, (int)max, 100.0*current/max) ;
  cerr.flush();
}

Double_t deltaPhi(Double_t phi1, Double_t phi2) {
  Double_t dPhi = phi1 - phi2;
  if (dPhi > TMath::Pi()) dPhi -= 2.*TMath::Pi();
  if (dPhi < -TMath::Pi()) dPhi += 2.*TMath::Pi();
  return dPhi;
}


Double_t deltaR(Double_t eta1, Double_t phi1, Double_t eta2, Double_t phi2) {
  Double_t dEta, dPhi ;
  dEta = eta1 - eta2;
  dPhi = deltaPhi(phi1, phi2);
  return sqrt(dEta*dEta+dPhi*dPhi);
}

int signnum_typical(double x) {
  if (x > 0.0) return 1;
  if (x < 0.0) return -1;
  return 0;
}

bool ComparePtLep(lepton_candidate *a, lepton_candidate *b) { return a->pt_ > b->pt_; }
bool ComparePtJet(jet_candidate *a, jet_candidate *b) { return a->pt_ > b->pt_; }
bool CompareMassJet(jet_candidate *a, jet_candidate *b) { return a->mass_ > b->mass_; }
std::vector<bool> parsePhotonVIDCuts(int bitMap, int cutLevel){
    //    *         | Int_t VID compressed bitmap (MinPtCut,PhoSCEtaMultiRangeCut,PhoSingleTowerHadOverEmCut,PhoFull5x5SigmaIEtaIEtaCut,PhoAnyPFIsoWithEACut,PhoAnyPFIsoWithEAAndQuadScalingCut,PhoAnyPFIsoWithEACut), 2 bits per cut*

    bool passHoverE  = (bitMap>>4&3)  >= cutLevel;
    bool passSIEIE   = (bitMap>>6&3)  >= cutLevel;
    bool passChIso   = (bitMap>>8&3)  >= cutLevel;
    bool passNeuIso  = (bitMap>>10&3) >= cutLevel;
    bool passPhoIso  = (bitMap>>12&3) >= cutLevel;


    bool passID = passHoverE && passSIEIE && passChIso && passNeuIso && passPhoIso;

    std::vector<bool> cuts;
    cuts.push_back(passID);
    cuts.push_back(passHoverE);
    cuts.push_back(passSIEIE);
    cuts.push_back(passChIso);
    cuts.push_back(passNeuIso);
    cuts.push_back(passPhoIso);

    return cuts;

}

/*
float scale_factor( TH2F* h, float X, float Y , TString uncert){
  int NbinsX=h->GetXaxis()->GetNbins();
  int NbinsY=h->GetYaxis()->GetNbins();
  float x_min=h->GetXaxis()->GetBinLowEdge(1);
  float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  float y_min=h->GetYaxis()->GetBinLowEdge(1);
  float y_max=h->GetYaxis()->GetBinLowEdge(NbinsY)+h->GetYaxis()->GetBinWidth(NbinsY);
  TAxis *Xaxis = h->GetXaxis();
  TAxis *Yaxis = h->GetYaxis();
  Int_t binx=1;
  Int_t biny=1;
  if(x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx= (X<=x_min) ? 1 : NbinsX ;
  if(y_min < Y && Y < y_max) biny = Yaxis->FindBin(Y);
  else biny= (Y<=y_min) ? 1 : NbinsY ;
  if(uncert=="up") return (h->GetBinContent(binx, biny)+h->GetBinError(binx, biny));
  else if(uncert=="down") return (h->GetBinContent(binx, biny)-h->GetBinError(binx, biny));
  else return  h->GetBinContent(binx, biny);
}
*/

float scale_factor( TH2F* h, float X, float Y , TString uncert){
  int NbinsX=h->GetXaxis()->GetNbins();
  int NbinsY=h->GetYaxis()->GetNbins();
  float x_min=h->GetXaxis()->GetBinLowEdge(1);
  float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  float y_min=h->GetYaxis()->GetBinLowEdge(1);
  float y_max=h->GetYaxis()->GetBinLowEdge(NbinsY)+h->GetYaxis()->GetBinWidth(NbinsY);
  TAxis *Xaxis = h->GetXaxis();
  TAxis *Yaxis = h->GetYaxis();
  Int_t binx=1;
  Int_t biny=1;
  if(x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx= (X<=x_min) ? 1 : NbinsX ;
  if(y_min < Y && Y < y_max) biny = Yaxis->FindBin(Y);
  else biny= (Y<=y_min) ? 1 : NbinsY ;
  if(uncert=="up") return (h->GetBinContent(binx, biny)+h->GetBinError(binx, biny));
  if(uncert=="down") return (h->GetBinContent(binx, biny)-h->GetBinError(binx, biny));
  if(uncert=="central") return  h->GetBinContent(binx, biny);
  return 1;
}

float scale_factorIJ( TH2F* h, float X, float Y , TString uncert, int i, int j){
  int NbinsX=h->GetXaxis()->GetNbins();
  int NbinsY=h->GetYaxis()->GetNbins();
  float x_min=h->GetXaxis()->GetBinLowEdge(1);
  float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  float y_min=h->GetYaxis()->GetBinLowEdge(1);
  float y_max=h->GetYaxis()->GetBinLowEdge(NbinsY)+h->GetYaxis()->GetBinWidth(NbinsY);
  TAxis *Xaxis = h->GetXaxis();
  TAxis *Yaxis = h->GetYaxis();
  Int_t binx=1;
  Int_t biny=1;
  if(x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx= (X<=x_min) ? 1 : NbinsX ;
  if(y_min < Y && Y < y_max) biny = Yaxis->FindBin(Y);
  else biny= (Y<=y_min) ? 1 : NbinsY ;
  if(uncert=="up" && i == binx && j == biny) return (h->GetBinContent(binx, biny)+h->GetBinError(binx, biny));
  else if(uncert=="down" && i == binx && j == biny) return (h->GetBinContent(binx, biny)-h->GetBinError(binx, biny));
  else return  h->GetBinContent(binx, biny);
}

float topPt(float pt){
  return (0.973 - (0.000134 * pt) + (0.103 * exp(pt * (-0.0118))));
}

  TLorentzVector Wneutrino(double MET, double METphi, double leptonPT, double leptonEta, double leptonPhi) {
    double mW=80.4;
    double neutrinoPX=0;
    double neutrinoPY=0;
    double neutrinoPZ=0;
    TLorentzVector lepton;
    lepton.SetPtEtaPhiM(leptonPT, leptonEta, leptonPhi, 0);
    double leptonPZ=lepton.Pz();
    double mu=(std::pow(mW,2)/2)+std::cos(deltaPhi(METphi,leptonPhi))*MET*leptonPT;
    double determinant = (std::pow(mu,2)*std::pow(leptonPZ,2)/std::pow(leptonPT,4))-(std::pow(MET,2)*(std::pow(leptonPT,2)+std::pow(leptonPZ,2))-std::pow(mu,2))/std::pow(leptonPT,2);
    if (determinant<0){
      MET=(1.+std::cos(deltaPhi(METphi,leptonPhi)))*std::pow(mW,2)/(2*leptonPT*std::pow(std::sin(deltaPhi(METphi,leptonPhi)),2));
      mu=(std::pow(mW,2)/2)+std::cos(deltaPhi(METphi,leptonPhi))*MET*leptonPT;
      determinant=0.;
    }
    double neutrinoPZplus=(mu*leptonPZ/std::pow(leptonPT,2))+std::sqrt(determinant);
    double neutrinoPZminus=(mu*leptonPZ/std::pow(leptonPT,2))-std::sqrt(determinant);
    neutrinoPZ=neutrinoPZminus;
    if(std::fabs(neutrinoPZplus)<std::fabs(neutrinoPZminus)){
      neutrinoPZ=neutrinoPZplus;
    }
    neutrinoPX=MET*std::cos(METphi);
    neutrinoPY=MET*std::sin(METphi);
    TLorentzVector neutrino;
    neutrino.SetPxPyPzE(neutrinoPX,neutrinoPY,neutrinoPZ,std::sqrt(std::pow(neutrinoPX,2)+std::pow(neutrinoPY,2)+std::pow(neutrinoPZ,2)));
    return  neutrino;
  }

float rate(TH1F* h, float X){
  int NbinsX=h->GetXaxis()->GetNbins();
  float x_min=h->GetXaxis()->GetBinLowEdge(1);
  float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  TAxis *Xaxis = h->GetXaxis();
  Int_t binx=1;
  if(x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx= (X<=x_min) ? 1 : NbinsX ;
  return  h->GetBinContent(binx);
}

float rateErr(TH1F* h, float X, TString uncert){
  int NbinsX=h->GetXaxis()->GetNbins();
  float x_min=h->GetXaxis()->GetBinLowEdge(1);
  float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
  TAxis *Xaxis = h->GetXaxis();
  Int_t binx=1;
  if(x_min < X && X < x_max) binx = Xaxis->FindBin(X);
  else binx= (X<=x_min) ? 1 : NbinsX ;

  if(uncert=="up") return (h->GetBinContent(binx)+h->GetBinError(binx));
  else if(uncert=="down") return (h->GetBinContent(binx)-h->GetBinError(binx));
  else cout<<"error in input of the rateErr function"<<endl; 
  return 0;
}

double TransverseMass(TLorentzVector A, TLorentzVector B, double mA, double mB) {
  double mt = sqrt(2 * A.Pt()*B.Pt()*(1 - cos(A.DeltaPhi(B))));
  //cout << "mt: " << mt << endl;
  return mt;
}
