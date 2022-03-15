#ifndef OVERLAP_H
#define OVERLAP_H

#include<iostream>
#include<cstdlib>
#include <math.h>
#include <algorithm>
#include <tuple>
#include <TROOT.h>
#include "Utils.h"
#include "MyAnalysis.h"
#include<vector>
using namespace std;

class OverlapRemove: public MyAnalysis {
   public:
     std::vector<double> minGenDr(int myInd, std::vector<int> ignorePID = std::vector<int>());
     
     bool overlapRemoval(double Et_cut, double Eta_cut, double dR_cut, bool verbose);
     bool overlapRemoval_2To3(double Et_cut, double Eta_cut, double dR_cut, bool verbose);
     bool overlapRemovalTT(bool verbose);
     bool overlapRemovalZJets(bool verbose=false);
     bool overlapRemovalWJets(bool verbose=false);
     bool overlapRemoval_Tchannel();
};
#endif
