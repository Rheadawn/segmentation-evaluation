import file_loading as fl
import path_enums as pe
import visualization as vis
import objectiveFunctionEvaluation as ofe

# Add show3DGraph for case speed
def showObjectiveFunction(town, segmentation, metric, tsc):
    evalData = fl.getEvaluationData(town, segmentation, metric, tsc)
    sortedEvalItems = ofe.sortByPrimarySegmentationValue(evalData.evaluationItems)
    xAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems))
    yAxis = ofe.getCoverages(sortedEvalItems, metric)
    vis.save2DGraph('plots/objective_functions/' + town + '_' + segmentation + '_' + metric + '_' + tsc + '.png', xAxis, yAxis, getTitle(segmentation), getXAxisLabel(segmentation), 'Abdeckung')


def showBrokenMetric():
    evalData = fl.getEvaluationData(pe.Town.ONE.value, pe.Segmentation.SECONDS.value, pe.Metric.TSC_COVERAGE.value, pe.Tsc.FULL.value)
    evalData2 = fl.getEvaluationData(pe.Town.ONE.value, pe.Segmentation.SECONDS.value, pe.Metric.TSC_AND_COMBINATION_COVERAGE.value, pe.Tsc.FULL.value)
    sortedEvalItems = ofe.sortByPrimarySegmentationValue(evalData.evaluationItems)
    sortedEvalItems2 = ofe.sortByPrimarySegmentationValue(evalData2.evaluationItems)
    tscXAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems))
    brokenMetricXAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems2))
    tscYAxis = list(map(lambda item: item.tscData.tscCoverage, sortedEvalItems))
    brokenMetricYAxis = list(map(lambda item: (item.tscData.tscCoverage + item.combinationData.combinationCoverage)/2, sortedEvalItems2))
    vis.save2DGraphComparisonWithSeparateScales('plots/metric_comparison/broken_metric.png', [tscXAxis, brokenMetricXAxis], [tscYAxis, brokenMetricYAxis],['Scenario coverage','Scenario and combination coverage'],  'Segmentierung nach Sekunden', 'Sekunden', ['Scenario coverage','Scenario and combination coverage'])

def compareTSCandCombinationCoverageNormalized(segmentation):
    evalData = fl.getEvaluationData(pe.Town.ONE.value, segmentation, pe.Metric.TSC_COVERAGE.value, pe.Tsc.FULL.value)
    sortedEvalItems = ofe.sortByPrimarySegmentationValue(evalData.evaluationItems)
    max = ofe.getGlobalMaximum(sortedEvalItems, pe.Metric.TSC_COVERAGE.value)[0].tscData.tscCoverage * 100
    max2 = ofe.getGlobalMaximum(sortedEvalItems, pe.Metric.TSC_AND_COMBINATION_COVERAGE.value)[0].combinationData.combinationCoverage * 100
    xAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems))
    tscYAxis = list(map(lambda item: item.tscData.tscCoverage, sortedEvalItems))
    combinationYAxis = list(map(lambda item: item.combinationData.combinationCoverage * (max/max2), sortedEvalItems))
    vis.save2DGraphComparison('plots/metric_comparison/tsc_vs_combination_' + segmentation + '_normalized.png', [xAxis, xAxis], [tscYAxis, combinationYAxis],['Scenario coverage','Combination coverage'],  getTitle(segmentation), getXAxisLabel(segmentation), 'Abdeckung')

def compareTSCandCombinationCoverage(segmentation):
    evalData = fl.getEvaluationData(pe.Town.ONE.value, segmentation, pe.Metric.TSC_COVERAGE.value, pe.Tsc.FULL.value)
    sortedEvalItems = ofe.sortByPrimarySegmentationValue(evalData.evaluationItems)
    xAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems))
    tscYAxis = list(map(lambda item: item.tscData.tscCoverage, sortedEvalItems))
    combinationYAxis = list(map(lambda item: item.combinationData.combinationCoverage, sortedEvalItems))
    vis.save2DGraphComparisonWithSeparateScales('plots/metric_comparison/tsc_vs_combination_' + segmentation + '.png', [xAxis, xAxis], [tscYAxis, combinationYAxis],['Scenario coverage','Combination coverage'],  getTitle(segmentation), getXAxisLabel(segmentation), ['Scenario coverage','Combination coverage'])

def compareOptimumPositionsOfMetrics(town, segmentation, threshold):
    metricResults = []
    metrics = pe.Metric.getRelevantMetrics()

    for metric in metrics:
        evalItems = fl.getEvaluationData(town, segmentation, metric.value, pe.Tsc.FULL.value).evaluationItems
        intervals = ofe.getGlobalOptimumInterval(evalItems, metric, threshold)
        metricResults.append(intervals)

    labels = list(map(lambda metric: metric.value, metrics))  


    evalData = fl.getEvaluationData(town, segmentation, pe.Metric.TSC_COVERAGE.value, pe.Tsc.FULL.value)
    sortedEvalItems = ofe.sortByPrimarySegmentationValue(evalData.evaluationItems)
    xAxis = list(map(lambda item: item.segmentationValues.primarySegmentationValue, sortedEvalItems))
    yAxis = list(map(lambda item: item.tscData.tscCoverage, sortedEvalItems))

    #vis.saveDumbellGraph('plots/metric_comparison/optimum_positions_' + segmentation + '_' + str(threshold) + '_' + '.png', metricResults, labels, getTitle(segmentation))
    vis.saveDumbellGraphAnd2DGraph('plots/metric_comparison/optimum_positions_' + town + "_" + segmentation + '_' + str(threshold) + '_2D.png', metricResults, labels, getTitle(segmentation), xAxis, yAxis, getXAxisLabel(segmentation), 'Szenarioabdeckung')

def getTitle(segmentation):
    match segmentation:
        case pe.Segmentation.SECONDS.value:
            return 'Segmentierung nach Sekunden'
        case pe.Segmentation.METERS.value:
            return 'Segmentierung nach Metern'
        case pe.Segmentation.BREMSWEG.value:
            return 'Segmentierung anhand des Anhaltewegs'
        case _:
            return 'Segmentierung anhand der Geschwindigkeit'
        
def getXAxisLabel(segmentation):
    match segmentation:
        case pe.Segmentation.SECONDS.value:
            return 'Sekunden'
        case pe.Segmentation.METERS.value:
            return 'Meter'
        case pe.Segmentation.BREMSWEG.value:
            return 'Lookahead'
        case _:
            return 'Geschwindigkeit'

for threshold in (0.9,0.95,0.99):
    for town in (pe.Town.ONE.value, pe.Town.TWO.value, pe.Town.TEN.value):
            compareOptimumPositionsOfMetrics(town, pe.Segmentation.BREMSWEG.value, threshold)
