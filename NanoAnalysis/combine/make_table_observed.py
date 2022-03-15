import gc
import sys
import ROOT
import numpy as np
import copy
import os
from array import array
import gc
import math

year=['2016preVFP', '2016postVFP', '2017','2018', '2016preVFP_2016postVFP_2017_2018']
yearLatex=['2016preVFP', '2016postVFP', '2017','2018', 'All years combined']
quark = ['DU','DC','SU','SC','BU','BC']
quarkLatex = [ 'du', 'dc', 'su', 'sc', 'bu', 'bc']
intType=['E','Mu']
intTypeLatex = ['e', '\mu']
theoryXS =[[32.53,16.81,11.32],[2.79,1.41,.98],[8.19,4.07,2.8],[0.77,0.36,0.26],[3.24,1.6,1.11],[0.28,0.14,0.10]]
BR = 1.21*4
Couplings = ['cS','cT']
CouplingsLatex = ['C_s','C_t']

le = '\\documentclass{article}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

print le
Obs=0.777
mu=0.777
muM2=0.777
muM1=0.777
muP1=0.777
muP2=0.777

for numyear, nameyear in enumerate(year):
    table = '\\begin{table}[!htb]' + "\n"
    table += '\\centering' + "\n"
    table += '\\caption{Expected/Observed upper limits on the signal cross sections (production + decay), effective BNV couplings, and top BNV branching ratios are shown for ' +  yearLatex[numyear] + '.} \n'
    #For expected limits [$-1\sigma , +1\sigma$] and ($-2\sigma , +2\sigma$) ranges are shown.}\n'
    table += '\\label{R' + nameyear + '} \n'
    table += '\\resizebox{\\textwidth}{!}{ \n'
    table += '\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}' + "\n"
    table += '\\hline' + "\n"
    table += 'Year & operator  &$\mu$ & $\mu$  & $C_y^x$ & $C_y^x$  & $BR_y^x \\times 10^{-6}$ & $BR_y^x \\times 10^{-6}$ '
    table += '\\\\' + "\n"
    table += '     &         &Exp.               &Obs.&Exp.               &Obs.&Exp.               &Obs.'
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    for numquark, namequark in enumerate(quark):
        for numintType, nameintType in enumerate(intType):
            for numcoup, coup in enumerate(Couplings):
                for fname in os.listdir('/hadoop/store/user/rgoldouz/FullProduction/TOPBNVLimits/' + coup +'_T'+ namequark + nameintType+'_'+nameyear):
                    if 'impact' in fname:
                        os.system('cp /hadoop/store/user/rgoldouz/FullProduction/TOPBNVLimits/' + coup +'_T'+ namequark + nameintType+'_'+nameyear+'/'+fname + ' ./'+ coup +'_T'+ namequark + nameintType+'_'+nameyear+'_impacts.pdf')
                    if 'results' not in fname:
                        continue 
                    file1 = open('/hadoop/store/user/rgoldouz/FullProduction/TOPBNVLimits/' + coup +'_T'+ namequark + nameintType+'_'+nameyear+'/'+fname, 'r') 
                    Lines = file1.readlines()
                    Obs= 0.0
                    mu=  0.0
                    muM2=0.0
                    muM1=0.0
                    muP1=0.0
                    muP2=0.0 
                    for line in Lines: 
                        if 'Observed Limit' in line:
                            Obs = float(line.split()[-1])/10.0
                        if 'Expected 50.0' in line:
                            mu = float(line.split()[-1])/10.0
                        if 'Expected  2.5' in line:
                            muM2 = float(line.split()[-1])/10.0
                        if 'Expected 16.0' in line:
                            muM1 = float(line.split()[-1])/10.0
                        if 'Expected 84.0' in line:
                            muP1 = float(line.split()[-1])/10.0
                        if 'Expected 97.5' in line:
                            muP2 = float(line.split()[-1])/10.0
                    table += yearLatex[numyear] + ' & $' + CouplingsLatex[numcoup] + '^{t' + quarkLatex[numquark] + intTypeLatex[numintType] + '}$ & ' + '{:.3}'.format(mu) + ' & ' + '{:.3}'.format(0.00) + ' & ' +  '{:.3}'.format(math.sqrt(mu)) + ' & ' + '{:.3}'.format(0.00) + ' & ' + '{:.3}'.format(BR*mu)+ ' & ' + '{:.3}'.format(0.0) +  '     '
                    table += '\\\\    ' + "\n"
            table += '\hline' + "\n"
    table += '\\hline' + "\n"
    table += '\\end{tabular}}' + "\n"
    table += '\\end{table}' + "\n"
#            table += '     &       & ' + '{:.3}'.format(mu) + ' & ' + '{:.3}'.format(Obs) + ' & ' +  '{:.3}'.format(math.sqrt(mu*(theoryXS[numquark][0]/sum(theoryXS[numquark])))) + ', ' + '{:.3}'.format(math.sqrt(mu*(theoryXS[numquark][2]/sum(theoryXS[numquark])))) + ' & ' + '{:.3}'.format(0.00) + ' & ' + '{:.3}'.format(mu*(theoryXS[numquark][0]/sum(theoryXS[numquark])*BR)+ ', ' +'{:.3}'.format(mu*(theoryXS[numquark][2]/sum(theoryXS[numquark])*BR) + ' & ' + '{:.3}'.format(Obs*BR[numintType]) +  '     '
#            table += '     &       & [' + '{:.3}'.format(muM1*theoryXS[numintType][numquark]) + ',' + '{:.3}'.format(muP1*theoryXS[numintType][numquark])+ '] & & [' + '{:.3}'.format(math.sqrt(muM1)) + ',' + '{:.3}'.format(math.sqrt(muP1)) + '] & & [' + '{:.3}'.format(muM1*BR[numintType]) + ',' + '{:.3}'.format(muP1*BR[numintType]) + ']&'
#            table += '\\\\    ' + "\n"
#            table += '     &     & (' + '{:.3}'.format(muM2*theoryXS[numintType][numquark]) + ',' + '{:.3}'.format(muP2*theoryXS[numintType][numquark])+ ') & & (' + '{:.3}'.format(math.sqrt(muM2)) + ',' + '{:.3}'.format(math.sqrt(muP2)) + ') & & (' + '{:.3}'.format(muM2*BR[numintType]) + ',' + '{:.3}'.format(muP2*BR[numintType]) + ')&'          
#            table += '\\\\    '  
#            table += '\\hline' + "\n"
    print table

#table = '\\begin{table}[!htb]' + "\n"
#table += '\\centering' + "\n"
#table += '\\caption{Expected/Observed upper limits on the signal cross sections (production + decay), effective LFV couplings, and top LFV branching ratios are shown for all three years combined. For expected limits [$-1\sigma , +1\sigma$] and ($-2\sigma , +2\sigma$) ranges are shown.}\n'
#table += '\\label{Rfull} \n'
#table += '\\resizebox{\\textwidth}{!}{ \n'
#table += '\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}' + "\n"
#table += '\\hline' + "\n"
#table += 'Year & quark & type &$\sigma$ [fb] & $\sigma$ [fb] & $C_x$ & $C_x$ & BR$\\times$10$^{-6}$ & BR$\\times$10$^{-6}$ '
#table += '\\\\' + "\n"
#table += '     &       &      &Exp.               &Obs.&Exp.               &Obs.&Exp.               &Obs.'
#table += '\\\\' + "\n"
#table += '\\hline' + "\n"

#for numyear, nameyear in enumerate(FullRun2):
#    for numquark, namequark in enumerate(quark):
#        for numintType, nameintType in enumerate(intType):
#            file1 = open('LFV' +nameintType+namequark +'_'+nameyear+'_results.tex', 'r')
#            Lines = file1.readlines()
#            for line in Lines:
#                if 'Observed Limit' in line:
#                    Obs = float(line.split()[-1])
#                if 'Expected 50.0' in line:
#                    mu = float(line.split()[-1])
#                if 'Expected  2.5' in line:
#                    muM2 = float(line.split()[-1])
#                if 'Expected 16.0' in line:
#                    muM1 = float(line.split()[-1])
#                if 'Expected 84.0' in line:
#                    muP1 = float(line.split()[-1])
#                if 'Expected 97.5' in line:
#                    muP2 = float(line.split()[-1])
#            table += nameyear + ' & ' + namequark + ' & ' + nameintType + ' & ' + '{:.3}'.format(mu*theoryXS[numintType][numquark]) + ' & ' + '{:.3}'.format(Obs*theoryXS[numintType][numquark]) + ' & ' +  '{:.3}'.format(math.sqrt(mu)) + ' & ' + '{:.3}'.format(math.sqrt(Obs)) + ' & ' + '{:.3}'.format(mu*BR[numintType]) + ' & ' + '{:.3}'.format(Obs*BR[numintType]) +  '     '
#            table += '\\\\    ' + "\n"
#            table += '     &       &      & [' + '{:.3}'.format(muM1*theoryXS[numintType][numquark]) + ',' + '{:.3}'.format(muP1*theoryXS[numintType][numquark])+ '] & & [' + '{:.3}'.format(math.sqrt(muM1)) + ',' + '{:.3}'.format(math.sqrt(muP1)) + '] & & [' + '{:.3}'.format(muM1*BR[numintType]) + ',' + '{:.3}'.format(muP1*BR[numintType]) + ']&'
#            table += '\\\\    ' + "\n"
#            table += '     &       &      & (' + '{:.3}'.format(muM2*theoryXS[numintType][numquark]) + ',' + '{:.3}'.format(muP2*theoryXS[numintType][numquark])+ ') & & (' + '{:.3}'.format(math.sqrt(muM2)) + ',' + '{:.3}'.format(math.sqrt(muP2)) + ') & & (' + '{:.3}'.format(muM2*BR[numintType]) + ',' + '{:.3}'.format(muP2*BR[numintType]) + ')&'
#            table += '\\\\    '
#            table += '\\hline' + "\n"
#    table += '\\hline' + "\n"
#table += '\\end{tabular}}' + "\n"
#table += '\\end{table}' + "\n"

#print table

print '\\end{document}' + "\n" 

