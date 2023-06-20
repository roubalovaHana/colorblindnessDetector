import os.path
from pathlib import Path
import image_format_converter
import kmeans
import deltaE_distance_calculator
from PIL import Image
from colorblind import colorblind
from SourceCode import pdf_generator
from report_result_object import ReportResultObject


class LogicControl:
    report_result_list = []

    def find_issues(self, image_file_path, prot_check, deut_check, trit_check):
        image_format_converter.convert_to_jpg(image_file_path)
        graph = Image.open(image_file_path)
        grouped_colors = kmeans.group_colors(graph)
        kmeans.visualize_colors(grouped_colors)
        distance_matrix = deltaE_distance_calculator.count_deltaE_distance(grouped_colors)
        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        # simulate protanopia
        if prot_check:
            simulated_protanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='protanopia')[0]
            distance_protanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_protanopia)
            prot_obj.found = any(distance_protanopia / distance_matrix < 0.5)
            prot_obj.simulated = kmeans.visualize_colors(simulated_protanopia)

        if deut_check:
            simulated_deuteranopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='deuteranopia')[0]
            deut_obj.simulated = kmeans.visualize_colors(simulated_deuteranopia)
            distance_deuteranopia = deltaE_distance_calculator.count_deltaE_distance(simulated_deuteranopia)
            deut_obj.found = any(distance_deuteranopia / distance_matrix < 0.5)

        if trit_check:
            simulated_tritanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='tritanopia')[0]
            trit_obj.simulated = kmeans.visualize_colors(simulated_tritanopia)
            distance_tritanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_tritanopia)
            trit_obj.found = any(distance_tritanopia / distance_matrix < 0.5)

        self.report_result_list = [prot_obj, deut_obj, trit_obj]

    def generate_report(self, path_to_img):
        img_name = os.path.basename(path_to_img)
        parent_dir = os.path.dirname(os.getcwd())
        path = os.path.join(parent_dir, 'reports')
        Path(path).mkdir(parents=True, exist_ok=True)
        path = os.path.join(path, os.path.splitext(img_name)[0] + '_ColorBlindDetector_report.pdf')
        print(path)
        header = "Color-Blind Detector report for " + img_name
        pdf_generator.generate(path, header, path_to_img, self.report_result_list)

# find_issues("../TestFiles/colorblind_unfriendly.jpg")
# find_issues(r"C:\Users\Mu\Documents\Škola\Matfyz\Bakalářka\roubalova\TestFiles\colorblind_unfriendly.jpg")
