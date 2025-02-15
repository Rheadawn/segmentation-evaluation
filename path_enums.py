from enum import Enum

class Town(Enum):
    ONE = "Town01"
    TWO = "Town02"
    TEN = "Town10"
    ALL = "*"

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

class Tsc(Enum):
    FULL = "full TSC"
    PEDESTRIAN = "pedestrian"
    MULTI_LANE = "multi-lane-dynamic-relations"
    LAYER_1_2 = "layer 1+2"
    LAYER_1_2_4 = "layer 1+2+4"
    LAYER_4 = "layer 4"
    LAYER_4_5 = "layer (4)+5"