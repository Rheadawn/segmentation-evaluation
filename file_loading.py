import os
import glob
import json
import path_enums as pe
import evaluation_data as ed

def getEvaluationData(town, segmentation, metric, tsc):

    saveFile = os.path.join('.', 'data', town + '_' + segmentation + '_' + metric + '_' + tsc + '.json')

    if os.path.exists(saveFile):
        print('Loading from file')
        json = loadJson(saveFile)
        evaluation = deserializeFromJson(json)

        return evaluation
    else:
        print('Loading from folders')
        path = os.path.join('..', town, segmentation + '_' + metric, 'serialized-results', '*') #GET CORRECT PATH
        folders = glob.glob(path)

        evaluationItems = list(map(lambda folder: getDataFromFolder(folder, tsc), folders))
        evaluationMetaData = ed.EvaluationMetaData(segmentation, town, metric, tsc)
        evaluation = ed.EvaluationData(evaluationMetaData, evaluationItems)

        json = serializeToJson(evaluation)
        saveJson(saveFile, json)

        return evaluation

def getDataFromFolder(folder,tsc):
    segmentationValues = getSegmentationValues(folder, tsc)
    segmentationMetaData = getSegmentationMetaData(folder, tsc)
    tscData = getTscData(folder, tsc)
    combinationData = getCombinationData(folder, tsc)
    featureData = getFeatureData(folder, tsc)
    segmentationLength = getSegmentationLength(folder, tsc)
    evaluationItems = ed.EvaluationItem(segmentationValues, segmentationMetaData, tscData, combinationData, featureData, segmentationLength)

    return evaluationItems

def getSegmentationValues(folder,tsc):
    segParams = loadJson(os.path.join(folder, 'segmentation-parameters', tsc + '.json'))
    segmentationValues = ed.SegmentationValues(segParams['primarySegmentationValue'], segParams['secondarySegmentationValue'], segParams['tertiarySegmentationValue'])
    return segmentationValues

def getSegmentationMetaData(folder,tsc):
    segParams = loadJson(os.path.join(folder, 'segmentation-parameters', tsc + '.json'))
    segmentationMetaData = ed.SegmentationMetaData(segParams['identifier'], segParams['segmentationType'], segParams['featureName'])
    return segmentationMetaData

def getTscData(folder,tsc):
    validTscInstances = loadJson(os.path.join(folder, 'valid-tsc-instances-per-tsc', tsc + '.json'))
    missedTscInstances = loadJson(os.path.join(folder, 'missed-tsc-instances-per-tsc', tsc + '.json'))

    foundInstances = validTscInstances['count']
    missedInstances = missedTscInstances['count']

    tscData = ed.TscData(foundInstances, missedInstances)
    return tscData

def getCombinationData(folder,tsc):
    missedAndFound = loadJson(os.path.join(folder, 'missed-and-found-predicate-combinations', tsc + '.json'))

    foundCombinations = missedAndFound['found']
    missedCombinations = missedAndFound['missed']

    combinationData = ed.CombinationData(foundCombinations, missedCombinations)
    return combinationData

def getFeatureData(folder,tsc):
    validTscInstances = loadJson(os.path.join(folder, 'valid-tsc-instances-per-tsc', tsc + '.json'))
    missedTscInstances = loadJson(os.path.join(folder, 'missed-tsc-instances-per-tsc', tsc + '.json'))

    foundFeatures = validTscInstances['featureCount']
    missedFeatures = missedTscInstances['featureCount']

    featureData = ed.FeatureData(foundFeatures, missedFeatures)
    return featureData

def getSegmentationLength(folder,tsc):
    segLength = loadJson(os.path.join(folder, 'segment-length-metric', tsc + '.json'))

    cvForSeconds = segLength['cvForSeconds']
    conformityRateSeconds = segLength['conformityRateSeconds']
    minSeconds = segLength['minSeconds']
    maxSeconds = segLength['maxSeconds']
    averageSeconds = segLength['averageSeconds']
    cvForMeters = segLength['cvForMeters']
    conformityRateMeters = segLength['conformityRateMeters']
    minMeters = segLength['minMeters']
    maxMeters = segLength['maxMeters']
    averageMeters = segLength['averageMeters']

    segmentationLength = ed.SegmentationLength(cvForSeconds, conformityRateSeconds, minSeconds, maxSeconds, averageSeconds, cvForMeters, conformityRateMeters, minMeters, maxMeters, averageMeters)
    return segmentationLength

def loadJson(path):
    content = open(path, 'r').read()
    return json.loads(content)

def saveJson(path, content):
    with open(path, 'w') as file:
        file.write(content)

def serializeToJson(evalObj):
    jsonContent = json.dumps(evalObj.to_dict())
    return jsonContent

def deserializeFromJson(json):
    evaluation = ed.EvaluationData.from_dict(json)
    return evaluation

t1 = pe.Town.ONE
seg = pe.Segmentation.SECONDS
met = pe.Metric.PEDESTRIAN_CROSSED
tsc = pe.Tsc.FULL

evalData = getEvaluationData(t1.value, seg.value, met.value, tsc.value)
print(evalData.evaluationItems[0].segmentationValues.primarySegmentationValue)