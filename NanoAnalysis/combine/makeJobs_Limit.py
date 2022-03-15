import sys
import os
import subprocess
import readline
import string

dire = '/user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/'
cms = '/user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/'
Limits = ['','--expectedFromGrid=0.025','--expectedFromGrid=0.16','--expectedFromGrid=0.5','--expectedFromGrid=0.84','--expectedFromGrid=0.975']

year=['2016','2017','2018']
regions=["llB1", "llBg1"]
SignalSamples = ['LFVVecC', 'LFVVecU', 'LFVScalarC', 'LFVScalarU', 'LFVTensorC', 'LFVTensorU']
#SignalSamples = []
#SignalSamples = ['LFVVecU']
os.system('rm -rf ' + cms  + "Combined_Limit")
os.system('mkdir ' + cms + "Combined_Limit")
os.system('cp CombinedFiles/* ' + cms + "Combined_Limit")
for quantile in Limits:
    for namesig in SignalSamples:
        print namesig
        SHNAME0 = quantile + namesig + "Combined_Limit" +'.sh'
        SHFILE0="#!/bin/bash\n" +\
        "cd "+ cms + "Combined_Limit" + "\n"+\
        "eval `scramv1 runtime -sh`\n"+\
        'combineCards.py ' + namesig + '_2016_llB1.txt ' + namesig + '_2017_llB1.txt '+ namesig + '_2018_llB1.txt '+  namesig + '_2016_llBg1.txt ' + namesig + '_2017_llBg1.txt ' + namesig + '_2018_llBg1.txt ' + ' > ' + namesig +'_' + 'Combined.txt'+ "\n"+\
        'text2workspace.py  ' + namesig + '_Combined.txt -m 125'+ "\n"+\
        'combine -M HybridNew --LHCmode LHC-limits '+ namesig + '_Combined.root ' + quantile + ' > ' + quantile + '_' + namesig +'_' + 'Combined_result.txt' +"\n"
        open('Jobs/'+SHNAME0, 'wt').write(SHFILE0)
        os.system("chmod +x "+'Jobs/'+SHNAME0)
        os.system("qsub -q localgrid  -o STDOUT/" + SHNAME0.split('.')[0] + ".stdout -e STDERR/" + SHNAME0.split('.')[0] + ".stderr Jobs/" + SHNAME0)
#        for numyear, nameyear in enumerate(year):
#            SHNAME1 = nameyear + namesig + "llB1_Limit" +'.sh'
#            SHFILE1="#!/bin/bash\n" +\
#            "cd "+ cms + nameyear + namesig + "llB1_data" + "\n"+\
#            "eval `scramv1 runtime -sh`\n"+\
#            'text2workspace.py  ' + namesig + '_' + nameyear + '_llB1.txt -m 125'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_llB1.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_llB1.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_llB1.root -m 125 -o impacts.json --rMin -3 --rMax 3'+ "\n"+\
#            'plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + namesig +'-'+ nameyear + '-llB1'+ "\n" +\
#            'cp impacts.pdf ' + dire + namesig + '_' + nameyear + '_llB1_impacts_data.pdf'+ "\n"
#            open('Jobs/'+SHNAME1, 'wt').write(SHFILE1)
#            os.system("chmod +x "+'Jobs/'+SHNAME1)
#    #        os.system("qsub -q localgrid  -o STDOUT/" + SHNAME1.split('.')[0] + ".stdout -e STDERR/" + SHNAME1.split('.')[0] + ".stderr Jobs/" + SHNAME1)
#    
#            SHNAME2 = nameyear + namesig + "All_data" +'.sh'
#            SHFILE2="#!/bin/bash\n" +\
#            "cd "+ cms + nameyear + namesig + "All_data" + "\n"+\
#            "eval `scramv1 runtime -sh`\n"+\
#            'combineCards.py ' + namesig + '_' + nameyear + '_llB1.txt ' +namesig + '_' + nameyear + '_llBg1.txt' + ' > ' + namesig +'_'+nameyear+'_' + 'com.txt'+ "\n"+\
#            'text2workspace.py  ' + namesig + '_' + nameyear + '_com.txt -m 125'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3'+ "\n"+\
#            'combineTool.py -M Impacts -d ' +namesig + '_' + nameyear + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3'+ "\n"+\
#            'plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + namesig + '-' + nameyear + "\n" +\
#            'cp impacts.pdf ' + dire + namesig + '_' + nameyear + '_com_impacts_data.pdf'+ "\n"
#            open('Jobs/'+SHNAME2, 'wt').write(SHFILE2)
#            os.system("chmod +x "+'Jobs/'+SHNAME2)
#    #        os.system("qsub -q localgrid  -o STDOUT/" + SHNAME2.split('.')[0] + ".stdout -e STDERR/" + SHNAME2.split('.')[0] + ".stderr Jobs/" + SHNAME2)
