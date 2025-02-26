import subprocess
import sys
import os

val = sys.argv[1:5]
print val
Y = val[1].split('_')
R = val[3].split('_')

AllReg={
"nAk81nTtag1":'CR1',
"nAk8G1nTtagG0":'SR',
"nAk81nTtagOffMt":'CR2'
}

regions=''
if len(R)==1:
    regions=AllReg[R[0]]
if len(R)==2:
    regions=AllReg[R[0]]+'+'+AllReg[R[1]]
if len(R)==3:
    regions=AllReg[R[0]]+'+'+AllReg[R[1]]+'+'+AllReg[R[2]]


sig='S12'+val[0].split('_')[1]
if '32' in val[0]:
    sig='S32'+val[0].split('_')[1]
cardNameB1=''
for year in Y:
    for reg in R:
        cardNameB1 += val[0] +'_'+year+'_' + reg +'.txt ' 
print cardNameB1

print 'combineCards.py ' + cardNameB1 + ' > ' +val[0] +'_'+val[1]+ '_'+val[3]+'_com.txt'
print 'combine -M  AsymptoticLimits '         +val[0] +'_'+val[1]+ '_'+val[3]+ '_com.txt -m ' + val[2] + ' > ' + val[0] +'_'+val[1]+ '_'+val[3]+'_results.tex' 

print 'text2workspace.py  '                   +val[0] +'_'+val[1]+ '_'+val[3] + '_com.txt -m 125'
print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1'
print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=1'
print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1'
print 'plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig +'_'+regions+'_RunII'

print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3'
print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3'
print 'combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3'
print 'plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig +'_'+regions+'_RunII'


os.system('cp CombinedFilesETop/* .')
os.system('combineCards.py ' + cardNameB1 + ' > ' +val[0] +'_'+val[1]+ '_'+val[3]+'_com.txt')
os.system('combine -M  AsymptoticLimits '         +val[0] +'_'+val[1]+ '_'+val[3]+ '_com.txt -m ' + val[2] + ' > ' + val[0] +'_'+val[1]+ '_'+val[3]+'_results.tex' )

os.system('text2workspace.py  '                   +val[0] +'_'+val[1]+ '_'+val[3] + '_com.txt -m 125')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=1')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1')
if len(Y)==1:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig+'_'+val[1]+ '_'+regions)
else:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig +'_'+regions+'_RunII')
os.system('cp impacts.pdf ' + val[0] +'_'+val[1]+ '_'+val[3]+'_Expected_mu1_impacts.pdf')

os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+ '_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3')
if len(Y)==1:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig+'_'+val[1]+ '_'+regions)
else:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03  --cms-label ,' + sig +'_'+regions+'_RunII')
os.system('cp impacts.pdf ' + val[0] +'_'+val[1]+ '_'+val[3]+'_Observed_mu1_impacts.pdf')

#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=0')
#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 -t -1 --expectSignal=0 --parallel 8')
#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=0')
#if len(Y)==1:
#    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + sig+'_'+val[1]+ '_'+regions)
#else:
#    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + sig +'_'+regions+'_RunII')
#os.system('mv impacts.pdf ' + val[0] +'_'+val[1]+'_'+val[3] + '_Expected_mu0_impacts.pdf')
#
#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 --expectSignal=0')
#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 --robustFit 1 --doFits --parallel 8 --rMin -3 --rMax 3 --expectSignal=0 --parallel 8')
#os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[3] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3  --expectSignal=0')
#if len(Y)==1:
#    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + sig+'_'+val[1]+ '_'+regions)
#else:
#    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + sig +'_'+regions+'_RunII')
#os.system('mv impacts.pdf ' + val[0] +'_'+val[1]+'_'+val[3] + '_Observed_mu0_impacts.pdf')
