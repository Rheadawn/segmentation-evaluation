import objectiveFunctionEvaluation as ofe
from evaluation_data import CurveData
from path_enums import Segmentation

# DIFFERENCE CURVE
def getDifferenceCurve(firstCurve, secondCurve):
    differenceCurve = []

    for firstItem, secondItem in zip(firstCurve, secondCurve):
        if firstItem != None and secondItem != None:
            tscDiff = firstItem.tscCoverage - secondItem.tscCoverage
            combinationDiff = firstItem.combinationCoverage - secondItem.combinationCoverage
            featureDiff = firstItem.featureCoverage - secondItem.featureCoverage
            differenceCurve.append(CurveData(firstItem.segmentationValue, tscDiff, combinationDiff, featureDiff))

    return differenceCurve

def getAbsoluteDifferenceCurve(firstCurve, secondCurve):
    differenceCurve = getDifferenceCurve(firstCurve, secondCurve)
    absoluteDifferenceCurve = list(map(lambda curveItem: CurveData(curveItem.segmentationValue, abs(curveItem.tscCoverage), abs(curveItem.combinationCoverage), abs(curveItem.featureCoverage)), differenceCurve))
    return absoluteDifferenceCurve

# TSC COMPARISON
def getEqualTscInstances(tscInstances1, tscInstances2):
    equalTscInstances = []
    for tscInstance1 in tscInstances1:
        isContained = any(tscEquals(tscInstance1.instance, tscInstance2.instance) for tscInstance2 in tscInstances2)
        if isContained:
            equalTscInstances.append(tscInstance1.instance)
    return equalTscInstances

def getAdditionalTscInstances(tscInstances1, tscInstances2):
    additionalTscInstances = []
    for tscInstance1 in tscInstances1:
        isContained = any(tscEquals(tscInstance1.instance, tscInstance2.instance) for tscInstance2 in tscInstances2)
        if not isContained:
            additionalTscInstances.append(tscInstance1.instance)
    return additionalTscInstances

# HELPER FUNCTIONS
def smoothObjectiveFunction(evalItems, segmentation):
    valueRange = getObjectiveFunctionBoundaries(segmentation)
    valueBinCount = int(((valueRange["stop"] - valueRange["start"]) / valueRange["step"]) + 1)

    curveItems = [None] * valueBinCount
    for segmentationValue in floatRange(valueRange["start"], valueRange["stop"], valueRange["step"]):
        index = int(segmentationValue/valueRange["step"] - 1)
        lowerBound = segmentationValue - valueRange["step"]/2
        upperBound = segmentationValue + valueRange["step"]/2
        filteredItems = list(filter(lambda evalItem: evalItem.segmentationValues.primarySegmentationValue >= lowerBound and evalItem.segmentationValues.primarySegmentationValue < upperBound, evalItems))
        itemCount = len(filteredItems)

        if itemCount > 0:
            tscCoverages = list(map(lambda item: item.tscData.tscCoverage, filteredItems))
            combinationCoverages = list(map(lambda item: item.combinationData.combinationCoverage, filteredItems))
            featureCoverages = list(map(lambda item: item.featureData.featureCoverage, filteredItems))
            curveItems[index] = CurveData(segmentationValue, sum(tscCoverages)/itemCount, sum(combinationCoverages)/itemCount, sum(featureCoverages)/itemCount)

    return curveItems

def getObjectiveFunctionBoundaries(segmentation):
    match segmentation:
        case Segmentation.SECONDS:
            return {"start": 0.5, "stop": 120.0, "step": 0.5}  # windowSize
        case Segmentation.METERS:
            return {"start": 0.5, "stop": 300.0, "step": 0.5}  # windowSize
        case Segmentation.BREMSWEG:
            return {"start": 0.5, "stop": 150.0, "step": 0.5}  # lookAhead
        case Segmentation.SPEED:
            return {"start": 0.1, "stop": 60.0, "step": 0.1} # lookAhead
        
def floatRange(start, stop, step):
    while start <= stop:
        yield start
        start += step

def tscEquals(tsc1, tsc2):
    if (tsc1.label != tsc2.label):
        return False
    
    if (len(tsc1.outgoingEdges) != len(tsc2.outgoingEdges)):
        return False
    
    if(len(tsc1.outgoingEdges) == 0):
        return True
    
    for index in range(0, len(tsc1.outgoingEdges)):
        if(not tscEquals(tsc1.outgoingEdges[index], tsc2.outgoingEdges[index])):
            return False
        
    return True

# TSC-Vergleich (Vergleich der Verteilung der gefundenen TSC-Instanzen)