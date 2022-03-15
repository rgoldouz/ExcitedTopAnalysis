#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/2016LFVScalarCAll_data
eval `scramv1 runtime -sh`
combineCards.py LFVScalarC_2016_llB1.txt LFVScalarC_2016_llBg1.txt > LFVScalarC_2016_com.txt
text2workspace.py  LFVScalarC_2016_com.txt -m 125
combineTool.py -M Impacts -d LFVScalarC_2016_com.root -m 125 --doInitialFit --robustFit 1 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVScalarC_2016_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -1 --rMax 1
combineTool.py -M Impacts -d LFVScalarC_2016_com.root -m 125 -o impacts.json --rMin -1 --rMax 1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVScalarC-2016
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVScalarC_2016_com_impacts_data.pdf
