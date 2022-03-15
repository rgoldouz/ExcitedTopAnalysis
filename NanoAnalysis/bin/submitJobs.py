import sys
import os
import subprocess
import readline
import string
import csv, subprocess

directory = '/user/rgoldouz/NewAnalysis2020/Analysis/bin/Jobs'

import Files_2016
import Files_2017
import Files_2018
SAMPLES = {}
MC = True
Data = True
mc_2016 = MC
data_2016 = Data
mc_2017 = MC
data_2017 = Data
mc_2018 = MC
data_2018 = Data

if mc_2016:
    SAMPLES.update(Files_2016.mc2016_samples)
if data_2016:
    SAMPLES.update(Files_2016.data2016_samples)
if mc_2017:
    SAMPLES.update(Files_2017.mc2017_samples)
if data_2017:
    SAMPLES.update(Files_2017.data2017_samples)
if mc_2018:
    SAMPLES.update(Files_2018.mc2018_samples)
if data_2018:
    SAMPLES.update(Files_2018.data2018_samples)


for key, value in SAMPLES.items():
    if 'CR' not in key:
        continue
    year = value[3]
    nf = 72
    for idx, S in enumerate(value[0]):
        if 'TTTo2L2Nu' in key or 'tw' in key or 'DY' in key:
            nf = 35
        if value[1]=='data':
            nf = 205
        for subdir, dirs, files in os.walk(S):
            sequance = [files[i:i+nf] for i in range(0,len(files),nf)]
            for num,  seq in enumerate(sequance):
                f = key +'_' + str(idx) +'_' + str(num)
#                subprocess.call('rm /user/rgoldouz/NewAnalysis2020/Analysis/hists/' + year + '/' + f + '.root', shell=True)
                qsub = "qsub -q localgrid  -o STDOUT/" + f + ".stdout -e STDERR/" + f + ".stderr Jobs/" + f + '.sh'
                subprocess.call(qsub, shell=True)
            break

