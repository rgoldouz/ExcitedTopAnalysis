#!/bin/bash
cd /user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/2017LFVScalarUllB1
eval `scramv1 runtime -sh`
text2workspace.py  LFVScalarU_2017_llB1.txt -m 125
combineTool.py -M Impacts -d LFVScalarU_2017_llB1.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarU_2017_llB1.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=1
combineTool.py -M Impacts -d LFVScalarU_2017_llB1.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1
plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,LFVScalarU-2017-llB1
cp impacts.pdf /user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/LFVScalarU_2017_llB1_impacts.pdf
