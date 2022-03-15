I run the CLs limits at cern in the following directory
/afs/cern.ch/work/r/rgoldouz/Combine/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/test/TOPLFV

first run make_workSpace.py to make workspace out of the cards and input files
then scan a range of POI using condor jobs by Run-LHC-Limit.py
then merge the output files and find limits using merged.py
and finally make a table for the limits using make_table_observed.py
