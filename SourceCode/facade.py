import base64
import os.path
from pathlib import Path
import io
import numpy as np
from matplotlib import pyplot as plt
import deltaE_distance_calculator
from PIL import Image
from colorblind import colorblind
from SourceCode import pdf_generator
from SourceCode.color_grouping_strategies import ColorGroupingStrategy, EuclideanDistColorGroupingStrategy, \
    KMeansColorGroupingStrategy
from report_result_object import ReportResultObject


class Facade:
    def __init__(self) -> None:
        # self._strategy = KMeansColorGroupingStrategy()
        self._strategy = EuclideanDistColorGroupingStrategy()
        self.report_result_list = []

    @property
    def strategy(self) -> ColorGroupingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ColorGroupingStrategy) -> None:
        self._strategy = strategy

    def array_to_img(self, img_arr: np.array):
        image = Image.fromarray(np.uint8(img_arr))
        image_stream = io.BytesIO()
        image.save(image_stream, format='JPEG')
        return base64.b64encode(image_stream.getvalue()).decode('utf-8')

    def find_issues(self, image_file_path, prot_check, deut_check, trit_check):
        graph = Image.open(image_file_path)
        img = np.array(graph)
        colors = np.array(list(set(graph.convert('RGB').getdata())))
        grouped_colors = self.strategy.group_colors(colors)
        distance_matrix = deltaE_distance_calculator.count_deltaE_distance(np.array(grouped_colors))
        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        # simulate protanopia
        if prot_check:
            simulated_protanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='protanopia')[0]
            distance_protanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_protanopia)
            prot_obj.found = any(distance_protanopia / distance_matrix < 0.5)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type='protanopia')
            prot_obj.simulated = self.array_to_img(sim_img)

        if deut_check:
            simulated_deuteranopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='deuteranopia')[0]
            distance_deuteranopia = deltaE_distance_calculator.count_deltaE_distance(simulated_deuteranopia)
            deut_obj.found = any(distance_deuteranopia / distance_matrix < 0.5)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type='deuteranopia')
            deut_obj.simulated = self.array_to_img(sim_img)

        if trit_check:
            simulated_tritanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='tritanopia')[0]
            distance_tritanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_tritanopia)
            trit_obj.found = any(distance_tritanopia / distance_matrix < 0.5)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type='tritanopia')
            deut_obj.simulated = self.array_to_img(sim_img)

        self.report_result_list = [prot_obj, deut_obj, trit_obj]

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
