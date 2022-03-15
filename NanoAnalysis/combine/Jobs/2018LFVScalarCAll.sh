#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/2018LFVScalarCAll
eval `scramv1 runtime -sh`
combineCards.py LFVScalarC_2018_llB1.txt LFVScalarC_2018_llBg1.txt > LFVScalarC_2018_com.txt
text2workspace.py  LFVScalarC_2018_com.txt -m 125
combineTool.py -M Impacts -d LFVScalarC_2018_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarC_2018_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarC_2018_com.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVScalarC-2018
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVScalarC_2018_com_impacts.pdf
