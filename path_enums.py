from enum import Enum

class Town(Enum):
    ONE = "Town01"
    TWO = "Town02"
    TEN = "Town10"
    ALL = "*"

    def getRelevantTowns():
        return [Town.ONE, Town.TWO, Town.TEN]

class Segmentation(Enum):
    SECONDS = "seconds"
    METERS = "meters"
    SPEED = "speed"
    BREMSWEG = "bremsweg"
    ALL = "*"

class Metric(Enum):
    TSC_COVERAGE = "tsc_coverage"
    TSC_AND_COMBINATION_COVERAGE = "tsc_combination_coverage"
    FOLLOWING_LEADING_VEHICLE = "following"
    LANE_CHANGE = "lane_change"
    LEFT_TURN = "left_turn"
    MUST_YIELD = "must_yield"
    OVERTAKING = "overtaking"
    PEDESTRIAN_CROSSED = "pedestrian"
    ALL = "*"

    def getRelevantMetrics():
        return [Metric.TSC_COVERAGE, Metric.FOLLOWING_LEADING_VEHICLE, Metric.LANE_CHANGE, Metric.LEFT_TURN, Metric.MUST_YIELD, Metric.OVERTAKING, Metric.PEDESTRIAN_CROSSED]
    
    def getMetricTitle(metric):
        match metric:
            case Metric.TSC_COVERAGE:
                return 'Szenarioabdeckung'
            case Metric.TSC_AND_COMBINATION_COVERAGE:
                return 'Szenario- und Kombinationsabdeckung'
            case Metric.FOLLOWING_LEADING_VEHICLE:
                return 'Vorausfahrendes Fahrzeug'
            case Metric.LANE_CHANGE:
                return 'Spurwechsel'
            case Metric.LEFT_TURN:
                return 'Linksabbiegen'
            case Metric.MUST_YIELD:
                return 'Vorfahrt gewähren'
            case Metric.OVERTAKING:
                return 'Überholen'
            case Metric.PEDESTRIAN_CROSSED:
                return 'Fußgänger'
            case _:
                return 'Unbekannt'

class Tsc(Enum):
    FULL = "full TSC"
    PEDESTRIAN = "pedestrian"
    MULTI_LANE = "multi-lane-dynamic-relations"
    LAYER_1_2 = "layer 1+2"
    LAYER_1_2_4 = "layer 1+2+4"
    LAYER_4 = "layer 4"
    LAYER_4_5 = "layer (4)+5"

    def getRelevantTSCs():
        return [Tsc.FULL, Tsc.PEDESTRIAN, Tsc.MULTI_LANE, Tsc.LAYER_1_2, Tsc.LAYER_1_2_4, Tsc.LAYER_4, Tsc.LAYER_4_5]