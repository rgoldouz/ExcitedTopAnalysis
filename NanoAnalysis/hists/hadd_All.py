import sys
import os
import subprocess
import readline
import string
import glob
from joblib import Parallel, delayed
sys.path.append('/afs/crc.nd.edu/user/r/rgoldouz/ExcitedTopAnalysis/NanoAnalysis/bin/')
import Files_ULall_nano

def f(name):
    os.system(name)

if __name__ == '__main__':
    Fhadd=[]
    SAMPLES = {}
    SAMPLES.update(Files_ULall_nano.UL17)
    
    
    addedFilesData = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []} 
    addedFilesMcGjets = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcFake = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcttG = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcmisIDele = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    
    os.system('rm *.root')
    dist = "/cms/cephfs/data/store/user/rgoldouz/FullProduction/AnalysisExcitedTop/Analysis_" 
    
    for keyUL, value in SAMPLES.items():
        key1 = keyUL.replace("UL", "20")
        key = key1.replace("slim","2017")
        hadd='hadd ' + key + '.root '
        for filename in os.listdir(dist + keyUL):
            hadd += dist + keyUL + '/' + filename + ' '
        Fhadd.append(hadd)
    Parallel(n_jobs=40)(delayed(f)(i) for i in Fhadd)
    #    os.system(hadd)
    for keyUL, value in SAMPLES.items():
        key1 = keyUL.replace("UL", "20")
        key = key1.replace("slim","2017")
        year = value[3]
        if value[1]=='data':
            addedFilesData[year].append(key + '.root')
        elif 'GJets' in key:
            addedFilesMcGjets[year].append( key + '.root')
#        elif 'TTToHadronic' in key or 'QCD' in key:
#            addedFilesMcFake[year].append(key + '.root')
        elif 'TTG' in key:
            addedFilesMcttG[year].append( key + '.root')
        elif 'TTga' in key:
#            os.system('mv ' + key + '.root ' + key.replace("UL", "20")+ '.root ')
            continue
#            os.system('mv ' + key + '.root ' + key.replace("UL17", "2017")+ '.root ') 
#        elif 'WJetsToLNu' in key or 'TTToSemiLeptonic' in key or 'TTTo2L2Nu' in key or 'tWNo' in key or 'ST_t' in key:
        else: 
            addedFilesMcmisIDele[year].append(key + '.root')
    for key, value in addedFilesData.items():
#        if key != '2017':
#            continue
        Fmerged=[]
        hadddata = 'hadd ' +key+'_data.root ' + ' '.join(addedFilesData[key])
        haddmcGjets ='hadd ' +key+'_Gjets.root ' + ' '.join(addedFilesMcGjets[key])
#        haddmcFake ='hadd ' +key+'_Fake.root ' + ' '.join(addedFilesMcFake[key])
        haddmcttG ='hadd ' +key+'_ttG.root ' + ' '.join(addedFilesMcttG[key])
        haddmcmisIDele ='hadd ' +key+'_Other.root ' + ' '.join(addedFilesMcmisIDele[key])
        print haddmcmisIDele
        Fmerged.append(hadddata)
        Fmerged.append(haddmcGjets)
#        Fmerged.append(haddmcFake)
        Fmerged.append(haddmcttG)
        Fmerged.append(haddmcmisIDele)
        Parallel(n_jobs=6)(delayed(f)(i) for i in Fmerged)
        os.system('hadd '+key+'_TOP.root '+key+'_TTTo2L2Nu.root '+key+'_ST_t_channel_antitop.root '+key+'_TTToHadronic.root '+key+'_tW_inclusiveDecays.root '+key+'_ST_t_channel_top.root '+key+'_TTToSemiLeptonic.root '+key+'_antitW_inclusiveDecays.root')
    os.system('hadd All_TTgaSpin32_M800.root 2016preVFP_TTgaSpin32_M800.root 2016postVFP_TTgaSpin32_M800.root 2017_TTgaSpin32_M800.root 2018_TTgaSpin32_M800.root')
    os.system('hadd All_TTgaSpin32_M1600.root 2016preVFP_TTgaSpin32_M1600.root 2016postVFP_TTgaSpin32_M1600.root 2017_TTgaSpin32_M1600.root 2018_TTgaSpin32_M1600.root')


