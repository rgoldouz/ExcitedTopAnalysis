import datetime
import os
from os import path
import sys

year=['2016preVFP', '2016postVFP', '2017','2018']
#year=['2017','2018']
#year=['2017']
top = 'T'
lep = ['E','Mu']
UP=['U','C']
DOWN=['D','S','B']
Couplings = ['cS','cT']
SignalSamples=[]
for l in lep:
    for u in UP:
        for d in DOWN:
            SignalSamples.append(top+d+u+l)

for coup in Couplings:
    for namesig in SignalSamples:
        All = ''
        for numyear, nameyear in enumerate(year):
            command='python Lobster_check.py '  + coup +' ' + namesig +' ' +nameyear
#            os.system(command)
            All += nameyear + '_'
        command='python Lobster_check.py '  + coup +' ' + namesig +' ' +All[:-1]
        os.system(command)

