#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/LFVScalarCCombined_data
eval `scramv1 runtime -sh`
combineCards.py LFVScalarC_2016_llB1.txt LFVScalarC_2017_llB1.txt LFVScalarC_2018_llB1.txt LFVScalarC_2016_llBg1.txt LFVScalarC_2017_llBg1.txt LFVScalarC_2018_llBg1.txt  > LFVScalarC_Combined.txt
text2workspace.py  LFVScalarC_Combined.txt -m 125
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 --doInitialFit --robustFit 1 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 -o impacts.json --rMin -1 --rMax 1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVScalarC-FullRun2
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVScalarC_Combined_impacts_data.pdf
combine -M MaxLikelihoodFit LFVScalarC_Combined.txt
PostFitShapesFromWorkspace -o postfit_shapes.root -f fitDiagnostics.root:fit_s --postfit --sampling --print -d LFVScalarC_Combined.txt -w LFVScalarC_Combined.root
cp postfit_shapes.root /user/rgoldouz/NewAnalysis2020/Analysis/combine/PostFit/LFVScalarC_Combined.root
