import os.path
from pathlib import Path
import numpy as np
from PIL import Image
from SourceCode import pdf_generator
from SourceCode.color_blindness_detection_strategies import ColorBlindnessDetectionStrategy, \
    KMeansDeltaDistanceDetectionStrategy, \
    EuclidianDistDeltaDistanceDetectionStrategy, \
    DeltaEDistDeltaDistanceDetectionStrategy, \
    EuclidianDistPercentageDetectionStrategy, \
    DeltaEDistPercentageDetectionStrategy


class Facade:
    def __init__(self, strategy=EuclidianDistDeltaDistanceDetectionStrategy()) -> None:
        self._strategy = strategy
        self.report_result_list = []

    @property
    def strategy(self) -> ColorBlindnessDetectionStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorBlindnessDetectionStrategy) -> None:
        self._strategy = strategy

    def find_issues(self, image_file_path, prot_check, deut_check, trit_check):
        graph = Image.open(image_file_path)
        img = np.array(graph)
        colors = np.array(list(set(graph.convert('RGB').getdata())))
        self.report_result_list = self.strategy.detect_color_blindness(colors, prot_check, deut_check, trit_check, img)

    def generate_report(self, path_to_img) -> None:
        img_name = os.path.basename(path_to_img)
        parent_dir = os.path.dirname(os.getcwd())
        pdf_path = os.path.join(parent_dir, 'reports')
        Path(pdf_path).mkdir(parents=True, exist_ok=True)
        pdf_path = os.path.join(pdf_path, os.path.splitext(img_name)[0] + '_ColorBlindDetector_report.pdf')
        print(pdf_path)
        header = "Color-Blind Detector report for " + img_name
        pdf_generator.generate(pdf_path, header, path_to_img, self.report_result_list)

# Facade().find_issues("../TestFiles/prot_deut (2).jpg", True, True, True)
# find_issues(r"C:\Users\Mu\Documents\Škola\Matfyz\Bakalářka\roubalova\TestFiles\colorblind_unfriendly.jpg")
