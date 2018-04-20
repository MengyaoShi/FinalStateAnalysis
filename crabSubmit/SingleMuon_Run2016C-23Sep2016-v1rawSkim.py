from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'SingleMuon_Run2016C-23Sep2016-v1rawSkim_MakeNtuples'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../NtupleTools/test/make_ntuples_cfg.py'
config.Data.userInputFiles = open('./AllRootFiles/SUB/SingleMuon_Run2016C-23Sep2016-v1rawSkim.txt').readlines()
config.JobType.numCores=1
config.JobType.pyCfgParams=['channels="mt"']
config.JobType.maxMemoryMB = 2000
config.JobType.sendPythonFolder = True
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 200
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/%s/' % (getUsernameFromSiteDB())
config.Data.publication = True
config.Data.outputPrimaryDataset = 'SingleMuon_Run2016C-23Sep2016-v1rawSkim_MakeNtuples'
config.Data.outputDatasetTag = 'SingleMuon_Run2016C-23Sep2016-v1rawSkim_MakeNtuples'
config.Site.whitelist=['T2_CH_CERN']
config.Site.storageSite = 'T2_CH_CERN'
