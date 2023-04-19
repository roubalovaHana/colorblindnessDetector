import image_format_converter
import kmeans
import deltaE_distance_calculator
from PIL import Image


def find_issues(image_file_path):
    image_format_converter.convert_to_jpg(image_file_path)
    graph = Image.open(image_file_path)
    grouped_colors = kmeans.group_colors(graph)
    distance_matrix = deltaE_distance_calculator.count_deltaE_distance(grouped_colors)


find_issues("../TestFiles/unfriendly_colormap.jpg")
