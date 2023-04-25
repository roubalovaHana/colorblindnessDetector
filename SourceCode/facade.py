import image_format_converter
import kmeans
import deltaE_distance_calculator
from PIL import Image
from colorblind import colorblind


def find_issues(image_file_path):
    image_format_converter.convert_to_jpg(image_file_path)
    graph = Image.open(image_file_path)
    grouped_colors = kmeans.group_colors(graph)
    distance_matrix = deltaE_distance_calculator.count_deltaE_distance(grouped_colors)
    # simulate protanopia
    simulated_protanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='protanopia')[0]
    simulated_deuteranopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='deuteranopia')[0]
    simulated_tritanopia = colorblind.simulate_colorblindness([grouped_colors], colorblind_type='tritanopia')[0]
    kmeans.visualize_colors(grouped_colors)
    kmeans.visualize_colors(simulated_protanopia)
    kmeans.visualize_colors(simulated_deuteranopia)
    kmeans.visualize_colors(simulated_tritanopia)


find_issues("../TestFiles/colorblind_unfriendly.jpg")
