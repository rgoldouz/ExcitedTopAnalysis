#include "sumOfWeights.h"

sumOfWeights::sumOfWeights(){};

std::vector<float> sumOfWeights::LHEWeight(TString year){
  if (year == "2016") return sumOfLHEWeight_2016;
  if (year == "2017") return sumOfLHEWeight_2017;
  if (year == "2018") return sumOfLHEWeight_2018;
}

std::vector<float> sumOfWeights::GenWeight(TString year){
  if (year == "2016") return sumOfMcWeight_2016;
  if (year == "2017") return sumOfMcWeight_2017;
  if (year == "2018") return sumOfMcWeight_2018;
}



