#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/LFVTensorUCombined_data
eval `scramv1 runtime -sh`
combineCards.py LFVTensorU_2016_llB1.txt LFVTensorU_2017_llB1.txt LFVTensorU_2018_llB1.txt LFVTensorU_2016_llBg1.txt LFVTensorU_2017_llBg1.txt LFVTensorU_2018_llBg1.txt  > LFVTensorU_Combined.txt
text2workspace.py  LFVTensorU_Combined.txt -m 125
combineTool.py -M Impacts -d LFVTensorU_Combined.root -m 125 --doInitialFit --robustFit 1 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVTensorU_Combined.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVTensorU_Combined.root -m 125 -o impacts.json --rMin -1 --rMax 1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVTensorU-FullRun2
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVTensorU_Combined_impacts_data.pdf
combine -M MaxLikelihoodFit LFVTensorU_Combined.txt
PostFitShapesFromWorkspace -o postfit_shapes.root -f fitDiagnostics.root:fit_s --postfit --sampling --print -d LFVTensorU_Combined.txt -w LFVTensorU_Combined.root
cp postfit_shapes.root /user/rgoldouz/NewAnalysis2020/Analysis/combine/PostFit/LFVTensorU_Combined.root
