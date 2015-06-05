#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import sys

name=sys.argv[2]

process = cms.Process("LHE")

process.source = cms.Source("LHESource",
	fileNames = cms.untracked.vstring('file:/nfs/dust/cms/user/usaiem/gen2/'+name+'/Events/prova2/unweighted_events.lhe')
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('alpha'),
	name = cms.untracked.string('LHEF input'),
	annotation = cms.untracked.string('ttbar')
)

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cout = cms.untracked.PSet( threshold = cms.untracked.string('INFO') )

process.LHE = cms.OutputModule("PoolOutputModule",
	dataset = cms.untracked.PSet(dataTier = cms.untracked.string('LHE')),
	fileName = cms.untracked.string('lhe.root')
)

process.lhedump = cms.EDAnalyzer("DummyLHEAnalyzer",
                                src = cms.InputTag("source")
                                )

process.TFileService=cms.Service("TFileService",fileName=cms.string(name+'.root'))

process.outpath = cms.EndPath(process.LHE+process.lhedump)
