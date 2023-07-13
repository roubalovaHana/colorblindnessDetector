import os.path
from pathlib import Path
import numpy as np
from PIL import Image
from SourceCode import pdf_generator
from SourceCode.color_grouping_algs import ColorGroupingStrategy, EuclideanDistColorGroupingStrategy
from SourceCode.detection_algs import DeltaDistanceDetection


class Facade:
    def __init__(self, strategy=EuclideanDistColorGroupingStrategy()) -> None:
        self._strategy = strategy
        self.report_result_list = []

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    def find_issues(self, image_file_path, prot_check, deut_check, trit_check):
        graph = Image.open(image_file_path)
        img = np.array(graph)
        colors = np.array(list(set(graph.convert('RGB').getdata())))
        grouped_colors = self.strategy.group_colors(colors, 190)
        self.report_result_list = DeltaDistanceDetection().detect(grouped_colors, prot_check, deut_check, trit_check, img)

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
