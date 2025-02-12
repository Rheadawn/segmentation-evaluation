class EvaluationData:
    def __init__(self, evaluationMetaData, evaluationItems):
        self.evaluationMetaData = evaluationMetaData
        self.evaluationItems = evaluationItems
    
    def to_dict(self):
        return {
            'evaluationMetaData': self.evaluationMetaData.to_dict(),
            'evaluationItems': [item.to_dict() for item in self.evaluationItems]
        }

    @staticmethod
    def from_dict(data):
        return EvaluationData(
            evaluationMetaData=EvaluationMetaData.from_dict(data['evaluationMetaData']),
            evaluationItems=[EvaluationItem.from_dict(item) for item in data['evaluationItems']]
        )

class EvaluationMetaData:
    def __init__(self, segmentation, town, metric, tsc):
        self.segmentation = segmentation
        self.town = town
        self.metric = metric
        self.tsc = tsc
    
    def to_dict(self):
        return {
            'segmentation': self.segmentation,
            'town': self.town,
            'metric': self.metric,
            'tsc': self.tsc
        }

    @staticmethod
    def from_dict(data):
        return EvaluationMetaData(
            segmentation=data['segmentation'],
            town=data['town'],
            metric=data['metric'],
            tsc=data['tsc']
        )

class EvaluationItem:
    def __init__(self, segmentationValues, segmentationMetaData, tscData, combinationData, featureData, segmentationLength, instanceData):
        self.segmentationValues = segmentationValues
        self.segmentationMetaData = segmentationMetaData
        self.tscData = tscData
        self.combinationData = combinationData
        self.featureData = featureData
        self.segmentationLength = segmentationLength
        self.instanceData = instanceData
    
    def to_dict(self):
        return {
            'segmentationValues': self.segmentationValues.to_dict(),
            'segmentationMetaData': self.segmentationMetaData.to_dict(),
            'tscData': self.tscData.to_dict(),
            'combinationData': self.combinationData.to_dict(),
            'featureData': self.featureData.to_dict(),
            'segmentationLength': self.segmentationLength.to_dict(),
            'instanceData': [item.to_dict() for item in self.instanceData]
        }

    @staticmethod
    def from_dict(data):
        return EvaluationItem(
            segmentationValues=SegmentationValues.from_dict(data['segmentationValues']),
            segmentationMetaData=SegmentationMetaData.from_dict(data['segmentationMetaData']),
            tscData=TscData.from_dict(data['tscData']),
            combinationData=CombinationData.from_dict(data['combinationData']),
            featureData=FeatureData.from_dict(data['featureData']),
            segmentationLength=SegmentationLength.from_dict(data['segmentationLength']),
            instanceData=[TSCInstance.from_dict(item) for item in data['instanceData']]
        )

class SegmentationValues:
    def __init__(self, primarySegmentationValue, secondarySegmentationValue, tertiarySegmentationValue):
        self.primarySegmentationValue = primarySegmentationValue
        self.secondarySegmentationValue = secondarySegmentationValue
        self.tertiarySegmentationValue = tertiarySegmentationValue
    
    def to_dict(self):
        return {
            'primarySegmentationValue': self.primarySegmentationValue,
            'secondarySegmentationValue': self.secondarySegmentationValue,
            'tertiarySegmentationValue': self.tertiarySegmentationValue
        }

    @staticmethod
    def from_dict(data):
        return SegmentationValues(
            primarySegmentationValue=data['primarySegmentationValue'],
            secondarySegmentationValue=data['secondarySegmentationValue'],
            tertiarySegmentationValue=data['tertiarySegmentationValue']
        )

class SegmentationMetaData:
    def __init__(self, tscType, segmentationType, featureName):
        self.tscType = tscType
        self.segmentationType = segmentationType
        self.featureName = featureName
    
    def to_dict(self):
        return {
            'tscType': self.tscType,
            'segmentationType': self.segmentationType,
            'featureName': self.featureName
        }

    @staticmethod
    def from_dict(data):
        return SegmentationMetaData(
            tscType=data['tscType'],
            segmentationType=data['segmentationType'],
            featureName=data['featureName']
        )

class TscData:
    def __init__(self, foundTSCInstances, missedTSCInstances):
        self.tscCoverage = foundTSCInstances / (foundTSCInstances + missedTSCInstances)
        self.foundTSCInstances = foundTSCInstances
        self.missedTSCInstances = missedTSCInstances
    
    def to_dict(self):
        return {
            'tscCoverage': self.tscCoverage,
            'foundTSCInstances': self.foundTSCInstances,
            'missedTSCInstances': self.missedTSCInstances
        }

    @staticmethod
    def from_dict(data):
        return TscData(
            foundTSCInstances=data['foundTSCInstances'],
            missedTSCInstances=data['missedTSCInstances']
        )

class CombinationData:
    def __init__(self, foundCombinations, missedCombinations):
        self.combinationCoverage = foundCombinations / (foundCombinations + missedCombinations)
        self.foundCombinations = foundCombinations
        self.missedCombinations = missedCombinations
    
    def to_dict(self):
        return {
            'combinationCoverage': self.combinationCoverage,
            'foundCombinations': self.foundCombinations,
            'missedCombinations': self.missedCombinations
        }

    @staticmethod
    def from_dict(data):
        return CombinationData(
            foundCombinations=data['foundCombinations'],
            missedCombinations=data['missedCombinations']
        )

class FeatureData:
    def __init__(self, foundFeatures, missedFeatures):
        self.featureCoverage = foundFeatures / (foundFeatures + missedFeatures)
        self.foundFeatures = foundFeatures
        self.missedFeatures = missedFeatures
    
    def to_dict(self):
        return {
            'featureCoverage': self.featureCoverage,
            'foundFeatures': self.foundFeatures,
            'missedFeatures': self.missedFeatures
        }

    @staticmethod
    def from_dict(data):
        return FeatureData(
            foundFeatures=data['foundFeatures'],
            missedFeatures=data['missedFeatures']
        )

class SegmentationLength:
    def __init__(self, cvForSeconds, conformityRateSeconds, minSeconds, maxSeconds, averageSeconds, 
                 cvForMeters, conformityRateMeters, minMeters, maxMeters, averageMeters):
        self.cvForSeconds = cvForSeconds
        self.conformityRateSeconds = conformityRateSeconds
        self.minSeconds = minSeconds
        self.maxSeconds = maxSeconds
        self.averageSeconds = averageSeconds
        self.conformityRateMeters = conformityRateMeters
        self.cvForMeters = cvForMeters
        self.minMeters = minMeters
        self.maxMeters = maxMeters
        self.averageMeters = averageMeters
    
    def to_dict(self):
        return {
            'cvForSeconds': self.cvForSeconds,
            'conformityRateSeconds': self.conformityRateSeconds,
            'minSeconds': self.minSeconds,
            'maxSeconds': self.maxSeconds,
            'averageSeconds': self.averageSeconds,
            'cvForMeters': self.cvForMeters,
            'conformityRateMeters': self.conformityRateMeters,
            'minMeters': self.minMeters,
            'maxMeters': self.maxMeters,
            'averageMeters': self.averageMeters
        }

    @staticmethod
    def from_dict(data):
        return SegmentationLength(
            cvForSeconds=data['cvForSeconds'],
            conformityRateSeconds=data['conformityRateSeconds'],
            minSeconds=data['minSeconds'],
            maxSeconds=data['maxSeconds'],
            averageSeconds=data['averageSeconds'],
            cvForMeters=data['cvForMeters'],
            conformityRateMeters=data['conformityRateMeters'],
            minMeters=data['minMeters'],
            maxMeters=data['maxMeters'],
            averageMeters=data['averageMeters']
        )
    
class CurveData:
    def __init__(self, segmentationValue, tscCoverage, combinationCoverage, featureCoverage):
        self.segmentationValue = segmentationValue
        self.tscDiff = tscCoverage
        self.combinationDiff = combinationCoverage
        self.featureDiff = featureCoverage

class TSCInstance:
    def __init__(self, instance, count):
        self.instance = instance
        self.count = count

    def to_dict(self):
        return {
            'instance': self.instance.to_dict(),	
            'count': self.count
        }
    
    @staticmethod
    def from_dict(data):
        return TSCInstance(
            instance=TSCEdge.from_dict(data['instance']),
            count=data['count']
        )

class TSCEdge:
    def __init__(self, label, outgoingEdges):
        self.label = label
        self.outgoingEdges = outgoingEdges

    def to_dict(self):
        return {
            'label': self.label,
            'outgoingEdges': [item.to_dict() for item in self.outgoingEdges]
        }
    
    @staticmethod
    def from_dict(data):
        return TSCEdge(
            label=data['label'],
            outgoingEdges=[TSCEdge.from_dict(item) for item in data['outgoingEdges']]
        )