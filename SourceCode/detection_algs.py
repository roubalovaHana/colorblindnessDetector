import base64
import io
import numpy as np
from PIL import Image
from colorblind import colorblind
from SourceCode import deltaE_distance_calculator
from SourceCode.report_result_object import ReportResultObject


def array_to_img(img_arr: np.array):
    image = Image.fromarray(np.uint8(img_arr))
    image_stream = io.BytesIO()
    image.save(image_stream, format='JPEG')
    return base64.b64encode(image_stream.getvalue()).decode('utf-8')


class DeltaDistanceDetection:

    def detect(self, grouped_colors, prot_check, deut_check, trit_check, img: np.array):
        def simulate(cb_type):
            simulated_protanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type=cb_type)[0]
            distance_protanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_protanopia)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type=cb_type)
            return any(distance_protanopia / distance_matrix < 0.5), array_to_img(sim_img)

        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        distance_matrix = deltaE_distance_calculator.count_deltaE_distance(np.array(grouped_colors))
        # simulate protanopia
        if prot_check:
            prot_obj.found, prot_obj.simulated = simulate('protanopia')
        if deut_check:
            deut_obj.found, deut_obj.simulated = simulate('deuteranopia')
        if trit_check:
            trit_obj.found, trit_obj.simulated = simulate('tritanopia')
        return [prot_obj, deut_obj, trit_obj]


class PercentageDetection:
    def detect(self, colors, grouping_strategy, prot, deut, trit, img: np.array):
        def simulate(cb_type):
            _, percentages = grouping_strategy.group_colors(colors)
            simulated_colors = colorblind.simulate_colorblindness([colors], colorblind_type=cb_type)[0]
            _, simulated_percentages = grouping_strategy.group_colors(simulated_colors)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type=cb_type)
            return True, array_to_img(sim_img)

        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        if prot:
            prot_obj.found, prot_obj.simulated = simulate('protanopia')
        if deut:
            deut_obj.found, deut_obj.simulated = simulate('deuteranopia')
        if trit:
            trit_obj.found, trit_obj.simulated = simulate('tritanopia')
        return [prot_obj, deut_obj, trit_obj]


