from abc import ABC, abstractmethod
import numpy as np
from SourceCode.color_grouping_algs import KMeansColorGroupingStrategy, EuclideanDistColorGroupingStrategy, \
    DeltaEDistColorGroupingStrategy
from SourceCode.detection_algs import DeltaDistanceDetection
from SourceCode.report_result_object import ReportResultObject


class ColorBlindnessDetectionStrategy(ABC):

    @abstractmethod
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        pass


class KMeansDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors = KMeansColorGroupingStrategy().group_colors(colors)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)


class EuclidianDistDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors, _ = EuclideanDistColorGroupingStrategy().group_colors(colors)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)


class DeltaEDistDeltaDistanceDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors, _ = DeltaEDistColorGroupingStrategy().group_colors(colors)
        return DeltaDistanceDetection().detect(grouped_colors, prot, deut, trit, img)


class EuclidianDistPercentageDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors, percentages = EuclideanDistColorGroupingStrategy().group_colors(colors)


class DeltaEDistPercentageDetectionStrategy(ColorBlindnessDetectionStrategy):
    def detect_color_blindness(self, colors: np.array, prot: bool, deut: bool, trit: bool, img: np.array) -> [ReportResultObject]:
        grouped_colors, percentages = DeltaEDistColorGroupingStrategy().group_colors(colors)
