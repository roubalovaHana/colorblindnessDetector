import numpy as np
from scipy.spatial.distance import pdist
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def convert_to_Lab(rgb_color):
    return [convert_color(sRGBColor(rgb_color[0], rgb_color[1], rgb_color[2], is_upscaled=True), LabColor)]


def pairwise_deltaE_distance(f_rgb_color, s_rgb_color) -> np.array:
    """
    Calculates deltaE distance for a pair of colors
    :param f_rgb_color: First color to calculate the deltaE distance for
    :param s_rgb_color: Second color to calculate the deltaE distance for
    :return: DeltaE distance for the pair of colors
    """
    # Convert RGB to LAB
    lab_colors = np.array(list(map(convert_to_Lab, [f_rgb_color, s_rgb_color])))
    # using lambda here, since pdist only accepts 2-D arrays, but delta_e_cie2000 only accepts LabColor
    return pdist(lab_colors, metric=lambda c1, c2: delta_e_cie2000(c1[0], c2[0]))


def count_deltaE_distance(rgb_colors):
    """
    Computes deltaE distances between every pair of colors
    :param rgb_colors: Colors to calculate the deltaE distances for
    :return: upper triangular distance matrix for every pair of colors in a 1D array
    """
    # Convert RGB to LAB
    lab_colors = np.array(list(map(convert_to_Lab, rgb_colors)))
    # using lambda here, since pdist only accepts 2-D arrays, but delta_e_cie2000 only accepts LabColor
    return pdist(lab_colors, metric=lambda c1, c2: delta_e_cie2000(c1[0], c2[0]))
