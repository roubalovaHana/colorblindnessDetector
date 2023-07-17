import os.path
from pathlib import Path
import numpy as np
from PIL import Image
from SourceCode import pdf_generator, detection_algs
from SourceCode.color_grouping_algs import ColorGroupingStrategy, EuclideanDistColorGroupingStrategy


class Facade:
    """
    Serves as a Facade to simplify the interaction between UI and colorblindness-related logic.
    Acts as a context for ColorGroupingStrategy.
    It provides a unified interface for mediating the colorblind issues detection process and PDF report generation.
    """
    def __init__(self, strategy=EuclideanDistColorGroupingStrategy()) -> None:
        self._strategy = strategy
        self.report_result_list = []

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    def find_issues(self, image_file_path: str, prot_check: bool, deut_check: bool, trit_check: bool) -> None:
        """
        Mediates the colorblind issues detection process for the provided image
        :param image_file_path: Path to the image to check for colorblindness issues
        :param prot_check: Whether to check for protanopia issues
        :param deut_check: Whether to check for deuteranopia issues
        :param trit_check: Whether to check for tritanopia issues
        """
        graph = Image.open(image_file_path)
        img = np.array(graph)
        colors = np.array(list(set(graph.convert('RGB').getdata())))
        grouped_colors = self.strategy.group_colors(colors, 190)
        self.report_result_list = detection_algs.detect_colorblindness_issues(grouped_colors, prot_check, deut_check, trit_check, img)

    def generate_report(self, path_to_img: str) -> None:
        """
        Mediates the PDF report generation based on the detected colorblindness issues
        :param path_to_img: Path to the image whose report to download
        """
        img_name = os.path.basename(path_to_img)
        parent_dir = os.path.dirname(os.getcwd())
        pdf_path = os.path.join(parent_dir, 'reports')
        Path(pdf_path).mkdir(parents=True, exist_ok=True)
        pdf_path = os.path.join(pdf_path, os.path.splitext(img_name)[0] + '_ColorBlindDetector_report.pdf')
        print(pdf_path)
        header = "Color-Blind Detector report for " + img_name
        pdf_generator.generate(pdf_path, header, path_to_img, self.report_result_list)
