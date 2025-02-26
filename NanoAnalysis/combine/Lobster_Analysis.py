import datetime
import os
from os import path
import sys
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow, Dataset,ParentDataset, EmptyDataset
sys.path.append(os.path.abspath("."))

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

username = "rgoldouz"

production_tag = "LimitsExcitedTop"            # For 'full_production' setup

# Only run over lhe steps from specific processes/coeffs/runs
process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []  # (i.e. MG starting points)

master_label = '%s_%s' % (production_tag,timestamp_tag)

input_path   = "/store/user/"
output_path  = "/store/user/$USER/FullProduction/%s" % (production_tag)
workdir_path = "/tmpscratch/users/$USER/FullProduction/%s" % (production_tag)
plotdir_path = "~/www/lobster/FullProduction/%s" % (production_tag)

storage = StorageConfiguration(
    input=[
        "file:///cms/cephfs/data/store/user/",
        "root://hactar01.crc.nd.edu//store/user/",
    ],
    output=[
        # Until a separate bug is fixed file://cms/cephfs needs to be the first output so the initial lobster validation passes.
        "file:///cms/cephfs/data"+output_path,
        "root://hactar01.crc.nd.edu/"+output_path,
    ],
    disable_input_streaming=True,
)


#################################################################
# Worker Res.:
#   Cores:  12    | 4
#   Memory: 16000 | 8000
#   Disk:   13000 | 6500
#################################################################
gs_resources = Category(
    name='gs',
    cores=4,
    memory=4000,
    disk=4000
)
#################################################################
wf = []

year=['2016preVFP', '2016postVFP', '2017','2018', '2016preVFP_2016postVFP_2017_2018']
year=['2016preVFP_2016postVFP_2017_2018']

SignalSamples=[
['TTga_M700','700'],
['TTga_M800','800'],
['TTga_M900','900'],
['TTga_M1000','1000'],
['TTga_M1200','1200'],
['TTga_M1300','1300'],
['TTga_M1400','1400'],
['TTga_M1500','1500'],
['TTga_M1600','1600'],
['TTga_M1800','1800'],
['TTga_M1900','1900'],
['TTga_M2000','2000'],
['TTga_M2250','2250'],
['TTga_M2500','2500'],
['TTga_M2750','2750'],
['TTga_M3000','3000'],
['TTgaSpin32_M700','700'],
['TTgaSpin32_M800','800'],
['TTgaSpin32_M900','900'],
['TTgaSpin32_M1000','1000'],
['TTgaSpin32_M1200','1200'],
['TTgaSpin32_M1300','1300'],
['TTgaSpin32_M1400','1400'],
['TTgaSpin32_M1500','1500'],
['TTgaSpin32_M1600','1600'],
['TTgaSpin32_M1800','1800'],
['TTgaSpin32_M1900','1900'],
['TTgaSpin32_M2000','2000'],
['TTgaSpin32_M2250','2250'],
['TTgaSpin32_M2500','2500'],
['TTgaSpin32_M2750','2750'],
['TTgaSpin32_M3000','3000'],
]
#SignalSamples=[
#['TTga_M1500','1500'],
#['TTgaSpin32_M1500','1500'],
#]

regions=[["nAk8G1nTtagG0"],["nAk81nTtag1", "nAk8G1nTtagG0"],["nAk81nTtag1", "nAk8G1nTtagG0", "nAk81nTtagOffMt"]]
regions=[["nAk81nTtag1"],["nAk81nTtagOffMt"]]
regions=[["nAk81nTtag1", "nAk8G1nTtagG0"]]
for namesig in SignalSamples:
    for numyear, nameyear in enumerate(year):
       for numreg, namereg in enumerate(regions):
            key = namesig[0] + '_' + nameyear +'_' + '_'.join(namereg)
            print key
            print 'python Lobster_check.py '  + ' ' + namesig[0] +' ' +nameyear +' '+namesig[1]+' '+'_'.join(namereg)
            Analysis = Workflow(
                label=key,
                sandbox=cmssw.Sandbox(release='/afs/crc.nd.edu/user/r/rgoldouz/Limit_combined/forLobster/CMSSW_10_2_13'),
                globaltag=False,
                command='python Lobster_check.py '  + ' ' + namesig[0] +' ' +nameyear +' '+namesig[1]+' '+'_'.join(namereg),
                extra_inputs=[
                    'Lobster_check.py',
                    'CombinedFilesETop',
                ],
#                outputs=[key+'_Expected_mu0_impacts.pdf', key+'_Expected_mu1_impacts.pdf', key+'_results.tex', 'higgsCombineTest.AsymptoticLimits.mH'+namesig[1]+'.root'],
                outputs=[key+'_Observed_mu1_impacts.pdf', key+'_Expected_mu1_impacts.pdf', key+'_results.tex', 'higgsCombineTest.AsymptoticLimits.mH'+namesig[1]+'.root'],
                dataset=EmptyDataset(),
                category=gs_resources
            )
            wf.append(Analysis)

config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wf,
    advanced=AdvancedOptions(
        bad_exit_codes=[127, 160],
        log_level=1,
        osg_version='3.6',
        abort_threshold=0,
        abort_multiplier=100,
    )
)

