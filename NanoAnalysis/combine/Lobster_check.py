import subprocess
import sys
import os

val = sys.argv[1:4]
print val
Y = val[2].split('_')
cardNameB1=''
for year in Y:
    cardNameB1 += val[0] +'_'+val[1]+'_ee_'+year+'_' + 'llB1.txt ' + val[0] +'_'+val[1]+'_emu_'+year+'_' + 'llB1.txt '+ val[0] +'_'+val[1]+'_mumu_'+year+'_' + 'llB1.txt '
print cardNameB1
os.system('cp CombinedFilesBNV/* .')
os.system('combineCards.py ' + cardNameB1 + ' > ' +val[0] +'_'+val[1]+'_'+val[2]  + '_com.txt')
os.system('combine --run blind -M  AsymptoticLimits '         +val[0] +'_'+val[1]+'_'+val[2]  + '_com.txt > ' + val[0] +'_'+val[1]+'_'+val[2] +'_results.tex' )
os.system('text2workspace.py  '                   +val[0] +'_'+val[1]+'_'+val[2] + '_com.txt -m 125')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[2] + '_com.root -m 125 --doInitialFit --robustFit 1 --rMin -3 --rMax 3 -t -1 --expectSignal=1')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[2] + '_com.root -m 125 --robustFit 1 --doFits --parallel 4 --rMin -3 --rMax 3 -t -1 --expectSignal=1')
os.system('combineTool.py -M Impacts -d '         +val[0] +'_'+val[1]+'_'+val[2] + '_com.root -m 125 -o impacts.json --rMin -3 --rMax 3 -t -1 --expectSignal=1')
if len(Y)==1:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + val[0] +'_'+val[1]+'_'+val[2])
else:
    os.system('plotImpacts.py -i impacts.json -o impacts --max-pages 1 --label-size 0.03 --cms-label ,' + val[0] +'_'+val[1]+'_AllYearsCombined')
os.system('cp impacts.pdf ' + val[0] +'_'+val[1]+'_'+val[2] + '_impacts.pdf')

