import base64
import io
import numpy as np
from PIL import Image
from colorblind import colorblind
from SourceCode import deltaE_distance_calculator
from SourceCode.report_result_object import ReportResultObject


class DeltaDistanceDetection:
    def array_to_img(self, img_arr: np.array):
        image = Image.fromarray(np.uint8(img_arr))
        image_stream = io.BytesIO()
        image.save(image_stream, format='JPEG')
        return base64.b64encode(image_stream.getvalue()).decode('utf-8')

    def detect(self, grouped_colors, prot_check, deut_check, trit_check, img: np.array):
        prot_obj = ReportResultObject("Protanopia")
        deut_obj = ReportResultObject("Deuteranopia")
        trit_obj = ReportResultObject("Tritanopia")
        distance_matrix = deltaE_distance_calculator.count_deltaE_distance(np.array(grouped_colors))
        # simulate protanopia
        if prot_check:
            simulated_protanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='protanopia')[0]
            distance_protanopia = deltaE_distance_calculator.count_deltaE_distance(simulated_protanopia)
            prot_obj.found = any(distance_protanopia / distance_matrix < 0.5)
            sim_img = colorblind.simulate_colorblindness(img, colorblind_type='protanopia')
            prot_obj.simulated = self.array_to_img(sim_img)

        if deut_check:
            simulated_deuteranopia = \
                colorblind.simulate_colorblindness([grouped_colors], colorblind_type='deuteranopia')[0]
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
        return [prot_obj, deut_obj, trit_obj]


class PercentageDetection:
    def detect(self):
        pass
