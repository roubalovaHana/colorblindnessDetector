import numpy as np
from scipy.spatial.distance import pdist
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def convert_to_Lab(rgb_color):
    return [convert_color(sRGBColor(rgb_color[0], rgb_color[1], rgb_color[2], is_upscaled=True), LabColor)]


# returns upper triangular distance matrix in a 1D array
def count_deltaE_distance(rgb_colors):
    # Convert RGB to LAB
    lab_colors = np.array(list(map(convert_to_Lab, rgb_colors)))
    # using lambda here, since pdist only accepts 2-D arrays, but delta_e_cie2000 only accepts LabColor
    return pdist(lab_colors, metric=lambda c1, c2: delta_e_cie2000(c1[0], c2[0]))
