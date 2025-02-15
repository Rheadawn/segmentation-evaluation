from math import ceil, sqrt
from path_enums import Metric

# EXTREME VALUES
def getGlobalMaximum(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    maxCoverage = max(coverages)
    if maxCoverage == 0:
        return []
    maxCoverageIndices = [index for index, coverage in enumerate(coverages) if coverage == maxCoverage]

    globalMaxima = []
    for index in maxCoverageIndices:
        globalMaxima.append(evalItems[index])

    return globalMaxima

def getGlobalMinimum(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    minCoverage = min(coverages)
    minCoverageIndices = [index for index, coverage in enumerate(coverages) if coverage == minCoverage]

    globalMinima = []
    for index in minCoverageIndices:
        globalMinima.append(evalItems[index])
    return globalMinima

def getLocalMaxima(evalItems, metric, localityRange):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    localMaxima = []

    for i in range(len(coverages)):
        left = max(0, i - localityRange)
        right = min(len(coverages) - 1, i + localityRange)

        if coverages[i] == max(coverages[left:right+1]):
            localMaxima.append(sortedEvalItems[i])

    return localMaxima

def getLocalMinima(evalItems, metric, localityRange):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    localMinima = []

    for i in range(len(coverages)):
        left = max(0, i - localityRange)
        right = min(len(coverages) - 1, i + localityRange)

        if coverages[i] == min(coverages[left:right+1]):
            localMinima.append(sortedEvalItems[i])

    return localMinima

# AVERAGES
def getAverage(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    return sum(coverages) / len(coverages)

def getMedian(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    coverages.sort()
    length = len(coverages)

    if length % 2 == 0:
        return (coverages[length // 2 - 1] + coverages[length // 2]) / 2
    else:
        return coverages[length // 2]
    
# DEVIATIONS
def getStandardDeviation(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    average = getAverage(evalItems, metric)
    return sqrt(sum([(coverage - average) ** 2 for coverage in coverages]) / (len(coverages)-1))

def getVariance(evalItems, metric):
    return getStandardDeviation(evalItems, metric) ** 2

def getInterquartileRange(evalItems, metric):
    coverages = getCoverages(evalItems, metric)
    coverages.sort()
    length = len(coverages)

    lowerQuartilIndex = length *  1/4
    lowerQuartil = 0
    if lowerQuartilIndex % 1 == 0:
        lowerQuartil = (coverages[lowerQuartilIndex] + coverages[lowerQuartilIndex + 1]) / 2
    else:
        lowerQuartil = coverages[ceil(lowerQuartilIndex)]

    upperQuartilIndex = length * 3/4
    upperQuartil = 0
    if upperQuartilIndex % 1 == 0:
        upperQuartil = (coverages[upperQuartilIndex] + coverages[upperQuartilIndex + 1]) / 2
    else:
        upperQuartil = coverages[ceil(upperQuartilIndex)]

    return upperQuartil - lowerQuartil

# ROBUSTNESS
def getGradientLeftOfOptimum(evalItems, metric, optimumIndex, localityRange):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    leftIndex = max(0, optimumIndex - localityRange)
    return (coverages[optimumIndex] - coverages[leftIndex]) / (optimumIndex - leftIndex)

def getGradientRightOfOptimum(evalItems, metric, optimumIndex, localityRange):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    rightIndex = min(len(coverages) - 1, optimumIndex + localityRange)
    return (coverages[rightIndex] - coverages[optimumIndex]) / (rightIndex - optimumIndex)

def getLocalVarianceAroundOptimum(evalItems, metric, optimumIndex, localityRange):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    leftIndex = max(0, optimumIndex - localityRange)
    rightIndex = min(len(sortedEvalItems) - 1, optimumIndex + localityRange)
    return getVariance(sortedEvalItems[leftIndex:rightIndex+1], metric)

def getGlobalOptimumInterval(evalItems, metric, threshold):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    globalOptima = getGlobalMaximum(sortedEvalItems, metric)
    if len(globalOptima) == 0:
        return []

    coverages = getCoverages(sortedEvalItems, metric)
    intervals = []

    for optimum in globalOptima:
        optimumIndex = sortedEvalItems.index(optimum)
        interval = []
        for i in range(optimumIndex, -1, -1):
            if coverages[i] < coverages[optimumIndex] * threshold:
                leftBound = i+1 if i < optimumIndex else i
                interval.append(sortedEvalItems[leftBound].segmentationValues.primarySegmentationValue)
                break
        if len(interval) == 0:
            interval.append(sortedEvalItems[0].segmentationValues.primarySegmentationValue)
        interval.append(sortedEvalItems[optimumIndex].segmentationValues.primarySegmentationValue)
        for i in range(optimumIndex, len(coverages)):
            if coverages[i] < coverages[optimumIndex] * threshold:
                rightBound = i-1 if i > optimumIndex else i
                interval.append(sortedEvalItems[rightBound].segmentationValues.primarySegmentationValue)
                break
        if len(interval) == 2:
            interval.append(sortedEvalItems[len(sortedEvalItems)-1].segmentationValues.primarySegmentationValue)
        intervals.append(interval)
    
    return intervals


def getOptimumIntervals(evalItems, metric, optimumIndex, threshold):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    optimumCoverage = coverages[optimumIndex]
    indices = [index for index, coverage in enumerate(coverages) if coverage >= optimumCoverage * threshold]

    intervals = []
    currentInterval = []
    for i, index in enumerate(indices):
        if len(currentInterval) == 0:
            currentInterval.append(sortedEvalItems[index])

        if (i < len(indices)-1) and (indices[i+1] != index+1):
            currentInterval.append(sortedEvalItems[index])

        if len(currentInterval) == 2:
            intervals.append(currentInterval.copy())
            currentInterval = []

    if len(currentInterval) == 1:
        currentInterval.append(sortedEvalItems[indices[len(indices)-1]])
        intervals.append(currentInterval)
    return intervals

def getHalfWidthItems(evalItems, metric, optimumIndex):
    sortedEvalItems = sortByPrimarySegmentationValue(evalItems)
    coverages = getCoverages(sortedEvalItems, metric)
    optimumCoverage = coverages[optimumIndex]
    halfCoverage = optimumCoverage / 2

    leftIndex = optimumIndex
    while leftIndex > 0 and coverages[leftIndex] > halfCoverage:
        leftIndex -= 1

    rightIndex = optimumIndex
    while rightIndex < len(coverages) - 1 and coverages[rightIndex] > halfCoverage:
        rightIndex += 1

    return [sortedEvalItems[leftIndex], sortedEvalItems[rightIndex]]

# DIVERSITY
def getSimpsonIndex(tscInstances):
    instanceCounts = list(map(lambda tscInstance: tscInstance.count, tscInstances))
    numberOfInstances = sum(instanceCounts)
    probabilities = list(map(lambda count: (count*(count-1)) / (numberOfInstances*(numberOfInstances-1)), instanceCounts))

    simpsonIndex = 1 - sum(probabilities)
    return simpsonIndex

# HELPER FUNCTIONS
def getCoverages(evalItems, metric):
    coverages = []
    match metric:
        case Metric.TSC_COVERAGE:
            coverages = list(map(lambda item: item.tscData.tscCoverage, evalItems))
        case Metric.TSC_AND_COMBINATION_COVERAGE:
            coverages = list(map(lambda item: item.combinationData.combinationCoverage, evalItems))
        case _:
            coverages = list(map(lambda item: item.featureData.featureCoverage, evalItems))

    return coverages

def sortByPrimarySegmentationValue(evalItems):
    return sorted(evalItems, key=lambda item: item.segmentationValues.primarySegmentationValue)

def sortBySecondarySegmentationValue(evalItems):
    return sorted(evalItems, key=lambda item: item.segmentationValues.secondarySegmentationValue)

def sortByTertiarySegmentationValue(evalItems):
    return sorted(evalItems, key=lambda item: item.segmentationValues.tertiarySegmentationValue)