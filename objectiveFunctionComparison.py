import objectiveFunctionEvaluation as ofe
from evaluation_data import CurveData
from path_enums import Segmentation

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


# Optimalwertüberlappung (Vergleicht die Position der Optimalwerte)

# TSC-Vergleich (Vergleich der Verteilung der gefundenen TSC-Instanzen)