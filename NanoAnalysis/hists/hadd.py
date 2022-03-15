import sys
import os
import subprocess
import readline
import string
import glob

sys.path.append('/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/analysis/bin')
import Files_2017_new
SAMPLES = {}
mc_2017 = True
data_2017 = True

if mc_2017:
    SAMPLES.update(Files_2017_new.mc2017_samples)
if data_2017:
    SAMPLES.update(Files_2017_new.data2017_samples)


addedFilesData = {"2016": [], "2017": [], "2018": []} 
addedFilesMcQCDHT = {"2016": [], "2017": [], "2018": []}
addedFilesMcGJets = {"2016": [], "2017": [], "2018": []}
addedFilesMcWG = {"2016": [], "2017": [], "2018": []}
addedFilesMcDY = {"2016": [], "2017": [], "2018": []}
addedFilesMctop = {"2016": [], "2017": [], "2018": []}

os.system('rm *.root')
dist = "/hadoop/store/user/rgoldouz/FullProduction/ETOPAnalysis/Analysis_" 

for key, value in SAMPLES.items():
    year = value[3]
    hadd='hadd ' + key + '.root '
    for filename in os.listdir(dist + key):
        hadd += dist + key + '/' + filename + ' '
    os.system(hadd)
    if value[1]=='data':
        addedFilesData[year].append(key + '.root')
    elif 'QCDHT' in key:
        addedFilesMcQCDHT[year].append( key + '.root')
    elif 'GJets' in key:
        addedFilesMcGJets[year].append(key + '.root')
    elif 'WG' in key:
        addedFilesMcWG[year].append( key + '.root')
    elif 'DY' in key:
        addedFilesMcDY[year].append( key + '.root')
    elif ('tt' in key or 'ST' in key or 'TT' in key):
        addedFilesMctop[year].append(key + '.root')




#    print glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')
#    year = value[3]
#    if value[1]=='data':
#        addedFilesData[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'QCDHT' in key:
#        addedFilesMcQCDHT[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'GJets' in key:
#        addedFilesMcGJets[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'WG' in key:
#        addedFilesMcWG[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'DY' in key:
#        addedFilesMcDY[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif ('tt' in key or 'ST' in key):
#        addedFilesMctop[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    else:
#        os.system('cp ' + glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0] + ' ' + key + '.root')


hadddata_2017 ='hadd 2017_data' + '.root ' + ' '.join(addedFilesData['2017'])
os.system(hadddata_2017)

haddmc_2017_McQCDHT ='hadd 2017_QCD' + '.root ' + ' '.join(addedFilesMcQCDHT['2017'])
haddmc_2017_McGJets ='hadd 2017_GJets' + '.root ' + ' '.join(addedFilesMcGJets['2017'])
haddmc_2017_McWG ='hadd 2017_WG' + '.root ' + ' '.join(addedFilesMcWG['2017'])
haddmc_2017_McDY ='hadd 2017_DY' + '.root ' + ' '.join(addedFilesMcDY['2017'])
haddmc_2017_Mctop ='hadd 2017_top' + '.root ' + ' '.join(addedFilesMctop['2017'])

os.system(haddmc_2017_McQCDHT)
os.system(haddmc_2017_McGJets)
os.system(haddmc_2017_McWG)
os.system(haddmc_2017_McDY)
os.system(haddmc_2017_Mctop)

