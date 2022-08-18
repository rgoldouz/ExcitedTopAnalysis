import datetime
import os
from os import path
import sys
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow, Dataset,ParentDataset
sys.path.append(os.path.abspath("."))
import Files_2017_nano
import Files_ULall_nano

SAMPLES = {}
SAMPLES.update(Files_ULall_nano.UL17)

cmsswbase = os.environ['CMSSW_BASE']
timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

username = "rgoldouz"

production_tag = "AnalysisExcitedTop"            # For 'full_production' setup

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
    "hdfs://eddie.crc.nd.edu:19000"  + input_path,
    "root://deepthought.crc.nd.edu/" + input_path
    ],
    output=[
        "hdfs://eddie.crc.nd.edu:19000"  + output_path,
        "root://deepthought.crc.nd.edu/" + output_path, # Note the extra slash after the hostname!
        "gsiftp://T3_US_NotreDame"       + output_path,
        "srm://T3_US_NotreDame"          + output_path,
        "file:///hadoop"                 + output_path,
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
    cores=1,
    memory=4000,
    disk=5000
)
#################################################################
wf = []
for key, value in SAMPLES.items():
    FPT=10
    if 'data' in key or 'GJets' in key or 'TTga' in key:
        FPT=1
    if path.exists('/hadoop/store/user/rgoldouz/FullProduction/AnalysisExcitedTop/Analysis_' + key) and len(os.listdir('/hadoop/store/user/rgoldouz/FullProduction/AnalysisExcitedTop/Analysis_' + key))>0:
        continue
    if path.exists('/hadoop/store/user/rgoldouz/FullProduction/AnalysisExcitedTop/Analysis_' + key):
        os.system('rm -r '+ '/hadoop/store/user/rgoldouz/FullProduction/AnalysisExcitedTop/Analysis_' + key)
    print key
#    if len(os.listdir('/hadoop/store/user/rgoldouz/FullProduction/TOPBNVAnalysis/Analysis_'+key))!=0:
#        continue
    Analysis = Workflow(
        label='Analysis_%s' % (key),
        sandbox=cmssw.Sandbox(release='/afs/crc.nd.edu/user/r/rgoldouz/CMSSW_10_4_0'),
        globaltag=False,
        command='python Lobster_check.py ' + key + ' ' + value[1] +' ' + value[2] +' ' +value[3] +' ' +value[4] +' ' +value[5] +' ' +value[6] +' ' +value[7] +' ' +value[8] +' ' +value[9] +' @inputfiles',
        extra_inputs=[
            'Lobster_check.py',
            '../lib/libmain.so',
            '../lib/libcorrectionlib.so',
            '../lib/libEFTGenReaderEFTHelperUtilities.so',
            '../lib/libCondFormatsJetMETObjects.so',
            '../lib/libCondFormatsSerialization.so',
            '../include/MyAnalysis.h',
        ],
        outputs=['ANoutput.root'],
        dataset=Dataset(
           files=value[0],
           patterns=["*.root"],
           files_per_task =FPT
        ),
#        merge_command='hadd @outputfiles @inputfiles',
#        merge_size='2G',
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
        payload=10,
        dashboard = False,
        xrootd_servers=['ndcms.crc.nd.edu',
                       'cmsxrootd.fnal.gov',
                       'deepthought.crc.nd.edu'],
    )
)

