import sys
import os
import subprocess
import readline
import string

dire = '/user/rgoldouz/NewAnalysis2020/Analysis/combine/CombinedFiles/'
cms = '/user/rgoldouz/NewAnalysis2020/Limit/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit/test/'

#year=['2016','2017','2018']
year=['2017']
regions=["llB1", "llBg1"]
SignalSamples = ['LFVVecC', 'LFVVecU', 'LFVScalarC', 'LFVScalarU', 'LFVTensorC', 'LFVTensorU']
#SignalSamples = ['LFVVecU']
for namesig in SignalSamples:
    print namesig
    SHNAME0 = namesig + "Combined" +'.sh'
    os.system("rm STDOUT/" + SHNAME0.split('.')[0] + ".stdout")
    os.system("qsub -q localgrid  -o STDOUT/" + SHNAME0.split('.')[0] + ".stdout -e STDERR/" + SHNAME0.split('.')[0] + ".stderr Jobs/" + SHNAME0)
    for numyear, nameyear in enumerate(year):
        SHNAME1 = nameyear + namesig + "llB1" +'.sh'
        os.system("rm STDOUT/" + SHNAME1.split('.')[0] + ".stdout") 
        os.system("qsub -q localgrid  -o STDOUT/" + SHNAME1.split('.')[0] + ".stdout -e STDERR/" + SHNAME1.split('.')[0] + ".stderr Jobs/" + SHNAME1)

        SHNAME2 = nameyear + namesig + "All" +'.sh'
        os.system("rm STDOUT/" + SHNAME2.split('.')[0] + ".stdout")
        os.system("qsub -q localgrid  -o STDOUT/" + SHNAME2.split('.')[0] + ".stdout -e STDERR/" + SHNAME2.split('.')[0] + ".stderr Jobs/" + SHNAME2)
