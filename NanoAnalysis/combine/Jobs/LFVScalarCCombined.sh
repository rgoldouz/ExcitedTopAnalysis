#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/LFVScalarCCombined
eval `scramv1 runtime -sh`
combineCards.py LFVScalarC_2016_llB1.txt LFVScalarC_2017_llB1.txt LFVScalarC_2018_llB1.txt LFVScalarC_2016_llBg1.txt LFVScalarC_2017_llBg1.txt LFVScalarC_2018_llBg1.txt  > LFVScalarC_Combined.txt
text2workspace.py  LFVScalarC_Combined.txt -m 125
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarC_Combined.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVScalarC-FullRun2
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVScalarC_Combined_impacts.pdf
