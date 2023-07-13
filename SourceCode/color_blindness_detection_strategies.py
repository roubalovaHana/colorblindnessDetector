from abc import ABC, abstractmethod
import numpy as np
from SourceCode.color_grouping_algs import KMeansColorGroupingStrategy, EuclideanDistColorGroupingStrategy, \
    DeltaEDistColorGroupingStrategy
from SourceCode.report_result_object import ReportResultObject
from SourceCode.detection_algs import DeltaDistanceDetection


class ColorBlindnessDetectionStrategy(ABC):

    @abstractmethod
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        pass


class KMeansDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors = KMeansColorGroupingStrategy().group_colors(colors, 0)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)


class EuclidianDistDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors = EuclideanDistColorGroupingStrategy().group_colors(colors, 150)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)


class DeltaEDistDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors = DeltaEDistColorGroupingStrategy().group_colors(colors, 40)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)
