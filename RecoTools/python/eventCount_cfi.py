import FWCore.ParameterSet.Config as cms

eventCount = cms.EDProducer("EventCountProducer")
summedWeight = cms.EDProducer("WeightedEventCountProducer",
                               summedWeights = cms.InputTag('lumiSummary','sumOfWeightedEvents'))
